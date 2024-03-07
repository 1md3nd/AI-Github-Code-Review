import streamlit as st
import requests

API_ENDPOINT = 'http://localhost:8080/'
# Title and Description
st.title('AI Github Code Review Dashboard')
st.write('Use this dashboard to get code review feedback for GitHub repositories.')

# Input Form
with st.form(key='github_form'):
    st.header('Enter GitHub Repository URL')
    github_url = st.text_input('GitHub URL')
    submit_button = st.form_submit_button(label='Get Code Review')
    print(github_url)
# Processing and Displaying Results
if github_url:
    st.header('Code Review Results')
    payload = {'repo_url':github_url}
    response = requests.get(API_ENDPOINT+'searchRepo',params=payload)
    # if response.status_code == '200':
    st.write(response.text)
    
    # Fetch and Process GitHub Repository
    # Call backend API to fetch and process GitHub repository based on the provided URL
    
    # Display Summary Statistics
    st.subheader('Summary Statistics')
    # Display summary statistics like total lines of code, commit limit, modules imported, etc.
    
    # Display Review Results for Each File
    st.subheader('Review Results')
    # Display review results for each file, including errors, typos, optimizations, LOC, etc.
    # Show these results in a table or as a list
    
    # Display Overall Rating
    st.subheader('Overall Rating')
    # Display overall rating based on cumulative feedback for all files
    
    # Provide Sorting Functionality
    st.subheader('Sort Repositories')
    # Allow the user to provide multiple repository URLs and sort them based on ratings
    
    # Provide Visualization (Optional)
    st.subheader('Visualization')
    # Optionally, provide visualizations of review results or summary statistics
    
    # Provide Download Option (Optional)
    st.subheader('Download Results')
    # Optionally, provide a button to download the review results as a CSV or Excel file
