import json

# Caminhos para os arquivos JSON
file_path_main = 'C:\\Users\\Victor\\Desktop\\Teste com Django\\producao_cientifica\\dados_normalizados_consolidados.json'
file_path_links = 'C:\\Users\\Victor\\Desktop\\Teste com Django\\producao_cientifica\\dados.json'

# Carregar os dados do arquivo principal
with open(file_path_main, 'r', encoding='utf-8') as file:
    data_main = json.load(file)

# Carregar os dados do arquivo com links
with open(file_path_links, 'r', encoding='utf-8') as file:
    data_links = json.load(file)

# Criar um dicionário para mapear IDs para Links
links_dict = {item['Id']: item.get('LinkArquivo', '') for item in data_links}

# Adicionar o campo 'LinkArquivo' ao arquivo principal
for item in data_main:
    item['LinkArquivo'] = links_dict.get(item['Id'], '')

# Função para reordenar as chaves incluindo 'LinkArquivo'
def reorder_keys(item):
    key_order = ['Id', 'Titulo', 'DataDaDefesa', 'NomeDoCurso', 'NomeOrientador', 'LinkArquivo', 'Autores', 'PalavrasChave']
    return {key: item[key] for key in key_order if key in item}

# Processar cada item para reordenar as chaves
processed_data = [reorder_keys(item) for item in data_main]

# Salvar os dados modificados de volta ao arquivo principal
with open(file_path_main, 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, ensure_ascii=False, indent=4)

print("Modificações realizadas com sucesso.")
