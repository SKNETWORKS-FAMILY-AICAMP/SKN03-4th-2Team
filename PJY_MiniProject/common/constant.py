import enum 

class CHATBOT_ROLE(enum.Enum):
    user = (enum.auto, "role")
    assistant = (enum.auto, "LLM 모델")

# message
class CHATBOT_MESSAGE(enum.Enum):
    role = (enum.auto, "role")
    content = (enum.auto, "메세지")