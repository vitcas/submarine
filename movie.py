import requests
from bs4 import BeautifulSoup

base_url = "https://www.opensubtitles.org"

def process_href(href, output_file):
    full_url = base_url + href  # Constrói a URL completa

    try:
        # Fazer a requisição à página do href
        response = requests.get(full_url)
        response.raise_for_status()  # Lança um erro se a resposta não for 200

        # Fazer o parsing do conteúdo da página com BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar a tabela com id='search_results'
        table = soup.find('table', {'id': 'search_results'})

        if table:
            # Variável para armazenar o primeiro href encontrado com 'subtitleserve'
            subtitleserve_href = None
            output_lines = []  # Lista para armazenar as saídas

            # Iterar sobre as linhas da tabela
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    col_texts = [col.text.strip().lower() for col in cols]

                    # Verificar se a palavra 'bluray' está presente na linha
                    if any('bluray' in col_text for col_text in col_texts):
                        # Mostrar apenas a primeira e a quinta coluna
                        first_col = cols[0].text.strip() if len(cols) > 0 else "N/A"
                        output_line = f"Encontrado 'bluray': {first_col}\n"
                        output_lines.append(output_line)
                        print(output_line.strip())  # Mostrar no console

                        link = cols[4].find('a', href=True)
                        if link and "subtitleserve" in link['href']:
                            subtitleserve_href = link['href']
                            subtitle_link_output = f"Encontrado link: {base_url}{subtitleserve_href}\n"
                            output_lines.append(subtitle_link_output)
                            print(subtitle_link_output.strip())  # Mostrar no console
                        break  # Parar no primeiro <tr> que contém 'bluray'

            if not subtitleserve_href:
                no_link_output = "Nenhum link com 'subtitleserve' encontrado.\n"
                output_lines.append(no_link_output)
                print(no_link_output.strip())

            # Salvar a saída em um arquivo
            with open(output_file, 'a', encoding='utf-8') as f:  # Modo 'a' para adicionar
                f.writelines(output_lines)
        else:
            print("Tabela com id='search_results' não encontrada na página.")
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")

def legendas_filme(href):
    output_file = 'link-legenda.txt'
    process_href(href, output_file)

def legendas_serie():
    input_file = 'episodios.txt'
    output_file = 'links-legendas.txt'
    # Lista para armazenar os valores de 'Href:'
    hrefs = []
    
    try:
        # Abrir e ler o arquivo
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # Iterar sobre cada linha do arquivo
            for line in lines:
                # Verificar se a linha contém 'Href:'
                if 'Href:' in line:
                    # Encontrar a parte após 'Href:'
                    href = line.split('Href:')[-1].strip()
                    hrefs.append(href)  # Armazenar o valor no array
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        exit()
    
    # Processar cada href encontrado
    for href in hrefs:
        process_href(href, output_file)
