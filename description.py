import datetime
import os
import pandas as pd
import openai
import description as tk
openai.api_key = ""

model_name = 'davinci:ft-personal-2023-05-11-22-58-24'


def on_submit():
    prompt = input_field.get()

    completion = openai.Completion.create(model = model_name, prompt=prompt, max_tokens = 200, stop=1, temperature=0.2)

    input_field.delete(0, "end")

    text = completion.choices[0]["text"]

    result_text.config(state= "normal")
    # result_text.delete("1.0")
    result_text.insert("end", text)
    result_text.config(state='disabled')


window = tk.Tk()
window.title("Fine-tuned GPT-3")
# Create the input field and submit button
input_field = tk.Entry(window)
submit_button = tk.Button(window, text="Submit", command=on_submit)
# Create the result text area
result_text = tk.Text(window, state="normal", width=80, height=20)
# Add the input field, submit button, and result text area to the window
input_field.pack()
submit_button.pack()
result_text.pack()

window.mainloop()