logp = b'bG5hcmRvLmNvbmNlaWNhbw=='
pwdp = b'bGVvbGVvMTIz'
host = b'em10YS50cnQxLmp1cy5icg=='
logm = b'bGVvbmFyZG8uY29uY2VpY2FvQHRydDEuanVzLmJy'
pwdm = b'bGVvbGVvMTIz'
dest_mail = b'bGVvbmFyZG9kZW9jQGdtYWlsLmNvbQ=='

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

sleeptime = 15
cmds = ["ppp","print","stop","status","ppa","del","?"]

conteudo = []
agendado = []


def enviaRetorno(login,password,destino,subject,texto,tipo):
    if(tipo=='img'):
        msg = MIMEMultipart()
        part = MIMEBase("image","octet-stream")
        part.set_payload(open('snapshot.jpg','rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="snapshot.jpg"')
        msg.attach(part)
    else:
        msg = MIMEText(str(texto))
    
    msg['Subject'] = subject
    msg['From'] = login
    msg['To'] = destino
        
    try:  
        server = smtplib.SMTP_SSL(decodificar(host), 465)
        server.ehlo()
        server.login(login, password)
        server.sendmail(login, destino, msg.as_string())
        server.close()
        print('Email enviado!')
    except smtplib.SMTPException as e:  
        print("Erro enviaStatus: "+str(e))

def criaDriver():
    driver = webdriver.Chrome()
    #driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 1050)

    return(driver)

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
        sys.stdout.flush()

def checkcomando(email):
    comandos = []
    try:
        pattern_comando = re.compile(r'(#:)(ppp|ppa|print|status|del|stop|agenda|\?)(:)?((\d)*)')
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
    wdriver.get(decodificar(b'aHR0cHM6Ly9wb250by50cnQxLmp1cy5icg=='))
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
        wdriver.find_element_by_link_text(decodificar(b'UkVHSVNUUkFSIFBPTlRP')).click()
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
        count = 1
        sys.stdout.write("\r\033[K")
        for hora_agendada in agendado:
            if(datetime.datetime.now()>=hora_agendada):
                driver = criaDriver()
                ppp(driver,decodificar(logp),decodificar(pwdp),False)
                print("DONE!")
                driver.close()
                enviaRetorno(decodificar(logm),decodificar(pwdm),decodificar(dest_mail),'Executado agendamento','','img')
                agendado.remove(hora_agendada)
            else:#####TIRAR DEPOIS
                sys.stdout.write("Ha PPP agendado para: (%d) - %s"%(count,str(hora_agendada)))
                sys.stdout.flush()
                count+=1

def checaAgendado():
    if(len(agendado)==0):
        texto="Nao ha horarios agendados"
    else:
        count = 1
        texto = "Ha ppp agendado para:\n"
        for hora_agendada in agendado:
            texto+="(%d) - %s\n"%(count,str(hora_agendada))
            count+=1 
    enviaRetorno(decodificar(logm),decodificar(pwdm),decodificar(dest_mail),'PPPs agendados',texto,'agenda')

def deletaAgendado(numero):
    if(len(agendado)==0 or (int(numero)-1)>len(agendado)):
        print('Nao ha o ppp a ser deletado')
    else:
        if(int(numero)==0):
            del(agendado[:])
            print("Itens removidos")
        else:
            del(agendado[int(numero)-1])
            print("Item removido")
            #checaAgendado()

def decodificar(entrada):
    return(base64.b64decode(entrada).decode('ascii'))


if __name__ == '__main__':

    if(len(sys.argv)==2):
        if(sys.argv[1]=='-n'):
            with open(__file__,'r') as arquivo:
                for linha in arquivo:
                    conteudo.append(linha)

            with open(__file__,'w') as arquivo:
                conteudo[0] = "logp = {}\n".format(base64.b64encode(bytes(input("Novo valor para logp:"),'utf-8')))
                conteudo[1] = "pwdp = {}\n".format(base64.b64encode(bytes(input("Novo valor para pwdp:"),'utf-8')))
                novo_host = input("Novo valor para host (Deixar em branco zmta):")
                if(novo_host==''):
                    conteudo[2] = "host = {}\n".format(b'em10YS50cnQxLmp1cy5icg==')
                else:
                    conteudo[2] = "host = {}\n".format(base64.b64encode(bytes(novo_host,'utf-8')))
                conteudo[3] = "logm = {}\n".format(base64.b64encode(bytes(input("Novo valor para log mail:"),'utf-8')))
                conteudo[4] = "pwdm = {}\n".format(base64.b64encode(bytes(input("Novo valor para pwd mail:"),'utf-8')))
                conteudo[5] = "dest_mail = {}\n".format(base64.b64encode(bytes(input("Novo valor para mail destino:"),'utf-8')))
                
                for i in range(len(conteudo)):
                    arquivo.write(conteudo[i])
    else:
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
                        
                conn = conectar(decodificar(logm),decodificar(pwdm),decodificar(host))
                email = leremail(conn)
                comandos = checkcomando(email)
                print("COMANDOS:%s \r"%(str(comandos)),end='')

                executaAgendado()

                if(comandos is not None):
                    print("\nExecutando: "+str(comandos[0]))

                    if(comandos[0]==cmds[0]): #ppp
                        driver = criaDriver()
                        ppp(driver,decodificar(logp),decodificar(pwdp),False)
                        print("DONE!")
                        driver.close()
                        enviaRetorno(decodificar(logm),decodificar(pwdm),decodificar(dest_mail),'Retorno ppp '+str(datetime.datetime.now().strftime("%d/%m-%H:%M")),'','img')
                    
                    if(comandos[0]==cmds[1]): #print
                        driver = criaDriver()
                        ppp(driver,decodificar(logp),decodificar(pwdp),True)
                        driver.close()
                        enviaRetorno(decodificar(logm),decodificar(pwdm),decodificar(dest_mail),'Retorno ppp '+str(datetime.datetime.now().strftime("%d/%m-%H:%M")),'','img')
                        print("SCREENSHOT ENVIADO!")                    
                    
                    if(comandos[0]==cmds[2]): #stop
                        print("EXIT!")
                        quit()
                    
                    if(comandos[0]==cmds[3]): #status
                        checaAgendado()
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
                                enviaRetorno(decodificar(logm),decodificar(pwdm),decodificar(dest_mail),'Retorno Agendamento','Agendado para: '+str(target),'ppa')
                                print(" Agendado! ")


                    if(comandos[0]==cmds[5]): #del
                        if(comandos[1] is None):
                            print("PPP faltando")
                        else:
                            deletaAgendado(comandos[1])
                    
                    if(comandos[0]==cmds[6]): #?
                        texto = "#:\nppp - point\nprint - snapshot\nstop - para daemon\nstatus - ve agenda\nppa:HHMM - agenda point\ndel - deleta agendamentos(0 deleta td)"
                        enviaRetorno(decodificar(logm),decodificar(pwdm),decodificar(dest_mail),'ppp Comandos',texto,'?')
                        print("HELP ENVIADO!")
                else:
                    time.sleep(sleeptime)       
            except Exception as e:
                    print("[-]ERRO MAIN:"+str(e))
