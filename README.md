# ktree_dibuteco26

## TP1 - Geometria Computacional (KD-Tree)

Um repositório para o trabalho prático de Algoritmos II - UFMG 2026/1.

## Sobre o trabalho

Este projeto foi desenvolvido para a disciplina de **Algoritmos 2 (DCC207 - UFMG)**.

O objetivo é implementar um sistema interativo para visualização de bares participantes do *Comida di Buteco 2026* em Belo Horizonte.

O sistema permite:

* Buscar bares a partir de um endereço informado pelo usuário
* Definir uma região retangular de interesse
* Filtrar os bares dentro dessa região
* Ordenar os resultados por distância
* Visualizar os bares em um mapa interativo

A estrutura de dados principal utilizada é uma **árvore k-dimensional (k-d tree)**, aplicada para realizar buscas espaciais eficientes.

---

## Tecnologias utilizadas

* Python
* KD-Tree (implementação própria)
* Dash + Dash Leaflet (visualização)
* OpenStreetMap (geocoding)
* Pandas (manipulação de dados)

---

## Gerenciamento de dependências com uv

Este projeto utiliza o **uv** para gerenciamento de ambiente e dependências.

### Instalação do ambiente

Após clonar o repositório:

```bash
uv sync
```

Isso irá:

* Criar o ambiente virtual automaticamente
* Instalar todas as dependências com base no arquivo `uv.lock`

### Como rodar

Para rodar o super web app, basta digitar no terminal:

```bash
uv run python -m src.app.app
```