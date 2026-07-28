---
marp: true
theme: default
paginate: true
size: 16:9

style: |
  section {
    font-family: Helvetica, Arial, sans-serif;
    background: #ffffff;
    color: #111111;
    padding: 60px 72px;
  }

  h1 {
    font-size:1.2rem;
    font-weight: 700;
    color: #111111;
    margin-bottom: 28px;
  }

  h2 {
    font-size: 30px;
    color: #00658a;
  }

  strong {
    color: #00658a;
  }

  footer {
    font-size: 12px;
    color: #777777;
  }

  section::after {
    font-size: 12px;
    color: #999999;
  }

  .azul {
    color: #00658a;
  }

  .cinza {
    color: #666666;
  }

  .pequeno {
    font-size: 16px;
  }

  .nota {
    font-size: 14px;
    color: #666666;
  }

  .numero {
    font-size: 48px;
    font-weight: 700;
    color: #00658a;
    margin-bottom: 0;
  }

  .label {
    font-size: 17px;
    color: #555555;
    margin-top: 0;
  }

  .metricas {
    display: flex;
    justify-content: space-between;
    gap: 32px;
    margin-top: 50px;
  }

  .metrica {
    flex: 1;
  }

  .fluxo {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 70px;
  }

  .etapa {
    width: 27%;
  }

  .etapa-numero {
    font-size: 30px;
    font-weight: bold;
    color: #00658a;
  }

  .etapa-titulo {
    font-size: 25px;
    font-weight: bold;
    margin: 8px 0;
  }

  .seta {
    font-size: 32px;
    color: #aaaaaa;
  }

  .cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
    margin-top: 30px;
  }

  .card {
    border-top: 3px solid #00658a;
    padding: 18px 8px;
  }

  .card h3 {
    margin: 0 0 10px 0;
    font-size: 21px;
  }

  .card p {
    margin: 4px 0;
    font-size: 17px;
    color: #555555;
  }

  .duas-colunas {
    display: flex;
    gap: 70px;
    margin-top: 35px;
  }

  .coluna {
    flex: 1;
  }

  .oportunidade {
    border-top: 4px solid #00658a;
    padding-top: 18px;
  }

  .oportunidade h2 {
    margin-bottom: 22px;
  }

  .destaque {
    font-size: 27px;
    font-weight: bold;
    color: #00658a;
  }

  .alerta {
    color: #a23b3b;
    font-weight: bold;
  }

  .positivo {
    color: #28735a;
    font-weight: bold;
  }

  table {
    width: 100%;
    font-size: 17px;
    border-collapse: collapse;
  }

  th {
    background: #f2f4f5;
    color: #333333;
  }

  th, td {
    padding: 12px 15px;
    border: none;
    border-bottom: 1px solid #dddddd;
  }

  .conclusao {
    border-left: 5px solid #00658a;
    padding-left: 25px;
    margin-top: 40px;
    font-size: 24px;
  }

  .rodape-nota {
    position: absolute;
    bottom: 35px;
    left: 72px;
    right: 72px;
    font-size: 12px;
    color: #777777;
  }
---

<!-- _paginate: false -->

# Análise  <span class="azul">Comercial</span> e <span class="azul">Rentabilidade</span> da frota

### *Desafio Maker | Data Science*


<br>
<br>

Elaborado por  
**Marco T. Dueñas**

---

# Como a análise foi conduzida

<div class="fluxo">

<div class="etapa">

<div class="etapa-numero">01</div>

<div class="etapa-titulo">Data Wrangling</div>

Limpeza, padronização e tratamento dos dados.

</div>

<div class="seta">→</div>

<div class="etapa">

<div class="etapa-numero">02</div>

<div class="etapa-titulo">Oportunidades</div>

Win Rate, velocidade de fechamento e volume.

</div>

<div class="seta">→</div>

<div class="etapa">

<div class="etapa-numero">03</div>

<div class="etapa-titulo">Rentabilidade</div>

Integração com frota e análise do mix.

</div>

</div>

<div class="conclusao">
Objetivo: transformar dados comerciais em uma recomendação de negócio.
</div>

---

# 01. Preparação e qualidade dos dados

<div class="cards">

<div class="card">

### Days_To_Close

**318 valores ausentes**

Recuperados a partir da diferença entre `Close_Date` e `Quote_Date`.

</div>

<div class="card">

### Stage

**9 representações → 2 categorias**

Padronização dos resultados em `Ganho` e `Perdido`.

</div>

<div class="card">

### Datas

**Tipos inconsistentes**

Conversão e padronização para permitir operações temporais confiáveis.

</div>

<div class="card">

### Amount_BRL

**Valores extremos identificados**

Winsorização baseada em IQR para reduzir influência de extremos nas análises estatísticas.

</div>

</div>

<div class="rodape-nota">
Os valores monetários originais foram preservados separadamente para as análises financeiras.
</div>

---

# 02. Benchmark da operação

Para identificar uma oportunidade, primeiro foi necessário entender o comportamento médio da operação.

<div class="metricas">

<div class="metrica">

<div class="numero">6.000</div>

<div class="label">propostas analisadas</div>

</div>

<div class="metrica">

<div class="numero">45,45%</div>

<div class="label">Win Rate geral</div>

</div>

<div class="metrica">

<div class="numero">24,95</div>

<div class="label">dias para fechamento</div>

</div>

</div>

<div class="conclusao">
Buscamos perfis que combinassem <strong>maior conversão</strong> com <strong>fechamento mais rápido</strong>.
</div>

---

# Como foi definido o Win Rate?

O indicador representa a proporção de propostas que foram efetivamente ganhas.

<br>

Win Rate = **Propostas Ganhas / Total de Propostas × 100**

<br>

Na operação:

**2.727 propostas ganhas** em **6.000 propostas**

### <span class="azul">Win Rate = 45,45%</span>

Esse valor foi utilizado como uma das referências para identificar os perfis de oportunidade.

---

# 03. Duas oportunidades se destacaram

<div class="duas-colunas">

<div class="coluna oportunidade">

## LOGISTICS

<div class="numero">82,11%</div>
<div class="label">Win Rate</div>

<br>

**2,05 dias** de fechamento

**788 propostas**

<br>

Setor de maior escala e robustez.

</div>

<div class="coluna oportunidade">

## SENNA HEAVY MACHINING 614

<div class="numero">90,00%</div>
<div class="label">Win Rate</div>

<br>

**3,70 dias** de fechamento

**10 propostas**

<br>

Oportunidade individual promissora.

</div>

</div>

<div class="rodape-nota">
Benchmark: 45,45% de Win Rate e 24,95 dias de fechamento médio.
</div>

---

# Por que escolher o setor de Logistics?

<div class="duas-colunas">

<div class="coluna">

## Operação geral

<div class="numero">45,45%</div>
<div class="label">Win Rate</div>

<br>

<div class="numero">24,95</div>
<div class="label">dias</div>

</div>

<div class="coluna">

## Logistics

<div class="numero">82,11%</div>
<div class="label">Win Rate</div>

<br>

<div class="numero">2,05</div>
<div class="label">dias</div>

</div>

</div>

<div class="conclusao">

**788 propostas** tornam Logistics a oportunidade comercial mais robusta encontrada na análise.

</div>

---

# Por que Senna Heavy Machining 614?

A análise individual apresentou vários clientes com Win Rate elevado, porém com poucas observações.

<br>

Foi utilizado um **suporte mínimo exploratório de 10 propostas** para reduzir conclusões baseadas em amostras excessivamente pequenas.

<div class="metricas">

<div class="metrica">

<div class="numero">10</div>
<div class="label">propostas</div>

</div>

<div class="metrica">

<div class="numero">90%</div>
<div class="label">Win Rate</div>

</div>

<div class="metrica">

<div class="numero">3,70</div>
<div class="label">dias</div>

</div>

</div>

<div class="rodape-nota">
O limite de 10 propostas é um critério exploratório de suporte, não um limiar de significância estatística.
</div>

---

# 04. O Fator Multiplicador

## Alta conversão significa alta rentabilidade?

<br>

A Missão 2 mostrou que **Senna Heavy Machining 614** possui comportamento comercial excepcional.

Mas a análise comercial não responde uma segunda pergunta:

<div class="conclusao">

**Os equipamentos associados a essas vendas também apresentam um comportamento economicamente favorável?**

</div>

---

# Cruzando comercial e frota

<div class="fluxo">

<div class="etapa">

<div class="etapa-numero">HISTÓRICO</div>

<div class="etapa-titulo">Propostas</div>

Cliente  
Valor  
Stage

</div>

<div class="seta">→</div>

<div class="etapa">

<div class="etapa-numero">CHAVE</div>

<div class="etapa-titulo">Serial_ID</div>

Identificação do ativo associado à proposta.

</div>

<div class="seta">→</div>

<div class="etapa">

<div class="etapa-numero">FROTA</div>

<div class="etapa-titulo">Equipamento</div>

Modelo  
Solução  
Manutenção

</div>

</div>

<div class="metricas">

<div class="metrica">
<div class="numero">580</div>
<div class="label">ativos relacionados</div>
</div>

<div class="metrica">
<div class="numero">4.290</div>
<div class="label">cotações com dados de frota</div>
</div>

<div class="metrica">
<div class="numero">71,5%</div>
<div class="label">cobertura das cotações</div>
</div>

</div>

---

# Senna continua convertendo...

Mesmo considerando somente as propostas que possuem correspondência com os dados de frota:

<div class="metricas">

<div class="metrica">

<div class="numero">87,5%</div>
<div class="label">Win Rate</div>

</div>

<div class="metrica">

<div class="numero">8</div>
<div class="label">propostas com cobertura</div>

</div>

</div>

<div class="conclusao">

O problema encontrado **não está na capacidade de conversão do cliente**.

Está no comportamento dos equipamentos associados.

</div>

---

# ...mas o mix revela um problema

| Indicador | **MP4/4** | **AMR23** |
|---|---:|---:|
| Propostas | 6 | 1 |
| Win Rate | **100%** | **100%** |
| Valor das propostas ganhas | R$ 696,6 mil | R$ 41,8 mil |
| Manutenção acumulada | **R$ 1,38 mi** | R$ 7,8 mil |
| Manutenção / valor ganho | **199%** | **19%** |

<br>

<div class="conclusao">

O **MP4/4 converte**, mas apresenta uma pressão de manutenção significativamente maior dentro da amostra analisada.

</div>

---

# O que significa 199%?

### MP4/4

**R$ 1,38 mi** em manutenção acumulada

versus

**R$ 696,6 mil** em valor de propostas ganhas

<br>

<div class="destaque">

Manutenção / Valor Ganho ≈ 1,99

</div>

Ou seja, a manutenção acumulada corresponde a aproximadamente **199% do valor comercial ganho analisado**.

<div class="rodape-nota">
Essa relação é uma proxy comparativa. Não representa margem ou prejuízo contábil, pois manutenção acumulada e propostas podem possuir horizontes temporais diferentes.
</div>

---

# 05. Recomendação

<div class="cards">

<div class="card">

### 01 — Priorizar

**Logistics**

Oportunidade comercial mais robusta em escala, conversão e velocidade.

</div>

<div class="card">

### 02 — Monitorar

**Senna Heavy Machining 614**

Alta conversão, porém com possível pressão econômica relacionada ao mix.

</div>

<div class="card">

### 03 — Rebalancear

**MP4/4**

Reduzir gradualmente a concentração e acompanhar o impacto operacional.

</div>

<div class="card">

### 04 — Testar

**AMR23**

Aumentar experimentalmente sua participação e validar o comportamento com novas observações.

</div>

</div>

---

# Conclusão

<br>

Conversão é apenas <span class="azul">**uma parte**</span> da oportunidade.

<br>

A análise identificou **Logistics** como a oportunidade comercial mais robusta e **Senna Heavy Machining 614** como uma oportunidade individual de alta conversão.

O cruzamento com a frota, entretanto, revelou que o desempenho comercial pode esconder **pressão relevante de manutenção**.

<div class="conclusao">

A decisão comercial deve considerar não apenas **quem compra**, mas também **qual equipamento está sendo colocado nesse cliente**.

</div>

---

<!-- _paginate: false -->

# OBRIGADO

### Marco T. Dueñas

<br><br>

**Desafio Maker | Data Science**