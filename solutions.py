import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as speech_recognition
import pyttsx3
import os
import random
import webbrowser
from datetime import datetime
from openai import OpenAI


url = 'https://youtube.com/'            

# MacOS
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

 
client = OpenAI(api_key = 'Insert API key Here')



# Function to interact with ChatGPT
def ask_gpt(prompt):
    
    messages = [
        {"role": "system", "content": "You are a creative assistant."},
        {"role": "user", "content": prompt},

        
    ]


  
    try:
        # Call the OpenAI API to generate a response
        response = client.chat.completions.create( model="gpt-4", 
                                                
            messages=messages,
            # You can choose another GPT-3.5 engine if needed
            max_tokens=100,
            temperature= 1.0 # Adjust max_tokens as needed for the length of response
        )

        
        text = response.choices[0].message.content.strip()


        return text
    except Exception as e:
        print(f"error generating: {e}")
    

# Example interaction loop
opener= "Welcome to ChatGPT! Ask me anything or say 'exit' to end."

#Load the Speaker
myspeaker = pyttsx3.init()
rate = myspeaker.getProperty('rate')
myspeaker.setProperty('rate', rate-50)


voices = myspeaker.getProperty('voices')       #getting details of current voice
myspeaker.setProperty('voice', voices[4].id)   #changing index, changes voices. 1 for female

#Push to talk(PTT)

# Function to handle user input
def handle_input():
    user_input = user_input_text.get("1.0", tk.END).strip()
    chat_history.insert(tk.END, f"You: {user_input}\n")
    chat_history.see(tk.END)

    if user_input.lower() == 'exit':
        root.destroy()
    else:
        response = ask_gpt(user_input)
        chat_history.insert(tk.END, f"ChatGPT: {response}\n")
        chat_history.see(tk.END)

# Initialize tkinter
root = tk.Tk()
root.title("ChatGPT UI")

# Create UI elements
user_input_label = tk.Label(root, text="User Input:")
user_input_label.pack()

user_input_text = scrolledtext.ScrolledText(root, width=50, height=5)
user_input_text.pack()

submit_button = tk.Button(root, text="Submit", command=handle_input)
submit_button.pack()

chat_history_label = tk.Label(root, text="Chat History:")
chat_history_label.pack()

chat_history = scrolledtext.ScrolledText(root, width=50, height=20)
chat_history.pack()

# Example interaction loop
opener = "Welcome to ChatGPT! Ask me anything or say 'exit' to end."
chat_history.insert(tk.END, f"System: {opener}\n")



#initialize-ation of the recognizer
recognizer = speech_recognition.Recognizer()

print(opener)

with speech_recognition.Microphone() as source:
    myspeaker.say(opener)

while True:
     # Increment session ID for the next interaction

    #Enables Mircophone
    with speech_recognition.Microphone() as source:
        myspeaker.runAndWait()


        print("Say Something...")
        audio = recognizer.listen(source)

        # Recognize speech with Google Speech API
        text = recognizer.recognize_google(audio)
        print("You:", text)

        if text.lower() == 'exit':
            break

        if "run" in text or "open" in text:
            if "browser" in text or "chrome" in text:
                webbrowser.get(chrome_path).open(url)

            elif "calc" in text or "calculator" in text:
                os.system("start calc")

            elif "notepad" in text or "editor" in text:
                os.system("start notepad")

            elif "explorer" in text or "file manager" in text:
                os.system("start explorer")
                
            elif "task manager" in text:
                os.system("start taskmgr")
            else: 
                myspeaker.say("Sorry, I didn't recognize the application.")
                myspeaker.runAndWait()
                break
                
        response = ask_gpt(text)
        print("ChatGPT:", response)
        myspeaker.say(response)

root.mainloop      
    



    