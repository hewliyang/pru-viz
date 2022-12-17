import streamlit as st

@st.experimental_singleton
def reduce_top_padding():
    return st.markdown("""
        <style>
            .css-18e3th9 {
                padding-top: 0rem;
                padding-bottom: 10rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
            .css-1d391kg {
                padding-top: 3.5rem;
                padding-right: 1rem;
                padding-bottom: 3.5rem;
                padding-left: 1rem;
                }
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
        section[data-testid="stSidebar"] .css-1d391kg {{width: 14rem;}}
        """, unsafe_allow_html=True)

@st.experimental_singleton
def load_css(path):
    with open(path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.experimental_singleton
def load_bootstrap_stylesheet(path):
    with open(path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)