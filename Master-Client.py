import xmlrpc.client
from concurrent.futures import ThreadPoolExecutor

def dividir_texto(caminho_arquivo, num_blocos):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    blocos = [linhas[i::num_blocos] for i in range(num_blocos)]
    return [''.join(bloco) for bloco in blocos]

def mestre_contar_palavras(caminho_arquivo):
    blocos = dividir_texto(caminho_arquivo, len(nodes))
    resultados = []

    for (apelido, ip), bloco in zip(nodes.items(), blocos):
        print(f"Enviando tarefa para {apelido} ({ip})...")
        try:
            proxy = xmlrpc.client.ServerProxy(f"http://{ip}:8000/", allow_none=True)
            resultado = proxy.contar_palavras(bloco)
            resultados.append(resultado)
        except Exception as e:
            print(f"Erro ao contatar {apelido}: {e}")
            resultados.append(0)

    total = sum(resultados)
    print(f"Total de palavras no arquivo: {total}")

def verificar_node(ip, porta=8000, timeout=1):

    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{ip}:{porta}/", allow_none=True)
        # Teste se a função alguma função está disponível
        proxy.system.listMethods()
        return ip
    except:
        return None

#descobre nós que são do tipo 192.168.0.xxx que são comuns em redes locais.
def descobrir_nodes_na_rede(prefixo_rede="192.168.0.", intervalo=(1, 254)):
    nodes_ativos = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        ips = [f"{prefixo_rede}{i}" for i in range(intervalo[0], intervalo[1] + 1)]
        resultados = executor.map(verificar_node, ips)

    for ip in resultados:
        if ip:
            apelido = f"node_{ip.split('.')[-1]}"
            nodes_ativos[apelido] = ip
    #garante que um nó do sistema descentralizado será o próprio cliente que emitiu a tarefa na rede descentralizada
    nodes_ativos["localhost"] = "127.168.0.1"
    return nodes_ativos

if __name__ == "__main__":
    #simula uma rede descentralizada onde cada nó conhece todos os outros nó da rede local
    nodes = descobrir_nodes_na_rede()
    mestre_contar_palavras("arquivo_grande.txt")
