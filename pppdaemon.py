import sys
import imaplib
import re
import time

host="imap.globo.com"
log=""
pwd = ""

def conectar(log,pwd,host):
    try:
        conn = imaplib.IMAP4_SSL(host)
        conn.login(log,pwd)
        readonly = True
        conn.select("inbox",readonly)
        return(conn)
    except Exception as e:
        raise("Nao foi possivel se conectar\n"+str(e))


def leremail(conn):
    try:
        result,data = conn.search(None,'(SUBJECT "ppp")')
        ids = data[0]
        listaid = ids.split()
        ultimo = listaid[-1]
        resultado,data = conn.fetch(ultimo,"(RFC822)")
        email = data[0][1]
        return(email)
    except IndexError as e:
        raise ComandoInexistente("Nao ha comandos a serem executados")

def checkcomando(email):
    try:
        pattern_comando = re.compile(r'(###comando:)(ponto|print)')
        comando = pattern_comando.search(email.decode('utf-8'))
        print(comando.group(2))
        return(comando.group(2))
    except Exception as e:
        print("Erro")


if __name__ == "__main__":

    while(True):
        sys.stdout.flush()
        sys.stdout.write("{}".format("Rodando..."))
        try:
            conn = conectar(log,pwd,host)
            email = leremail(conn)
            comando = checkcomando(email)
        except:
            pass
        time.sleep(5)
