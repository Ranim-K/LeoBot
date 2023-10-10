# Made By Ranim
import json
from difflib import get_close_matches
import pywhatkit

# Load the knowledge base from the specified JSON file. 
def load_knowldge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data : dict = json.load(file)
    return data

# Save the knowledge base to the specified JSON file.
def save_knowldge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find the best matching question from the user input using difflib.
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Get the answer for the specified question from the knowledge base.
def get_answer_for_question(question: str, knowldge_base: dict) -> str | None:
    for q in knowldge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

# Main function to run the chat bot.
def chat_bot():
    knowldge_base : dict = load_knowldge_base('knowldge_base.json')

    while True:
        user_input : str = input("You: ")
        if 'play' in user_input.lower():
            song = user_input.replace('play', '')
            pywhatkit.playonyt(song)
            print('Playing...')
        elif 'search' in user_input.lower():
            search = user_input.replace('search', '')
            pywhatkit.search(search)
            print('Searching...')
        elif user_input.lower() == 'quit' or user_input.lower() == 'exit':
            break
        else:
            best_match : str | None = find_best_match(user_input, [q["question"] for q in knowldge_base["questions"]])

            if best_match:
                answer: str = get_answer_for_question(best_match, knowldge_base)
                print(f"Bot: {answer}")
            else:
                print("Bot: I don\'t know the answer. Can you teach me?")
                new_answer: str = input("Type the answer or 'skip' to Skip: ")

                if new_answer.lower() != 'skip':
                    knowldge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowldge_base("knowldge_base.json", knowldge_base)
                    print("Bot: Thank you! I learned a new response!")

if __name__ == "__main__":
    chat_bot()
