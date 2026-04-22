BUILTIN_TOOLS = [
    {"name": "http_request", "description": "Make HTTP requests to external APIs", "tool_type": "function", "config": '{"method": "GET", "url": "", "headers": {}}', "is_builtin": True},
    {"name": "file_read", "description": "Read file content", "tool_type": "function", "config": '{"path": ""}', "is_builtin": True},
    {"name": "file_write", "description": "Write content to file", "tool_type": "function", "config": '{"path": "", "content": ""}', "is_builtin": True},
    {"name": "json_parse", "description": "Parse and extract data from JSON", "tool_type": "function", "config": '{"path": ""}', "is_builtin": True},
    {"name": "web_search", "description": "Search the web for information", "tool_type": "function", "config": '{"query": "", "max_results": 5}', "is_builtin": True},
]
