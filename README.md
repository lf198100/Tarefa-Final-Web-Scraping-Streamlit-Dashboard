[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/97-nCYdQ)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=19859465)
# Programa Aplicada 1
Prof. Jefferson Santos

## Tarefa Final: Web Scraping + Streamlit Dashboard

### 🎯 Descrição
Nesta atividade final, vocês vão integrar tudo o que aprenderam sobre web scraping com `requests` + `BeautifulSoup` e construção de dashboards interativos em Streamlit. Você deverá:

1. **Selecionar** um site público simples (conteúdo estático) e extrair dados relevantes.
2. **Implementar** funções de scraping com assinaturas já definidas em `scraper.py`.
3. **Construir** um dashboard Streamlit que consuma os dados gerados em `dados/output.csv` e apresente:
   - Filtros em sidebar
   - Tabela de dados
   - Gráficos interativos

---

### 📁 Estrutura obrigatória do repositório

```
.
├── .github/*                   ← não mexam
├── .devcontainer/*             ← não mexam
├── dados/
│   └── output.csv              ← gerado pela função save_to_csv
├── main.py                     ← editem para construir o dashboard streamlit
├── tests/*                     ← não mexam
├── README.md                   ← este arquivo (instruções da atividade)
├── scraper.py                  ← editem para fazer o scrape da página escolhida
└── test_scraping.py            ← não mexam
```

---

### ✅ Etapas da atividade

1. **Escolha do site**
   - Deve ser público, sem JavaScript dinâmico, com elementos html (tags e classes css) fáceis de ser identificados.
   - Ex.: Wikipedia, IMDB, Oxylabs, Quotes to Scrape, Reddit.
   - Não usem Books to Scrape e Yahoo Finance, porque já usamos em aula.
   - Informem até a proxima aula da respectiva turma, nos links abaixo, qual o site sua dupla irá usar. A mesma url só pode ser usada por até duas duplas. Se, ao tentarem editar a planilha, a url desejada já estiver citada, escolham outra.
     - [Barra](https://docs.google.com/spreadsheets/d/11U5fICUEJEU6CPKlOsfUEc-M75L7kAt8wk66yiFyEAw/edit?usp=sharing)

     - [Botafogo1](https://docs.google.com/spreadsheets/d/1HZi-2hqh0inLDt-IUQvCVF911OFnfE_29doBAHKOL4A/edit?usp=sharing)

     - [Botafogo2](https://docs.google.com/spreadsheets/d/1ueXGzTlblsPjDkB0HNW4MQAn4Hp3wqfW-j76sO9EBJw/edit?usp=sharing)

2. **Implementação em `scraper.py`** (veja os comentários no código)
   - **generate_user_agent()**
     - Já está pronta, deve funcionar para a maioria dos sites simples. Mexam com cuidado, se necessário.
   - **fetch_page(url)**
     - Completem o código. Ajustem o retorno.
   - **parse_data(html)**
     - Completem o código. Ajustem o retorno.
   - **save_to_csv(data, filename)**
     - Já está pronta, não mexam.
   - **generate_csv()**
     - Alterem apenas a linha onde a `URL` é definida pela url do site que escolheu realizar o scraping.

3. **Desenvolvimento do Dashboard em `main.py`**
   - O Dashboard já foi iniciado no `main.py`
   - O Dashboard deve conter os seguintes itens obrigatórios:
   1. Título do app
      - O código que monta o título já foi dado, apenas alterem-o para nomear corretamente o seu trabalho. 
        - Usem o padrão: "Dashboard Final: <Título do seu Projeto>" 
        - Exemplo:  "Dashboard Final: List of S&P 500 companies"

   2. Filtros na sidebar
      - Escolham 3 opções de filtros usando os widgets que vimos em sala (text_input, checkbox, radio, selectbox, multiselect, slider)
      - Veja a [documentação sobre widgets](https://docs.streamlit.io/develop/api-reference/widgets) para detalhes.

   3. Tabela de dados
      - Apresente uma visão de tabela dos dados carregados.
      
   4. Graficos
      - Avaliem seus dados e decidam o que exibir em dois gráficos que façam sentido. A escolha é um dos critérios de avaliação. 
      - Vocês podem usar os gráficos nativos do Streamlit, os gráficos com `plotly` ou com `altair`. 

   5. **Descrição ou resumo**
      - Use `st.markdown` ou `st.write` para apresentar estatísticas básicas, título de seções, legendas etc.
      - Vejam a [documentação sobre gráficos](https://docs.streamlit.io/develop/api-reference/charts) para detalhes.



### 💻 Execução dos Códigos

- Executar o Scraper (os dados serão baixados para `dados/output.csv`):
   
   ```bash
   python scraper.py
   ```

- Executar o Dashboard (o dashboard será exibido no browser):

   ```bash
   streamlit run main.py
   ```
---
### 🎥 Vídeo de Apresentação

A dupla deve gravar um vídeo apresentando o projeto em duas partes: 

1. A aplicação executando e como ela funciona.
2. O código-fonte explicando resumidamente suas principais partes.

- Não é necessário explicar linha a linha o código-fonte, a ideia é convencer o professor que vocês o que o código entregue está fazendo. 
- Não é para ler roteiros prontos.
- Os dois membros da dupla devem aparecer no vídeo.
- O vídeo deve ser gravado simultaneamente pelos dois alunos: não é para gravar separadamente e juntar as gravações posteriormente.
- O vídeo deve ter por volta de 10 min (±2).

---
### 💯 Critérios de avaliação

| Critério                                            | Peso |
| --------------------------------------------------- | ---- |
| Funcionamento correto do scraping                   | 40%  |
| Dashboard em funcionamento com Widgets obrigatórios | 50%  |
| Escolha dos filtros e dos gráficos                  | 10%  |

---

### ⚠️ Dicas finais:

> - Não modifique nomes nem parâmetros de funções dadas.
> - Mantenham a separação clara entre scraping e apresentação.
> - Testem toda a cadeia: 
> scraping → csv → carregamento do dashboard → filtros → exibição da tabela e dos gráficos.


#### 🤞🏽 Bom trabalho e boa sorte!
