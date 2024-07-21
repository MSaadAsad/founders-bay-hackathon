import os
from dotenv import load_dotenv
from multion.client import MultiOn
from fastapi import FastAPI
from pydantic import BaseModel

"""
Prompt:

Analyze the following conversation transcript for both formal and informal logical fallacies. For each fallacy found, provide the following information:

Type of Fallacy: Specify the fallacy (e.g., Ad Hominem, Straw Man, etc.).
Excerpt: Include the exact part of the transcript where the fallacy occurs.
Explanation: Explain how the excerpt exemplifies the fallacy.
Format the results in a clear, readable manner with bullet points and headings.

Conversation Transcript:

[Insert transcript here]
"""
    
load_dotenv()

app = FastAPI()

api_key = os.getenv("MULTI_ON_API_KEY")
client = MultiOn(api_key=api_key)

class CommandRequest(BaseModel):
    command: str
    agent_id: str = "e5f447e3"

@app.post("/")
def execute_command(request: CommandRequest):
    try:

        response = client.browse(cmd="Fact check this claim: "+request.command, agent_id=request.agent_id)
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
