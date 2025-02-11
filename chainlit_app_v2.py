from literalai import LiteralClient
import os
from openai import OpenAI
import json
from datetime import datetime
import logging
from pathlib import Path

# Set up logging
log_filename = f"literalai_error_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_chat_completion(client, prompt):
    """
    Get chat completion from OpenAI API with error handling
    
    Args:
        client: OpenAI client instance
        prompt: String prompt to send to API
        
    Returns:
        dict: Response data including completion text and metadata
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract completion text
        completion_data = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "completion": response.choices[0].message.content,
            "model": response.model,
            "response_id": response.id
        }
        
        # Save to JSON file
        output_filename = f"literalAI_demos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(completion_data, f, indent=4)
            
        return completion_data
        
    except Exception as e:
        error_msg = f"Error getting chat completion: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg}

# Initialize clients
try:
    lai = LiteralClient(api_key=os.getenv("LITERAL_API_KEY"))
    lai.instrument_openai()
    oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    logging.error(f"Error initializing clients: {str(e)}")
    raise

# Example usage
prompt = "Hello, how are you?"
result = get_chat_completion(oai, prompt)

if "error" not in result:
    print(f"Completion saved to: {result['completion']}")
else:
    print(f"Error occurred: {result['error']}")