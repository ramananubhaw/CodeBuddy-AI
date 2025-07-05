import time
import threading
import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials

load_dotenv()

creds = Credentials(
    api_key = os.getenv("IBM_API_KEY"),
    url = os.getenv("SERVICE_URL")
)

model = ModelInference(
    model_id = "ibm/granite-3-3-8b-instruct",
    credentials = creds,
    project_id = os.getenv("PROJECT_ID"),
    params = {
        "max_new_tokens": 1000
    }
)

result = { "ready": False, "text": "" }

def explain_code(code: str):
    response = model.generate(prompt=f"Assume that you are a software engineer, not an AI. Explain the following code line-by-line:\n{code}")
    # print(response["results"][0])
    result["text"] = response["results"][0]["generated_text"][2:]
    result["ready"] = True

def stream_explanation(code: str):
    # print("Generating..........")
    thread = threading.Thread(target=explain_code, args=(code, ))
    thread.start()

    while not result["ready"]:
        yield ""
        time.sleep(0.05)

    explanation = result["text"]
    # print(explanation)
    lines = explanation.splitlines()
    for line in lines:
        for c in line:
            yield c
        yield "\n"
        time.sleep(0.1)

    result["ready"] = False
    result["text"] = ""