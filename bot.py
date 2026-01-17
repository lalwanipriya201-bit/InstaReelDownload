from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
import shutil
import uuid
import time
import logging
import yt_dlp
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv("BOT_TOKEN")








async def start(update:Update, context:ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text(
        "Hello I am alive. Send me an Instagram Reel Link."
    )

async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    url=update.message.text.split("?")[0].strip()

    if "instagram.com/reel" not in url:
        await update.message.reply_text("❌ Please send a valid Instagram Reel link")
        return
    
    await update.message.reply_text("⏳ Downloading reel, please wait...")
    
    
    folder=f"reel_{uuid.uuid4().hex}"
    os.makedirs(folder, exist_ok=True)

    ydl_opts={
        "format":"mp4",
        "outtmpl":f"{folder}/%(id)s.%(ext)s",
        "quiet":True,
        "noplaylist":True,
        "no_warnings":True,
    }

    video_sent=False
    
    

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        

        
    except Exception as e:
        await update.message.reply_text(
        f"⚠️ Failed to download reel.\nError: {str(e)}"
        )

    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.endswith(".mp4"):
                video_path = os.path.join(folder, file)
                with open(video_path, "rb") as video:
                    await update.message.reply_video(video=video)
                video_sent = True
                break
    shutil.rmtree(folder, ignore_errors=True)

    if not video_sent:
        await update.message.reply_text("⚠️ Failed to download reel.")


app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...🤖")
app.run_polling()