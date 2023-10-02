"""
Author: Zella King (zella.king@ucl.ac.uk)

File: pick_medical_condition.py
Description: Functions specific to picking a medical condition
"""

# Load libraries
import json
import toml
import os
from pathlib import Path
import logging
import ast

# Load functions
from functions.prompt_functions import generate_prompt, generate_ChatGPT_response
from functions import set_up_logging


# Identify the path to the templates folder
PROJECT_ROOT = os.getenv("PROJECT_ROOT")
config = toml.load(Path(PROJECT_ROOT) / 'config.toml')
template_folder = str(Path(PROJECT_ROOT) / config['Paths']['PROMPT_TEMPLATE_PATH'])

# Function to generate the prompt
def generate_prompt_presenting_condition(persona):
    """
    Takes in details of a patient, and a prompt template
    Populates the template with the details
    ARGS:
      persona: the patient details as an instance of class Patient()
      template_folder: the path to the folder where templates are stored.
    RETURNS:
      a str prompt that will be sent to OpenAI's GPT server.
    """

    # load the relevant prompt template
    prompt_lib_file = template_folder + "/pick_medical_condition.txt"

    # populate the input with data from the persona
    prompt_input = []
    prompt_input.append(persona.Age_Band)
    prompt_input.append(persona.AE_Arrive_HourOfDay)
    prompt_input.append(persona.AE_Time_Mins)
    prompt_input.append(persona.Length_Of_Stay_Days)
    prompt_input.append(persona.ICD10_Chapter_Code)
    prompt_input.append(persona.Title)

    # generate the prompt
    return generate_prompt(prompt_input, prompt_lib_file)


def pick_medical_condition(persona):
    """
    Takes in details of a patient, and uses OpenAI to generate a medical
    condition and an admission note.
    ARGS:
      persona: the patient as an instance of class Patient()
    RETURNS:
      a response from OpenAI's GPT server.
      If successful, will return a medical condition and an admission note
      If unsuccesful, will return a 'fail' in both fiels
    """

    # Setup logging
    set_up_logging.setup_logging()
    logger = logging.getLogger()

    # generate the prompt for ChatGPT
    prompt = generate_prompt_presenting_condition(persona)

    # print(prompt)

    function = {
        "name": "pick_medical_condition",
        "description": "A function that takes in patient details and returns a medical condition",
        "parameters": {
            "type": "object",
            "properties": {
                "possible_conditions": {
                    "type": "array",
                    "description": "A list of the 10 possible medical conditions for this patient.",
                    "items": {
                        "name": {
                            "type": "string",
                            "description": "A medical condition",
                        },
                    },
                },
                "most_likely_condition": {
                    "type": "string",
                    "description": "The most likely medical condition",
                },
                "admission_note": {
                    "type": "string",
                    "description": "Admission note",
                },
            },
        },
        "required": ["possible_conditions", "most_likely_condition", "admission_note"],
    }

    function_call = {"name": "pick_medical_condition"}

    messages = [
        {
            "role": "system",
            "content": "As a medical expert, you are tasked with identifying a patient's most likely reason for being admitted to hospital. You have information about the patient's ultimate length of stay in hospital that is unknown to the doctors writing notes about the patient. Use this information in deciding on the patient's most likely condition and level of acuity, and in writing the admission note. But don't reveal the length of stay in the admission note.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    try:
        response = generate_ChatGPT_response(messages, function, function_call)
        logger.info("Got GPT response.")
    except:
        logger.error("No GPT response.")

    content = response["choices"][0]["message"]["function_call"]["arguments"]

    # return(content)

    # print(response)

    content_json = None  # Initialize content_json

    try:
        content_json = json.loads(content)
        logger.info("successful json load")
        logger.info(content_json)
    except:
        logger.info("failed on json loads")

    if content_json is None:
        try:
            content_json = ast.literal_eval(content)
            logger.info("successful json load with ast")
            logger.info(content_json)
        except:
            logger.info("failed on json load with ast")

    if content_json is None:
    
        try:
            content_json = json.loads(json.dumps(content))
            logger.info("successful json dump and load")
            logger.info(content_json)
        except:
            logger.info("failed on json dump and load")
            logger.info(content)
            return tuple(
                ["failed on json.loads", "failed on json.loads", "failed on json.loads"]
            )
    try:
        return (
            content_json["most_likely_condition"],
            content_json["admission_note"],
            content_json["admission_note"],
        )  # return admission note twice to populate latest note as well
    except:
        logger.info("failed on json argument")
        logger.info(content_json)
        return tuple(
            [
                "failed on json argument",
                "failed on json argument",
                "failed on json argument",
            ]
        )
