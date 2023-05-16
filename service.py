import pandas as pd
import streamlit as st
import datetime
import os
import re
import openai
import pdb
import threading
from utils import LLMFunctions, ColumnSuggestions
from transform import Transform
# state = st.session_state.get(template=None, table_a=None, selected_options={})
llm = LLMFunctions()
transformation = Transform()

st.set_page_config(layout='wide')
st.title('Candidate tables to Template table')
col1, col2 = st.columns(2)


def transform_data(col, template_data, selected_data, session):
    suggest_code = transformation.generate_code(template_data, selected_data)
    # print(suggest_code)
    if suggest_code:
        default = suggest_code
        if col not in session:
            session[col] = default
        print(st.session_state)
        user_edit = st.text_area(f'generated code for {col}', session[col])
        code = f"""{user_edit}"""
        exec(code, {'candidate_data': selected_data})
        st.write(selected_data)

def main():
    st.session_state['selected_option'] = {}
    st.session_state['text'] = {}
    table_a = st.file_uploader('upload candidate table ', type=["csv"])
    template = st.file_uploader('upload Template table', type=["csv"])
    with col1:
        if table_a and template is not None:
            template = pd.read_csv(template)
            suggest = ColumnSuggestions(template)
            table_a_df = pd.read_csv(table_a)
            tbl_a_cols = table_a_df.columns.to_list()
            response = llm.get_similar_cols(table_a_df, template)
            # test for Policy_No column
            threads = []
            for col in template.columns:
                template_data = template[col].to_string()
                st.text(f'similar columns for {col}')
                all_cols, reason = suggest.common_cols(col, response)
                comm = list(set(all_cols).intersection(tbl_a_cols))
                default_text = comm[0]
                if col not in st.session_state.selected_option:
                    st.session_state.selected_option[col] = default_text
                selected_option = st.selectbox('Select an option:', comm)
                st.session_state.selected_option[col] = selected_option
                selected_data = table_a_df[selected_option].to_list()
                st.write(f'Showing data for {selected_option}')
                st.write(selected_data)
                t = threading.Thread(target=transform_data, args=(col, template_data, selected_data, st.session_state['text']))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()

if __name__ == "__main__":
    main()