import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Включим логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен вашего бота (получите у @BotFather)
BOT_TOKEN = "5696379337:AAFOKBjO0wiMZDs2lqsc7RPPFnODOJK4Qi4"

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я простой бот. Просто напиши мне что-нибудь!')

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Я просто отвечаю на твои сообщения. Попробуй написать что-нибудь!')

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    # Простые ответы на сообщения
    if 'привет' in text:
        response = 'Привет! Как дела?'
    elif 'как дела' in text:
        response = 'У меня всё отлично! А у тебя?'
    elif 'пока' in text or 'до свидания' in text:
        response = 'До встречи! Было приятно пообщаться!'
    else:
        response = 'Интересно! Расскажи ещё что-нибудь!'
    
    await update.message.reply_text(response)

# Обработчик ошибок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Основная функция
def main():
    # Создаем приложение
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавляем обработчик ошибок
    app.add_error_handler(error)
    
    # Запускаем бота
    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()