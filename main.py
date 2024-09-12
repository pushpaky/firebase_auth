import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

import pyrebase
import firebase_admin
from firebase_admin import credentials, auth as admin_auth

from models import LoginSchema, SignupSchema


app = FastAPI(
    description="This is a simple app to show Firebase Auth with FastAPI",
    title="Firebase Auth",
)

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

firebaseConfig = {
    "apiKey": "AIzaSyDS8BD5qlsYSjqlnejzkHrsYPfxvOiKd9o",
    "authDomain": "fastapiauth-299ae.firebaseapp.com",
    "projectId": "fastapiauth-299ae",
    "storageBucket": "fastapiauth-299ae.appspot.com",
    "messagingSenderId": "370571782137",
    "appId": "1:370571782137:web:2cf9515d3ef4b67dc87f28",
    "measurementId": "G-4H965J01NF",
    "databaseURL": "",
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()  # Initialize Pyrebase auth object


@app.post("/signup")
async def create_an_account(user_data: SignupSchema):
    email = user_data.email
    password = user_data.password

    try:
        auth.create_user_with_email_and_password(
            email=email, password=password
        )  # noqa
        return JSONResponse(
            content={"message": "User account Created "},  # noqa
            status_code=201,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error creating account: {e}"
        )  # noqa


@app.post("/login")
async def create_access_token(user_data: LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email, password=password
        )
        print(user)
        token = user["idToken"]
        print(token)
        return JSONResponse(
            content={
                "token": token,
            },
            status_code=200,
        )

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Invalid access token{e}")


# @app.post("/ping")
# async def validate_token(request: Request):
#     headers = request.headers
#     jwt = headers.get('authorization')

#     user = auth.verify_id_token(jwt)

#     return user["user_id"]

@app.post("/ping")
async def validate_token(request: Request):
    headers = request.headers
    jwt = headers.get("authorization")

    if not jwt:
        raise HTTPException(status_code=400, detail="Authorization token missing") # noqa

    try:
        # Verify token using Firebase Admin SDK
        user = admin_auth.verify_id_token(jwt)
        return JSONResponse(content={"user_id": user["uid"]}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
