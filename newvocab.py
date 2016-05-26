#!/usr/bin/python3

from bottle import *
import mysql.connector as mysqldb


def page_template(body_html):
 head = '''
 <meta charset="utf-8" />
 <link rel="stylesheet" type="text/css" href="/css/main.css">
 <title> Словарь </title>
   '''
 return '''<!DOCTYPE html>
    <html>
     <head>
         %s
     </head>
     <body>
    %s
   </body>
   </html>''' % (head,body_html)


welcome_message = '''
     <p class="intro"> 
      Привет! Это твой личный онлайн-словарь.<br>
      Ты всегда можешь <a href="/addword">добавить в него новое слово или новое значение</a>.<br>
      Пользуйся на здоровье!
    </p>
   '''
form = '''
         <form action="/gotoword" method="post" >
             <p color:blue >Введите слово: </p><input type="text" name="myword"><br>
             <input type="submit" value="Submit">
      </form>
    '''


@route('/')
def root_page():
   return page_template(welcome_message+"<br>"+form)

@route("/css/main.css")
def get_css():
       return static_file("slovar.css",root="./")

@route("/word/<inputword>.html")
def get_translation (inputword):
   return page_template(welcome_message+"<br>"+form+"<br>"+answer(inputword))



def answer(word): #Проверяет, если слово есть в словаре - выводит его значение. Если нет - пишет сообщение
    db=mysqldb.Connect(host='localhost', user='root', password='1', database='slovar',charset='utf8', use_unicode=True)
    cur=db.cursor()
    cur.execute("SELECT * FROM words WHERE words.word = %s ", (word,) )
    print (word)
    wordID=False
    for row in cur.fetchall():
        (wordID, word)=row
    print (wordID)
    if not wordID:
        cur.close()
        db.close()
        return (word) + '<br>' + "Такого слова нет"
    
    #здесь мы уже знаем wordID и можем делать запрос на получение значений 

    cur.execute("SELECT * FROM means WHERE word_id= %s ", (wordID,)  )
    meanlist=[]
    for row in cur.fetchall():
        (id, mean, id_word)=row
        meanlist.append(mean)  
    cur.close()
    db.close()
    return word + '<br>' + str(meanlist)

@route("/gotoword",method="POST")#берет из формы слово и переводит нас на раут этого слова.
def gotoword():
   word = request.forms.getunicode('myword')
   redirect ("/word/%s.html" % word)
   
  

  
@route("/addword") #Выводит форму, куда можно ввести новое слово и его значение
def newin(): # Вызывает /postaddword
    return '''<br>
<style>
body {background-color:#F5DEB3}
</style>
      <form action="/postaddword" method="post">
         Введите новое слово: <input type="text" name="newword"><br>
         Введите новое значение: <input type="text" name="newmean"><br>
         <input type="submit" value="Submit">
      </form><br>  
     '''

@route("/postaddword", method='POST') #Принимает введенные пользователем слово и значение. Проверяет: если такого слова нет в словаре - добавляет и слово и значение.
#Если слово есть - добавляет значение вместе с предыдущими значениями этого слова. 
def new_post():
    new=request.forms.getunicode('newword')
    mean=request.forms.getunicode('newmean')
    db=mysqldb.Connect(host='localhost', user='root', password='1', database='slovar',charset='utf8', use_unicode=True)
    cur=db.cursor()

    cur.execute("SELECT * FROM words WHERE words.word = %s ", (new,) )
    print (new)
    wordIDzzz=False
    for row in cur.fetchall():
        (wordID, word)=row
        wordIDzzz=True
 
    if wordIDzzz: # слово есть, нужно только добавить новое значение
        cur.execute("INSERT INTO means (mean, word_id) VALUES (%s, %s)", (mean, wordID)    )
        db.commit()
        cur.close() 
        db.close()
        
    else: #слова нет, нужно ввести и слово и значение в базу данных         
        cur.execute("INSERT INTO words (word) VALUES (%s)", (new,))
        db.commit()
        lastID=cur.lastrowid
        cur.execute("INSERT INTO means (mean, word_id) VALUES (%s, %s)", (mean, lastID)    )
        db.commit()
        cur.close()
        db.close()
        
    redirect ("/word/%s.html" % new)


run(host='localhost', port=8080)


