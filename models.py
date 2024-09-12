from pydantic import BaseModel


class SignupSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "pushpa@gmail.com",
                "password": "pushpa@123"
            }
        }


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "pushpa@gmail.com",
                "password": "pushpa@123"
            }
        }
