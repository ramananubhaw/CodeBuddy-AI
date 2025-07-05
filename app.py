import streamlit as st
# from model import explain_code
from model import stream_explanation

st.set_page_config(page_title="CodeBuddy AI", layout="wide")

if "generating" not in st.session_state:
    st.session_state.generating = False

def start_explanation():
    st.session_state.generating = True

st.title("CodeBuddy AI")
st.subheader("Paste your code below, and I'll explain it!")

col1, spacer, col2 = st.columns([1, 0.1, 1])

with col1:
    st.markdown("### Input Code")
    code_input = st.text_area("Your code", height=400, placeholder="Write here....")

with col2:
    # Button to trigger explanation
    explain = st.button("Explain Code", disabled=st.session_state.generating, on_click=start_explanation)

    if explain:
        if not code_input.strip():
            st.warning("Please enter some code.")
            st.session_state.generating = False
        else:
            placeholder = st.empty()
            explanation = ""
            stream = stream_explanation(code_input)
            with (st.spinner("Generating explanation....")):
                for chunk in stream:
                    if (chunk==""):
                        continue
                    explanation += chunk
                    placeholder.text_area("Explanation", value=explanation, height=400, disabled=True)
                    break
            for chunk in stream:
                explanation += chunk
                placeholder.text_area("Explanation", value=explanation, height=400, disabled=True)

            st.session_state.generating = False
    else:
        st.info("Enter code on the left and click on the button.")