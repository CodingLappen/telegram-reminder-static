import sqlite3 as lite
import sys
import logging
import locale
locale.setlocale(locale.LC_TIME,'de_DE' )
from telegram.ext import Updater,CommandHandler,MessageHandler,Dispatcher,JobQueue
from datetime import datetime,timedelta


TIMEDELTA=2419200 # 4 Weeks

# TIMEDELTA=1
STD_FILENAME ='Telegram.db'
con = None

def add_timedelta(time):
    time += timedelta(seconds=TIMEDELTA)

now = datetime.now()
beginning_datetime = datetime(2021,1,19,16,0,0)
if  beginning_datetime < now:
    timediff  =  (now - beginning_datetime).total_seconds()
    timedelta_var=timediff //TIMEDELTA
    if timediff%TIMEDELTA >0:
        timedelta_var+=1
    else:
       pass
    beginning_datetime +=timedelta(seconds=(timedelta_var * TIMEDELTA))

print(beginning_datetime)

try:
    con = lite.connect(STD_FILENAME)
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
finally:
    con.close()


def deletion(filename, id):
    try:
        con = lite.connect(filename)
        cur = con.cursor()
        cur.execute("DELETE FROM ID WHERE rid=" + str(id) +";");
        con.commit()
#    except lite.Error:
#        print("error %s"% e.args[0])
#        sys.exit(-1)
    finally:
        con.close()


def adding(filename, id):
    try:
        con = lite.connect(filename)
        cur = con.cursor()
        print(id)
        cur.execute("INSERT INTO ID (rid) VALUES (" + str(id)+ ")")
        con.commit()
    except lite.Error:
        print("error %s"% e.args[0])
        sys.exit(-1)
    finally:
        con.close()

def id_list(filename):
    try:
        con = lite.connect(filename)
        cur = con.cursor()
        cur.execute("SELECT rid FROM ID")
        con.commit()
        s= set()
        for i  in cur.fetchall():
            s.add(i[0])
        return s
        #return set(cur.fetchall())
    except lite.Error:
        print("error %s"% e.args[0])
        sys.exit(-1)
    finally:
        con.close()

def next_event(time_stamp):
    """
        Not yet implemented.
    """
    return None

SOME_DAY = None
updater =  Updater(token='',use_context=True)
bot =updater.bot
due =0
list_of_ids=id_list(STD_FILENAME)
print("Read ID LIST: " +str( list_of_ids))

def send_everyone(name):
    bot = updater
    print("Sending everyone a message")
    print(str(list_of_ids))
    for i in  list_of_ids:
        print("Wrote: "+ str(i))
        time =datetime.now().replace(microsecond=0)+timedelta(seconds=TIMEDELTA)
        bot.bot.send_message(chat_id=i,
            text="Ich wollte dich daran erinnern, dass die Termine abgegeben werden sollen. Ich werde dich wieder in 4 Wochen am {} um {}  erinnern".format(time.date().strftime("%A den %d. %B %Y"), time.time().isoformat(timespec= 'minutes')))
        pass

first=beginning_datetime
first.replace(microsecond=0)
print("Adding the repeatedly run job"+ str(beginning_datetime))
if first > datetime.now():
    now =datetime.now()
    job = updater.job_queue.run_repeating(send_everyone,name="Repeating Action",interval=TIMEDELTA, first=int ((first - now).total_seconds())) #,  interval=10.0)
    print(str(updater.job_queue))
    updater.job_queue.start()
    print(updater.job_queue.jobs())
    print(str(beginning_datetime)+"     Now:"+str(datetime.now()))
    print(str(job)+" "+ str(job.enabled))


def start(update ,context):
    context.bot.send_message(chat_id=update.effective_char.id, text="Hallo, I verwalte die Aboliste zu dem Netto Erinnerungs Kalendar!")

def register(update,context):
    user = None
    message=update.message
    if (message.from_user!=None):
        user = message.from_user
    else:
        return
    list_of_ids.add(user.id)
    adding(STD_FILENAME,update.effective_chat.id)
    update.effective_chat.send_message( text="Du bist nun registriert!")
    job.run(updater.dispatcher)

def unregister(update,context):
    user = None
    message=update.message
    if (message.from_user!=None):
        user = message.from_user
    else:
        return
    list_of_ids.remove(user.id)
    deletion(STD_FILENAME,user.id)
    update.effective_chat.send_message( text="Ich habe dich von der Liste entfernt!")

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start',start));
dispatcher.add_handler(CommandHandler('registrieren',register));
dispatcher.add_handler(CommandHandler('entfernen',unregister));


updater.start_polling()
updater.idle()
