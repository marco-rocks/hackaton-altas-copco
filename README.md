# Hackathon Desafio Maker

Projeto de análise de dados desenvolvido para o **Desafio Maker**, com foco na identificação de oportunidades comerciais e na avaliação da relação entre desempenho de vendas, perfil dos clientes e custos associados à frota de equipamentos.

## Sobre o projeto

O projeto tem como objetivo transformar dados comerciais e operacionais em informações úteis para apoiar a tomada de decisão.

A análise parte do histórico de cotações para identificar clientes e segmentos que apresentam alta taxa de conversão e baixo tempo de fechamento. Em seguida, os dados comerciais são integrados aos dados da frota para investigar se o bom desempenho de vendas também está associado a um mix de equipamentos economicamente favorável.

O desenvolvimento foi dividido em três etapas principais:

1. **Data Wrangling** — limpeza, tratamento e padronização dos dados;
2. **Análise de oportunidades** — identificação de clientes e segmentos com desempenho comercial acima da média;
3. **Análise de frota** — integração das bases e avaliação do impacto dos custos de manutenção sobre as oportunidades encontradas.

---

## Objetivos

- Preparar e validar os dados fornecidos para análise;
- Identificar inconsistências, valores ausentes e valores extremos;
- Calcular indicadores de desempenho comercial;
- Estabelecer benchmarks da operação;
- Identificar clientes e segmentos com alta conversão e fechamento rápido;
- Integrar informações comerciais aos dados da frota;
- Avaliar o impacto da manutenção no desempenho econômico dos equipamentos;
- Gerar recomendações baseadas nos dados analisados.

---

## Tecnologias utilizadas

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Seaborn**
- **Jupyter Notebook**

---

## Estrutura do projeto

```text
.
├── data/
│   └── db_atlas.xlsx
│
├── notebooks/
│   └── 01_analise_exploratoria.ipynb
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── src/
│   ├── ...
│
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
└── instrucoes_desafio.pdf
```

A estrutura separa a exploração dos dados da implementação principal:

- `data/`: base utilizada na análise;
- `notebooks/`: análise exploratória e validação das hipóteses;
- `src/`: módulos responsáveis pelas regras de processamento e análise;
- `outputs/`: gráficos e tabelas gerados pelo projeto;
- `main.py`: ponto de entrada e orquestração do pipeline;
- `requirements.txt`: dependências necessárias para execução.

---

## Metodologia

### 1. Data Wrangling

Inicialmente foi realizada uma análise da qualidade dos dados, buscando identificar problemas que poderiam comprometer os indicadores posteriores.

Entre os principais tratamentos realizados estão:

- conversão e padronização das colunas de data;
- recuperação de valores ausentes em `Days_To_Close` utilizando `Quote_Date` e `Close_Date`;
- padronização dos diferentes valores encontrados em `Stage`;
- investigação de valores anômalos em `Amount_BRL`;
- tratamento de valores extremos para determinadas análises estatísticas;
- preservação dos valores monetários originais para análises financeiras.

---

### 2. Benchmark da operação

Após a preparação dos dados, foram calculados indicadores gerais utilizados como referência para comparação dos diferentes perfis comerciais.

Os principais indicadores analisados foram:

- quantidade de propostas;
- Win Rate;
- tempo médio de fechamento.

O **Win Rate** representa a proporção de propostas ganhas em relação ao total de propostas:

```text
Win Rate = Propostas Ganhas / Total de Propostas × 100
```

A partir desses indicadores, clientes e segmentos puderam ser comparados com o comportamento geral da operação.

---

### 3. Identificação de oportunidades

A análise buscou encontrar perfis que combinassem:

- Win Rate superior à média;
- tempo de fechamento inferior à média;
- volume de propostas suficiente para sustentar a análise.

Foram realizadas análises tanto em nível de **segmento** quanto em nível de **cliente**, evitando selecionar oportunidades apenas por taxas elevadas obtidas em amostras muito pequenas.

---

### 4. Integração com os dados da frota

Para aprofundar a análise comercial, o histórico de cotações foi relacionado aos dados dos ativos através da coluna:

```text
Serial_ID
```

Essa integração permite associar cada proposta às características do equipamento correspondente, incluindo:

- modelo;
- tipo de solução;
- custo de aquisição;
- depreciação acumulada;
- custo de manutenção.

Com isso, tornou-se possível avaliar se clientes com excelente desempenho comercial também apresentam um mix de equipamentos operacionalmente favorável.

---

## Principais resultados

### Benchmark da operação

A base analisada apresentou:

| Indicador | Resultado |
|---|---:|
| Propostas analisadas | 6.000 |
| Win Rate geral | 45,45% |
| Tempo médio de fechamento | 24,95 dias |

### Oportunidades comerciais

A análise identificou dois perfis de destaque:

| Perfil | Propostas | Win Rate | Tempo médio |
|---|---:|---:|---:|
| Logistics | 788 | 82,11% | 2,05 dias |
| Senna Heavy Machining 614 | 10 | 90,00% | 3,70 dias |

O segmento **Logistics** representa a oportunidade comercial mais robusta devido à combinação de alta conversão, fechamento rápido e grande volume de propostas.

**Senna Heavy Machining 614** foi identificado como uma oportunidade individual relevante, embora baseado em uma amostra significativamente menor.

---

## Análise do mix de equipamentos

O cruzamento entre histórico comercial e frota permitiu encontrar informações de ativos para aproximadamente **71,5% das cotações**.

No caso de **Senna Heavy Machining 614**, a alta conversão permaneceu presente mesmo após o cruzamento das bases. Entretanto, a análise dos equipamentos revelou diferenças importantes no comportamento dos custos de manutenção.

| Modelo | Propostas | Win Rate | Valor das propostas ganhas | Manutenção acumulada | Manutenção / Valor |
|---|---:|---:|---:|---:|---:|
| MP4/4 | 6 | 100% | R$ 696,6 mil | R$ 1,38 mi | 199% |
| AMR23 | 1 | 100% | R$ 41,8 mil | R$ 7,8 mil | 19% |

O `MP4/4` apresenta excelente desempenho comercial, porém uma elevada relação entre manutenção acumulada e valor comercial observado.

O `AMR23` apresenta uma relação significativamente menor na amostra disponível, mas possui apenas uma observação. Portanto, o resultado deve ser interpretado como uma **hipótese para investigação e teste**, e não como evidência suficiente para uma substituição completa do mix.

---

## Recomendação

Com base nos resultados, a análise sugere:

- priorizar o segmento **Logistics** como oportunidade comercial de maior escala;
- acompanhar **Senna Heavy Machining 614** como oportunidade individual de alta conversão;
- investigar a elevada pressão de manutenção associada ao `MP4/4`;
- testar gradualmente uma maior participação do `AMR23` no mix do cliente;
- acompanhar novas observações antes de realizar alterações definitivas na estratégia comercial.

> **Alta conversão, isoladamente, não garante uma oportunidade economicamente sustentável. O mix de equipamentos também deve ser considerado na tomada de decisão.**

---

## Limitações da análise

Os resultados devem ser interpretados considerando algumas limitações da base:

- nem todas as cotações possuem correspondência com os dados da frota;
- o número de observações varia significativamente entre clientes e equipamentos;
- os custos de manutenção são acumulados e podem representar períodos diferentes dos valores comerciais analisados;
- a relação entre manutenção e valor das propostas é utilizada como uma **proxy comparativa**, não como cálculo de lucro ou prejuízo contábil;
- o número de observações do `AMR23` ainda é insuficiente para afirmar que ele representa definitivamente o mix ideal.

---

## Como executar

### Pré-requisitos

Certifique-se de possuir o **Python 3** instalado.

Clone o repositório:

```bash
git clone <url-do-repositorio>
```

Acesse o diretório:

```bash
cd <nome-do-repositorio>
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o projeto:

```bash
python main.py
```

---

## Notebook

A análise exploratória completa está disponível em:

```text
notebooks/01_analise_exploratoria.ipynb
```

O notebook documenta o processo de exploração, limpeza, validação das hipóteses e desenvolvimento das análises que posteriormente foram estruturadas nos módulos Python.

---

## Autor

**Marco T. Dueñas**

Projeto desenvolvido como parte do **Hackathon Desafio Maker**.
