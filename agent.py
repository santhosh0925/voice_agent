import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the directory of this script
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, inference
from livekit.plugins import google, cartesia, noise_cancellation, silero
from livekit.plugins.google.beta import gemini_tts
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from tools.order_tools import track_order
from tools.policy_tools import lookup_policy
from tools.product_tools import recommend_bouquet, search_flowers

class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are BLOOM AI, a warm, friendly, and professional female floral shop salesperson for a real-time flower shop. "
                "Always speak in a warm, welcoming, and polite female tone. "
                "Always respond in the same language the customer speaks to you (e.g. if they speak Hindi, respond in Hindi; if Spanish, respond in Spanish; if English, respond in English). "
                "CRITICAL: Always refer to prices in Indian Rupees (INR, ₹). Never use dollars ($) or mention USD. If the user asks for roses under 1000, refer to it as 1000 Rupees or ₹1000, not $1000. "
                "Help customers choose flowers, recommend bouquets, track orders, and answer flower-care or shop-policy questions. "
                "Use search_flowers for catalog requests, recommend_bouquet for occasions, track_order for order IDs, "
                "and lookup_policy for delivery, returns, refunds, care, or FAQ questions. Never invent catalog, order, "
                "availability, or policy facts. Explain briefly why a recommendation matches. Remember the customer's name, "
                "favorite flower, budget, occasion, and current order during this conversation."
            ),
            tools=[search_flowers, recommend_bouquet, track_order, lookup_policy],
        )



async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=inference.STT("deepgram/nova-3"),
        llm=google.LLM(
            model="gemini-flash-lite-latest",
            api_key=os.environ.get("GOOGLE_API_KEY")
        ),
        tts=inference.TTS("cartesia/sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
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

    @session.on("user_input_transcribed")
    def on_user_input(ev):
        if ev.language:
            lang_str = getattr(ev.language, "language", None) or str(ev.language)
            if "-" in lang_str:
                lang_str = lang_str.split("-")[0]
            print(f"DEBUG: Detected language: {lang_str}")
            try:
                if hasattr(session.tts, "update_options"):
                    session.tts.update_options(language=lang_str)
            except Exception as tts_err:
                print(f"Error updating TTS language: {tts_err}")

    await session.say("Welcome to BLOOM AI Floral Shop! How can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
