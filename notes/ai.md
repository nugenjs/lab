# AI


### Dictionary
`tool calling`: ability for LLM to access information or perform actions (search, database) [source](https://medium.com/@developer.yasir.pk/tool-calling-for-llms-a-detailed-tutorial-a2b4d78633e2)\
`function calling`: llm to interact with predefined functions with structured inputs and outputs [source](https://medium.com/@shuremsyed41/function-calling-vs-tool-calling-in-llms-a-beginner-friendly-guide-2d9d7cbee261)\
``



### LLM suggestions [source](https://medium.com/data-science-collective/youre-using-chatgpt-wrong-here-s-how-to-prompt-like-a-pro-1814b4243064)
- Ask LLM to play a role. This adjusts tone and narrows context
- Role based decomposition to effectively get a result based on layers of roles (scientist for white paper explaination, then uni professor to simplify explanation to college level)
- Use Train-of-Thought prompts to elicit intermediate steps. Those steps become self-conditioning context that reduces uncertainty (lower entropy) and biases generation toward learned reasoning patterns; by committing to intermediate claims, the model constrains later tokens to stay consistent with them.


