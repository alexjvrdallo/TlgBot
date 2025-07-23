from telegram.ext import Updater, CommandHandler

# Función de respuesta al comando /start
def start(update, context):
    update.message.reply_text("✅ El bot está funcionando correctamente en este grupo.")

def main():
    # Reemplaza TU_TOKEN con tu token real
    updater = Updater("TU_TOKEN", use_context=True)

    dp = updater.dispatcher

    # Agregamos el manejador para el comando /start
    dp.add_handler(CommandHandler("start", start))

    # Iniciamos el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()