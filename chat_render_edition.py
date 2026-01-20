from flask import Flask, render_template, request, session, redirect, url_for
import openai

app = Flask(__name__)
app.secret_key = ''

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
    "Show a picture of a cat",
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
        model="gpt-4o", 
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content


def get_action_options(action_verb):
    prompt_text = f"Generate a list (no numbers, no dashes, just the items) of 8 basic, general Amazon Alexa commands that start with the action verb '{action_verb}' in a smart home context. No quotations. These tasks should be similar to those given in {task_ideas}. Do not specify details such as rooms (i.e. just 'lights', not 'kitchen lights'). Consider the items in this smart home environment, given in {home_environment}, and do not offer tasks that involve smart home objects or technology besides that list. Also consider the user's historical data, which is given in {commands_so_far} (will be empty to begin), to provide relevant predictions for commands. For example, if a user has turned on the lights, a logical next command is to set scenes, turn them off or change brightness. Do not include the details of the command (do not specify color, time, date, etc). For example, say 'Set an alarm for' and do not include the time. No explanations needed."
    response = openai.chat.completions.create(
        model="gpt-4o", 
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content


def task_details_check(task):
    prompt_text = f"You are Amazon Alexa. The user has chosen the task: '{task}'. Does this task require more information from the user? Some examples of tasks that do not need more information are 'Turn on the lights', 'Turn off the lights', etc. Some examples of tasks that do need more information are 'Schedule an alarm', 'Show my calendar', 'Set the lights to a specific color'. Basically, check if the sentence is complete or not. If the task does need more information, respond exactly 'Yes', with no quotes and no other explanation. If it does not need more information, respond 'No'"
    response = openai.chat.completions.create(
        model="gpt-4o", 
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content

def get_final_action_options(task):
    prompt_text = f"You are Amazon Alexa. The user has chosen the task: '{task}'. Generate one most important follow-up question that might be needed to complete this task effectively through an Amazon Alexa command. Consider various settings and preferences that might affect the execution of the task. Also consider the user's historical data, given in {commands_so_far} (but do not reveal this knowledge to the user). The follow-up question must eliminate ambiguity and be specific to the task at hand. For example, if the task is 'Set the lights to a color,' the model should ask 'What color?'. If the task is 'Show a recipe,' ask 'What specific food would you like a recipe for?' If the question relates to calendars, ask 'What day?'. Don't ask about room or location, assume the user wants tasks within the current unspecified room. No explanation or other text needed besides the question. Do not put quotation marks around the question."
    response = openai.chat.completions.create(
        model="gpt-4o", 
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content

def get_suggestions(question):
    prompt_text = f"Generate a list (no numbers, no dashes, just the items) of 8 most common expected responses to the question {question}. If (and only if) the question relates to directions, consider popular locations within a 3 mile radius of Gallaudet University. If (and only if) the question relates to weather, suggest popular locations, including a current location. If (and only if) the question relates to recipes, suggest popular recipes. If (and only if) the question relates to date, suggest options like 'today,' 'tomorrow,' etc. If (and only if) the question relates to light brightness, suggest percentages. If (and only if) the question relates to timers, suggest small intervals of time (seconds or minutes). No quotations or explanations needed."
    response = openai.chat.completions.create(
        model="gpt-4o", 
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content

def get_final_command(task, ans):
    prompt_text = f"The user has chosen the task: '{task}'. In response to the question, the user has responded '{ans}'. Formulate a complete, concise command for an Amazon Echo Show based on this information. Do not include the wake word."
    response = openai.chat.completions.create(
        model="gpt-4o", 
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content

def customCommand(task):
    prompt_text = f"You are Amazon Alexa. The user has entered a potentially ambiguous task: '{task}'. Please ask a question and answer it yourself, such as 'open lamp' or 'Set the brightness of the lamp'. There is no need to ask the user about the choices and questions that need to be made during this process, such as which room's light to turn on or what brightness to set. Decide by yourself. Based on this information, formulate a complete and concise command for Amazon Echo Show (a smart display device). Do not include the wake word."
    response = openai.chat.completions.create(
        model="gpt-4o", 
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content

def task_details_check_start(task):
    prompt_text = f'You are Amazon Alexa. A task {task} is provided by the user.Here are the rules for determining the type of the task:Initial tasks: Only single - word commands like "Turn", "Set", "Dim", "Show", "Play", "Find", "Read", "Send" (regardless of case) are considered initial tasks. If the task is one of these single - word commands, return "1".Tasks requiring additional details: If the task contains extra elements (details or objects) that make the action not fully specified, for example, "Turn on the light" (where "on the light" indicates the target of the "Turn" action but the specific state or other details might still need to be added), "Set the lights" (more details about the "Set" action like color, brightness etc. are not given), "Show the latest sports news" (it doesn "t specify how to "Show" exactly), "Play my playlist" (doesn"t specify from which device or with what settings etc.). In general, if the task seems to need more elements to be a complete and specific instruction, then return "2".Final results: If the task is a fully - specified instruction with all necessary details for execution, such as "Set the light color to blue" (the action "Set", the object "the light color" and the specific value "to blue" are all there), "Play BBC Radio on Amazon Echo Show at 8 am" (the action "Play", the content "BBC Radio", the device "Amazon Echo Show" and the time "at 8 am" are all specified). Only when the task has no ambiguity in terms of what to do and how to do it, return "3".Do not provide any explanations or additional text. Do not put quotation marks around the answer.'
    response = openai.chat.completions.create(
        model="gpt-4o", 
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        options2 = get_action_options(user_input)
        return render_template("step2.html", options=options2.split('\n'), action_verb_choice=user_input)
    return render_template("index.html", options=get_action_verbs().split('\n'))


@app.route("/step3", methods=["POST"])
def step3():
    task_selection = request.form.get("task_selection")
    gpt_answer = task_details_check(task_selection)
    if gpt_answer == 'Yes':
        question = get_final_action_options(task_selection)
        suggestions = get_suggestions(question).split('\n')
        return render_template("step3.html",tisp=question, question=suggestions, task_selection=task_selection)
    else:
        final_command = task_selection
        return render_template("step4.html", final_command=final_command)


@app.route("/step4", methods=["POST", "GET"])
def step4():
    if request.method == "POST":
        task_selection = request.form.get("task_selection")
        question_answer = request.form.get("question_answer")
        final_command = get_final_command(task_selection, question_answer)
        return render_template("step4.html", final_command=final_command)
    final_command = request.args.get("customcommand")
    return render_template("step4.html", final_command=final_command)


@app.route('/clear', methods=['get'])
def clear():
    return redirect(url_for('main'))


@app.route('/final', methods=['POST'])
def final():
    final_check = request.form.get('final_check')
    print(final_check)
    if final_check == 'no':
        result = "Oh no! Let us start over"
    else:
        result = "Perfect! Sent your final command to Alexa"
    return render_template('result.html', result=result)

@app.route('/customcommand', methods=['GET'])
def customcommand():
    task = request.args.get('task')
    task_details_start = task_details_check_start(task)
    if task_details_start == '1':
        options2 = get_action_options(task)
        return render_template("step2.html", options=options2.split('\n'), action_verb_choice=task)
    elif task_details_start == '2':
        gpt_answer = task_details_check(task)
        if gpt_answer == 'Yes':
            question = get_final_action_options(task)
            suggestions = get_suggestions(question).split('\n')
            return render_template("step3.html",tisp=question, question=suggestions, task_selection=task)
        else:
            return render_template("step4.html", final_command=task)
    elif task_details_start == '3':
        final_command = task
        return render_template("step4.html", final_command=final_command)

if __name__ == "__main__":
    app.run()