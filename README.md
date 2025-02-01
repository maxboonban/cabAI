cab-llm

reference : https://python.langchain.com/docs/tutorials/rag/

```
touch .env
LANGSMITH_TRACING="true"
LANGSMITH_API_KEY="..."
OPENAI_API_KEY=
```

```
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file
api_key = os.getenv("API_KEY")
print(api_key)
```