import openai
import os
import re
import pandas as pd


class LLMFunctions:
    def __init__(self):
        openai.api_key = "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"
        self.model_name = 'davinci:ft-personal-2023-05-11-22-58-24'

    @staticmethod
    def get_similar_cols(table, template):
        similar_columns = {}
        for col in template.columns:
            prompt = f"Find the most similar columns in template table for column '{col}' in the following candidate table are:\n\n{table.to_string(index=False)}"
            prompt += f"\n data for template column {template[[col]]}"
            prompt += f"\n also return the reason for decision"

            # print(prompt)
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.2,
            )
            # Parse the response and get the suggested column
            suggestion = response.choices[0].text.strip()
            similar_columns[col] = suggestion
        return similar_columns

    def generate_text_description(self, input):

        completion = openai.Completion.create(model=self.model_name, prompt=input, stop=1, temperature=0.2)
        return completion


class ColumnSuggestions:
    def __init__(self, template):
        self.template_cols = template.columns.to_list()
        openai.api_key = "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"

    @staticmethod
    def common_cols(column, response):
        if response[column]:
            ans = response[column].split('.')
            all_cols = re.findall("'(.*?)'", ans[0])
            return all_cols, ans
        else:
            return []

