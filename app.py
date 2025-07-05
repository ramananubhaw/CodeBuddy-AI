import streamlit as st
from model import stream_explanation

st.set_page_config(page_title="CodeBuddy AI", layout="wide")

st.markdown("""
    <style>
    textarea[disabled] {
        color: white;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

if "generating" not in st.session_state:
    st.session_state.generating = False

if "finished" not in st.session_state:
    st.session_state.finished = False

def start_explanation():
    st.session_state.generating = True

st.title("CodeBuddy AI")
st.subheader("Paste your code below, and I'll explain it!")

col1, spacer, col2 = st.columns([1, 0.1, 1])

with col1:
    st.markdown("### Input Code")
    code_input = st.text_area("Your code", height=400, placeholder="Paste here....")

with col2:
    col_btn1, col_btn2, space_btn = st.columns([1, 1, 2.5])
    with col_btn1:
        explain_button = st.button("Explain Code", disabled=st.session_state.generating, on_click=start_explanation)
    with col_btn2:
        refresh_button = st.button("Refresh")
        if refresh_button:
            st.rerun()

    if st.session_state.generating:
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
        st.info("Paste code on the left and click on the 'Explain Code' button.")