from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
import base64
import getpass
import sys
import re
import imaplib

logp = "leonardo.conceicao"
pwdp = b'bGVvbGVvMTIz'
host="zmta.trt1.jus.br"
logm= "leonardo.conceicao@trt1.jus.br"
pwdm = b'bGVvbGVvMTIz'
cmds = ["ponto","print","stop","getnum"]


def conectar(log,pwd,host):
        try:
                conn = imaplib.IMAP4_SSL(host)
                conn.login(log,pwd)
                readonly = True
                conn.select("inbox")
                return(conn)
        except Exception as e:
                print("ERRO NA CONEXAO\n"+str(e))


def leremail(conn):
        try:
                result,data = conn.search(None,'(SUBJECT "ppp")')
                ids = data[0]
                listaid = ids.split()
                ultimo = listaid[-1]
                resultado,data = conn.fetch(ultimo,"(RFC822)")
                email = data[0][1]
                #print(conn.list())
                conn.store(ultimo,'+FLAGS',r'(\Deleted)')
                conn.expunge()
                conn.close()
                conn.logout()
                return(email)
        except IndexError as e:
                print("Nao ha comandos a serem executados")
                sys.stdout.flush()

def checkcomando(email):
        try:
                pattern_comando = re.compile(r'(###comando:)(ponto|print|getnum)')
                comando = pattern_comando.search(email.decode('utf-8'))
                #print(comando.group(2))
                return(comando.group(2))
        except Exception as e:
                pass

def ppp(wdriver, logp,pwdp):
	print("\nConectando...")
	wdriver.get("https://ponto.trt1.jus.br")
	print("Logando...")
	wdriver.implicitly_wait(5)
	try:
		wdriver.find_element_by_id('form:j_idt51').send_keys(logp)
	except:
		wdriver.find_element_by_id('form:j_idt50').send_keys(logp)
		
	try:
		wdriver.find_element_by_id('form:j_idt56').send_keys(pwdp)
	except:
		wdriver.find_element_by_id('form:j_idt55').send_keys(pwdp)
	
	try:
		wdriver.find_element_by_id('form:j_idt58').click()
	except:
		wdriver.find_element_by_id('form:j_idt57').click()

	wdriver.implicitly_wait(2)
	wdriver.find_element_by_link_text('REGISTRAR PONTO').click()
	wdriver.implicitly_wait(2)
	#wdriver.find_element_by_id('form:j_idt77').click()


if __name__ == '__main__':

	'''target = datetime.datetime(2017,10,10,15,33)

	while(datetime.datetime.now()<=target):
		sys.stdout.write("\r({0}) Aguardando:-{1}".format(datetime.datetime.now(),target))
		sys.stdout.flush()
		time.sleep(5)

	driver = webdriver.Chrome()
	#driver = webdriver.PhantomJS()
	driver.set_window_size(1120, 1050)
	ppp(driver,log,pwd)
	print("DONE!")
	driver.close()'''
	while(True):
                sys.stdout.write("\r{}".format("Rodando..."))
                sys.stdout.flush()
                try:
                        conn = conectar(logm,base64.b64decode(pwdm).decode('ascii'),host)
                        email = leremail(conn)
                        comando = checkcomando(email)
                        if(comando):
                                driver = webdriver.Chrome()
                                driver.set_window_size(1120, 1050)
                                print("Execuntado: "+comando)
                                if(comando==cmds[0]):
                                        ppp(driver,logp,base64.b64decode(pwdp).decode('ascii'))
                                        print("DONE!")
                                        driver.close()                                        
                except Exception as e:
                        print("nA CARA"+str(e))
                time.sleep(60)
