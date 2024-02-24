from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()

@app.get('/')
def root():
    return {'message':'This is home page.'}


@app.get('/searchRepo')
def serachRepo(request):
    repos = request.get('repo')