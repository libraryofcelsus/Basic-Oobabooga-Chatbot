import os
import json
import requests


# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/chat'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'


# Function for generating a reply form the Oobabooga Api
def oobabooga(instruction, user_name, prompt):
    # History is set to empty, a custom conversation list will be used instead.
    history = {'internal': [], 'visible': []}
    request = {
        'user_input': prompt,
        'max_new_tokens': 800,
        'history': history,
        'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        'instruction_template': 'Llama-v2',  # Will get autodetected if unset
        # Set to a passthrough Variable so the function can be used with multiple system prompts.
        'context_instruct': f"{instruction}",  # Optional
        # Set to a passthrough Variable so the function can be used across multiple user's.
        'your_name': f'{user_name}',

        'regenerate': False,
        '_continue': False,
        'stop_at_newline': False,
        'chat_generation_attempts': 1,
        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',  
        'do_sample': True,
        'temperature': 0.85,
        'top_p': 0.2,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'top_k': 40,
        'min_length': 100,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 4096,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['history']
        return result['visible'][-1][1]
        
        
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
        
    
# Custom Conversation History List, this was done so the api can be swapped without major code rewrites.
class MainConversation:
    def __init__(self, max_entries, prompt, greeting):
        try:
            # Set Maximum conversation Length
            self.max_entries = max_entries
            # Set path for Conversation History
            self.file_path = f'./main_conversation_history.json'
            # Set Main Conversatoin with Main and Greeting Prompt
            self.main_conversation = [prompt, greeting]
            # Load existing conversation from file or set to empty.
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.running_conversation = data.get('running_conversation', [])
            else:
                self.running_conversation = []
        except Exception as e:
            print(e)

    def append(self, usernameupper, user_input, botnameupper, output):
        # Append new entry to the running conversation
        entry = []
        entry.append(f"[INST] {usernameupper}: {user_input} [/INST]")
        entry.append(f"{botnameupper}: {output}")
        self.running_conversation.append("\n\n".join(entry))  # Join the entry with "\n\n"
        # Remove oldest entry if conversation length exceeds max entries
        while len(self.running_conversation) > self.max_entries:
            self.running_conversation.pop(0)
        self.save_to_file()

    def save_to_file(self):
        # Combine main conversation and formatted running conversation for saving to file
        data_to_save = {
            'main_conversation': self.main_conversation,
            'running_conversation': self.running_conversation
        }
        
        # Save the joined list to a json file
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4)

    # Create function to call conversation history
    def get_conversation_history(self):
        if not os.path.exists(self.file_path):
            self.save_to_file()
        # Join Main Conversation and Running Conversation
        return self.main_conversation + ["\n\n".join(entry.split(" ")) for entry in self.running_conversation]
            

# Start the main chatbot loop
if __name__ == '__main__':
    # Create a conversation list for the chatbot prompts.
    conversation = list()
    # Define User and Bot name from .txt files
    bot_name = open_file('bot_name.txt')
    user_name = open_file('user_name.txt')
    # Create variables for upper case bot and username
    usernameupper = user_name.upper()
    botnameupper = bot_name.upper()
    # Define Main Prompt and Greeting Prompt from .txt files
    main_prompt = open_file(f'prompt_main.txt').replace('<<NAME>>', bot_name)
    greeting_prompt = open_file(f'prompt_greeting.txt').replace('<<NAME>>', bot_name)
    # Set the instruction for the api
    instruction = (f"[INST] <<SYS>>\n{main_prompt}\n<</SYS>>")
    # Define Maximum Conversation List
    max_entries = 12
    # Define the main conversation class and pass through the needed variables
    main_conversation = MainConversation(max_entries, main_prompt, greeting_prompt)
    while True:
        # Wrap in an error handler
        try:
            # Get Conversation History
            conversation_history = main_conversation.get_conversation_history()
            # Get user input
            user_input = input(f'\n\n{usernameupper}: ')
            # Append generation list with the conversation history
            conversation.append({'content': f"{conversation_history}"})
            # Append generation list with the user input
            conversation.append({'content': f"[INST] {usernameupper}: {user_input} [/INST]"})
            # Prime response generation with upper case bot name
            conversation.append({'content': f"{botnameupper}: "})    
            # Join conversation list to be passed through to the api
            prompt = ''.join([message_dict['content'] for message_dict in conversation])
            # Pass through the instruction, user name, and the conversation list
            output = oobabooga(instruction, user_name, prompt)
            # Print the response
            print(f"{botnameupper}: {output}")
            # Append json file with newest response
            main_conversation.append(usernameupper, user_input, botnameupper, output)
            # Clear Generation List 
            conversation.clear()
        except Exception as e:
            print(e)