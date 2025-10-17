import socket
import sys

#Variabili per Ip host e porte da scannerizzere
target_Host = "192.168.50.16"
ports_to_Scan = [80,25,53,44444]
TIMEOUT = 1

#Mappatura porte comuni 
ports_Map = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 
    53: "DNS", 80: "HTTP", 443: "HTTPS"}

def scansiona_porte (host , port) :

    print(f"\n--- Inizio scansione su IP:{host}---\n")
    report_data_port_scanner=[]
    for porta in ports_to_Scan : 
        risultato = {"Host": host , "Porta" : porta ,"Servizio" : ports_Map.get(porta,"Unknown"),"Stato" : "Errore","Messaggio" :"printRisultato" } 

        try : 
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            stato = s.connect_ex((target_Host,porta))
            s.close() #Chiusura socket 
            if(stato == 0):
                risultato["Stato"] = "Aperta"
                risultato["Messaggio"] = "Accesso consentito."
            
            else:
                risultato["Stato"] = "Chiusa"
                risultato["Messaggio"] = "Porta chiusa o esiste una regola per tale porta all'interno del Firewall"
           

        except (socket.gaierror,socket.error) as error : 
            risultato["Stato"] = "Errore nell'host o nella connessione"
            risultato["Messaggio"] = f"Impossibile connettersi all'host {error}"
        print(f"Porta {risultato['Porta']:<5} ({risultato['Servizio']:<10}) : {risultato['Stato']:<15}")
        #Usando : inizia una specifica del formato < specifica allineamento e il numero quanto spazio deve occupare in caratteri
        report_data_port_scanner.append(risultato)


    return report_data_port_scanner

if __name__ == "__main__" : 
    report_scanner = scansiona_porte(target_Host, ports_to_Scan)

    print("\n Dati per Report ")
    for item in report_scanner : 
        if "Aperta" in item["Stato"]:
            print(f"Porta Aperta: {item['Porta']} ({item["Servizio"]}) ---> Sicurezza : {item["Messaggio"]}")
        if "Chiusa" in item["Stato"] : 
            print(f"Porta Chiusa : {item["Porta"]} ({item["Servizio"]}) ")    

