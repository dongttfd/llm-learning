from app.llm_loader import load_llm
from app.context import ChatContext
from app.chat_engine import chat_once

def run_llm_loop():
    llm = load_llm()

    context = ChatContext(
        system_prompt=(
            "You are a friendly Vietnamese assistant.\n"
            "You are chatting with a human.\n"
            "If the user introduces their name, remember it and reply naturally.\n"
            "Do not explain words like a dictionary."
        )
    )

    print("=== LLM Hello World + Context ===")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("User > ")
        if user_input.lower() == "exit":
            break

        answer = chat_once(llm, context, user_input)
        print("LLM  >", answer)
        print("-" * 50)

if __name__ == "__main__":
    run_llm_loop()
