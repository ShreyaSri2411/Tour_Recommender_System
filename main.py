from fastapi import FastAPI
import subprocess
from pydantic import BaseModel
from recommender import recommend
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins = ['*'],
allow_credentials = True,
allow_methods = ["GET","OPTIONS","POST","DELETE","PUT"],
allow_headers = ["*"],
expose_headers=["*"],
)


class ask_user(BaseModel):
    area_type : str
    budget : float
    description : str

@app.post("/user_guide")
def user_guide(info: ask_user):
    response = {'status' : True}
    budget = info.budget
    area_type = info.area_type
    description = info.description


    recommendations = recommend(your_type=area_type,budget=budget,user_description=description)
    print('recommendations : ', recommendations)

    return recommendations

