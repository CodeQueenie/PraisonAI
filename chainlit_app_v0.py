from literalai import LiteralClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize LiteralAI client
lai = LiteralClient(api_key=os.getenv("LITERAL_API_KEY"))
lai.instrument_openai()

# Initialize OpenAI client
from openai import OpenAI
oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Run a regular OpenAI chat completion
oai.chat.completions.create(
    model="gpt-4o",
    messages=[{ "role": "user", "content": "Hello, how are you?" }]
)

# Run a LiteralAI chat completion
lai.chat.completions.create(
    model="gpt-4o",
    messages=[{ "role": "user", "content": "Hello, how are you?" }]
)
