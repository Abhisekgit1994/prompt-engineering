import pandas as pd
import streamlit as st
import datetime
import os
import re
import openai
from utils import LLMFunctions, ColumnSuggestions
from transform import Transform
# state = st.session_state.get(template=None, table_a=None, selected_options={})
llm = LLMFunctions()
transformation = Transform()

st.set_page_config(layout='wide')
st.title('Candidate tables to Template table')
col1, col2 = st.columns(2)
with col1:
    table_a = st.file_uploader('upload candidate table', type=["csv"])
    template = st.file_uploader('upload Template table', type=["csv"])
    if table_a and template is not None:
        template = pd.read_csv(template)
        suggest = ColumnSuggestions(template)
        table_a_df = pd.read_csv(table_a)
        tbl_a_cols = table_a_df.columns.to_list()
        response = llm.get_similar_cols(table_a_df, template)
        template_data = template['PolicyNumber'].to_string()
        st.text('similar columns for PolicyNumber')
        all_cols, reason = suggest.common_cols('PolicyNumber', response)
        comm = list(set(all_cols).intersection(tbl_a_cols))
        if "selected_option" not in st.session_state:
            st.session_state.selected_option = comm[0]
        selected_option = st.selectbox('Select an option:', comm)
        st.session_state.selected_option = selected_option
        selected_data = table_a_df[selected_option].to_list()
        st.write(f'Showing data for {selected_option}')
        st.write(selected_data)

        suggest_code = transformation.generate_code(template_data, selected_data)
        if suggest_code:
            default_text = suggest_code
            if 'text' not in st.session_state:
                st.session_state.text = default_text
            user_edit = st.text_area('generated code', st.session_state.text)
            # exec(suggest_code, {'candidate_data': selected_data})
            # st.write("Transformed data", user_edit)
            code = f"""{user_edit}"""
            exec(code, {'candidate_data': selected_data})
            st.write(selected_data)