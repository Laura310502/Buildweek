import socket #libreria da importare
import sys

def scan_ports (host, start_port, end_port):
    print(f"[*] scansione di {host} da porta {start_port} a {end_port} ...")

    for port in range(start_port,end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0) #imposta un timeout per la connessione
                result = s.connet_ex((host, port))
                if result == 0:
                    print(f"   [+] Porta {port} aperta")

        except socket.gaierror:
            print("[-] Errore: impossibile connettersi al server.")
            sys.exit()
        except socket.error:
            print("[-] Errore: impossibile connettersi al server.")
            sys.exit()


if __name__ == "__main__": #__name__ variabile comune in python --> Target Host
    target_host = input("Inserisci l'indirizzo IP da scansionare: ")
    start_port_num = input("Inserisci la porta iniziale: ")
    end_port_num = input("Inserisci la porta finale: ")

scan_ports(target_host, start_port_num, end_port_num)