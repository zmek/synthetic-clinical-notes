"""
Author: Zella King (zella.king@ucl.ac.uk)

File: write_admission_note.py
Description: Functions specific to writing admission note
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
config = toml.load(Path(PROJECT_ROOT) / "config.toml")
template_folder = str(Path(PROJECT_ROOT) / config["Paths"]["PROMPT_TEMPLATE_PATH"])


# Function to generate the prompt
def generate_prompt_presenting_condition(patient_info):
    """
    Takes in an admission note, and a prompt template
    Populates the template with the details
    ARGS:
      Admission_Note: the note documenting a decision to admit
      template_folder: the path to the folder where templates are stored.
    RETURNS:
      a str prompt that will be sent to OpenAI's GPT server.
    """

    # load the relevant prompt template
    prompt_lib_file = template_folder + "/write_admission_note.txt"

    # populate the input with data from the persona
    prompt_input = []
    prompt_input.append(patient_info)

    # generate the prompt
    return generate_prompt(prompt_input, prompt_lib_file)


def write_admission_note(persona):
    """
    Takes in admission note, and uses OpenAI to verify whether the
    patient should be admitted
    ARGS:
      Admission_Note: the note documenting a decision to admit
    RETURNS:
      a response from OpenAI's GPT server.
      If successful, will return a agree/disagree and some feedback
      If unsuccesful, will return a 'fail' in both fiels
    """

    # Setup logging
    set_up_logging.setup_logging()
    logger = logging.getLogger()

    # generate the prompt for ChatGPT
    prompt = generate_prompt_presenting_condition(persona)

    # print(prompt)

    function = {
        "name": "write_admission_note",
        "description": "A function that writes an admission note",
        "parameters": {
            "type": "object",
            "properties": {
                "admission_note": {
                    "type": "string",
                    "description": "Admission note.",
                },
                "diagnosis": {
                    "type": "string",
                    "description": "diagnosis",
                },
                "length_of_stay": {
                    "type": "string",
                    "description": "Estimate lenght of hospital visit.",
                },
            },
        },
        "required": [
            "admission_note",
            "diagnosis",
            "length_of_stay",
        ],
    }

    function_call = {"name": "write_admission_note"}

    messages = [
        {
            "role": "system",
            "content": "You are an emergency doctor with decades of experience. You are an expert in medical conditions and in best practice for documentation of hospital visits.",
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
        logger.info("No GPT response.")
        return tuple(
            [
                "failed on GPT response",
                "failed on GPT response",
                "failed on GPT response",
            ]
        )

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
            content_json["admission_note"],
            content_json["diagnosis"],
            content_json["length_of_stay"],
        )
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
