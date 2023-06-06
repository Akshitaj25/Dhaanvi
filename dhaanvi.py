import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '6271866429:AAEGUK2LO_3UtiH0c-nr-NiBFF_AZh-4KxQ'
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Welcome to Bijuka. Please select you language. Enter /English for English, /Hindi for Hindi and /Punjabi for Punjabi.\n\nनमस्ते! बीजूका में आपका स्वागत है। कृपया अपनी भाषा चुनें। अंग्रेजी के लिए /English, हिंदी के लिए /Hindi और पंजाबी के लिए /Punjabi दर्ज करें।\n\nਹੈਲੋ! ਬੀਜੂਕਾ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ। ਅੰਗਰੇਜ਼ੀ ਲਈ /English, /Hindi ਲਈ ਹਿੰਦੀ ਅਤੇ ਪੰਜਾਬੀ ਲਈ /Punjabi ਦਰਜ ਕਰੋ।\n\n/help")
def English(update, context):
    update.message.reply_text('Use /Image command to identify the disease your rice crop has so that you can do the applicable treatment for you crop. Enter /Image and then enter the picture of affected crop.')

def Hindi(update, context):
    update.message.reply_text('अपनी धान की फसल में रोग की पहचान करने के लिए /Image कमांड का प्रयोग करें ताकि आप अपनी फसल के लिए उपयुक्त उपचार कर सकें। /Image दर्ज करें और फिर प्रभावित फसल की तस्वीर दर्ज करें।')

def Punjabi(update, context):
    update.message.reply_text('ਤੁਹਾਡੀ ਚੌਲਾਂ ਦੀ ਫਸਲ ਨੂੰ ਬਿਮਾਰੀ ਦੀ ਪਛਾਣ ਕਰਨ ਲਈ /Image ਕਮਾਂਡ ਦੀ ਵਰਤੋਂ ਕਰੋ ਤਾਂ ਜੋ ਤੁਸੀਂ ਆਪਣੀ ਫਸਲ ਲਈ ਲਾਗੂ ਇਲਾਜ ਕਰ ਸਕੋ। /Image ਦਰਜ ਕਰੋ ਅਤੇ ਫਿਰ ਪ੍ਰਭਾਵਿਤ ਫਸਲ ਦੀ ਤਸਵੀਰ ਦਰਜ ਕਰੋ।')
def helpline(update, context):
    "displays farmers helpline numbers"
    update.message.reply_text('9416135999, 01722970605')
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="/start \n/help\n/helpline\n/English\n/Hindi\n/Punjabi\n/Image")
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
def image_handler(update, context):
    # Access the image file
    photo = context.bot.get_file(update.message.photo[-1].file_id)
    # Download the image
    photo.download('image.jpg')
    
    # Process the image using the API
    api_url = 'https://543d-2405-201-6005-5d91-88c4-4dd-b01c-a2bb.in.ngrok.io/'  # Replace with your API URL
    
    try:
        with open('image.jpg', 'rb') as image_file:
            # Make a POST request to the API with the image file
            response = requests.post(api_url, files={'image': image_file})
            # Process the API response
            if response.status_code == 200:
                result = response.json()
                # Extract the desired information from the API response
                # Customize this part based on your API's response structure
                output = result['output']
                # Send the output back to the user
                context.bot.send_message(chat_id=update.effective_chat.id, text=output)
            else:
                # Handle API request errors
                context.bot.send_message(chat_id=update.effective_chat.id, text='API request failed.')
    except IOError:
        # Handle image file errors
        context.bot.send_message(chat_id=update.effective_chat.id, text='Error processing the image.')
def main():
    # Initialize the Telegram Bot API with your bot's API token
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)

    dp.add_handler(start_handler)
    dp.add_handler(help_handler)
    dp.add_handler(CommandHandler("helpline",helpline))
    dp.add_handler(CommandHandler("English",English))
    dp.add_handler(CommandHandler("Hindi",Hindi))
    dp.add_handler(CommandHandler("Punjabi",Punjabi))

    # Add image handler
    image_handler = MessageHandler(filters.photo, image_handler)
    dp.add_handler(image_handler)
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(filters.text, echo))
    # log all errors
    dp.add_error_handler(error)
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '_main_':
    main()