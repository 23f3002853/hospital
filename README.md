# AI Enabled Conversational IVR Modernization Framework (Hospital Management)

## Problem Statement
Traditional IVR systems used in hospitals are rule-based, inflexible, and difficult to integrate
with modern platforms. They lack conversational intelligence and real-time interaction.

## Objective
To design and implement an AI-enabled conversational IVR system that supports voice-based
hospital services such as balance enquiry and complaint registration using open-source tools.

## Approach Taken
- Twilio: Voice call handling (Speech-to-Text & Text-to-Speech)
- Rasa: Conversational AI engine
- Flask: Integration layer (replaces ACS/BAP)

## Architecture Overview
The caller interacts via a phone call. Twilio captures speech and forwards it to the Flask
application, which sends the request to Rasa for intent processing. The response is converted
back to voice and played to the caller.

## Features
- Voice-based interaction
- AI-driven conversation flow
- Modular and scalable architecture
- Replacement for legacy ACS/BAP IVR systems

## Limitations
- Trial account limitations in Twilio
- Limited intents for demonstration

## Conclusion
This project demonstrates a modern IVR system using conversational AI, suitable for hospital
management applications.

## How to Run
1. Start Rasa server
2. Start Flask application
3. Expose Flask using ngrok
4. Configure Twilio webhook
