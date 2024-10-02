import requests
from bs4 import BeautifulSoup

# URL da página alvo
#url = "https://www.opensubtitles.org/pb/ssearch/sublanguageid-pob/idmovie-63130"

def listar_episodios(url):
    # Fazer a requisição à página
    response = requests.get(url)
    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Fazer o parsing do conteúdo da página com BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'search_results'})
        # Lista para armazenar todas as linhas que vamos gravar no arquivo
        output_lines = []
        # Encontrar todas as linhas da tabela (com e sem itemprop)
        rows = table.find_all('tr')
        for row in rows:
            # Se a linha tiver itemprop="episode"
            if row.has_attr('itemprop') and row['itemprop'] == 'episode':
                # Encontrar o <a> dentro da linha
                link = row.find('a')
                # Se o <a> existir e possuir os atributos title e href
                if link and 'title' in link.attrs and 'href' in link.attrs:
                    title = link['title']
                    href = link['href']
                    line = f"Title: {title}, Href: {href}"
                    print(line)  # Exibe no console
                    output_lines.append(line)  # Armazena na lista
            else:
                # Se a linha não tiver itemprop="episode", exibimos as células da linha
                cols = row.find_all('td')
                if cols:
                    col_texts = [col.text.strip() for col in cols]
                    line = f"{col_texts}"
                    print(line)  # Exibe no console
                    output_lines.append(line)  # Armazena na lista
        # Salvar as linhas no arquivo output.txt
        with open('episodios.txt', 'w', encoding='utf-8') as file:
            for output_line in output_lines:
                file.write(output_line + '\n')
        print("Dados salvos no arquivo episodios.txt")
    else:
        print(f"Erro ao acessar a página: {response.status_code}")
