# Escalonamento de Tarefas em Projetos de Consultoria

Este repositório contém um exemplo completo de modelagem e resolução do problema de escalonamento de tarefas em projetos de consultoria. O objetivo é distribuir as tarefas entre os consultores de forma que o tempo total de conclusão do projeto (o **makespan**) seja minimizado. Para isso, foram implementadas duas abordagens:

1. **Otimização MILP com CBC** (arquivo `cbc_mixed.py`):  
   Utiliza o solver de programação linear inteira mista (MILP) do OR‑Tools (CBC) para resolver o modelo formulado via branch-and-bound.

2. **Validação por Força Bruta** (arquivo `bruteforce.py`):  
   Implementa uma busca exaustiva para instanciar todas as possíveis atribuições de tarefas aos consultores e identificar, para instâncias pequenas, a solução ótima. Essa abordagem é útil para validação e testes, mas não é escalável para problemas de grande dimensão.

Além disso, o script `gerar_compatibilidade.py` é utilizado para gerar a tabela de compatibilidade (fatores de produção) a partir dos dados de tarefas e consultores.

---

## Contexto e Modelagem do Problema

Em projetos de consultoria, cada projeto é composto por um conjunto de tarefas com tempos base (horas) e cada tarefa pode ser executada por diferentes consultores com diferentes níveis de compatibilidade (fator de produção). O problema é modelado como um problema de *Unrelated Machines Scheduling*

O modelo distribui as tarefas entre os consultores de modo que o consultor com maior carga (o bottleneck) seja otimizado, minimizando o tempo total (makespan) de conclusão do projeto.

---

## Estrutura do Repositório

```
.
├── README.md
├── Relatório final.docx
├── bruteforce.py              # Validação por força bruta para instâncias pequenas
├── cbc_mixed.py               # Implementação do modelo MILP usando OR‑Tools (CBC)
├── gerar_compatibilidade.py   # Gera o arquivo de compatibilidade a partir dos dados de tasks e consultants
├── data
│   ├── compatibility.csv      # Tabela de compatibilidade (fatores de produção)
│   ├── consultants.csv        # Dados dos consultores (id, custo, senioridade, especializacao, skills, etc.)
│   └── tasks.csv              # Dados das tarefas (id, horas, descrição, skills, etc.)
├── poetry.lock
└── pyproject.toml
```

---

## Pré-Requisitos

- **Python 3.8+**
- **[Poetry](https://python-poetry.org/)** instalado globalmente  
- (Opcional) **Jupyter Lab** para execução interativa dos notebooks, se desejado.

---

## Instalação e Configuração

1. **Clone o repositório:**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <nome_do_repositorio>
   ```

2. **Instale as dependências utilizando o Poetry:**

   ```bash
   poetry install
   ```

3. **(Opcional) Inicie o Jupyter Lab:**

   Para iniciar o Jupyter Lab utilizando o ambiente gerenciado pelo Poetry, execute:

   ```bash
   poetry run jupyter lab --ip='*' --NotebookApp.token='' --NotebookApp.password=''
   ```

   Abra o navegador e acesse a URL exibida (geralmente `http://localhost:8888`).

---

## Execução

### Utilizando o Solver CBC (cbc_mixed.py)

Este script resolve o problema de escalonamento utilizando o solver MILP do OR‑Tools (CBC).

Para executá-lo:

```bash
poetry run python cbc_mixed.py
```

O script exibirá:
- O makespan (tempo total do projeto).
- O total de horas contratadas.
- Para cada consultor: as tarefas atribuídas, horas efetivas de trabalho, horas ociosas e custo individual.
- O custo total do projeto.

### Validação por Força Bruta (bruteforce.py)

Este script realiza uma busca exaustiva para validar a solução ótima em instâncias pequenas.

Para executá-lo:

```bash
poetry run python bruteforce.py
```

Durante a execução, uma barra de progresso (usando a biblioteca **tqdm**) mostrará o andamento do processo.

---

## Metodologia e Considerações

- **Otimização com CBC:**  
  A abordagem baseada em MILP utiliza técnicas sofisticadas (branch-and-bound, relaxações e poda) que permitem encontrar a solução ótima sem precisar explorar todas as combinações possíveis.

- **Validação por Força Bruta:**  
  A busca exaustiva gera todas as possíveis atribuições de tarefas aos consultores e calcula o makespan para cada uma. Embora essa abordagem seja garantidamente precisa para pequenas instâncias, seu custo computacional cresce exponencialmente (se \(n\) é o número de tarefas e \(m\) o número de consultores, há \(m^n\) combinações). Isso a torna impraticável para problemas maiores, sendo útil apenas para testes e validação de instâncias reduzidas.

---

## Considerações Finais

- **Atualizações e Contribuições:**  
  Sinta-se à vontade para contribuir com melhorias ou adaptações ao modelo e aos scripts. Todas as sugestões são bem-vindas!

- **Documentação Adicional:**  
  Para mais detalhes sobre o OR‑Tools, consulte a [documentação oficial](https://developers.google.com/optimization). Para mais informações sobre o Poetry, visite a [documentação do Poetry](https://python-poetry.org/docs/).

- **Dúvidas e Suporte:**  
  Se encontrar problemas ou tiver dúvidas, abra uma issue neste repositório.

---
