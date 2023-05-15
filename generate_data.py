import csv
import json

with open('template.csv', 'r') as file:
    data = list(csv.reader(file))
    cols = data[0]
    data = data[1:]

print(cols)
# The health insurance plan is a Gold level plan and has a policy number of AB12345.
# The employee enrolled in the plan is named John Doe. The plan starts on January 5th, 2023, and the employee is required to pay a premium of $150 for the coverage.
pairs = []
for emp in data:
    prompt = f"Write a health insurance summary for {emp[cols.index('EmployeeName')]}"
    report = f"The health insurance plan is a {emp[cols.index('Plan')]} level plan and has a policy number of {emp[cols.index('PolicyNumber')]}. The employee enrolled in the plan is named {emp[cols.index('EmployeeName')]}" \
             f"The plan starts on {emp[cols.index('Date')]}, and the employee is required to pay a premium of ${emp[cols.index('Premium')]} for the coverage."
    pairs.append({"prompt": prompt, "completion": report})

with open('prompt_reports.json', 'w') as file:
    json.dump(pairs, file)