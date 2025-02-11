"""
TODO: Fix this: DeprecationWarning: Use Literal.initialize instead
  lai.instrument_openai()

"""

from literalai import LiteralClient
import os
from openai import OpenAI
import json
from datetime import datetime
import logging
from pathlib import Path
from dotenv import load_dotenv

# Create output directories
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR = OUTPUT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
COMPLETION_DIR = OUTPUT_DIR / "completions"
COMPLETION_DIR.mkdir(exist_ok=True)

# Load environment variables
load_dotenv()

# Set up logging
log_filename = LOG_DIR / f"chainlit_error_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_api_keys():
    """
    Validate that required API keys are present in environment variables
    
    Returns:
        bool: True if all required keys are present, False otherwise
    """
    required_keys = ["LITERAL_API_KEY", "OPENAI_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        logging.error(f"Missing required API keys: {', '.join(missing_keys)}")
        return False
    return True

def get_chat_completion(client, prompt):
    """
    Get chat completion from OpenAI API with error handling
    
    Args:
        client: OpenAI client instance
        prompt: String prompt to send to API
        
    Returns:
        tuple: (dict with response data, str filepath) or (dict with error, None)
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        completion_data = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "completion": response.choices[0].message.content,
            "model": response.model,
            "response_id": response.id
        }
        
        output_filename = COMPLETION_DIR / f"chainlit_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(completion_data, f, indent=4)
            
        return completion_data, str(output_filename.absolute())
        
    except Exception as e:
        error_msg = f"Error getting chat completion: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg}, None

def main():
    """Main execution function"""
    if not validate_api_keys():
        logging.error("Missing required API keys. Please check your .env file.")
        print("Missing required API keys. Please check your .env file.")
        return

    try:
        lai = LiteralClient(api_key=os.getenv("LITERAL_API_KEY"))
        lai.instrument_openai()
        oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = "Hello, how are you?"
        result, filepath = get_chat_completion(oai, prompt)

        if "error" not in result:
            print("\nAPI Response:")
            print("-" * 50)
            print(f"Prompt: {prompt}")
            print(f"Response: {result['completion']}")
            print("-" * 50)
            print(f"\nOutput saved to: {filepath}")
        else:
            print(f"Error occurred: {result['error']}")
            
    except Exception as e:
        logging.error(f"Error initializing clients: {str(e)}")
        raise

if __name__ == "__main__":
    main()