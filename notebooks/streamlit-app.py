import streamlit as st
import json


# load unstuctured data
with open("../src/data_exports/explore_llama_20240225_1202.json") as f:
    notes_data = json.load(f)


# set up streamlit
st.title("Patient Notes Viewer")
patient_id = st.text_input("Enter Patient ID", "")


def fetch_patient_notes(notes_data, patient_id):
    # Replace this function with your actual SQL query logic
    # This function should return notes for the given patient ID for the last 24 hours
    return "Sample notes for patient ID " + json.dumps(notes_data[int(patient_id)])


if st.button("Show Notes"):
    if patient_id:
        notes = fetch_patient_notes(notes_data, patient_id)
        st.text_area("Notes", notes, height=300)
    else:
        st.error("Please enter a valid Patient ID")
