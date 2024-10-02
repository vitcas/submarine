import requests
import movie
import tvshow
from bs4 import BeautifulSoup

base_url = "https://www.opensubtitles.org"

def verificar_se_eh_serie(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        # Fazer requisição à página
        response = requests.get(url, headers=headers)

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Analisar o conteúdo da página
            soup = BeautifulSoup(response.text, 'html.parser')

            # Procurar pelo elemento com id="season-1"
            if soup.find(id="season-1"):
                return True
            else:
                return False
        else:
            print(f"Erro ao acessar a página: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return False

def buscar_legenda(nome_filme):
    url = f"https://www.opensubtitles.org/pb/search2/sublanguageid-pob/moviename-{nome_filme.replace(' ', '+')}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tabela_resultados = soup.find(id="search_results")
        if tabela_resultados:
            linhas = tabela_resultados.find_all('tr')
            resultados = []  # Lista para acumular resultados
            links = []  # Lista para acumular os links
            for linha in linhas[1:]:  # Ignora a primeira linha (cabeçalho)
                strong_tags = linha.find_all('strong')
                for strong in strong_tags:
                    a_tag = strong.find('a')
                    if a_tag:
                        txt = a_tag.get('title')
                        title = txt.replace("Legendas - ","")
                        href = a_tag.get('href')
                        resultados.append(f"{title}")
                        links.append(href)  # Adiciona o href à lista de links
            # Exibe resultados, cada um em uma linha
            if resultados:
                print("Resultados encontrados:")
                for i, resultado in enumerate(resultados, start=1):
                    print(f"{i}. {resultado}")
                print(f"Foram encontrados {len(resultados)} resultados.")
                # Solicita ao usuário para escolher um número
                escolha = int(input("Escolha um número da lista: ")) - 1
                if 0 <= escolha < len(links):
                    escolhido = links[escolha]
                    print(f"Você escolheu o link: {escolhido}")
                    #lisleg.legendas_filme(escolhido)
                    full_url = base_url + escolhido
                    if verificar_se_eh_serie(full_url):
                        print("Essa página corresponde a uma série.")
                        print("\nVou listar os episodios.")
                        tvshow.listar_episodios(full_url)
                    else:
                        print("Essa página não corresponde a uma série.")
                        print("\nVou procurar uma legenda bluray.")
                        movie.legendas_filme(escolhido)
                else:
                    print("Escolha inválida. Tente novamente.")
            else:
                print("Nenhum resultado encontrado.")
        else:
            print("Nenhuma tabela de resultados encontrada.")
    else:
        print("Erro ao acessar a página.")

def main():
    nome_filme = input("Digite o nome do filme: ")
    buscar_legenda(nome_filme)    

if __name__ == "__main__":
    main()
