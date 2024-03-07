# Project Name: AI Github Code Review

## Use Case: We can utilize the code review to shortlist resumes based on github repo rating.

### Rating System:
The rating can be done using the various aspect like
- Line of Code
- Commit limit
- module imported
- proper staging of ml pipelines (optional)
- proper commenting
- Inclusion of unit testcases
- not forked form other repo
- Readme.md
- Errors and improper use of functions
- Typos / code breaking
- Use of OpenAI for code review


### FLOW:

1. We get the url for some repo
2. Fetch the repo using Github API
3. Process the github tree inMemory and filter out files for each programming language
4. Count LOC for each programming language
5. Again use filter to filter out test files and main files
6. We now then use Some AI model to provide feedback for our files, in response we get {Error: {Line-No*: Context for error}}
7. (Imagination) Based on the response of each files, we can use some sort of rating based on count of errors, typos, optimizations, LOC 
- After generating data for each files and do cummlative for each programming language
8. Provide feedback to user using streamlit as dashboard
9. User can see their errors in each files, and their ratings 
10. Also user can provide multiple repo and we can use our ratings to sort them