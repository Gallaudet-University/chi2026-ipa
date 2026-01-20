# Supplemental code for the Alexa LLM-assisted touch interface

This code is provided as a companion to replicate the results in the following CHI 2026 paper:

Paige S. DeVries, Michaela Okosi, Ming Li, Nora Dunphy, Gidey Gezae,
Dante Conway, Abraham Glasser, Raja Kushalnagar, and Christian Vogler.
2026. Deaf and Hard of Hearing Access to Intelligent Personal Assistants:
Comparison of Voice-Based Options with an LLM-Powered Touch Interface.
In Proceedings of the 2026 CHI Conference on Human Factors in Computing
Systems (CHI ’26), April 13–17, 2026, Barcelona, Spain. ACM, New York, NY,
USA, 16 pages. https://doi.org/10.1145/3772318.3791869

## Running the code

There are two main Python files: testing prompts in `chat_updated.py` and running
the Flask-based web server with the full touch user interface in `chat_render_edition.py`.

You need to set up a Python environment with the Flask and openai modules installed. The easiest
way is via a virtual environment, such as `venv`.

If you run the touch interface on a tablet (recommended), you need to run Flask with an SSL
certificate installed. One easy way is to run it in the Google cloud via the "Run" service. Otherwise, it's probably not too difficult to build a Docker image, but you will be on your own for that.

Prior to running the code, you need to sign up for the OpenAI GPT API, and set up a secret key. Copy and
paste the secret key into the `openai.api_key = ""` line in both files. In addition, we recommend setting a secret key for session management in Flask in the `app.secret_key = ''` line in `chat_render_edition.py`.

## Acknowledgments

The contents of this paper were developed under a grant from the
National Institute on Disability, Independent Living, and Rehabili-
tation Research (NIDILRR grant number 90REGE0013). NIDILRR is
a Center within the Administration for Community Living (ACL),
Department of Health and Human Services (HHS). The contents
of this paper do not necessarily represent the policy of NIDILRR,
ACL, HHS, and you should not assume endorsement by the Fed-
eral Government. Additional support has been provided by the
National Science Foundation under Awards No. 2150429, 2348221
and 2447704