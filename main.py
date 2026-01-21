import os
import sys
import argparse
from google import genai
from dotenv import load_dotenv
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("Gemini api-key not found.")
client = genai.Client(api_key=api_key)



def main():
    print("Hello from aiagent!")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    # Now we can access `args.user_prompt`
    for _ in range(20):
        response = generate_content(client,messages,args.verbose)
        if isinstance(response,str):
            print("Fi   nal response:")
            print(response)
            return
        else:
            if response.candidates:
                for item in response.candidates:
                    messages.append(item.content)
    print("Maximum iterations reached without a final response")
    sys.exit(1)

def generate_content(client, messages,verbose):
    response =  client.models.generate_content(
        model='gemini-2.5-flash', contents= messages, config = types.GenerateContentConfig(tools = [available_functions], system_instruction = system_prompt),)
    if not response.usage_metadata:
        raise RuntimeError("Property usage_metadata not found, failed API request.")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if not response.function_calls:
        return response.text
    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call,verbose)
        if not function_call_result.parts:
            raise Exception("No parts returned from function call")
        first_part = function_call_result.parts[0]
        if not first_part.function_response:
            raise Exception("Function response is None")
        if first_part.function_response.response is None:
            raise Exception("Function response body is None")
        if verbose:
            print(f"-> {first_part.function_response.response['result']}")
        function_responses.append(first_part)
    messages.append(types.Content(role="user", parts=function_responses))
    return response
if __name__ == "__main__":
    main()