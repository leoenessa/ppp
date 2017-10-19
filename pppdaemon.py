from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
import base64
import sys
import re
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os

sleeptime = 10

logp = "leonardo.conceicao"
pwdp = b'bGVvbGVvMTIz'
host="zmta.trt1.jus.br"
#host = "imap.globo.com"
logm= "leonardo.conceicao@trt1.jus.br"
#logm= "leonardooc@globo.com"
pwdm = b'bGVvbGVvMTIz'
#pwdm = b'bGVvZW5lc3Nh'
cmds = ["ppp","print","stop","getnum"]


def enviaEmail(login,password,destino,img):
    msg = MIMEMultipart()
    msg['Subject'] = 'Retorno ppp '+str(datetime.datetime.now().strftime("%d-%m-%H-%M"))
    #msg['From'] = 'leonardooc@globo.com'
    msg['From'] = 'leonardo.conceicao@trt1.jus.br'
    msg['To'] = 'leonardodeoc@gmail.com'
    #msg.preamble = "reuniao de familia"

    part = MIMEBase("image","octet-stream")
    part.set_payload(open('snapshot.jpg','rb').read())
    encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="snapshot.jpg"')

    msg.attach(part)

    try:  
        server = smtplib.SMTP_SSL(host, 465)
        server.ehlo()
        server.login(login, password)
        server.sendmail(login, destino, msg.as_string())
        server.close()
        print('Email enviado!')
    except smtplib.SMTPException as e:  
        print(str(e))

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
        conn.store(ultimo,'+FLAGS',r'(\Deleted)')
        conn.expunge()
        conn.close()
        conn.logout()
        return(email)
    except IndexError as e:
        sys.stdout.write("Nao ha comandos a serem executados")

def checkcomando(email):
    try:
        pattern_comando = re.compile(r'(###comando:)(ppp|print|getnum|stop)')
        comando = pattern_comando.search(email.decode('utf-8'))
        print(comando.group(2))
        return(comando.group(2))
    except Exception as e:
        pass

def ppp(wdriver, logp,pwdp, sofoto):
    print("\nConectando...")
    wdriver.get(base64.b64decode(b'aHR0cHM6Ly9wb250by50cnQxLmp1cy5icg==').decode('ascii'))
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
    try:
        wdriver.find_element_by_id('form:j_idt44:0:j_idt54').click()
    except:
        pass
    if(not sofoto):
        wdriver.implicitly_wait(2)
        wdriver.find_element_by_link_text(base64.b64decode(b'UkVHSVNUUkFSIFBPTlRP').decode('ascii')).click()
        wdriver.implicitly_wait(2)
        #wdriver.find_element_by_id('form:j_idt77').click()
        wdriver.find_element_by_id('form:j_idt75').click() #voltar
    wdriver.find_element_by_link_text('FREQUÊNCIA').click() #frequencia    
    #wdriver.find_elements_by_xpath('//label[contains(text(), "{0}")]'.format(str(datetime.datetime.now().strftime("%d/%m/%y"))))
    scheight = .1
    while(scheight<9.9):
        #wdriver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        driver.execute_script("document.body.style.zoom='zoom 80%'")
        wdriver.execute_script("window.scrollTo(0,document.body.height/2")
        scheight += .1
    wdriver.save_screenshot('snapshot.jpg')


if __name__ == '__main__':
    '''
    os.system('cls')

    while(True):
        #sys.stdout.write
        print("\r{}".format("Rodando..."))
        #sys.stdout.flush()
        try:
            now = datetime.datetime.now().time()
            while(now.hour not in range(6,20)):
                sys.stdout.write("\r({}) Sleeping...".format(datetime.datetime.now().time()))
                sys.stdout.flush()
                time.sleep(30)
                now = datetime.datetime.now().time()

                    
            conn = conectar(logm,base64.b64decode(pwdm).decode('ascii'),host)
            email = leremail(conn)
            comando = checkcomando(email)
            if(comando):
                print("Executando: "+comando)
                if(comando==cmds[0]): #ppp
                    driver = webdriver.Chrome()
                    driver.set_window_size(1120, 1050)
                    ppp(driver,logp,base64.b64decode(pwdp).decode('ascii'))
                    print("DONE!")
                    driver.close()
                if(comando==cmds[1]): #print
                    print("SCREENSHOT ENVIADO!")
                if(comando==cmds[2]): #stop
                    print("EXIT!")
                    quit()
                if(comando==cmds[3]): #pega num sequencia
                    print("Num sequencia enviado")
            else:
                time.sleep(sleeptime)
        except Exception as e:
                print("[-]ERRO:"+str(e))
    '''
    driver = webdriver.Chrome()
    driver.set_window_size(1120, 1050)
    ppp(driver,logp,base64.b64decode(pwdp).decode('ascii'),True)
    print("DONE!")
    driver.close()
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
