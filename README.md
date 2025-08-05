# SaúdeLink: RAG clínico com dados fisiológicos e comportamentais

Este repositório contém o projeto **SaúdeLink**, uma aplicação de Recuperação Aumentada por Geração (RAG) voltada para dados clínicos e comportamentais. O objetivo é permitir consultas semânticas sobre a saúde de pacientes com base em dados fisiológicos coletados ao longo do tempo.

## Base de Dados

Utilizamos a base pública [Health Data](https://www.kaggle.com/datasets/whenamancodes/health-data) disponível no Kaggle, que contém registros diários de pacientes com os seguintes atributos:

- Medidas fisiológicas: altura, peso, batimentos cardíacos
- Dados comportamentais: passos, calorias
- Dados de sono: sono leve, profundo, REM, tempo acordado e total

## Etapas do Projeto

### 1. Preparação dos Dados
- Agrupamento dos registros por paciente em intervalos de 7 dias
- Geração de descrições textuais padronizadas com estatísticas por período
- Armazenamento dos documentos em formato estruturado (`CSV`)

### 2. Vetorização e Indexação
- Vetorização dos textos com o modelo `all-MiniLM-L6-v2` via `SentenceTransformers`
- Indexação dos vetores com `FAISS` para busca por similaridade
- Associação dos vetores a metadados clínicos e temporais

### 3. Pipeline RAG
- Implementação de uma pipeline de Recuperação Aumentada por Geração
- Consulta semântica por linguagem natural
- Recuperação dos documentos mais relevantes via FAISS
- Geração de respostas contextualizadas com LLM

### 4. Interface Interativa
- Interface web para interação com o sistema
- Entrada de perguntas clínicas e retorno de respostas explicativas
- Visualização dos documentos relacionados e histórico de consultas

## Objetivo

Demonstrar como técnicas modernas de NLP e IA podem ser aplicadas à análise de dados clínicos, oferecendo uma ferramenta inteligente para exploração semântica, explicação de padrões e suporte à tomada de decisão.
