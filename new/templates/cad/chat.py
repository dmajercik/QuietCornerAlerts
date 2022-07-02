from new.database.models import Chat
from flask_jwt_extended import jwt_required


@cad.route('/chat')
@jwt_required()
def chat():
    chatlog = Chat.objects()
    chat_data = []
    for msg in chatlog():
        messageline = [Chat.dispatcher, Chat.message]
        chat_data.append(messageline)