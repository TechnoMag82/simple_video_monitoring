from threading import Thread

from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import time


bot = Bot(token='TELEGRAN-BOT-TOKEN',)
updater = Updater(bot=bot,)

def do_start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    #print(chat_id)
    context.bot.sendMessage(chat_id=chat_id, text="Is private bot",)

def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    #print(chat_id)
    context.bot.send_message(chat_id=chat_id, text="Is private bot. You cannot use it.",)

def on_created(event):
    print(f"File {event.src_path} has been created!")
    time.sleep(1)
    bot.send_photo(chat_id='bot_owner_id', photo=open(event.src_path, 'rb'), caption=f"Обнаружено движение в помещении \n{event.src_path}",)

def myWatchDir():
    patterns = "*.jpg"
    ignore_patterns = ""
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created

    watch_path = "watch_directory"

    my_observer = Observer()
    my_observer.schedule(my_event_handler, watch_path, recursive=False)
    
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
    

def main():
    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)
  
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    thread1 = Thread(target=myWatchDir)
    thread1.start()
            
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()