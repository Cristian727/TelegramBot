from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtén el token desde la variable de entorno
BOT_TOKEN = os.getenv("API_KEY")

# Función para responder a los mensajes
async def responder_hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hola')

# Función para manejar el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Hola! Envíame un mensaje y te responderé.')

# Función principal
def main():
    # Crear la aplicación con ApplicationBuilder
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Manejar el comando /start
    app.add_handler(CommandHandler("start", start))

    # Manejar mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_hola))

    # Iniciar el bot
    print("Bot está funcionando. Presiona Ctrl+C para detener.")
    app.run_polling()

# Ejecutar el programa
if __name__ == "__main__":
    main()
