# Импорт необходимых модулей
import telebot
import sqlite3
from telebot import types

# Инициализация бота с токеном
bot = telebot.TeleBot('token')

login = None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect('database.db')  # Установление соединения с базой данных
    crs = connect.cursor()
    
    # Создание таблицы пользователей (если не существует)
    crs.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                login TEXT,
                password TEXT
    )""")
    
    connect.commit()
    crs.close()
    
    # Приветственное сообщение и запрос логина для регистрации
    bot.send_message(message.chat.id, 'Здравствуйте уважаемый пользователь, для начала нужно зарегистрироваться. Пожалуйста, введите свой логин для регистрации!')
    bot.register_next_step_handler(message, login)

# Функция для обработки ввода логина
def login(message):
    global login
    login = message.text.strip()
    bot.send_message(message.chat.id, 'Теперь введите пароль!')
    bot.register_next_step_handler(message, password)

# Функция для обработки ввода пароля и сохранения данных в базу
def password(message):
    password = message.text.strip()
    connect = sqlite3.connect('database.db')  # Подключение к базе данных
    crs = connect.cursor()
    
    crs.execute("INSERT INTO users(login, password) VALUES(?, ?)", (login, password))  # Вставка логина и пароля в базу данных

    connect.commit()
    crs.close()   
    
    bot.send_message(message.chat.id, 'Приятной вам работы, вы успешно зарегистрированы!')

bot.infinity_polling()  # Запуск постоянного опроса бота
