import cx_Oracle 
import random 
import parsing
import DB
import numpy as np
import matplotlib.pyplot as plt

from DemoBot import DemoBot

def start_command(message,bot):
   return ("""  Здравствуй, уважаемый пользователь!
Я могу показать Вам актуальные новости!
Вам нужно написать "Собери новости" и указать количество страниц
Написать "Покажи нвовсть"
Так же я могу удалить все новости из БД
Для этого достаточно ввести "Удали все новости"
   """,None)

def answer_command(mesage):
    return "Разработчик работает над модернизацией бота"

def show_news(mesage):
    result = []
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.execute("Select id, link, title, text, link from News ")
    res=cur.fetchall() 
     
    for record in res:
       result.append(record[4])  
   
    con.commit()  
    cur.close()
    con.close()
    if len(result) == 0:
        return "Новостей нет"
        
    random.seed()   
    i = random.randint(0,len(result)-1) 
    return result[i]
def delete_all_news(mesage):
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.execute("DELETE from News")

    con.commit()  
    cur.close()
    con.close()
    return "Все новости стерты" 

def get_news(mesage):
    return "Со скольки страниц собрать новости?"

def gathering_news(mesage):
    pages = int(mesage.split(' ')[0])
    news = parsing.parsing(pages)
    DB.insert_into_db(news)
    return 'Новости сохранены'

def get_search_news(mesage):
    return "Что бы Вы хотели найти?"

def get_text(mesage):
    result=[]
    mesage= [mesage]
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.execute("Select link from News where regexp_like (text, :1)", mesage)
    res =cur.fetchall() 
        
    for record in res:
       result.append(record[0])  
   
    con.commit()  
    cur.close()
    con.close()
    if len(result) == 0:
        return "Новостей нет"
        
    random.seed()   
    i = random.randint(0,len(result)-1) 
    return result[i]

def schedule(mesage):
    data = show_news()
    plt.style.use('_mpl-gallery')
    x = np.array(data[1])
    y = np.array(data[2])

    fig, ax = plt.subplots()

    ax.plot(x, y, linewidth = 2.0)

    plt.show()



def main():
    bot = DemoBot()
    bot.register_start_handler(start_command)
    bot.register_text_handler(answer_command,regexp = 'test')
    bot.register_text_handler(show_news, regexp = '^Покажи новость')
    bot.register_text_handler(delete_all_news, regexp = '^Удали все новости')
    bot.register_text_handler(get_news, regexp = '^Собери новости')
    bot.register_text_handler(gathering_news,regexp = '^[0-9]+ страниц')
    bot.register_text_handler(get_search_news, regexp = 'Найди новость')
    bot.register_text_handler(get_text,regexp=  """'a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|
    s|t|u|v|w|x|y|z|а|б|в|г|д|е|ё|ж|з|и|й|к|л|м|н|о|п|р|с|т|у|ф|х|ц|ч||ш|щ|ъ|ы|ь|э|ю|я'""")
    bot.register_text_handler(schedule, regexp = '^Выведи график')
    bot.run()
  
if __name__ == '__main__':
    main()