# FetchAI Hackathon - Team 3

1. [Problem Statement](#problem-statement)
2. [Solution](#solution)
   1. [Extraction Agent](#1-extraction-agent)
   2. [Rules Generator Agent](#2-rules-generator-agent)
   3. [Recommendation Agent](#3-recommendation-agent)
3. [Assumptions/Considerations](#assumptionsconsiderations)
4. [Improvements/Questions](#improvementsquestions)

**Quick links**

- Backend [README](./backend/README.md)
- Frontend [README](./frontend/README.md)

### Problem statement

Life Insurance companies will receive requests from companies (technically their trustees) to take responsibility their pension scheme. This request can come in multiple formats but is officially known as a Pension Transfer Risk document. Two important components of this document are the Defined Benefit Pension Scheme and employee data. The latter may contain information, such as age, tenure, health risks, status (active, retired, deferred, etc).

When a insurer receives a PTR document, they typically will gauge the risk involved and send an offer for a premium price plan. Using insurers can provide a safety net for employers against risks, such as investment risk, longetivity risk, and inflation risk.

Our challenge specically deals with the **Defined Benefit Scheme**, which is a type of occupational pension scheme and will provide a fixed income for live. Hence there are a few factors that would affect the pricing of this scheme, such as life expectancy, what happens with the pension once a person dies (e.g. is it passed to a partner or dependants and at which percentage?)

Our application attempts to calculate the likely pension cost of an individual employee, and with all these summed up, the total pension cost for the company. Based on this cost and some other factors, a premium is calculated.

### Solution

The program functionality mainly revolves around three agents:

**Extraction agent**
This agent extracts key information from Defined Benefit Scheme. It focuses on key information such as, age boundaries (which can be based on gender, disability, tenure, etc), inflation factors, post-mortem pension benefits to partner or children, and more.

**Rules generator agent**
With the use of a LLM, a python script is generated that is based on the Defined Benefit Scheme and the employee data (the actual script will get saved at `src/temp.py` if you want to check it out).
This script is subsequently called with the dummy Employee data found in `src/data/data.json` and will generate another file with pension meta data for each employee. This meta data answers questions, such as

- Can the employee be described as 'incapacitated' and/or has the employee right to any disability benefits?
- what happens to the pension when the person dies, at what percentage is it passed to a parter or dependents?
- what is the inflation percentage applied to a employee's pension
- is the employee already receiving a pension or do they need to wait X more years?

**Recommendation agent**
The output from above helps to estimate the total pension amount each employee is eligible for, which in turn, is used to calculate the risk that the employer will pay in the form of a insurance premium.
The recommendation agent utilises a mathematical model that is well-described in `src/agents/recommendations_utils.py`. In essence, it calculates a certain risk factor for each employee which is a small percentage of their total theoretical pension payout. This percentage can change based on the person's gender, habits (such as smoking), having a family, age, etc.
**Final output**
The final output is the total payable insurance premium that will cover all risks of all the employees' pensions that were included at the time of request.
Lastly, a final yearly premium is included. This is the final output divided by the avg number of pension years across all employees.

##### Assumptions/considerations

- A **buy-in** pension plan is assumed in the mathematical model in the 3rd agent. The employer remains responsible for the fixed payments. The insurer takes responsibility for the risks that were earlier mentioned.
- The program works based on a simplified, structured model of employee records. Normally, employee records may be unstructured.
- The OpenAI is used for code generation and does not guarantee an executable result each time. Most of the time it works though.
- No security measures are applied when executing the generated code. This would be future work.

### Improvements/questions

- Integration between frontend and backend
- Developing more insurance premium pricing plans or estimation models.
- Improve reliability of code generation: try to get consistent, stable results each time. 95% of the time it works tough.
- Make agents compatible with the AI engine to enable inter-agent communication instead of outsourcing that to the Flask backend.
- The current premium pricing plan can be expensive for large companies since it linearly scales with the number of employees. An other idea would be to apply fix rates, however, such as scheme may not be profitable from the insurer's perspective. This is still an open-ended question
