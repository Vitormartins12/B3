"""
Preenche a tabela.

Consulta os dados e salva nas respectivas tabelas.
"""

import os
import sqlite3
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
from threading import Thread


conn = sqlite3.connect('b3.db', check_same_thread=False)
cursor = conn.cursor()
codigos = cursor.execute("""SELECT code FROM empresas""").fetchall()
conn.close()
url = 'http://cotacoes.economia.uol.com.br/acao/index.html?codigo='

iteracoes = 0


def getvalues(start):
    for i in range(start, int(len(codigos)), 4):
        os.system('clear')
        global iteracoes
        iteracoes += 1
        print('Baixados %d / 1974.' % iteracoes)
        html = urlopen(url+codigos[i][0])
        bsObj = BeautifulSoup(html.read(), 'html5lib')
        body = bsObj.findAll("td")
        dados = [j.getText() for j in body]
        if len(dados) > 1:
            del(dados[0])
            dados = [str(date.today())] + dados
            conn = sqlite3.connect('b3.db', check_same_thread=False)
            cursor = conn.cursor()
            command = 'INSERT INTO %s (data, var, var_percentual, ultima, maxima, minima, abertura, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)' % codigos[i][0][:-3]
            cursor.execute("""%s""" % command, dados)
            conn.commit()
            conn.close()


a = Thread(target=getvalues, args=(0,))
b = Thread(target=getvalues, args=(1,))
c = Thread(target=getvalues, args=(2,))
d = Thread(target=getvalues, args=(3,))

a.start()
b.start()
c.start()
d.start()
