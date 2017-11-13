from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
import base64
import sys
import re
import imaplib
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os

sleeptime = 30

logp = "leonardo.conceicao"
pwdp = b'bGVvbGVvMTIz'

host="zmta.trt1.jus.br"
logm= "leonardo.conceicao@trt1.jus.br"
pwdm = b'bGVvbGVvMTIz'

cmds = ["ppp","print","stop","status","ppa","agenda","?"]
agendado = []


def enviaEmail(login,password,destino):
    msg = MIMEMultipart()
    msg['Subject'] = 'Retorno ppp '+str(datetime.datetime.now().strftime("%d-%m-%H-%M"))
    msg['From'] = 'leonardo.conceicao@trt1.jus.br'
    msg['To'] = 'leonardodeoc@gmail.com'

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
        print("Erro enviaEmail: "+str(e))

def enviaStatus(login,password,destino,texto):
    msg = MIMEText(str(texto))
    msg['Subject'] = "Status ppp OK"
    msg['From'] = login
    msg['To'] = destino

    try:  
        server = smtplib.SMTP_SSL(host, 465)
        server.ehlo()
        server.login(login, password)
        server.sendmail(login, destino, msg.as_string())
        server.close()
        print('Email enviado!')
    except smtplib.SMTPException as e:  
        print("Erro enviaStatus: "+str(e))

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
        sys.stdout.write("Nao ha comandos a serem executados ")

def checkcomando(email):
    comandos = []
    try:
        pattern_comando = re.compile(r'(###:)(ppp|ppa|print|status|stop|agenda|\?)(:)?((\d)*)')
        comando = pattern_comando.search(email.decode('utf-8'))
        comandos.append(comando.group(2))
        try:
            comandos.append(comando.group(4))
        except:
            pass
        return(comandos)
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
        wdriver.implicitly_wait(1)
        wdriver.find_element_by_link_text(base64.b64decode(b'UkVHSVNUUkFSIFBPTlRP').decode('ascii')).click()
        wdriver.implicitly_wait(1)
        wdriver.find_element_by_id('form:j_idt77').click() #bingo
        time.sleep(3)
        wdriver.find_element_by_id('form:j_idt75').click() #voltar
    wdriver.find_element_by_link_text(base64.b64decode(b'RlJFUVXDik5DSUE=').decode('utf-8')).click()
    wdriver.execute_script("document.body.style.zoom='73%'")
    wdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wdriver.save_screenshot('snapshot.jpg')

def executaAgendado():
    if(len(agendado)==0):
        pass
    else:
        for hora_agendada in agendado:
            if(datetime.datetime.now()>=hora_agendada):
                driver = webdriver.Chrome()
                driver.set_window_size(1120, 1050)
                ppp(driver,logp,base64.b64decode(pwdp).decode('ascii'),False)
                print("DONE!")
                driver.close()
                enviaEmail(logm,base64.b64decode(pwdm).decode('ascii'),"leonardodeoc@gmail.com")
                agendado.remove(hora_agendada)
            else:#####TIRAR DEPOIS
                print("Ha um PPP agendado para: "+str(hora_agendada))

if __name__ == '__main__':
    
    os.system('cls')

    while(True):
        sys.stdout.write("\r{}".format("Rodando..."))
        sys.stdout.flush()
        try:        
            if(datetime.datetime.today().weekday()>=5):
                sys.stdout.write("\r{}".format("Sleeping(fds)..."))
                sys.stdout.flush()
                time.sleep(300)
            
            now = datetime.datetime.now().time()
            while(now.hour not in range(6,20)):
                sys.stdout.write("\r({}) Sleeping...".format(datetime.datetime.now().time()))
                sys.stdout.flush()
                time.sleep(60)
                now = datetime.datetime.now().time()
                    
            conn = conectar(logm,base64.b64decode(pwdm).decode('ascii'),host)
            email = leremail(conn)
            comandos = checkcomando(email)
            print("COMANDOS:%s \r"%(str(comandos)),end='')

            executaAgendado()

            if(comandos is not None):
                print("\nExecutando: "+str(comandos[0]))

                if(comandos[0]==cmds[0]): #ppp
                    driver = webdriver.Chrome()
                    #driver = webdriver.PhantomJS()
                    driver.set_window_size(1120, 1050)
                    ppp(driver,logp,base64.b64decode(pwdp).decode('ascii'),False)
                    print("DONE!")
                    driver.close()
                    enviaEmail(logm,base64.b64decode(pwdm).decode('ascii'),"leonardodeoc@gmail.com")
                
                if(comandos[0]==cmds[1]): #print
                    driver = webdriver.Chrome()
                    driver.set_window_size(1120, 1050)
                    ppp(driver,logp,base64.b64decode(pwdp).decode('ascii'),True)
                    driver.close()
                    enviaEmail(logm,base64.b64decode(pwdm).decode('ascii'),"leonardodeoc@gmail.com")
                    print("SCREENSHOT ENVIADO!")                    
                
                if(comandos[0]==cmds[2]): #stop
                    print("EXIT!")
                    quit()
                
                if(comandos[0]==cmds[3]): #status
                    if(len(agendado)>0):
                        todasashoras = ""
                        for hora_agendada in agendado:
                            todasashoras+=str(hora_agendada)
                            todasashoras+="\n"
                        texto = "OK\nHa agendamento para:%s"%(str(todasashoras))
                    else:
                        texto = "OK"

                    enviaStatus(logm,base64.b64decode(pwdm).decode('ascii'),"leonardodeoc@gmail.com",texto)
                    print("STATUS ENVIADO!")
                
                if(comandos[0]==cmds[4]): #ppa
                    if(comandos[1] is None ): #Nao tem o segundo argumento, tempo.
                        print("Time faltando")
                    else:
                        tempo = str(comandos[1])
                        if(len(tempo)!=4):#hm
                            print("Erro - padrao deve ser HHMM")
                        else:
                            target = datetime.datetime.today().replace(hour=int(tempo[0:2]),minute=int(tempo[2:4]))
                            agendado.append(target)
                            enviaStatus(logm,base64.b64decode(pwdm).decode('ascii'),"leonardodeoc@gmail.com","Agendado para: "+str(target))
                            print(" Agendado! ")


                if(comandos[0]==cmds[5]): #agenda
                    pass
                
                if(comandos[0]==cmds[6]): #?
                    texto = "###:\nppp - point\nprint - snapshot\nstop - para daemon\nstatus - ve se esta rodando\nppa:HHMM - agenda point\nagenda - checa agendamentos"
                    enviaStatus(logm,base64.b64decode(pwdm).decode('ascii'),"leonardodeoc@gmail.com",texto)
                    print("HELP ENVIADO!")
            else:
                time.sleep(sleeptime)
        except Exception as e:
                print("[-]ERRO MAIN:"+str(e))
