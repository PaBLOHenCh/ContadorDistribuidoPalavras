from xmlrpc.server import SimpleXMLRPCServer

def contar_palavras(texto):
    return len(texto.split())

#permite que o servidor seja acessado de qualquer interface de rede
server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True)
server.register_function(contar_palavras, "contar_palavras")
print("Worker rodando na porta 8000...")
server.serve_forever()
