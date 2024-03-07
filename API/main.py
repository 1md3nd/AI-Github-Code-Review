from fastapi import FastAPI, HTTPException, Request
from helper.utils import extract_owner_and_repo
from helper.helper import process_repo
import json
import uvicorn

app = FastAPI()

@app.get('/')
def root():
    return {'message':'This is home page.'}

@app.get('/searchRepo')
async def search_repo(request: Request):
    repo_url = request.query_params.get('repo_url')
    print(repo_url)
    if not repo_url:
        raise HTTPException(status_code=400, detail="Repository URL not provided")
    
    owner, repo = extract_owner_and_repo(url=repo_url)
    if not owner or not repo:
        raise HTTPException(status_code=400, detail="Invalid repository URL provided")
    
    files_data, cumulative_res = process_repo(owner=owner, repo=repo)
    return {'files_data': files_data, 'cumulative_res': cumulative_res}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
