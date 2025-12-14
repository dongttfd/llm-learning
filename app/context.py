class ChatContext:
    """
    Application-level context.
    LLM itself is stateless.
    """
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.history = []  # list of (role, content)

    def add_user(self, msg: str):
        self.history.append(("user", msg))

    def add_assistant(self, msg: str):
        self.history.append(("assistant", msg))

    def build_prompt(self) -> str:
        prompt = f"<|system|>\n{self.system_prompt}\n"

        for role, content in self.history:
            prompt += f"<|{role}|>\n{content}\n"

        # Only ask assistant to speak if last message is from user
        if not self.history or self.history[-1][0] == "user":
            prompt += "<|assistant|>\n"

        return prompt
