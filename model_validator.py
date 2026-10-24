from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import Dict, List, Optional, Annotated

# step 1 of pydantic  model creation 
class Patient(BaseModel):
    name: str
    # pydantic alsso provide built-in data  validation
    email: EmailStr
    age: int
    linked_url: AnyUrl
    weight: float 
    married: bool 
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

    #model_validator
    
    @model_validator(mode='after')
    def emergency_cont(cls, model):
        if model.age > 60 and emergency_cont not in model.contact_details:
            raise ValueError('Emergency contact required for age > 60')
        return model

#step 2 data example
# patient_data = {'name': 'Rahul', 'age': 22, 'Email': 'adc@mail.com', 'weight': 90, 'married': False, 'allergies' : ['Pollen', 'Dust'], 'contact_details': {'Rahul': '56789765668', 'mail':'adc@mail.com'}}

# using optional and default value 
patient_data = {'name': 'Rahul', 'email': 'abc@gmail.com', 'age': 22, 'linked_url': 'https://www.google.com', 'weight': 90, 'allergies' : ['Pollen', 'Dust'], 'contact_details': {'Rahul': '56789765668'}}

# step 3: validate and parse the data
patient = Patient(**patient_data)

# step 4: pass the validated data to the function
def insert_data(patient: Patient):
    name = print(patient.name)
    email = print(patient.email)
    age = print(patient.age)
    linked_url = print(patient.linked_url)
    allergies = print(patient.allergies)
    married = print(patient.married)
    print('inserted into database')

def update_data(patient: Patient):
    name = print(patient.name)
    email = print(patient.email)
    age = print(patient.age)
    linked_url = print(patient.linked_url)
    allergies = print(patient.allergies)
    married = print(patient.married)
    print('updated database')

#calling
insert_data(patient)
update_data(patient)