# Capstone Project: Bloom AI Voice Assistant Demo Guide

This guide outlines a structured sequence of questions and interaction scenarios designed to showcase the full capabilities of **Bloom AI** during your classroom demo.

---

## 📋 Recommended Demo Scenarios & Questions

To demonstrate the full breadth of the voice bot, ask questions from each of the core feature categories below.

### 1. Catalog Search & Filtering (Database/Memory Tools)
*Showcases the bot's ability to query the catalog using complex search constraints (color, flower type, and budget).*
* **Question 1:** *"Show me red roses under 1000 rupees."*
* **Question 2:** *"What yellow flowers do you have available for Friendship Day?"*
* **What to highlight to your class:** The bot parses multiple criteria (color, category, price, and event context) dynamically from voice input.

### 2. Tailored Recommendations
*Demonstrates natural language reasoning for custom arrangements.*
* **Question 3:** *"Can you recommend a premium wedding bouquet for under 3000 rupees?"*
* **Question 4:** *"Suggest a good birthday arrangement."*
* **What to highlight to your class:** The assistant cross-references the catalog's categories (Bouquets, Baskets) and occasions to choose the single best recommendation.

### 3. Live Order Tracking (Real-time Database Lookup)
*Demonstrates state tracking, session memory, and integration with an order database.*
* **Question 5:** *"Can you track my order ORD001?"*
* **Question 6:** *"Where is ORD003?"*
* **What to highlight to your class:** The bot successfully extracts tracking IDs (standardizing them to uppercase) and retrieves customer name, status, delivery date, item details, and price in real-time.

### 4. Policy & Flower Care Knowledge (RAG Integration)
*Demonstrates Retrieval-Augmented Generation (RAG) querying against local knowledge documents (cancellation policies, delivery ranges, care advice).*
* **Question 7:** *"What is your return and refund policy?"*
* **Question 8:** *"Do you offer same-day delivery?"*
* **Question 9:** *"How do I keep my fresh-cut roses alive longer?"*
* **What to highlight to your class:** The bot utilizes a vector database (RAG) to find local store documentation and synthesize answers directly from standard policy PDFs/TXTs rather than generic internet search.

---

## 💡 Tips for a Smooth Live Presentation

1. **Clear Enunciation**: Since you are using a real-time speech-to-text pipeline (Deepgram Nova-3), speak clearly at a normal conversational pace.
2. **Audio Setup**: Ensure your microphone is active and not catching high background noise, as the voice assistant uses voice activity detection (VAD) to decide when you finish speaking.
3. **Session Reset**: If you want to demonstrate a clean run for the next group or class, simply hit **Leave** in the browser interface and then click **Join** to start a fresh chat session.
