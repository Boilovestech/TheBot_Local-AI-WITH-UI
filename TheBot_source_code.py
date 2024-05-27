import requests
import json
import customtkinter as ctk
from tkinter import END, N, S, E, W
import threading

# URL and headers for API requests
url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json',
}

# Conversation history
conversation_history = []

# Function to generate a response from the AI
def generate_response(prompt):
    # Append the new prompt to the conversation history
    conversation_history.append("You: " + prompt)

    # Combine the conversation history into a single prompt
    full_prompt = "\n".join(conversation_history)

    data = {
        "model": "phi3:mini",  # Using the "phi3" model which is available
        "stream": False,
        "prompt": full_prompt,
    }

    # Make the POST request to the API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check for a successful response
    if response.status_code == 200:
        response_data = response.json()
        actual_response = response_data.get("response", "")
        conversation_history.append("AI: " + actual_response)
        return actual_response
    else:
        print("Error:", response.status_code, response.text)
        return "Error: Unable to get a response from the server."

# Function to send message and update the chatbox
def send_message():
    user_input = input_entry.get()
    if user_input.strip() == "":
        return
    update_chatbox("🙂: " + user_input + "\n")
    input_entry.delete(0, END)

    # Start a new thread to handle the API request
    threading.Thread(target=handle_response, args=(user_input,)).start()

# Function to handle response in a separate thread
def handle_response(user_input):
    # Start the loading animation
    start_loading_animation()

    response = generate_response(user_input)
    
    # Stop the loading animation
    stop_loading_animation()

    update_chatbox("🤖: " + response + "\n")

# Function to update the chatbox
def update_chatbox(message):
    chatbox.configure(state="normal")
    chatbox.insert(END, message)
    chatbox.configure(state="disabled")
    chatbox.see(END)  # Scroll to the end of the chatbox

# Function to start the loading animation
def start_loading_animation():
    global loading, loading_label
    loading = True
    loading_label.grid(row=2, column=0, columnspan=2, pady=10)
    rotate_loading_circle()

# Function to stop the loading animation
def stop_loading_animation():
    global loading, loading_label
    loading = False
    loading_label.grid_forget()

# Function to rotate the loading circle
def rotate_loading_circle():
    if loading:
        current_text = loading_label.cget("text")
        new_text = "Processing" + "." * ((current_text.count(".") + 1) % 3)
        loading_label.configure(text=new_text)
        app.after(500, rotate_loading_circle)
ctk.set_default_color_theme("dark-blue")
# Setting up the main application window
app = ctk.CTk()

app.title("AI Chatbot (Phi-3 Mini)")
app.geometry("600x400")
# Configure the grid layout to make the widgets resizable
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=0)
app.grid_rowconfigure(2, weight=0)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=0)

# Font used in the application
app_font = ("Tw Cen MT Bold", 20)  # Tw Cen MT Bold font with size 12

# Creating the chatbox to display conversation history
chatbox = ctk.CTkTextbox(app, state="disabled", font=app_font)
chatbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=N+S+E+W)
update_chatbox("Chat with me!\n")

# Creating an entry widget for user input
input_entry = ctk.CTkEntry(app, font=app_font)
input_entry.grid(row=1, column=0, padx=10, pady=10, sticky=E+W)

# Creating a send button
send_button = ctk.CTkButton(app, text="Send", command=send_message, font=app_font)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky=E)

# Creating a loading label
loading_label = ctk.CTkLabel(app, text="Loading", font=app_font)

# Running the application
app.mainloop()

