import os
import json
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AkeylessClient:
    """Client to interact with Akeyless API"""
    
    def __init__(self, access_id, access_key, gateway_url="https://api.akeyless.io"):
        self.access_id = access_id
        self.access_key = access_key
        self.gateway_url = gateway_url
        self.token = None
        print("✓ Akeyless client initialized")
    
    def _get_token(self):
        """Get a fresh authentication token"""
        url = f"{self.gateway_url}/auth"
        payload = {
            "access-id": self.access_id,
            "access-key": self.access_key
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            token = response.json().get("token")
            return token
        except Exception as e:
            print(f"✗ Authentication failed: {str(e)}")
            raise
    
    def get_static_secret(self, secret_name):
        """Get static secret value"""
        token = self._get_token()  # Fresh token for each call
        url = f"{self.gateway_url}/get-secret-value"
        clean_name = secret_name.lstrip('/')
        
        payload = {
            "token": token,
            "names": [clean_name],
            "json": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            print(f"   ✓ Retrieved secret successfully")
            
            if isinstance(result, dict) and clean_name in result:
                secret_value = result[clean_name]
                
                if isinstance(secret_value, str):
                    try:
                        parsed_value = json.loads(secret_value)
                        if isinstance(parsed_value, dict):
                            return {
                                "name": secret_name,
                                "type": "structured",
                                "fields": parsed_value,
                                "success": True
                            }
                    except json.JSONDecodeError:
                        pass
                    
                    return {
                        "name": secret_name,
                        "type": "simple",
                        "value": secret_value,
                        "success": True
                    }
                else:
                    return {"name": secret_name, "value": secret_value, "success": True}
            else:
                return {"name": secret_name, "value": result, "success": True}
                
        except Exception as e:
            error_detail = e.response.text if hasattr(e, 'response') else str(e)
            print(f"   ✗ Error: {error_detail}")
            return {"error": str(e), "detail": error_detail}
    
    def get_rotated_secret(self, secret_name):
        """Get rotated secret details"""
        token = self._get_token()
        url = f"{self.gateway_url}/get-rotated-secret-value"
        clean_name = secret_name.lstrip('/')
        
        payload = {"token": token, "names": [clean_name], "json": False}
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, dict) and clean_name in result:
                secret_value = result[clean_name]
                
                if isinstance(secret_value, str):
                    try:
                        parsed_value = json.loads(secret_value)
                        if isinstance(parsed_value, dict):
                            return {"name": secret_name, "type": "structured", "fields": parsed_value}
                    except:
                        pass
                
                return {"name": secret_name, "value": secret_value}
            else:
                return {"name": secret_name, "value": result}
        except Exception as e:
            return {"error": str(e)}
    
    def get_dynamic_secret(self, secret_name):
        """Get dynamic secret value"""
        token = self._get_token()
        url = f"{self.gateway_url}/get-dynamic-secret-value"
        clean_name = secret_name.lstrip('/')
        
        payload = {"token": token, "name": clean_name}
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def list_secrets(self, path="/", secret_type=None):
        """List all secrets at a given path"""
        token = self._get_token()
        url = f"{self.gateway_url}/list-items"
        
        clean_path = path.rstrip('/*').rstrip('/')
        if not clean_path:
            clean_path = "/"
            
        payload = {"token": token, "path": clean_path}
        
        if secret_type:
            payload["type"] = secret_type
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_secret_metadata(self, secret_name):
        """Get secret metadata"""
        token = self._get_token()
        url = f"{self.gateway_url}/describe-item"
        clean_name = secret_name.lstrip('/')
        
        payload = {"token": token, "name": clean_name}
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def count_secrets_by_type(self, path="/"):
        """Count secrets by type"""
        all_items = self.list_secrets(path)
        
        if "error" in all_items:
            return all_items
        
        items = all_items.get("items", [])
        
        counts = {"total": len(items), "static": 0, "rotated": 0, "dynamic": 0, "other": 0}
        items_by_type = {"static": [], "rotated": [], "dynamic": [], "other": []}
        
        for item in items:
            item_type = item.get("item_type", "").upper()
            item_name = item.get("item_name", "unknown")
            
            if "STATIC" in item_type:
                counts["static"] += 1
                items_by_type["static"].append(item_name)
            elif "ROTATED" in item_type:
                counts["rotated"] += 1
                items_by_type["rotated"].append(item_name)
            elif "DYNAMIC" in item_type:
                counts["dynamic"] += 1
                items_by_type["dynamic"].append(item_name)
            else:
                counts["other"] += 1
                items_by_type["other"].append(item_name)
        
        return {"counts": counts, "items_by_type": items_by_type}


class AkeylessGeminiAgent:
    """AI Agent that uses Gemini to interact with Akeyless"""
    
    def __init__(self, akeyless_client, gemini_api_key):
        self.akeyless = akeyless_client
        
        genai.configure(api_key=gemini_api_key)
        
        self.model = genai.GenerativeModel(
            model_name='models/gemini-2.5-flash',
            tools=[
                self.get_static_secret,
                self.get_rotated_secret,
                self.get_dynamic_secret,
                self.list_secrets,
                self.get_secret_metadata,
                self.count_secrets_by_type
            ]
        )
        
        self.chat_session = self.model.start_chat(history=[])
        
        self.system_instruction = """You are an AI assistant that helps users manage and retrieve secrets from Akeyless Secret Management. 

You have access to several tools to interact with Akeyless:
- get_static_secret: For manually managed key-value secrets
- get_rotated_secret: For automatically rotated secrets (passwords, API keys)
- get_dynamic_secret: For on-demand generated secrets with TTL (temporary credentials)
- list_secrets: To browse and list secrets
- get_secret_metadata: To get detailed information about secrets
- count_secrets_by_type: To count secrets by type

When users ask about secrets, use the appropriate tool to fetch the information. Be helpful, clear, and security-conscious in your responses."""
    
    def get_static_secret(self, secret_name: str) -> dict:
        """Retrieves the value of a static secret from Akeyless."""
        return self.akeyless.get_static_secret(secret_name)
    
    def get_rotated_secret(self, secret_name: str) -> dict:
        """Retrieves a rotated secret from Akeyless."""
        return self.akeyless.get_rotated_secret(secret_name)
    
    def get_dynamic_secret(self, secret_name: str) -> dict:
        """Generates and retrieves a dynamic secret from Akeyless."""
        return self.akeyless.get_dynamic_secret(secret_name)
    
    def list_secrets(self, path: str = "/", secret_type: str = None) -> dict:
        """Lists all secrets in Akeyless at a given path."""
        return self.akeyless.list_secrets(path, secret_type)
    
    def get_secret_metadata(self, secret_name: str) -> dict:
        """Gets detailed metadata about a secret."""
        return self.akeyless.get_secret_metadata(secret_name)
    
    def count_secrets_by_type(self, path: str = "/") -> dict:
        """Counts the total number of secrets and breaks them down by type."""
        return self.akeyless.count_secrets_by_type(path)
    
    def chat(self, user_message):
        """Send a message and get a response from the AI agent"""
        
        print(f"\n🤖 Processing your request...\n")
        
        try:
            full_message = f"{self.system_instruction}\n\nUser: {user_message}"
            response = self.chat_session.send_message(full_message)
            
            while response.candidates[0].content.parts:
                part = response.candidates[0].content.parts[0]
                
                if hasattr(part, 'function_call') and part.function_call:
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = dict(function_call.args)
                    
                    print(f"🔧 Using tool: {function_name}")
                    print(f"   Input: {json.dumps(function_args, indent=2)}")
                    
                    if function_name == "get_static_secret":
                        result = self.get_static_secret(**function_args)
                    elif function_name == "get_rotated_secret":
                        result = self.get_rotated_secret(**function_args)
                    elif function_name == "get_dynamic_secret":
                        result = self.get_dynamic_secret(**function_args)
                    elif function_name == "list_secrets":
                        result = self.list_secrets(**function_args)
                    elif function_name == "get_secret_metadata":
                        result = self.get_secret_metadata(**function_args)
                    elif function_name == "count_secrets_by_type":
                        result = self.count_secrets_by_type(**function_args)
                    else:
                        result = {"error": f"Unknown function: {function_name}"}
                    
                    response = self.chat_session.send_message(
                        genai.protos.Content(
                            parts=[
                                genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=function_name,
                                        response={'result': result}
                                    )
                                )
                            ]
                        )
                    )
                else:
                    break
            
            return response.text
            
        except Exception as e:
            return f"Error: {str(e)}"


def main():
    """Main function to run the AI agent"""
    
    print("=" * 60)
    print("  Akeyless AI Agent - Powered by Gemini")
    print("=" * 60)
    
    akeyless_access_id = os.getenv("AKEYLESS_ACCESS_ID")
    akeyless_access_key = os.getenv("AKEYLESS_ACCESS_KEY")
    akeyless_gateway_url = os.getenv("AKEYLESS_GATEWAY_URL", "https://api.akeyless.io")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not all([akeyless_access_id, akeyless_access_key, gemini_api_key]):
        print("\n❌ Error: Missing required environment variables")
        print("\nPlease create a .env file with:")
        print("  AKEYLESS_ACCESS_ID=your_access_id")
        print("  AKEYLESS_ACCESS_KEY=your_access_key")
        print("  AKEYLESS_GATEWAY_URL=https://api.akeyless.io")
        print("  GEMINI_API_KEY=your_gemini_key")
        return
    
    try:
        akeyless_client = AkeylessClient(
            access_id=akeyless_access_id,
            access_key=akeyless_access_key,
            gateway_url=akeyless_gateway_url
        )
        
        agent = AkeylessGeminiAgent(akeyless_client, gemini_api_key)
        
        print("\n✓ Agent initialized successfully!")
        print("\nYou can now ask questions about your secrets. Examples:")
        print("  - 'List all my secrets'")
        print("  - 'Get the secret secrets/MysecondSecret'")
        print("  - 'How many secrets do I have?'")
        print("  - 'Show me MyFirstSecret'")
        print("\nType 'quit' or 'exit' to stop.\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            try:
                response = agent.chat(user_input)
                print(f"\nAgent: {response}\n")
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
    
    except Exception as e:
        print(f"\n❌ Failed to initialize agent: {str(e)}")


if __name__ == "__main__":
    main()