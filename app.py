import streamlit as st
import schema as sch
import query as qry
st.set_page_config("SQL GENERATOR", layout='wide')
st.title("SQL GENERATOR USING OPENAI")

if "schema_status" not in st.session_state:
    st.session_state.schema_status = False
if "query_status" not in st.session_state:
    st.session_state.query_status = False

# getting the schema
if not st.session_state.schema_status:
    st.session_state.schema_status = sch.get_schema()

if st.session_state.schema_status and not st.session_state.query_status:
    qry.get_query()
