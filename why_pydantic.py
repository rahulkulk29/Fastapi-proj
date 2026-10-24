# Basically pythoon doessnt allow any type conversion in advance and pydantic helps us to ver come this.

# for example 

# def inser_data(name: str, age: int): # age can be str so we have age: int
#     print(name, (name))
#     print(age,(age))

# inser_data("rohan", "34") #doesnt throw error


# def insert_patient_data(name: str, age: int):

#     if type(name) == str and type(age) == int:
#         if age < 0:
#             raise ValueError('Age cant be negative')
#         else:
#             print(name)
#             print(age)
#             print('inserted into database')
#     else:
#         raise TypeError('Incorrect data type')

# def update_patient_data(name: str, age: int):
#     if type(name) == str and type(age) == int:
#         print(name)
#         print(age)
#         print('updated')
#     else:
#         raise TypeError('Incorrect data type')

# insert_patient_data('nitish', 30)
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import Dict, List, Optional, Annotated

# step 1 of pydantic  model creation 
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Enter name', description='name of the patient', examples='rahul')]
    # pydantic alsso provide built-in data  validation
    email: EmailStr
    age: int
    linked_url: AnyUrl
    weight: float = Field(gt = 0)
    married: bool = False
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

#field used to add custom validation with own data typess
    @field_validator('email') #on which field we want to apply validation
    @classmethod #fieldvalidator is always a class method, so import classmethod decorator from the functool module
    def domain_valid(cls, value):
        valid_value = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_value:
            raise ValueError('Invalid domain name')
        return value


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