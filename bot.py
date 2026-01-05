from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import instaloader
import os
import shutil
import uuid


BOT_TOKEN="8319252236:AAGrDnC3X_AjeDlE1zq7ZJxPU9zZwCVTuLc"

loader=instaloader.Instaloader(
    download_videos=True,
    download_video_thumbnails=False,
    save_metadata=False,
    post_metadata_txt_pattern=""
)


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

    try:
        shortcode=url.split("/")[-2]
        post=instaloader.Post.from_shortcode(loader.context,shortcode)

        folder=f"reel_{uuid.uuid4().hex}"
        loader.download_post(post, target=folder)

        for file in os.listdir(folder):
            if file.endswith(".mp4"):
                video_path = os.path.join(folder, file)
                with open(video_path, "rb") as video:
                    await update.message.reply_video(video=video)
                break

    except Exception as e:
        await update.message.reply_text(
        f"⚠️ Failed to download reel.\nError: {str(e)}"
        )

app=ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...🤖")
app.run_polling()