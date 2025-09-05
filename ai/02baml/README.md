# BAML 

### Issue
Native structured output exists on few proprietary models.\
Models with native JSON mode can still return hallucinate structures.

### Solution
LLMs are good at responding with JSON. Use libraries to parse JSON that implement boilerplate checks.\
BAML handles creating Pydantic (and other language typedefs)\
Build in retries\
Fall back to other models



### 01_coercing_structured_response, a look into parsing output standard LLM output
Sometimes this fails due to llm returning an entirely different structure\
Good response: `{"name": "John Doe","skills": ["Python programming","Machine Learning","Web Development","Database Management","API Development"]}`\
Bad response: `{"candidate": {"name": "John Doe", "skills": ["Python programming", "Machine Learning", "Web Development", "Database Management", "API Development"]}}`


### Setup
`uv init`\
`uv add pydantic requests`

### Run
`uv run python3 01_coercing_structured_response.py`


### 02


### Setup
`uv init`\
`uv add baml-py`\
`uv run baml-cli init`\
Installing BAML extention for vscode if applicable\



### sources
[baml-the-structured-output-power...](https://medium.com/@manavisrani07/baml-the-structured-output-power-tool-your-llm-workflow-has-been-missing-f326046d019b)\
[baml-vs-pydantic](https://docs.boundaryml.com/guide/comparisons/baml-vs-pydantic)
[TypeChat](https://microsoft.github.io/TypeChat/docs/introduction/)
