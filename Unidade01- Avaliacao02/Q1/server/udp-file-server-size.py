import socket
import os

DIRBASE = "files/"
INTERFACE = '127.0.0.1'
PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((INTERFACE, PORT))

print("Escutando em ...", (INTERFACE, PORT))
while True:
    #recebe o nome do arquivo
    data, source = sock.recvfrom(512)
    fileName = data.decode('utf-8')
    filePath = DIRBASE + fileName

    try:
        #verifica se o arquivo existe
        if not os.path.exists(filePath):
            raise FileNotFoundError("Arquivo não encontrado.")

        print("Recebi pedido para o arquivo", fileName)

        #abre o arquivo e pega o tamanho
        fileSize = os.path.getsize(filePath)
        sock.sendto(str(fileSize).encode('utf-8'), source)  #envia o tamanho do arquivo

        #lê o conteúdo do arquivo 
        with open(filePath, 'rb') as fd:
            print("Enviando arquivo", fileName)
            while True:
                fileData = fd.read(4096)
                if not fileData:
                    break
                sock.sendto(fileData, source)
    except Exception as e:
        #tratamento de erro
        print(f"Erro: {e}")
        sock.sendto(b'ERROR', source)

sock.close()
