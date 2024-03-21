from fastapi import FastAPI, HTTPException, Request
from helper.utils import extract_owner_and_repo
from helper.helper import process_repo
import json
import uvicorn

app = FastAPI()

@app.get('/')
def root():
    """ 
    A simple endpoint that returns a message indicating the home page. 
    """
    return {'message':'This is home page.'}

@app.get('/searchRepo')
async def search_repo(request: Request):
    """ 
    An endpoint to search and process a repository given its URL. 
    Parameters: - request: Request object provided by FastAPI. 
    Returns a dictionary with two keys: 
    - 'files_data': Contains the processed files data, where keys are file types and values are lists of processed file dictionaries returned by 'process_repo' function. 
    - 'cumulative_res': Contains the cumulative LOC and comment count for each file type, along with the 'forked' key to indicate if the repository is a fork. 
    """
    repo_url = request.query_params.get('repo_url')
    print(repo_url)
    if not repo_url:
        raise HTTPException(status_code=400, detail="Repository URL not provided")
    # Extract owner and repo name from the provided URL 
    owner, repo = extract_owner_and_repo(url=repo_url)
    if not owner or not repo:
        raise HTTPException(status_code=400, detail="Invalid repository URL provided")
    # Process the repository and retrieve files data and cumulative results 
    files_data, cumulative_res = process_repo(owner=owner, repo=repo)
    return {'files_data': files_data, 'cumulative_res': cumulative_res}

if __name__ == '__main__':  # Run the FastAPI server using uvicorn 
    uvicorn.run(app, host='0.0.0.0', port=8080)
