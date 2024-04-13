
# from hugchat import hugchat
# from bs4 import BeautifulSoup

# def chatBot():
#     chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
#     while True:
#         user_input = input("You: ").lower()
#         if user_input == "exit":
#             print("Goodbye!")
#             break
#         id = chatbot.new_conversation()
#         chatbot.change_conversation(id)
#         response =  chatbot.chat(user_input)
#         print("ChatBot:", response)

# if __name__ == "__main__":
#     chatBot()


# from pathlib import Path
# import torch
# import pandas as pd
# import numpy as np
# import tqdm
# import cv2
# import matplotlib.pyplot as plt
# from diffusers import StableDiffusionPipeline
# from transformers import pipeline, set_seed
# import torch

# # Ensure all import statements are present
# # Ensure token authentication if using a private model from Hugging Face

# # Define CFG class before usage
# class CFG:
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     seed = 42
#     generator = torch.Generator(device=device).manual_seed(seed)
#     image_gen_steps = 35
#     image_gen_model_id = "stabilityai/stable-diffusion-2"
#     image_gen_size = (400,400)
#     image_gen_guidance_scale = 9
#     prompt_gen_model_id = "gpt2"
#     prompt_dataset_size = 6
#     prompt_max_length = 12

# # Define generate_image function before calling it
# def generate_image(prompt, model):
#     image = model(
#         prompt, num_inference_steps=CFG.image_gen_steps,
#         generator=CFG.generator,
#         guidance_scale=CFG.image_gen_guidance_scale
#     ).images[0]
    
#     image = image.resize(CFG.image_gen_size)
#     return image

# # Initialize the image generation model
# image_gen_model = StableDiffusionPipeline.from_pretrained(
#     CFG.image_gen_model_id,
#     use_auth_token='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', 
#     guidance_scale=9
# )
# image_gen_model = image_gen_model.to(CFG.device)

# # Call the generate_image function with a prompt
# generated_image = generate_image("dog on tree", image_gen_model)
# # Display or save the generated image as needed
# generated_image.show()

import sys
import webbrowser
from numpy import source
import psutil
import pyttsx3
import speech_recognition as sr
import eel
import time
import pyautogui
import os
from PIL import Image

# Import CLIP from Hugging Face
from transformers import CLIPProcessor, CLIPModel
import torch

# Initialize CLIP model and processor
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

# Function to generate image from text
def generate_image(text):
    inputs = clip_processor(text, return_tensors="pt", padding=True)
    image_features = clip_model.get_image_features(**inputs)
    return image_features.cpu().numpy()

# Initialize text-to-speech engine
def initialize_engine():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    return engine

# Initialize speech recognizer
def initialize_recognizer():
    recognizer = sr.Recognizer()
    return recognizer

# Function to speak text
def speak(engine, text):
    text = str(text)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech(recognizer):
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10)
    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        return query.lower()
    except Exception as e:
        print("Error:", e)
        return ""

# Main function to handle commands
@eel.expose
def handle_command():
    engine = initialize_engine()
    recognizer = initialize_recognizer()
    query = recognize_speech(recognizer)

    if query:
        if "generate image" in query:
            # Extract text for generating image
            text_to_generate = query.replace("generate image", "").strip()
            image_features = generate_image(text_to_generate)
            # Process image_features to generate image
            # ...
            speak(engine, "Image generated successfully.")
        elif "other_commands" in query:
            # Handle other commands
            pass
        else:
            speak(engine, "Command not recognized.")

# Expose a function to start the application
@eel.expose
def start_application():
    eel.init('web')
    eel.start('index.html', size=(700, 600))

# Start the application
start_application()
