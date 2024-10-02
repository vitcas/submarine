# OpenSubtitles Web Scraper

Este projeto é um web scraper em Python que coleta informações sobre legendas do site [OpenSubtitles](https://www.opensubtitles.org) e verifica se uma legenda pertence a uma série.

## Funcionalidades

- Coleta informações de legendas.
- Verifica se uma página contém uma série (procurando o `id="season-1"`).

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Execute o script principal para começar a raspar dados:
```bash
python scraper.py
