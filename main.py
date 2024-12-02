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

# Lista de IDs de Pokémon legendarios conocidos (puedes agregar más IDs a esta lista)
legendary_pokemon_ids = [
    144, 145, 146, 150, 151, 249, 250, 251, 382, 383, 384, 385, 386, 387, 388, 389, 490, 491, 492, 493, 243, 244, 245, 377, 378, 379, 380, 381, 480, 481, 482, 483, 484, 485, 486, 487, 488, 638, 639, 640, 641, 642, 643, 644, 645, 646, 716, 717, 718, 785, 786, 787, 788, 789, 790, 791, 792, 800, 888, 889, 890, 891, 892, 894, 895, 896, 897, 898, 905, 1001, 1002, 1003, 1004, 1007, 1008, 1014, 1015, 1016, 1017, 1024
    # Añade aquí más IDs de Pokémon legendarios si es necesario
]

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

# Función para manejar el comando /legendario
async def legendario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Seleccionar un Pokémon legendario aleatorio de la lista
    legendary_pokemon_id = random.choice(legendary_pokemon_ids)
    
    # URL de la API de PokeAPI para obtener la información del Pokémon legendario
    url = f"https://pokeapi.co/api/v2/pokemon/{legendary_pokemon_id}"
    
    # Hacer la solicitud a la API
    response = requests.get(url)
    data = response.json()
    
    # Obtener la imagen del Pokémon legendario y su nombre
    pokemon_image_url = data['sprites']['front_default']
    pokemon_name = data['name'].capitalize()  # Convertir el nombre a formato "Capitalized"
    
    # Enviar la imagen del Pokémon legendario con su nombre en el caption
    if pokemon_image_url:
        await update.message.reply_photo(pokemon_image_url, caption=f"¡Aquí tienes a {pokemon_name} legendario!")
    else:
        await update.message.reply_text("Hubo un problema al obtener la imagen del Pokémon legendario.")

# Función principal
def main():
    # Crear la aplicación con ApplicationBuilder
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Manejar el comando /start
    app.add_handler(CommandHandler("start", start))

    # Manejar el comando /pokemon
    app.add_handler(CommandHandler("pokemon", pokemon))

    # Manejar el comando /legendario
    app.add_handler(CommandHandler("legendario", legendario))

    # Manejar mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_hola))

    # Iniciar el bot
    print("Bot está funcionando. Presiona Ctrl+C para detener.")
    app.run_polling()

# Ejecutar el programa
if __name__ == "__main__":
    main()
