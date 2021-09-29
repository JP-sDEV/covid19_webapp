import streamlit as st

def page_config():
    config = st.set_page_config(
    page_title = "Toronto COVID-19",
    page_icon = "📍",
    layout = "wide",
    initial_sidebar_state = "auto"
    )
    return config

def responsive_style():
    style = """
    <style>
    [title~="st.iframe"]{
    width: 100%;
    height: 70vh;
    }

    .stSidebar {
    padding: 5em;
    }

    .stRadio{
    margin-left: 10%;
    }

    .stSlider{
    margin-left: 10%;
    padding: 10%;
    padding-top: 0%;
    }

    h2{
    text-align: center;
    }

    ul{
        text-align: center;
        list-style-type: none;
    }

    </style>
    """
    return style