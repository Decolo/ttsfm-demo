from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ttsfm import TTSClient, AudioFormat

app = FastAPI(title="TTS API", description="Text-to-Speech API using TTSFM")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize TTS client
client = TTSClient()

class TTSRequest(BaseModel):
    text: str
    voice: str = "alloy"
    format: str = "mp3"

@app.get("/")
def read_root():
    return {"message": "TTS API is running"}

@app.post("/tts")
def generate_speech(request: TTSRequest):
    try:
        # Generate speech
        response = client.generate_speech(
            text=request.text,
            voice=request.voice,
            response_format=AudioFormat.MP3 if request.format == "mp3" else AudioFormat.WAV
        )
        
        # Return audio data directly
        return Response(
            content=response.audio_data,
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/voices")
def get_voices():
    return {
        "voices": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 