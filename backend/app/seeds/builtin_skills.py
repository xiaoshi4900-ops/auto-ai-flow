BUILTIN_SKILLS = [
    {"name": "summarize", "description": "Summarize text content", "prompt_template": "Please summarize the following content concisely:\n\n{input}", "is_builtin": True},
    {"name": "extract", "description": "Extract structured information from text", "prompt_template": "Extract the following information from the text:\n\nFields: {fields}\n\nText: {input}", "is_builtin": True},
    {"name": "translate", "description": "Translate text to target language", "prompt_template": "Translate the following text to {target_language}:\n\n{input}", "is_builtin": True},
    {"name": "analyze", "description": "Analyze and provide insights on content", "prompt_template": "Analyze the following content and provide insights:\n\n{input}", "is_builtin": True},
    {"name": "code_review", "description": "Review code and provide feedback", "prompt_template": "Review the following code and provide feedback on quality, bugs, and improvements:\n\n{input}", "is_builtin": True},
]
