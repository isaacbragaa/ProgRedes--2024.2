import socket

DIRBASE = "files/"
SERVER = '127.0.0.1'
PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    #lê do usuário o nome do arquivo a pedir ao servidor
    fileName = input("Arquivo a pedir ao servidor: ")

    #envia ao servidor o nome do arquivo desejado pelo usuário
    print("Enviando pedido a", (SERVER, PORT), "para", fileName)
    sock.sendto(fileName.encode('utf-8'), (SERVER, PORT))

    try:
        #recebe o tamanho do arquivo
        fileSizeData, source = sock.recvfrom(512)
        fileSize = int(fileSizeData.decode('utf-8'))

        if fileSize == 0:
            print("Erro: o arquivo está vazio ou não foi encontrado.")
            continue

        #grava o arquivo
        print("\nGravando arquivo")
        receivedSize = 0
        with open(DIRBASE + fileName, 'wb') as fd:
            while receivedSize < fileSize:
                data, _ = sock.recvfrom(4096)
                if not data:
                    break
                fd.write(data)
                receivedSize += len(data)

        print("Arquivo recebido com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

sock.close()
