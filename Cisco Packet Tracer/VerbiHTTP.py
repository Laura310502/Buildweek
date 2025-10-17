import http.client

host = "192.168.20.10"
port = 80 #Porta di default per HTTP
path= "/dvwa/index.php"

payload_POST = b"data=test_post_data"
payload_PUT = b"data=test_put_update"
content_type = "application/x-www-form-urlencoded" #Header per POST e PUT 

def verifica_Http() : 
    report_data_http = []
    verbi_test = ["GET","DELETE","POST","PUT"]


    # try : 
    #     conn = http.client.HTTPConnection(host,port,timeout=5)
    # except Exception as error : 
    #     print(f"Errore durante inizializzazione connessione : {error}")
    #     report_data_http.append({"Verbo" : "INITIALIZATION", "Codice_Stato": "non presente", "Dettaglio_Risposta": "Errore Connessione", "URL_Testato": f"http://{host}:{port}", "Payload": "Non presente"})
    #     return report_data_http
    
    for verbo in verbi_test : 
        #Variabili per payload e headers
        body = None
        headers={}
        payload_sent = "Non presente"
        if verbo == "POST" : 
            body = payload_POST
            headers = {"Content-Type" : content_type}
            payload_sent = body.decode()
        elif verbo == "PUT" : 
            body = payload_PUT
            headers = {"Content-Type" : content_type}
            payload_sent = body.decode()
        risultato = {"Verbo":verbo , "URL_Test":f"http://{host}:{port}{path}","Codice_Stato":"non presente","Dettaglio_Risposta" : "non presente" , "Payload" : "non presente"}

        conn =None
        try : 
            conn = http.client.HTTPConnection(host,port,timeout=5)
            conn.request(verbo,path,body=body,headers=headers)
            response = conn.getresponse()
            risultato["Codice_Stato"] = response.status
            if 200 <= risultato["Codice_Stato"] < 400 :
                risultato["Dettaglio_Risposta"] = f"Successo : {response.reason}" 
            elif verbo == "OPTIONS" and response.status == 200:
                risultato["Dettaglio_Risposta"] = f"Metodi Abilitati : {response.getheader('Allow','Non trovato')}"
            else : 
                risultato["Dettaglio_Risposta"] = response.reason
            
            print(f"{verbo:<8} : Stato{risultato['Codice_Stato']} - {risultato['Dettaglio_Risposta'][:40]}...")
        except ConnectionRefusedError: 
            risultato["Dettaglio_Risposta"] = "Connessione Fallita"
            print(f"{verbo}:{risultato['Dettaglio_Risposta']}")
        except Exception as error :
            risultato ["Dettaglio_Risposta"] = f"Errore generico {str(error)}"
        finally :
            if conn : 
                 conn.close()


        report_data_http.append(risultato)



    return report_data_http

if __name__ == "__main__":
    risultati_test = verifica_Http()
    
    for risultato in risultati_test:
        payload_disp = ""
        if risultato['Payload'] != 'Non presente' : 
            payload_disp = f" (Payload: {risultato['Payload']})"  
        print(f"[{risultato['Verbo']:<8}] Stato: {risultato['Codice_Stato']} | Dettaglio: {risultato['Dettaglio_Risposta']}{payload_disp}")
    
