from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

# creating FastAPI app
app = FastAPI()


# defining patient model
class Patient(BaseModel):

    # defining the fields required to create a patient
    id: Annotated[str, Field(..., description="Required", examples=["P001"])]
    name: Annotated[str, Field(..., description="Required", examples=["Ananya Sharma"])]
    city: Annotated[str, Field(..., description="Required", examples=["Guwahati"])]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Required", examples=[28])]
    gender: Literal["male", "female"]
    height: Annotated[float, Field(..., gt=0, description="Required", examples=[1.65])]
    weight: Annotated[float, Field(..., gt=0, description="Required", examples=[90.0])]

    # calculating BMI using height in metres and weight in kilograms
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height * self.height), 2)

    # calculating BMI verdict based on the BMI value
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"


# defining a model for updating patient information
# all fields are optional because we may update only selected fields
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# loading data from JSON file
def load_data():
    # opening patient.json in read mode
    with open("patient.json", "r") as f:
        data = json.load(f)

    # returning all patient data as a Python dictionary
    return data


# saving data to JSON file
def save_data(data):
    # opening patient.json in write mode
    with open("patient.json", "w") as f:
        # saving dictionary data in readable JSON format
        json.dump(data, f, indent=4)


# home endpoint
@app.get("/")
def hello():
    # returning a welcome message
    return {"message": "Welcome to patients data"}


# about endpoint
@app.get("/about")
def about():
    # returning information about this API
    return {"message": "This is about page for patients API"}


# viewing all patient data
@app.get("/view")
def view():
    # loading all patient records from the JSON file
    data = load_data()
    return data


# viewing a particular patient using patient ID
@app.get("/patients/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="Enter the patient ID",
        examples=["P001"]
    )
):
    # loading all patient records
    data = load_data()

    # checking whether the given patient ID exists
    if patient_id in data:
        return data[patient_id]

    # returning a 404 error if the patient does not exist
    raise HTTPException(status_code=404, detail="Patient not found")


# sorting patient data
@app.get("/sort")
def sort_data(
    sort_by: str = Query(..., description="Sort by height, weight, or bmi"),
    order: str = Query("asc", description="asc or desc")
):
    # defining the fields that can be used for sorting
    valid_fields = ["weight", "height", "bmi"]

    # converting input to lowercase to avoid case-sensitivity issues
    sort_by = sort_by.lower()
    order = order.lower()

    # checking whether the sorting field is valid
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Bad request. Select from {valid_fields}"
        )

    # checking whether the sorting order is valid
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Bad request. Choose asc or desc"
        )

    # loading patient records
    data = load_data()

    # True means descending order; False means ascending order
    sort_order = order == "desc"

    # sorting patient records using the selected field
    sorted_data = sorted(
        data.values(),
        key=lambda x: (
            # calculate BMI if it is not already stored in the JSON data
            x.get("bmi", round(x["weight"] / (x["height"] ** 2), 2))
            if sort_by == "bmi"
            else x[sort_by]
        ),
        reverse=sort_order
    )

    # returning the sorted patient records
    return sorted_data


# creating a new patient
@app.post("/create", status_code=201)
def create_patient(patient: Patient):

    # loading existing patient data
    data = load_data()

    # checking whether the patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # converting the Pydantic model into a dictionary
    # excluding id because it is already used as the dictionary key
    # BMI and verdict are included as computed fields
    data[patient.id] = patient.model_dump(exclude=["id"])

    # saving the new patient record to the JSON file
    save_data(data)

    # returning a success response with HTTP status code 201
    return JSONResponse(
        status_code=201,
        content={"message": "Data added successfully"}
    )


# updating an existing patient using patient ID
@app.put("/update/{patient_id}")
def update_user(patient_id: str, patient: PatientUpdate):

    # loading all patient records
    data = load_data()

    # checking whether the patient ID exists
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # getting the existing information of the selected patient
    existing_patient_info = data[patient_id]

    # converting the update model into a dictionary
    # exclude_unset=True includes only fields sent in the request
    update_info = patient.model_dump(exclude_unset=True)

    # updating only the fields provided by the user
    for key, value in update_info.items():
        existing_patient_info[key] = value

    # adding the ID back temporarily to validate the complete patient record
    # Patient validates the fields and recalculates BMI and verdict
    existing_patient_info["id"] = patient_id
    patient_object = Patient(**existing_patient_info)

    # converting the validated Pydantic object back into a dictionary
    # excluding id because it is already the dictionary key
    data[patient_id] = patient_object.model_dump(exclude={"id"})

    # saving the updated patient data to the JSON file
    save_data(data)

    # returning a success message
    return {
        "message": "Data updated successfully"
    }


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='data not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Deleted data successfully'})
