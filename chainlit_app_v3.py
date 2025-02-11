from literalai import LiteralClient
import os
from openai import OpenAI
import json
from datetime import datetime
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
log_filename = f"literalai_error_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
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
        dict: Response data including completion text and metadata
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
        
        output_filename = f"literalAI_demos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(completion_data, f, indent=4)
            
        return completion_data
        
    except Exception as e:
        error_msg = f"Error getting chat completion: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg}

def main():
    """Main execution function"""
    if not validate_api_keys():
        print("Missing required API keys. Please check your .env file.")
        return

    try:
        lai = LiteralClient(api_key=os.getenv("LITERAL_API_KEY"))
        lai.instrument_openai()
        oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = "Hello, how are you?"
        result = get_chat_completion(oai, prompt)

        if "error" not in result:
            print(f"Completion saved to: {result['completion']}")
        else:
            print(f"Error occurred: {result['error']}")
            
    except Exception as e:
        logging.error(f"Error initializing clients: {str(e)}")
        raise

if __name__ == "__main__":
    main()