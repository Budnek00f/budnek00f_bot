import logging
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки
BOT_TOKEN = "5696379337:AAFOKBjO0wiMZDs2lqsc7RPPFnODOJK4Qi4"  # Получите у @BotFather
DEEPSEEK_API_KEY = "sk-607fc0ab6aab4909ad516014cc5a5710"  # Получите на platform.deepseek.com
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def get_deepseek_response(message_text):
    """Получает ответ от DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system", 
                "content": "Ты полезный AI-ассистент в Telegram. Отвечай кратко, дружелюбно и по делу. Максимум 2-3 предложения."
            },
            {
                "role": "user",
                "content": message_text
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка API: {e}")
        return "Извините, возникла техническая ошибка. Попробуйте позже."
    except (KeyError, IndexError) as e:
        logging.error(f"Ошибка парсинга ответа: {e}")
        return "Не удалось обработать ответ. Попробуйте еще раз."

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Привет! Я умный бот с искусственным интеллектом DeepSeek.\n\n"
        "Задайте мне любой вопрос, и я постараюсь помочь!\n"
        "Например:\n"
        "• 'Расскажи о космосе'\n"
        "• 'Напиши рецепт омлета'\n"
        "• 'Объясни квантовую физику'\n"
        "• 'Помоги с кодом на Python'"
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = (
        "🤖 Я использую мощный AI от DeepSeek для ответов на ваши вопросы.\n\n"
        "Просто напишите мне сообщение, и я отвечу!\n\n"
        "Команды:\n"
        "/start - начать общение\n"
        "/help - показать эту справку\n\n"
        "Я могу:\n"
        "• Отвечать на вопросы\n"
        "• Помогать с программированием\n"
        "• Объяснять сложные concepts\n"
        "• Генерировать идеи и многое другое!"
    )
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_message = update.message.text
    
    # Показываем статус "печатает"
    await update.message.chat.send_action(action="typing")
    
    # Получаем ответ от DeepSeek
    bot_response = await get_deepseek_response(user_message)
    
    # Отправляем ответ
    await update.message.reply_text(bot_response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logging.error(f"Ошибка: {context.error}")
    if update and update.message:
        await update.message.reply_text("Произошла ошибка. Попробуйте еще раз.")

def main():
    """Основная функция"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🤖 Бот с DeepSeek AI запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()