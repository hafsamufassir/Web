from messages import START,NEW,SHOW,DELETE,TIME,TASK,SAVE,NONE,DELETE2,ERROR  
from constants import TOKEN
from datetime import datetime
import telebot
from telebot import types
import requests
import os

bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(row_width = 2)
btn1 = types.KeyboardButton('ADD👍')
btn2 = types.KeyboardButton('TIMETABLE👐')
#btn3 = types.KeyboardButton('CUT👊')
markup.row(btn1, btn2)

@bot.message_handler(commands = ['start', 'help'])
def start(message):
	file = open("/Users/hafsamufassir/Documents/KBTU/practice_python/Rembot/%s.txt"%message.chat.id,"a")
	print(message.chat.first_name)
	bot.send_message(message.chat.id, START%(message.chat.first_name), reply_markup = markup)
	file.close()

@bot.message_handler(func = lambda message: message.text == "ADD👍")
def add_day(message):
	week = types.InlineKeyboardMarkup()
	days = ['MONDAY🙁','TUESDAY😤','WEDNESDAY🤤','THURSDAY👿','FRIDAY👹','SATURDAY🙃','SUNDAY🙂', '👋👋👋', '😴😴😴']
	week.add(*[types.InlineKeyboardButton(text = name,callback_data = name) for name in days])
	bot.send_message(message.chat.id, NEW, reply_markup = week)

@bot.message_handler(func = lambda message: message.text == "TIMETABLE👐")
def show_task(message):
	bot.send_message(message.chat.id,SHOW)
	file = open("/Users/hafsamufassir/Documents/KBTU/practice_python/Rembot/%s.txt"%message.chat.id, "r")
	s = file.read()
	if s.isspace() == False:
		bot.send_message(message.chat.id, s)
	else:
		bot.send_message(message.chat.id, NONE)
	file.close()

@bot.callback_query_handler(func = lambda c: True)
def save_day(c):
	file = open("/Users/hafsamufassir/Documents/KBTU/practice_python/Rembot/%s.txt"%c.message.chat.id, "a")
	file.write(c.data + " ")
	file.close()
	bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.message_id, text = c.data + '\n'+ TIME,
	parse_mode = 'Markdown')

# @bot.message_handler(func = lambda message: message.text == "CUT👊")
# def delete_task(message):
# 	dele = types.ReplyKeyboardMarkup()
# 	file = open("%s.txt"%message.chat.id, "r")
# 	s1 = file.read()
# 	s2 = s1.split('\n')
# 	file.close()
# 	for i in range(0, len(s2)):
# 		if(s2[i] != ''):
# 			name = i + 1
# 	dele.row(types.InlineKeyboardButton('YES' + s2[i]))
# 	bot.send_message(message.chat.id, s1 + DELETE, reply_markup = dele)

# @bot.message_handler(func = lambda message: 'YES' in message.text)
# def ddd(message):
# 	file = open("%s.txt"%message.chat.id,"r")
# 	s3 = file.read()
# 	os.remove("%s.txt"%message.chat.id)
# 	file = open("%s.txt"%message.chat.id,"a")
# 	s3 = s3.replace(message.text.split('::'), '')
# 	file.write(s3)
# 	file.close()
# 	bot.send_message(message.chat.id, DELETE2, reply_markup = markup)

@bot.message_handler(func = lambda message: 'At:' in message.text )
def add_time(message):
	message.text = message.text.replace('At:', '')
	if len(message.text.split(':')[0]) == 2 and len(message.text.split(':')[1]) == 2:
		if int(message.text.split(':')[0]) >= 0 and int(message.text.split(':')[0]) < 24:
			if int(message.text.split(':')[1]) >= 0 and int(message.text.split(':')[1]) < 59:
				file = open("/Users/hafsamufassir/Documents/KBTU/practice_python/Rembot/%s.txt"%message.chat.id,"a")
				file.write(message.text + " ")
				file.close()
				bot.send_message(message.chat.id, TASK)
	else: 
		bot.send_message(message.chat.id, ERROR)

@bot.message_handler(func = lambda message: 'Task:' in message.text)
def add_task(message):
	file = open("/Users/hafsamufassir/Documents/KBTU/practice_python/Rembot/%s.txt"%message.chat.id,"a")
	file.write(message.text.split(':')[1] + "\n")
	file.close()
	bot.send_message(message.chat.id, SAVE, reply_markup = markup)


if __name__ == '__main__':
    print('REMINDERBOT')
bot.polling()