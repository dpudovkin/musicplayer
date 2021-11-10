from chat.models import ChatMessage


class ChatMessageRepository:
    __instance = None

    def __init__(self):
        if not ChatMessageRepository.__instance:
            print("__init__ method called..")
        else:
            print("Instance already created:", self.get_instance())

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = ChatMessageRepository()
        return cls.__instance

    def messages_by_room(self, room_name):
        return ChatMessage.objects.filter(room_name=room_name)