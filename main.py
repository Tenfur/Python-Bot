import qrcode
import os
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ChatAction

INPUT_TEXT = 0

# Este handler se ejecutará cuando se ejecute el comando start
def start(update, context):
    update.message.reply_text("Hola, te saluda el bot de peter")


def qr_command_handler(update, context):
    update.message.reply_text("Send a text to generate a qr code")

    return INPUT_TEXT

def generate_qr(text):
    filename = text + ".jpg"

    img = qrcode.make(text)

    img.save(filename)

    return filename

def send_qr(filename, chat): #Debemos enviar la imagen generada y el chat actual con el que estamos hablando
    # Enviamos una acción a telegram
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )

    chat.send_photo(
        photo=open(filename, 'rb')
    )

    os.unlink(filename)


def input_text(update, context): # Esta función va a tomar el texto que el usuario ingrese
    text = update.message.text

    filename = generate_qr(text) # Generamos el código qr usando el texto

    chat = update.message.chat

    send_qr(filename, chat) #Le enviamos el código qr al usuario

    return ConversationHandler.END


if __name__ == "__main__":

    updater = Updater(token="5339455077:AAER0hCI6qT5RxEnazd53x8YOz547Y6o1Ws", use_context=True)

    dp = updater.dispatcher # Se encarga de enviar las acciones

    dp.add_handler(CommandHandler("start", start)) # Un manejador de comandos

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("qr", qr_command_handler)
        ],
        states={
            INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
        },
        fallbacks=[]
    ))

    # Es para que el bot se active y empieza un ciclo infinito para estar revisando si el usuario
    # manda más comandos
    updater.start_polling()
    updater.idle()
