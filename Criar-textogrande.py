import random

# Lista com 50 palavras diferentes
palavras = [
    "abacate", "banheiro", "cachorro", "dinheiro", "elefante", "foguete", "guitarra", "hamburguer", "igreja", "janela",
    "kiwi", "lousa", "mala", "navio", "ocelote", "papel", "quadro", "rosa", "sapato", "tigre",
    "urso", "violão", "watt", "xadrez", "yeti", "zebra", "algodão", "bambu", "cebola", "dedal",
    "escada", "feira", "girassol", "hortelã", "ilha", "jacaré", "karatê", "limão", "moeda", "nuvem",
    "ovo", "pizza", "quibe", "raquete", "sabão", "tomate", "uva", "vassoura", "xampu", "zangão"
]

arquivo_saida = "arquivo_grande.txt"

total_palavras = 10_000_000
tamanho_linha = 100 

with open(arquivo_saida, 'w', encoding='utf-8') as f:
    for i in range(0, total_palavras, tamanho_linha):
        bloco = random.choices(palavras, k=tamanho_linha)
        f.write(' '.join(bloco) + '\n')
        #print(f"Bloco {i//tamanho_linha + 1} concluído")

print(f"Arquivo '{arquivo_saida}' criado com sucesso contendo {total_palavras} palavras.")