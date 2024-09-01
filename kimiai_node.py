class KimiAINode:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "input_text": ("STRING", {"default": "", "multiline": True}),
                "multi_turn": (
                    ["开启", "关闭"],  # 使用选项列表提供多个选项
                    {"default": "关闭", "label": "是否开启多轮对话"}  # 设置默认值并添加标签
                ),
            }
        }
        return inputs
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_text",)
    FUNCTION = "generate_text"
    CATEGORY = "CustomNodes/LLM"

    # 初始化全局变量，用于保存多轮对话的历史消息
    system_messages = [
        {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
    ]
    messages = []

    def make_messages(self, input: str, n: int = 20) -> list[dict]:
        """构建用于请求的消息列表，包括系统消息和历史消息"""
        
        # 在每次用户输入前添加前缀
        modified_input = "" + input
        
        self.messages.append({
            "role": "user",
            "content": modified_input,    
        })

        # 构建新的消息列表
        new_messages = []
        new_messages.extend(self.system_messages)

        if len(self.messages) > n:
            self.messages = self.messages[-n:]

        new_messages.extend(self.messages)
        return new_messages

    def generate_text(self, input_text, multi_turn):
        import openai

        client = openai.OpenAI(
            api_key="Your AIP KEY",  # 替换为你的 API Key
            base_url="https://api.moonshot.cn/v1",
        )

        # 如果选择“开启”，则携带历史对话信息
        if multi_turn == "开启":
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=self.make_messages(input_text),
                temperature=0.3,
            )

            assistant_message = completion.choices[0].message
            self.messages.append(assistant_message)

        else:
            # 如果选择“关闭”，清除之前的对话记录，并只发送当前的用户输入
            self.messages = [] 
            modified_input = "" + input_text
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=self.system_messages + [{"role": "user", "content": modified_input}],
                temperature=0.3,
            )

            assistant_message = completion.choices[0].message

        return (assistant_message.content,)
