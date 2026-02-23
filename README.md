---
title: SQL Detective
emoji: 🔍
colorFrom: yellow
colorTo: red
sdk: streamlit
sdk_version: 1.41.1
app_file: app.py
pinned: true
license: mit
short_description: Jogo estilo Carmen Sandiego com pistas de SQL Server
---

# 🔍 SQL Detective — Onde no Mundo está o Hacker das Queries?

Jogo interativo de investigação no estilo **Carmen Sandiego**, com pistas e enredo totalmente baseados em **SQL Server / T-SQL**.

## 🎮 Como Jogar

1. Investigue cada localização coletando as **3 pistas SQL**
2. Cada pista revela um conceito real de SQL Server com explicação técnica
3. Escolha o **destino correto** com base nas evidências (destino errado = perde vida ❤️)
4. Chegue ao destino final e **emita o mandado de prisão**

## 📚 Conceitos SQL Server Ensinados

- SQL Injection e parametrização com `sp_executesql`
- Dynamic Management Views (`sys.dm_exec_requests`, `sys.dm_exec_cached_plans`)
- Deadlocks e bloqueios
- `BACKUP DATABASE ... COPY_ONLY`
- Linked Servers (`sp_addlinkedserver`)
- `xp_cmdshell` e Triggers maliciosos
- CTEs Recursivas (`WITH ... UNION ALL`)
- `INNER JOIN` e cruzamento de dados

## 🗺️ Cidades do Caso 001

🇧🇷 São Paulo → 🇳🇱 Amsterdã → 🇩🇪 Berlim

## 🛠️ Stack

- **Python** + **Streamlit**
- Deploy no **HuggingFace Spaces**
