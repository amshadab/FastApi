from fastapi import FastAPI
from pydantic import BaseModel
import aiprocess as ap  
import backend  

app = FastAPI()

class Query(BaseModel):
    user_input: str

@app.post("/from_frontend")
async def process_query(query: Query):
    user_input = query.user_input
    try:
        # Process the user's input
        processed_response = ap.processcmd(user_input)
        command, param = backend.process_airesponse(processed_response)

        # Handle cases where command or param is None
        if command is None and param is None:
            result = backend.default_fucntion(processed_response)
            return {"response": result}

        # Call the appropriate action based on the command and param
        action = backend.command_actions.get(command)
        if action:
            if param:
                result = action(param)  # Execute the action with the parameter
            else:
                result = action()  # Execute the action without parameters

            if result:
                return {"response": result}

        # If no meaningful result, return a fallback response
        return {"response": "Command executed but no specific result returned."}

    except Exception as e:
        # Handle unexpected errors
        return {"error": f"An error occurred: {str(e)}"}
