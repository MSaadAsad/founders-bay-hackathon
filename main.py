import os
from dotenv import load_dotenv
from multion.client import MultiOn
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

api_key = os.getenv("MULTI_ON_API_KEY")
client = MultiOn(api_key=api_key)

class CommandRequest(BaseModel):
    command: str
    agent_id: str = "c9a5d7b0"

@app.post("/")
def execute_command(request: CommandRequest):
    try:
        response = client.browse(cmd=request.command, agent_id=request.agent_id)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

@app.post('/examine-convo')
def orchestrate_agents(uid: str, data: dict):
    session_id = data['session_id']
    segments = data['segments']

    transcript_text = segments['text']
    speaker = segments['speaker']
    speaker_id = segments['speaker_id']
    is_user = segments['is_user']

    request = CommandRequest(command=transcript_text)

    response = execute_command(request)

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
