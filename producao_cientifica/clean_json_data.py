import json
import html

def unescape_html_in_data(item):
    """
    Função recursiva para desescapar entidades HTML em strings dentro de uma estrutura de dados.
    """
    if isinstance(item, list):
        return [unescape_html_in_data(e) for e in item]
    elif isinstance(item, dict):
        return {k: unescape_html_in_data(v) for k, v in item.items()}
    elif isinstance(item, str):
        return html.unescape(item)
    else:
        return item

def clean_json_file(filename):
    """
    Lê um arquivo JSON, desescapa entidades HTML e escreve os dados corrigidos de volta no arquivo.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data = unescape_html_in_data(data)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    json_filename = 'dados_normalizados_consolidados.json'
    clean_json_file(json_filename)
    print(f"Entidades HTML no arquivo {json_filename} foram desescapadas com sucesso!")
