from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from dotenv import load_dotenv
import os
import requests
import random

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

# Función para manejar el comando /pokemon
async def pokemon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Número aleatorio entre 1 y 898 (total de Pokémon registrados en la PokeAPI)
    pokemon_id = random.randint(1, 898)
    
    # URL de la API de PokeAPI para obtener la información del Pokémon
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    
    # Hacer la solicitud a la API
    response = requests.get(url)
    data = response.json()
    
    # Obtener la imagen del Pokémon y su nombre
    pokemon_image_url = data['sprites']['front_default']
    pokemon_name = data['name'].capitalize()  # Convertir el nombre a formato "Capitalized"
    
    # Enviar la imagen al chat con el nombre del Pokémon en el caption
    if pokemon_image_url:
        await update.message.reply_photo(pokemon_image_url, caption=f"¡Aquí tienes a {pokemon_name}!")
    else:
        await update.message.reply_text("Hubo un problema al obtener la imagen del Pokémon.")

# Función principal
def main():
    # Crear la aplicación con ApplicationBuilder
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Manejar el comando /start
    app.add_handler(CommandHandler("start", start))

    # Manejar el comando /pokemon
    app.add_handler(CommandHandler("pokemon", pokemon))

    # Manejar mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_hola))

    # Iniciar el bot
    print("Bot está funcionando. Presiona Ctrl+C para detener.")
    app.run_polling()

# Ejecutar el programa
if __name__ == "__main__":
    main()
