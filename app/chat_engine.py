from app.context import ChatContext

def chat_once(llm, context: ChatContext, user_input: str) -> str:
    context.add_user(user_input)

    prompt = context.build_prompt()

    reply = llm.invoke(prompt)
    reply = reply.strip()

    context.add_assistant(reply)
    return reply