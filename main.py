import logging, asyncio, os
from functools import wraps
from colorama import Fore
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
load_dotenv()
TOKEN = os.getenv("TOKEN")
myid = int(os.getenv("MYID", "0"))
ideas_f = "ideas.txt"
w = Fore.WHITE
lb = Fore.LIGHTBLACK_EX
rd = Fore.RED
ylw = Fore.YELLOW
reset = Fore.RESET

def restricted(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != myid:
            logging.warning(f"{lb}[{w}Warning{lb}] {rd}Access Denied: {w}{user_id}{reset}")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

def get_ideas():
    if not os.path.exists(ideas_f):
        return []
    with open(ideas_f, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]
    
def save_ideas(ideas):
    with open(ideas_f, "w", encoding="utf-8") as f:
        for idea in ideas:
            f.write(f"{idea}\n")

@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any ideas you want to save.")

@restricted
async def handle_new_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idea = update.message.text
    with open(ideas_f, "a", encoding="utf-8") as f:
        f.write(f"{idea}\n")
    await update.message.reply_text(f"Written: [{idea}]")

@restricted
async def list_ideas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ideas = get_ideas()
    if not ideas:
        await update.message.reply_text("There are no ideas saved")
        return
    resp = f"Ideas list:\n"
    for i, idea in enumerate(ideas, 1):
        resp += f"[{i}] - {idea}\n"
    await update.message.reply_text(resp)
    
@restricted
async def remove_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        index = int(context.args[0]) - 1
        ideas = get_ideas(ideas)
        if 0 <= index < len(ideas):
            removed = ideas.pop(index)
            save_ideas(ideas)
            await update.message.reply_text(f"Deleted: [{removed}]")
        else:
            await update.message.reply_text("This idea is not there")
    except (IndexError, ValueError):
        await update.message.reply_text("You need to type this: /remove 1")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_ideas))
    app.add_handler(CommandHandler("remove", remove_idea))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_new_idea))
    print(f"{lb}[{w}Info{lb}] {w}Running{reset}")
    app.run_polling()