from fastapi import FastAPI, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from starlette.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import User
from jose import jwt
from passlib.context import CryptContext
import models
import requests
import csv
import os

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


SECRET_KEY = os.getenv("MYSECRETKEY")
ALGORITHM = os.getenv("MYALGORITHM")

@app.get("/topClassical/")
async def getTopClassical(token: Annotated[str | None, Header()] = None):
    uid = verify_token(token)
    if not uid:
        return {"success": False}

    response = requests.get("https://lichess.org/api/player/top/50/classical")
    return response.json()


@app.get("/{username}/ratinghistory/")
async def getTopClassical(username: str, token: Annotated[str | None, Header()] = None):
    uid = verify_token(token)
    if not uid:
        return {"success": False}

    last_30_days = datetime.now() - timedelta(days=30)
    new_data = []
    response = requests.get(
        f"https://lichess.org/api/user/{username}/rating-history")
    data = response.json()
    for d in data:
        filtered_points = []
        points = d["points"]
        for p_set in points:
            year = p_set[0]
            month = p_set[1]+1
            day = p_set[2]

            entry_date = datetime(year, month, day)

            if entry_date >= last_30_days:
                filtered_points.append(p_set)
            new_data.append({
                "name": d["name"],
                "points": filtered_points
            })

    return new_data


@app.get("/players/rating-history-csv")
async def generate_rating_history_csv():

    top_classical_players_response = requests.get("https://lichess.org/api/player/top/50/classical")
    top_classical_players = top_classical_players_response.json()

    start_date = datetime.now() - timedelta(days=30)

    csv_data = []
    for player in top_classical_players["users"]:
        username = player["username"]
        try:
            rating_history_response = requests.get(
                f"https://lichess.org/api/user/{username}/rating-history")
            rating_history = rating_history_response.json()
            filtered_points = []

            for i in rating_history:
                game_mode = i["name"]
                points = i["points"]
                for p_set in points:
                    year = p_set[0]
                    month = p_set[1]+1
                    day = p_set[2]
                    entry_date = datetime(year, month, day)
                    if entry_date >= start_date:
                        filtered_points.append([game_mode, p_set])

            for entry in filtered_points:
                game_mode = entry[0]
                year = entry[1][0]
                month = entry[1][1]+1
                day = entry[1][2]
                entry_date = f"{year}/{month}/{day}"
                row = [username, game_mode, entry_date, entry[1][3]]
                csv_data.append(row)
        except:
            continue

    csv_filename = f"rating_history-{str(datetime.now()).replace(':','_').replace(' ','_')}.csv"
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Game Mode", "Date", "Rating 30 Days Ago"])
        writer.writerows(csv_data)

    return FileResponse(csv_filename, media_type='text/csv', filename=csv_filename)


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("id")
        if username is None:
            return False
        return username
    except Exception as e:
        print("exception", e)
        return False


class SignupRequest(BaseModel):
    email_ID: str
    password: str


class LoginRequest(BaseModel):
    email_ID: str
    password: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email_ID == body.email_ID).first()
    if not user or not verify_password(body.password, user.hashed_password):
        return {"success": False}

    token = create_access_token({"id": user.id, "email_ID": user.email_ID})
    return {"token": token, "success": True}


@app.post("/signup")
def signup(body: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email_ID == body.email_ID).first()
    if user:
        return {"success": False}
    create_user_model = User(
        email_ID=body.email_ID,
        hashed_password=bcrypt_context.hash(body.password),
    )
    db.add(create_user_model)
    db.commit()
    user = db.query(models.User).filter(models.User.email_ID == body.email_ID).first()
    token = create_access_token({"id": user.id, "email_ID": user.email_ID})
    return {"token": token, "success": True}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=80)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
