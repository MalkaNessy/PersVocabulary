#!/usr/bin/python3

from bottle import *
from threading import Lock
import shelve
#from urllib.parse import urlparse
from urllib.parse import quote

slovar=shelve.open("myslovar" ,writeback=True)
mutex = Lock()


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
    global slovar
    if word in slovar:
        myOutput = str(slovar.get(word))
        return(word + '<br>' + 'Перевод: ' + myOutput)
    else:
      return (word) + '<br>' + 'Такого слова нет.'



@route("/gotoword",method="POST")#берет из формы слово и переводит нас на раут этого слова.
def gotoword():
   word = request.forms.getunicode('myword')
   red = "/word/%s.html" % quote(word)
   print(red)
   #response.content_type = 'text/html; charset=UTF8'
   #response.charset = 'UTF8'
   redirect (red)
   
  

  
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
    global slovar
    if new not in slovar:
        mutex.acquire()
        slovar[new]=[mean] 
        slovar.sync()
        mutex.release()
    else:
        slovar[new].append(mean)  
    return page_template(welcome_message+"<br>"+form)+"<br>" + str("Вы добавили к слову " + new + " значение " + mean)

run(host='localhost', port=8080)


