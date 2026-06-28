import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the directory of this script
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, inference
from livekit.plugins import google, cartesia, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

class Assistant(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice AI assistant behalf of Santhosh")



async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=inference.STT("deepgram/nova-3"),
        llm=google.LLM(
            model="gemini-2.5-flash",
            api_key=os.environ.get("GOOGLE_API_KEY")
        ),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.say("Hello! How can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
