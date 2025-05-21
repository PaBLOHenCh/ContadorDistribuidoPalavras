import asyncio
from aioxmlrpc.client import ServerProxy
from concurrent.futures import ThreadPoolExecutor
import time

#função para dividir texto em blocos
def dividir_texto(caminho_arquivo, num_blocos):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    blocos = [linhas[i::num_blocos] for i in range(num_blocos)]
    return [''.join(linha) for linha in blocos]

#verifica se o nó responde corretamente à funçãocontar palavras
def verificar_node(ip, porta=8000):
    import xmlrpc.client
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{ip}:{porta}/", allow_none=True)
        try:
            proxy.contar_palavras("teste")
            print(f"Nó {ip} conectado e respondeu corretamente.")
            return ip
        except:
            print(f"Nó {ip} não executou 'contar_palavras'.")
            return None
    except:
        return None

#descobre nós ativos na rede
def descobrir_nodes_na_rede(prefixo_rede="192.168.52.", intervalo=(140, 215)):
    nodes_ativos = {}
    ips = [f"{prefixo_rede}{i}" for i in range(intervalo[0], intervalo[1] + 1)]
    #ips.append("127.168.0.1")
    with ThreadPoolExecutor(max_workers=6) as executor:
        resultados = executor.map(verificar_node, ips)

    for ip in resultados:
        if ip:
            apelido = f"node_{ip.split('.')[-1]}"
            nodes_ativos[apelido] = ip
    return nodes_ativos

#função assíncrona para contar palavras via rpc
async def contar_palavras_remoto(ip, bloco):
    try:
        proxy = ServerProxy(f"http://{ip}:8000/", timeout=100.0)
        resultado = await proxy.contar_palavras(bloco)
        return resultado
    except Exception as e:
        print(f"Erro ao contatar {ip}: {e}")
        return 0

#função mestre usando asyncio + aioxmlrpc
async def mestre_contar_palavras(caminho_arquivo, nodes):
    blocos = dividir_texto(caminho_arquivo, len(nodes))
    tarefas = []

    for (apelido, ip), bloco in zip(nodes.items(), blocos):
        print(f"Enviando tarefa para {apelido} ({ip})...")
        tarefas.append(contar_palavras_remoto(ip, bloco))

    #ponto de unificação das tarefas assincronas
    resultados = await asyncio.gather(*tarefas)
    print("Resultados individuais:", resultados)
    print("Total de palavras:", sum(r for r in resultados))

if __name__ == "__main__":
    nodes = descobrir_nodes_na_rede()
    inicio = time.time()
    asyncio.run(mestre_contar_palavras("arquivo_grande.txt", nodes))
    fim = time.time()

    print(f"Tempo decorrido da contagem de palavras: {fim - inicio}")