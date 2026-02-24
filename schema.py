import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import query as qry


if 'table_name' not in st.session_state:
    st.session_state.table_name = False

if 'column_details' not in st.session_state:
    st.session_state.column_details = False

def get_schema():
    st.header("Define the Schema", divider='blue')
    col1, col2 = st.columns([1, 1])
    with col1:
        get_table_name()
        get_column_names()
        validate_btn = st.button("Validate the schema", type='primary')

    with col2:
        if validate_btn:
            validate_status = validate_col_details()
            if st.session_state.table_name and st.session_state.column_details and validate_status.content == 'Yes':
                st.text_area("Validated Schema", value = f"""This is the table name: {st.session_state.table_name}\n\nBelow are column details: \n{st.session_state.column_details}""", height=330, disabled=True)
                st.toast("✅ Schema Validated Successfully.")
                if st.button("Proceed", type='primary'):
                    return True
            elif not st.session_state.table_name or  not st.session_state.column_details or validate_status.content == 'No':
                st.toast("⚠️Error in Schema Defination.")



def get_table_name():
    st.session_state.table_name = st.text_input("Enter the table name: ", placeholder="Enter the table name", value=None)

def get_column_names():
    st.session_state.column_details = st.text_area("Enter the Column Names: ", placeholder="""
    Enter as below format:
    1. order_id (int)
    2. order_date (date)
    3. region (string)
    4. revenue (float)
    .
    .     
""", value=None, height=250)



def validate_col_details():
    validate_chat = ChatOpenAI(model='gpt-4', seed=25, max_completion_tokens=50, temperature=0)
    prompt = f"""Check the below column details entered by the user\n{st.session_state.column_details}\n is enetered in list pattern with column name and their datatype in parenthesis.\nReply only in one word (Yes or No)"""
    validate_response = validate_chat.invoke([
        SystemMessage("You are a bot checking the column details entered by the user"),
        HumanMessage(content=prompt)
    ])
    return validate_response