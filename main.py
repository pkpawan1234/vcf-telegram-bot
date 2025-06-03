from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

def generate_vcf(name, phone, email):
    return f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL;TYPE=CELL:{phone}
EMAIL:{email}
END:VCARD
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send your contact like this:\nName, Phone, Email")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        name, phone, email = map(str.strip, update.message.text.split(','))
        vcf_data = generate_vcf(name, phone, email)

        with open("contact.vcf", "w") as f:
            f.write(vcf_data)

        await update.message.reply_document(document=InputFile("contact.vcf"), filename="contact.vcf")
    except:
        await update.message.reply_text("❌ Format galat hai. Send like:\nName, Phone, Email")

def main():
    TOKEN = os.getenv("TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
