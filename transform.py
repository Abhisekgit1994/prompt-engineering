import openai
import json


class Transform:
    def __init__(self):
        openai.api_key = ""

    @staticmethod
    def generate_code(template, candidate):
        """

        :param template: template table column
        :param candidate: candidate table column
        :return: generated code to transform
        """
        prompt = f"Given the following template data and candidate data, generate python code to transform data from candidate data to template data format." \
                     f"\n\nTemplate data:\n{template}\n\nCandidate data:\n{candidate}\n\nThe generated code should replace the values of  candidate data."

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.2
        )

        code = response.choices[-1].text.strip()
        return code
