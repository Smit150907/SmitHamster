import subprocess
import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import server

# Bot Token and Channel IDs with URLs
TOKEN = "7427471717:AAHgP-SKaeGSKD7VkoI6T-G7NgiHk61ARgY"  # Use the token you provided
CHANNELS = [
    ("Join Channel 1", "https://t.me/smitlounge", -1002240543376),  # Channel 1 ID
    ("Join Channel 2", "https://t.me/+WeJmSXu60OwzOTJl", -1002178979577),  # Channel 2 ID
    ("Join Channel 3", "https://t.me/+x6bhmGBvDjplNzY1", -1002154826388)   # Channel 3 ID
]

AUTHORIZED_USERS = []
EXCLUSIVE = False

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    keyboard = [
        [InlineKeyboardButton(name, url=url) for name, url, _ in CHANNELS],
        [InlineKeyboardButton("Verify", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id,
        text="Welcome! Please join our channels to use the bot by clicking the buttons below. After joining, click 'Verify' to start using the bot.",
        reply_markup=reply_markup
    )

async def check_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for _, _, channel_id in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel_id, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            logging.error(f"Error checking membership for channel {channel_id}: {e}")
            return False
    return True

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    command = query.data

    if command == 'verify':
        is_member = await check_membership(user_id, context)
        
        if is_member:
            await query.edit_message_text("Thank you!! You are now verified 💸😴")
            
            # Define command buttons
            keyboard = [
                [InlineKeyboardButton("🚴 Bike", callback_data='/bike')],
                [InlineKeyboardButton("Clone 💸", callback_data='/clone')],
                [InlineKeyboardButton("Cube 🎲", callback_data='/cube')],
                [InlineKeyboardButton("Train 🚂", callback_data='/train')],
                [InlineKeyboardButton("Merge 🤖", callback_data='/merge')],
                [InlineKeyboardButton("Twerk 🍑", callback_data='/twerk')],
                [InlineKeyboardButton("Poly ✨", callback_data='/poly')],
                [InlineKeyboardButton("Mud 🧭", callback_data='/mud')],
                [InlineKeyboardButton("Trim 🤪", callback_data='/trim')],
                [InlineKeyboardButton("All 😴", callback_data='/all')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send the command buttons to the user
            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    "Use these commands to generate keys 👇\n\n"
                    "Click on the buttons below to generate keys for the respective games."
                ),
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text("You need to join all channels to use the bot. Please try again after joining.")
            await start(update, context)  # Re-send the instructions
    else:
        # Handle command execution based on callback_data
        command_handlers = {
            '/bike': bike,
            '/clone': clone,
            '/cube': cube,
            '/train': train,
            '/merge': merge,
            '/twerk': twerk,
            '/poly': poly,
            '/mud': mud,
            '/trim': trim,
            '/all': all
        }
        
        if command in command_handlers:
            # Call the respective handler function
            handler = command_handlers[command]
            await handler(update, context)
        else:
            await query.answer("Invalid command.")

async def game_handler(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    chosen_game: int, 
    all: bool, 
    delay = 0
    ):
    await asyncio.sleep(delay)
    server.logger.info(f"Delay for {delay} seconds")

    if EXCLUSIVE and update.effective_chat.id not in AUTHORIZED_USERS:
        return

    server.logger.info(f"Generating for client: {update.effective_chat.first_name} : {update.effective_chat.id}")
    if not all:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="🐹")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating\.\.\.", parse_mode='MARKDOWNV2')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"This will only take a moment\.\.\.", parse_mode='MARKDOWNV2')

    no_of_keys = int(context.args[0]) if context.args else 4
    keys = await server.run(chosen_game=chosen_game, no_of_keys=no_of_keys)
    generated_keys = [f"`{key}`" for key in keys]
    formatted_keys = '\n'.join(generated_keys)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{formatted_keys}", parse_mode='MARKDOWNV2')
    server.logger.info("Message sent to the client.")

async def bike(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=1, all=all)

async def clone(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=2, all=all)

async def cube(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=3, all=all)

async def train(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=4, all=all)

async def merge(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=5, all=all)

async def twerk(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=6, all=all)

async def poly(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=7, all=all)

async def mud(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=8, all=all)

async def trim(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=9, all=all)

async def all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if EXCLUSIVE and update.effective_chat.id not in AUTHORIZED_USERS:
        return
    
    server.logger.info(f"Generating for client: {update.effective_chat.first_name} : {update.effective_chat.id}")
    server.logger.info(f"Generating keys for All Games.")

    await context.bot.send_message(chat_id=update.effective_chat.id, text="🐹")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Currently generating for all games\.\.\.", parse_mode='MARKDOWNV2')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Come Back in about 5\-10 minutes\.", parse_mode='MARKDOWNV2')

    # Wait a certain number of seconds between each game
    tasks = [game_handler(update, context, i + 1, True, i * 30) for i in range(6)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # Create the application with the token
    application = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    
    # Add command handlers for hidden commands
    application.add_handler(CallbackQueryHandler(bike, pattern=r'^/bike$'))
    application.add_handler(CallbackQueryHandler(clone, pattern=r'^/clone$'))
    application.add_handler(CallbackQueryHandler(cube, pattern=r'^/cube$'))
    application.add_handler(CallbackQueryHandler(train, pattern=r'^/train$'))
    application.add_handler(CallbackQueryHandler(merge, pattern=r'^/merge$'))
    application.add_handler(CallbackQueryHandler(twerk, pattern=r'^/twerk$'))
    application.add_handler(CallbackQueryHandler(poly, pattern=r'^/poly$'))
    application.add_handler(CallbackQueryHandler(mud, pattern=r'^/mud$'))
    application.add_handler(CallbackQueryHandler(trim, pattern=r'^/trim$'))
    application.add_handler(CallbackQueryHandler(all, pattern=r'^/all$'))

    application.run_polling()
