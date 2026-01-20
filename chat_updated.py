import openai

# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = openai()

openai.api_key = ""
commands_so_far = []
task_ideas = [
    "Turn on the lights",
    "Set the light color to blue",
    "Dim the lights 50%",
    "Turn off the lights",
    "Show my calendar for tomorrow",
    "Show my calendar for next week",
    "Show the weather forecast tomorrow",
    "Show the weather in Chicago",
    "Show directions to Starbucks on H Street",
    "Show directions to Union Market",
    "Show the latest sports news",
    "Set a timer for 1 minute",
    "Set a timer for 3 minutes",
    "Set a reminder to call a friend at 4pm",
    "Show me a recipe for chocolate cake",
    "Play my favorite playlist",
    "Set an alarm for 7am",
    "Send a message to John",
    "Find the nearest coffee shop",
    "Read my latest emails"
]
home_environment = ["Smart light"]


def get_chat_response(messages):
    response = openai.chat.completions.create(
        engine="text-davinci-003",
        prompt=[{"role": msg["role"], "content": msg["content"]} for msg in messages],
        max_tokens=150
    )
    return response.choices[0].text.strip()


def get_action_verbs():
    prompt_text = f"Generate a list (no numbers, no dashes, just the items) of 8 action verbs that are ideal for starting commands in a voice-controlled assistant interface. These verbs should be straightforward, commonly understood, and versatile enough to apply across various tasks including managing home automation, scheduling events, querying information, and controlling media playback. Provide verbs that ensure clear and concise commands suitable for quick voice interactions. No quotations around the verbs. Some examples of commands are in {task_ideas}. Include a verb to show information as well, such as viewing a calendar or a to-do list. Consider the items in this smart home environment, given in {home_environment} and the user's historical data, which is given in {commands_so_far} (will be empty to begin), to provide relevant predictions for command verbs. For example, if a user has turned on the lights, a logical next command is to set scenes, turn them off or change brightness. No explanations needed."
    response = openai.chat.completions.create(
        temperature=0.2,
        model="gpt-4o",  # Updated model name
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content


def get_action_options(action_verb):
    prompt_text = f"Generate a list (no numbers, no dashes, just the items) of 8 basic, general Amazon Alexa commands that start with the action verb '{action_verb}' in a smart home context. No quotations. These tasks should be similar to those given in {task_ideas}. Do not specify details such as rooms (i.e. just 'lights', not 'kitchen lights'). Consider the items in this smart home environment, given in {home_environment}, and do not offer tasks that involve smart home objects or technology besides that list. Also consider the user's historical data, which is given in {commands_so_far} (will be empty to begin), to provide relevant predictions for commands. For example, if a user has turned on the lights, a logical next command is to set scenes, turn them off or change brightness. Do not include the details of the command (do not specify color, time, date, etc). For example, say 'Set an alarm for' and do not include the time. No explanations needed."
    response = openai.chat.completions.create(
        model="gpt-4o",  # Updated model name
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content


def task_details_check(task):
    prompt_text = f"You are Amazon Alexa. The user has chosen the task: '{task}'. Does this task require more information from the user? Some examples of tasks that do not need more information are 'Turn on/off the lights', 'Turn on/off the TV', etc. Some examples of tasks that do need more information are 'Schedule an alarm', 'Show my calendar', 'Set the temperature to'. Basically, check if the sentence is complete or not. If the task does need more information, respond exactly 'Yes', with no quotes and no other explanation. If it does not need more information, respond 'No'"
    response = openai.chat.completions.create(
        model="gpt-4o",  # Updated model name
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content


def get_final_action_options(task):
    prompt_text = f"You are Amazon Alexa. The user has chosen the task: '{task}'. Generate one most important follow-up question that might be needed to complete this task effectively through an Amazon Alexa command. Consider various settings and preferences that might affect the execution of the task. Also consider the user's historical data, given in {commands_so_far} (but do not reveal this knowledge to the user). The follow-up question must eliminate ambiguity and be specific to the task at hand. For example, if the task is 'Set the lights to a color,' the model should ask 'What color?'. If the task is 'Show a recipe,' ask 'What specific food would you like a recipe for?' If the question relates to calendars, ask 'What day?'. Don't ask about room or location, assume the user wants tasks within the current unspecified room. No explanation or other text needed besides the question. Do not put quotation marks around the question."
    response = openai.chat.completions.create(
        model="gpt-4o",  # Updated model name
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content


def get_suggestions(question):
    prompt_text = f"Generate a list (no numbers, no dashes, just the items) of 8 most common expected responses to the question {question}. If (and only if) the question relates to directions, consider popular locations within a 3 mile radius of Gallaudet University. If (and only if) the question relates to weather, suggest popular locations, including a current location. If (and only if) the question relates to recipes, suggest popular recipes. If (and only if) the question relates to date, suggest options like 'today,' 'tomorrow,' etc. If (and only if) the question relates to light brightness, suggest percentages. If (and only if) the question relates to timers, suggest small intervals of time (seconds or minutes). No quotations or explanations needed."
    response = openai.chat.completions.create(
        model="gpt-4o",  # Updated model name
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content


def get_final_command(task, q, ans):
    prompt_text = f"The user has chosen the task: '{task}'. In response to the question, '{q}', the user has responded '{ans}'. Formulate a complete, concise command for an Amazon Echo Show based on this information. Do not include the wake word."
    response = openai.chat.completions.create(
        model="gpt-4o",  # Updated model name
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content


def main():
    action_verbs = get_action_verbs()

    print("Hi! How can I help you?")
    print(action_verbs)

    # get the user input
    user_input = int(input("👤: "))  # User inputs a number corresponding to the options
    action_verb_choice = action_verbs.split('\n')[user_input - 1]

    # get the actions from the initial verb
    options2 = get_action_options(action_verb_choice)
    print(f"Options for '{action_verb_choice}': \n{options2}")

    # get the next input
    user_input2 = int(input("👤: "))  # User inputs a number corresponding to the options
    task_selection = options2.split('\n')[user_input2 - 1]

    # do we need a follow-up question?
    gpt_answer = task_details_check(task_selection)
    if gpt_answer == 'Yes':
        # get the actions from the initial verb
        question = get_final_action_options(task_selection)
        print(question)
        # get the details

        suggestions = get_suggestions(question)
        print(suggestions)

        question_answer = suggestions.split('\n')[int(input("👤: ")) - 1]

        # question_answer = str(input("👤: "))  # User inputs a number corresponding to the options
        final_command = get_final_command(task_selection, question, question_answer)
    else:
        final_command = task_selection

    print(f"Your final command is: {final_command}.\nDoes this look correct? Type 'yes' or 'no'")

    # get the response to final check
    final_check = str(input("👤: "))

    if final_check == 'yes':
        commands_so_far.append(final_command)
        print("Perfect! Sending your command to Alexa now.")
        main()
    else:
        print(f"Oh no! Let's start over")
        main()


if __name__ == "__main__":
    main()