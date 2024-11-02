import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Import your existing functions
from your_module import (
    gogo_auth,
    get_search_results,
    get_anime_recent,
    get_anime_popular,
    get_anime_details,
    get_anime_episode
)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define command handlers
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Anime Stream Bot! Use /search <anime_name> to find anime.')

def search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Please provide an anime name to search for. Usage: /search <anime_name>')
        return

    results = get_search_results(query)
    if 'status' in results and results['status'] == "204":
        update.message.reply_text(results['reason'])
        return

    message = "Search Results:\n\n"
    for idx, anime in enumerate(results):
        message += f"{idx + 1}. {anime['title']}\nLink: {anime['id']}\nImage: {anime['image']}\n\n"

    update.message.reply_text(message)

def recent(update: Update, _: CallbackContext) -> None:
    results = get_anime_recent()
    if 'status' in results and results['status'] == "204":
        update.message.reply_text(results['reason'])
        return

    message = "Recent Releases:\n\n"
    for anime in results:
        message += f"{anime['title']}\nLink: {anime['id']}\nImage: {anime['image']}\n\n"

    update.message.reply_text(message)

def popular(update: Update, _: CallbackContext) -> None:
    results = get_anime_popular()
    if 'status' in results and results['status'] == "204":
        update.message.reply_text(results['reason'])
        return
    
    message = "Popular Anime:\n\n"
    for anime in results:
        message += f"{anime['title']}\nLink: {anime['id']}\nImage: {anime['image']}\n\n"

    update.message.reply_text(message)

def episode(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 3:
        update.message.reply_text('Usage: /episode <email> <password> <anime_id> <episode_number>')
        return
    email, password, anime_id, episode_number = context.args

    anime_details = get_anime_details(anime_id)
    if 'status' in anime_details and anime_details['status'] == "204":
        update.message.reply_text(anime_details['reason'])
        return

    episode_links = get_anime_episode(email, password, anime_id, episode_number)
    if 'status' in episode_links and episode_links['status'] == "204":
        update.message.reply_text(episode_links['reason'])
        return

    message = "Episode Links:\n\n"
    for link in episode_links:
        message += f"{link['quality']}: {link['link']}\n"

    update.message.reply_text(message)

def main():
    # Replace 'YOUR_TOKEN' with your bot's token
    updater = Updater("6426712374:AAFU9KhMK4Ahf5U6PJ_Bf1OBiVhCk3OFY2U")

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("search", search))
    updater.dispatcher.add_handler(CommandHandler("recent", recent))
    updater.dispatcher.add_handler(CommandHandler("popular", popular))
    updater.dispatcher.add_handler(CommandHandler("episode", episode))

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
