"""
Author: Zella King (zella.king@ucl.ac.uk)

File: verify_medical_condition.py
Description: Functions specific to verifying an admission decision
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
def generate_prompt_presenting_condition(Admission_Note):
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
    prompt_lib_file = template_folder + "/verify_medical_condition.txt"

    # populate the input with data from the persona
    prompt_input = []
    prompt_input.append(Admission_Note)

    # generate the prompt
    return generate_prompt(prompt_input, prompt_lib_file)


def verify_medical_condition(persona):
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
        "name": "verify_medical_condition",
        "description": "A function that verfies whether a patient should be admitted",
        "parameters": {
            "type": "object",
            "properties": {
                "agree_disagree": {
                    "type": "string",
                    "description": "A one word expression of agree or disagree.",
                },
                "feedback_to_colleague": {
                    "type": "string",
                    "description": "Feeback to colleague",
                },
            },
        },
        "required": ["agree_disagree", "feedback_to_colleague"],
    }

    function_call = {"name": "verify_medical_condition"}

    messages = [
        {
            "role": "system",
            "content": "As a senior hospital doctor, your job is to make sure that only patients who need definitely hospital care are admitted.",
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
                ["failed on json.loads", "failed on json.loads"]
            )
    try:
        return (
            content_json["agree_disagree"],
            content_json["feedback_to_colleague"],
        )  
    except:
        logger.info("failed on json argument")
        logger.info(content_json)
        return tuple(
            [
                "failed on json argument",
                "failed on json argument",
            ]
        )
