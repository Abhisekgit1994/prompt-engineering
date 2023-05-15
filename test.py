import datetime
import os
import re

import pandas as pd
import openai
from utils import LLMFunctions, ColumnSuggestions
from transform import Transform
# openai.api_key = "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"
# llm = LLMFunctions()


tbl_a = pd.read_csv('table_A.csv')
tbl_a_cols = tbl_a.columns.to_list()
tbl_b = pd.read_csv('table_B.csv')
tbl_b_cols = tbl_b.columns.to_list()
template = pd.read_csv('template.csv')

# suggest = ColumnSuggestions(template)

print(tbl_a_cols)
template_data = template['PolicyNumber'].to_string()
candidate = tbl_a['Policy_No'].to_list()

# trans = Transform()

# print(trans.generate_code(template_data, candidate))

# prompt = f"Given the following template data and candidate data, generate only the code to transform data from candidate data to template data format." \
#          f"\n\nTemplate data:\n{template_data}\n\nCandidate data:\n{candidate}\n\nThe generated code should output a list of values in the template format using the candidate data."
#
# response = openai.Completion.create(
#             engine="text-davinci-002",
#             prompt=prompt,
#             max_tokens=100,
#             n=1,
#             stop=None,
#             temperature=0.5
#         )
#
# code = response.choices[-1].text.strip()

code = """
for i in range(len(candidate_data)):\n\tcandidate_data[i]=candidate_data[i].replace("-", "")
"""
print(code)
exec(code, {'candidate_data': candidate})
print(candidate)



# {'Date': "The most similar columns to the template column 'Date' in the candidate table are the 'Date_of_Policy' and 'Policy_Start' columns. The reason for this decision is that both of these columns contain dates that are formatted in a similar way (mm/dd/yyyy).",
# 'EmployeeName': "The most similar columns for the template table column 'EmployeeName' are 'Full_Name' and 'FullName'. The decision is based on the fact that both columns contain the employee's first and last name.",
# 'Plan': "The most similar columns for the template column 'Plan' are 'Insurance_Plan' and 'Insurance_Type' from the candidate table. The reason for this decision is that these columns contain the same type of information as the template column 'Plan'.",
# 'PolicyNumber': "The most similar columns for the template column 'PolicyNumber' are 'Policy_No' and 'Policy_Num'. The reason for this decision is that both of these columns contain data that appears to be formatted in the same way (i.e. as policy numbers).",
# 'Premium': ':\n\nThe most similar columns for the template column "Premium" are "Monthly_Premium" and "Monthly_Cost". The reason for this decision is that both of these columns contain data for the monthly cost of the insurance policy.'}



