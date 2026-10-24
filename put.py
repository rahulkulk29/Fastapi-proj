# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

# creating FastAPI app
app = FastAPI()


# defining patient model
class Patient(BaseModel):

    id: Annotated[str, Field(..., description="Required", examples=["P001"])]
    name: Annotated[str, Field(..., description="Required", examples=["Ananya Sharma"])]
    city: Annotated[str, Field(..., description="Required", examples=["Guwahati"])]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Required", examples=[28])]
    gender: Literal["male", "female"]
    height: Annotated[float, Field(..., gt=0, description="Required", examples=[1.65])]
    weight: Annotated[float, Field(..., gt=0, description="Required", examples=[90.0])]

    # calculating BMI
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height * self.height), 2)

    # calculating BMI verdict
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


# loading data from JSON file
def load_data():
    with open("patient.json", "r") as f:
        data = json.load(f)
    return data


# saving data to JSON file
def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)


# home endpoint
@app.get("/")
def hello():
    return {"message": "Welcome to patients data"}


# about endpoint
@app.get("/about")
def about():
    return {"message": "This is about page for patients API"}


# viewing all patient data
@app.get("/view")
def view():
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
    data = load_data()

    # checking whether patient ID exists
    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient not found")


# sorting patient data
@app.get("/sort")
def sort_data(
    sort_by: str = Query(..., description="Sort by height, weight, or bmi"),
    order: str = Query("asc", description="asc or desc")
):
    valid_fields = ["weight", "height", "bmi"]

    # converting input to lowercase
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

    data = load_data()

    # deciding sorting order
    sort_order = order == "desc"

    # sorting the patient data
    sorted_data = sorted(
        data.values(),
        key=lambda x: (
            x.get("bmi", round(x["weight"] / (x["height"] ** 2), 2))
            if sort_by == "bmi"
            else x[sort_by]
        ),
        reverse=sort_order
    )

    return sorted_data


# creating a new patient
@app.post("/create", status_code=201)
def create_patient(patient: Patient):

    # loading existing patient data
    data = load_data()

    # checking for duplicate patient ID
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # adding new patient data
    # converting Pydantic model into a dictionary
    data[patient.id] = patient.model_dump(exclude=["id"])

    # saving updated patient data
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={"message": "Data added successfully"}
    )