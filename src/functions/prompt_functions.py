"""
Author: Zella King (zella.king@ucl.ac.uk)

File: prompt_functions.py
Description: Wrapper functions for calling OpenAI APIs.
Origin: Based on the Github for the Generative Agents paper 
https://github.com/joonspk-research/generative_agents
"""

from openai import ChatCompletion


def generate_prompt(curr_input, prompt_lib_file):
    """
    Takes in the current input (e.g. comment that you want to classifiy) and
    the path to a prompt file. The prompt file contains the raw str prompt that
    will be used, which contains the following substr: !<INPUT>! -- this
    function replaces this substr with the actual curr_input to produce the
    final promopt that will be sent to the GPT3 server.
    ARGS:
      curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                  INPUT, THIS CAN BE A LIST.)
      prompt_lib_file: the path to the prompt file.
    RETURNS:
      a str prompt that will be sent to OpenAI's GPT server.
    """
    if type(curr_input) == type("string"):
        curr_input = [curr_input]
    curr_input = [str(i) for i in curr_input]

    # read the prompt input file
    f = open(prompt_lib_file, "r")
    prompt = f.read()
    f.close()
    for count, i in enumerate(curr_input):
        prompt = prompt.replace(f"!<INPUT {count}>!", i)
    if "<commentblockmarker>###</commentblockmarker>" in prompt:
        prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
    return prompt.strip()


def generate_ChatGPT_response(messages, function, function_call):
    """
    Takes in string variables that represent a prompt for ChatGPT
    Use of function call forces a response from ChatGPT in a certain format
    ARGS:
      messages: the system and user messages to be passed
      function: a template
      function_call: the name of the function in the format {"name": "pick_medical_condition"}
    RETURNS:
      a response string from OpenAI's GPT server.
    """

    # messages=[
    #   {
    #     "role": "system",
    #     "content": "You are a medical doctor, who works in the emergency department of a hospital.",
    #   },
    #   {
    #     "role": "user",
    #     "content": prompt,
    #   },
    # ]

    response = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=[function],
        function_call=function_call,  # this forces calling `function`
    )

    # response = ChatCompletion.create(
    # model="gpt-3.5-turbo",
    # messages=[messages],
    # functions=[function],
    # function_call=function_call,
    # )
    return response
