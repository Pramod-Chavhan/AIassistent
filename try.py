# import tkinter as tk
# from hugchat import hugchat

# def send_message():
#     user_input = entry.get().lower()
#     if user_input == "exit":
#         response.config(text="Goodbye!")
#         entry.config(state=tk.DISABLED)
#     else:
#         id = chatbot.new_conversation()
#         chatbot.change_conversation(id)
#         response_text = chatbot.chat(user_input)
#         response.config(text=response_text)

# # Initialize the chatbot
# chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")

# # Create the main window
# root = tk.Tk()
# root.title("ChatBot")

# # Create the chat history display
# response = tk.Label(root, text="", wraplength=400, justify=tk.LEFT)
# response.pack(padx=10, pady=10)

# # Create the user input field
# entry = tk.Entry(root, width=50)
# entry.pack(padx=10, pady=10)

# # Create the send button
# send_button = tk.Button(root, text="Send", command=send_message)
# send_button.pack(padx=10, pady=10)

# # Run the application
# root.mainloop()
