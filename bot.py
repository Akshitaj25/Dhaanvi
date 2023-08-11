from aiogram import Bot, Dispatcher, executor, types
import tensorflow as tf
import cv2
import numpy as np
from PIL import Image
import json

Token = "6548382969:AAGzK4KoDlbobqtc-6v2zLqHh_tQBLo-5o8"
bot = Bot(token=Token)
dp = Dispatcher(bot)

model = tf.keras.models.load_model("dhaanviapi.hdf5")
map_dict = {0: 'Bacterial Leaf Blight',
            1: 'Brown Spot',
            2: 'Healthy',
            3: 'Leaf Blast',
            4: 'Leaf Scald',
            5: 'Narrow Brown Spot'}

with open('disease_info.json', 'r') as json_file:
    disease_details = json.load(json_file)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("HI! I'm Dhaanvi.\nPress /Help for all commands")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply("/start - Start the bot\n/help - Get all commands\n/predict - predict the disease\n/details - Get details about the disease\n/helpline - Get helpline numbers\n/credits - Get credits\n/feedback - Give feedback\n/stop - Stop the bot")

@dp.message_handler(commands=['predict'])
async def predict(message: types.Message):
    await message.reply("Send one image of the leaf")

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    try:
        #get photo file
        photo = message.photo[-1]
        photo_file = await photo.get_file()
        photo_url = photo_file.file_path

        # Download and process the image
        photo_path = await photo.download()
        image = Image.open(photo_url)
        processed = preprocess_image(np.array(image))

        if processed is None:
            await message.reply("An error occurred while processing the image.")
            return
        
        #predict image
        prediction = model.predict(np.expand_dims(processed, axis=0))
        predicted_class = np.argmax(prediction)
        disease_name = map_dict[predicted_class]

        # await message.reply(f"The predicted disease is: {disease_name}")
        details = disease_details.get(disease_name, {})
        symptoms = details.get('symptoms', [])
        treatments = details.get('treatments', [])

        # Prepare response
        response = f"The predicted disease is: {disease_name}\n"
        if symptoms:
            response += "\nSymptoms:\n" + "\n".join(symptoms)
        if treatments:
            response += "\n\nTreatments:\n" + "\n".join(treatments)
        response += "\n \nPress /help for all commands"

        await message.reply(response)

    
    except Exception as e:
        print(e)
        await message.reply(f"An error occurred: {str(e)}")

def preprocess_image(image):
    try:
        image = cv2.resize(image, (224, 224))
        image = image / 255.0
        return image
    except Exception as e:
        print("error preprocessing:",e)
        return None
    
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


executor.start_polling(dp)