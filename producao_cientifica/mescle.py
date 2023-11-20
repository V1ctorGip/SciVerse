import json

# Carregue os arquivos JSON em variáveis (assumindo que você já fez isso)
with open('dados_biblioteca.json', 'r', encoding='utf-8') as file:
    dados_biblioteca = json.load(file)
with open('dados_normalizados_consolidados.json', encoding='utf-8') as file:
     dados_consolidados = json.load(file)


biblioteca_index = {item['Id']: item for item in dados_biblioteca}

# Atualize os dados consolidados com as informações faltantes
for item in dados_consolidados:
    id_correspondente = item['Id']
    if id_correspondente in biblioteca_index:
        dados_biblioteca_correspondente = biblioteca_index[id_correspondente]
        # Atualiza as palavras-chave, data da defesa e banca
        item['PalavrasChave'] = dados_biblioteca_correspondente.get('PalavrasChave', [])
        item['DataDaDefesa'] = dados_biblioteca_correspondente.get('DataDaDefesa', '')
        item['Banca'] = dados_biblioteca_correspondente.get('Banca', [])

# Escrever os dados atualizados de volta para um arquivo JSON
with open('dados_normalizados_consolidados_atualizados.json', 'w') as file:
    json.dump(dados_consolidados, file, ensure_ascii=False, indent=4)
