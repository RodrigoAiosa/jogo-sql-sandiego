# 🚀 Guia de Deploy — SQL Detective no HuggingFace Spaces

## Estrutura de Arquivos

```
sql-detective/
├── app.py              ← App principal Streamlit
├── game_data.py        ← Dados do jogo (casos, pistas, locais)
├── requirements.txt    ← Dependências Python
├── README.md           ← Metadata do HuggingFace Space
└── .streamlit/
    └── config.toml     ← Configuração do Streamlit (porta 7860)
```

---

## Passo a Passo para Deploy

### 1. Criar conta no HuggingFace
Acesse https://huggingface.co e crie uma conta gratuita.

### 2. Criar um novo Space

- Vá em: https://huggingface.co/new-space
- Preencha:
  - **Space name:** `sql-detective`
  - **License:** MIT
  - **SDK:** Streamlit ← *importante!*
  - **Visibility:** Public (ou Private)
- Clique em **"Create Space"**

### 3. Fazer upload dos arquivos

**Opção A — Interface Web (mais simples):**
1. No seu Space recém-criado, clique em **"Files"**
2. Clique em **"Add file" → "Upload files"**
3. Faça upload de todos os arquivos:
   - `app.py`
   - `game_data.py`
   - `requirements.txt`
   - `README.md`
4. Crie a pasta `.streamlit/` e faça upload do `config.toml`

**Opção B — Git (recomendado):**
```bash
# Clone o Space criado
git clone https://huggingface.co/spaces/SEU_USER/sql-detective
cd sql-detective

# Copie os arquivos do projeto para esta pasta
cp /caminho/para/app.py .
cp /caminho/para/game_data.py .
cp /caminho/para/requirements.txt .
cp /caminho/para/README.md .
mkdir -p .streamlit
cp /caminho/para/config.toml .streamlit/

# Commit e push
git add .
git commit -m "Initial commit — SQL Detective"
git push
```

### 4. Aguardar o build

O HuggingFace irá automaticamente:
1. Instalar as dependências do `requirements.txt`
2. Iniciar o Streamlit na porta 7860
3. Disponibilizar a URL: `https://huggingface.co/spaces/SEU_USER/sql-detective`

O build leva cerca de **1-2 minutos**.

---

## Teste Local (antes do deploy)

```bash
# Instalar dependências
pip install streamlit

# Rodar localmente
streamlit run app.py

# Acesse: http://localhost:8501
```

---

## Solução de Problemas

| Problema | Solução |
|---|---|
| Build falha | Verifique se `requirements.txt` tem `streamlit==1.41.1` |
| App não carrega | Confirme que `config.toml` está em `.streamlit/config.toml` |
| Erro de importação | Verifique se `game_data.py` está na raiz do projeto |
| Porta errada | O HuggingFace usa porta 7860 — já configurado no `config.toml` |

---

## Expandir o Jogo

Para adicionar mais casos, edite `game_data.py` e adicione novos dicionários na lista `CASES`. Cada caso precisa de:

- `villain` — dados do criminoso
- `locations` — lista de localizações com `clues` e `travel_options`
- A última localização deve ter `"is_final": True`

Temas sugeridos para novos casos:
- **Caso 002:** Performance — o "Slow Query Bandit" que sabota índices
- **Caso 003:** Segurança — o "Permission Thief" que escala privilégios
- **Caso 004:** Alta Disponibilidade — o "Always Off" que derruba clusters
