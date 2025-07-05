import time
import threading

result = { "ready": False, "text": "" }

def explain_code(code: str):
    # for i in range(100000):
    #     pass
    result["text"] = f"Nice code:\n{code}"
    result["ready"] = True

def stream_explanation(code: str):
    thread = threading.Thread(target=explain_code, args=(code, ))
    thread.start()

    while not result["ready"]:
        yield ""
        time.sleep(0.05)

    explanation = result["text"]
    lines = explanation.splitlines()
    for line in lines:
        for c in line:
            yield c
        yield "\n"
        time.sleep(0.1)
    # yield "END-OF-EXPLANATION"

    result["ready"] = False
    result["text"] = ""