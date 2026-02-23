"""
SQL Detective — Streamlit App
Onde no Mundo está o Hacker das Queries?
"""

import streamlit as st
from game_data import CASES

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Detective",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — estilo noir / Carmen Sandiego
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Special+Elite&family=Courier+Prime:wght@400;700&display=swap');

/* ---------- GLOBAL ---------- */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a0800 0%, #0d1a2e 100%) !important;
    color: #f5ead0;
    font-family: 'Courier Prime', monospace;
}

[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
[data-testid="block-container"] { padding-top: 1rem !important; }

/* ---------- HIDE STREAMLIT CHROME ---------- */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.8) !important;
    border-right: 1px solid rgba(184,134,11,0.3);
}

/* ---------- TITLE ---------- */
.game-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    color: #b8860b;
    text-align: center;
    text-shadow: 0 0 30px rgba(184,134,11,0.4);
    margin-bottom: 0;
    letter-spacing: 0.05em;
}
.game-subtitle {
    font-family: 'Special Elite', cursive;
    color: #666;
    text-align: center;
    font-size: 0.8rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ---------- HUD BAR ---------- */
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

/* ---------- LOCATION HEADER ---------- */
.loc-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}
.loc-icon { font-size: 2.8rem; }
.loc-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #f5ead0;
}
.loc-country { color: #888; font-size: 0.8rem; letter-spacing: 0.2em; text-transform: uppercase; }

/* ---------- SCENE BOX ---------- */
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

/* ---------- SECTION TITLE ---------- */
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

/* ---------- CLUE CARD ---------- */
.clue-card {
    background: rgba(245,234,208,0.05);
    border: 1px solid rgba(245,234,208,0.12);
    border-left: 3px solid #b8860b;
    border-radius: 2px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.5rem;
    transition: all 0.2s;
    cursor: pointer;
}
.clue-card.collected {
    border-left-color: #2d6a4f;
    background: rgba(45,106,79,0.08);
}
.clue-card-title { color: #b8860b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; }
.clue-card-text { color: #f5ead0; font-size: 0.9rem; margin-top: 0.2rem; }

/* ---------- SQL CODE BLOCK ---------- */
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

/* ---------- EXPLANATION BOX ---------- */
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

/* ---------- SUSPECT CARD ---------- */
.suspect-card {
    background: rgba(245,234,208,0.03);
    border: 1px solid rgba(245,234,208,0.1);
    border-radius: 4px;
    padding: 1rem;
    text-align: center;
}
.suspect-icon { font-size: 3.5rem; margin-bottom: 0.3rem; }
.suspect-name {
    font-family: 'Playfair Display', serif;
    color: #f5ead0;
    font-size: 1.1rem;
}
.suspect-alias { color: #c0392b; font-size: 0.8rem; letter-spacing: 0.15em; margin-bottom: 0.8rem; }
.suspect-row {
    display: flex;
    justify-content: space-between;
    padding: 0.3rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.82rem;
}
.suspect-label { color: #555; }
.suspect-value { color: #e8d5a3; }

/* ---------- TRAVEL BUTTONS ---------- */
.travel-btn-custom {
    width: 100%;
    background: rgba(26,58,92,0.25);
    border: 1px solid rgba(26,58,92,0.4);
    border-radius: 3px;
    padding: 0.7rem 1rem;
    color: #f5ead0;
    font-family: 'Courier Prime', monospace;
    font-size: 0.9rem;
    text-align: left;
    margin-bottom: 0.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    transition: all 0.2s;
}
.travel-btn-custom:hover {
    background: rgba(26,58,92,0.55);
    border-color: #1a3a5c;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    font-family: 'Special Elite', cursive !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    transition: all 0.2s !important;
}

/* ---------- PROGRESS ---------- */
.certainty-bar-outer {
    background: #111;
    height: 5px;
    border-radius: 3px;
    margin: 0.4rem 0 0.2rem 0;
    overflow: hidden;
}
.certainty-bar-inner {
    height: 100%;
    background: linear-gradient(to right, #b8860b, #c0392b);
    border-radius: 3px;
    transition: width 0.5s ease;
}
.certainty-label {
    font-size: 0.72rem;
    color: #555;
    display: flex;
    justify-content: space-between;
}

/* ---------- ALERT / TOAST-LIKE ---------- */
.stAlert { border-radius: 3px !important; }

/* ---------- EXPANDER ---------- */
[data-testid="stExpander"] {
    background: rgba(245,234,208,0.04) !important;
    border: 1px solid rgba(245,234,208,0.1) !important;
    border-left: 3px solid #b8860b !important;
    border-radius: 2px !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stExpander"] summary {
    color: #f5ead0 !important;
    font-family: 'Courier Prime', monospace !important;
}

/* ---------- METRIC ---------- */
[data-testid="metric-container"] {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(184,134,11,0.2);
    border-radius: 4px;
    padding: 0.5rem !important;
}
[data-testid="stMetricValue"] { color: #b8860b !important; font-family: 'Special Elite', cursive !important; }
[data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.75rem !important; }

/* ---------- TABS ---------- */
[data-testid="stTabs"] button {
    font-family: 'Courier Prime', monospace !important;
    color: #888 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #b8860b !important;
    border-bottom-color: #b8860b !important;
}

/* ---------- DIVIDER ---------- */
hr { border-color: rgba(184,134,11,0.2) !important; }

/* scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "intro",          # intro | game | win | lose
        "case_idx": 0,
        "location_id": "sp",
        "collected_clues": set(),
        "learned_facts": set(),
        "lives": 3,
        "score": 0,
        "locations_visited": 1,
        "wrong_travel": None,
        "show_clue": None,          # id of clue to show in expander
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
    case = current_case()
    for loc in case["locations"]:
        if loc["id"] == st.session_state.location_id:
            return loc
    return case["locations"][0]

def total_clues():
    return sum(len(loc["clues"]) for loc in current_case()["locations"])

def lives_display():
    n = st.session_state.lives
    return "❤️ " * n + "🖤 " * (3 - n)

def certainty_pct():
    facts = st.session_state.learned_facts
    return min(100, int(len(facts) / 4 * 100))

def collect_clue(clue_id, learns_fact, fact_value, points=150):
    if clue_id not in st.session_state.collected_clues:
        st.session_state.collected_clues.add(clue_id)
        st.session_state.score += points
        if learns_fact:
            st.session_state.learned_facts.add(learns_fact)
        return True
    return False

def villain_fact(field):
    v = current_case()["villain"]
    unlocked = st.session_state.learned_facts
    mapping = {
        "drink":  "drink",
        "accent": "accent",
        "hobby":  "hobby",
        "sign":   "sign",
    }
    if field in unlocked:
        return v[field]
    return "???"


# ─────────────────────────────────────────────
# SCREENS
# ─────────────────────────────────────────────

def render_intro():
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem;">
        <div style="font-family:'Special Elite',cursive; color:#666; font-size:0.8rem;
                    letter-spacing:0.4em; text-transform:uppercase; margin-bottom:1rem;">
            Divisão de Crimes Cibernéticos — Interpol SQL
        </div>
        <div style="font-family:'Playfair Display',serif; color:#b8860b; font-size:3rem;
                    text-shadow: 0 0 40px rgba(184,134,11,0.4); line-height:1.2; margin-bottom:0.5rem;">
            Onde no Mundo está o<br><em style="color:#c0392b">Hacker das Queries?</em>
        </div>
        <div style="font-size:5rem; margin: 2rem 0; filter: drop-shadow(0 0 20px rgba(192,57,43,0.5));">
            🕵️‍♀️
        </div>
        <div style="color:#777; font-size:1rem; max-width:500px; margin:0 auto 2rem auto;
                    font-style:italic; line-height:1.8;">
            O criminoso mais procurado do submundo digital roubou os dados de 42 bancos de dados
            ao redor do mundo usando técnicas avançadas de SQL Server.
            Siga as pistas, aprenda SQL e capture o culpado.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("▶  INICIAR INVESTIGAÇÃO", use_container_width=True, type="primary"):
            st.session_state.screen = "game"
            st.rerun()


def render_hud():
    loc = current_location()
    n_collected = len(st.session_state.collected_clues)
    n_total = total_clues()

    st.markdown(f"""
    <div class="hud-bar">
        <span class="hud-stat">🔍 SQL DETECTIVE</span>
        <span class="hud-stat">CASO: <span>{current_case()['id']}</span></span>
        <span class="hud-stat">PISTAS: <span>{n_collected}/{n_total}</span></span>
        <span class="hud-stat">LOCAIS: <span>{st.session_state.locations_visited}</span></span>
        <span class="hud-stat">PONTOS: <span>{st.session_state.score}</span></span>
        <span class="hud-lives">{lives_display()}</span>
    </div>
    """, unsafe_allow_html=True)


def render_game():
    render_hud()

    loc = current_location()
    villain = current_case()["villain"]

    # ── Layout: esquerda + direita ──
    left, right = st.columns([3, 1.3], gap="medium")

    # ────────────────────────────────
    # LEFT — Cena + Pistas + Viagem
    # ────────────────────────────────
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

        # Narrative
        st.markdown(f'<div class="scene-box">{loc["narrative"]}</div>', unsafe_allow_html=True)

        # ── CLUES ──
        st.markdown('<div class="section-title">📁 Pistas Disponíveis</div>', unsafe_allow_html=True)

        for clue in loc["clues"]:
            collected = clue["id"] in st.session_state.collected_clues
            badge = "✅ " if collected else "🔒 "
            label = f"{clue['icon']} {badge}{clue['title']}"

            with st.expander(label, expanded=False):
                st.markdown(f"*{clue['narrative']}*")

                # SQL block
                st.markdown(f'<div class="sql-block">{clue["sql"]}</div>', unsafe_allow_html=True)

                # Explanation
                st.markdown(f'<div class="explanation-box">{clue["explanation"]}</div>',
                            unsafe_allow_html=True)

                if not collected:
                    if st.button(f"🔍 Coletar esta pista", key=f"btn_clue_{clue['id']}"):
                        collect_clue(clue["id"], clue.get("learns_fact"), clue.get("fact_value"))
                        st.success(f"✅ Pista coletada! +150 pontos")
                        st.rerun()
                else:
                    st.success("✅ Pista já coletada.")

        # ── TRAVEL ──
        loc_clues_collected = sum(
            1 for c in loc["clues"] if c["id"] in st.session_state.collected_clues
        )
        all_clues_here = loc_clues_collected == len(loc["clues"])

        if not loc["is_final"]:
            st.markdown('<div class="section-title">✈️ Viajar para...</div>', unsafe_allow_html=True)

            if not all_clues_here:
                st.warning(f"⚠️ Colete todas as {len(loc['clues'])} pistas antes de viajar! ({loc_clues_collected}/{len(loc['clues'])})")
            else:
                for opt in loc["travel_options"]:
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.markdown(f"**{opt['flag']} {opt['name']}** — *{opt['hint']}*")
                    with col_b:
                        if st.button("✈️ Ir", key=f"travel_{opt['dest']}"):
                            if opt["correct"]:
                                st.session_state.score += 300
                                st.session_state.locations_visited += 1
                                st.session_state.location_id = opt["dest"]
                                st.session_state.wrong_travel = None
                                st.success(f"✈️ Viajando para {opt['name']}! +300 pontos")
                                st.rerun()
                            else:
                                st.session_state.lives -= 1
                                st.session_state.score = max(0, st.session_state.score - 200)
                                st.session_state.wrong_travel = opt["name"]
                                if st.session_state.lives <= 0:
                                    st.session_state.screen = "lose"
                                st.rerun()

                if st.session_state.wrong_travel:
                    st.error(f"❌ Pista falsa! {st.session_state.wrong_travel} não era o destino certo. Perdeu uma vida! -200 pontos")

        else:
            # Final location — ARREST
            st.markdown('<div class="section-title">⚖️ Mandado de Prisão</div>', unsafe_allow_html=True)

            if all_clues_here:
                st.success("🎯 Todas as evidências coletadas! Você pode efetuar a prisão.")
                if st.button("🚨  EFETUAR PRISÃO", type="primary", use_container_width=True):
                    bonus = st.session_state.lives * 500 + len(st.session_state.collected_clues) * 50 + 1000
                    st.session_state.score += bonus
                    st.session_state.screen = "win"
                    st.rerun()
            else:
                st.warning(f"Colete todas as {len(loc['clues'])} pistas desta localização para emitir o mandado. ({loc_clues_collected}/{len(loc['clues'])})")

    # ────────────────────────────────
    # RIGHT — Dossiê + Métricas
    # ────────────────────────────────
    with right:
        # Suspect dossier
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

        # Certainty bar
        pct = certainty_pct()
        st.markdown(f"""
        <div style="margin-top:0.8rem;">
            <div class="certainty-label">
                <span>Nível de Certeza</span>
                <span style="color:#b8860b">{pct}%</span>
            </div>
            <div class="certainty-bar-outer">
                <div class="certainty-bar-inner" style="width:{pct}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Metrics
        st.metric("🏆 Pontos", st.session_state.score)
        st.metric("📍 Locais", st.session_state.locations_visited)
        st.metric("🔍 Pistas", f"{len(st.session_state.collected_clues)}/{total_clues()}")

        st.divider()

        # Quick reference card
        st.markdown('<div class="section-title">📖 Referência SQL</div>', unsafe_allow_html=True)
        with st.expander("Comandos usados até agora"):
            commands = [
                ("sp_executesql", "Executa T-SQL parametrizado com segurança"),
                ("sys.dm_exec_requests", "DMV: mostra requisições ativas"),
                ("BACKUP ... COPY_ONLY", "Backup independente da cadeia"),
                ("sys.dm_exec_cached_plans", "DMV: planos de execução em cache"),
                ("sp_addlinkedserver", "Cria conexão com servidor remoto"),
                ("xp_cmdshell", "Executa SO — perigoso!"),
                ("WITH ... RECURSIVE", "CTE recursiva"),
                ("INNER JOIN", "Combina tabelas por coluna comum"),
            ]
            for cmd, desc in commands:
                st.markdown(f"`{cmd}` — {desc}")


def render_win():
    v = current_case()["villain"]
    st.markdown(f"""
    <div style="text-align:center; padding:4rem 2rem;">
        <div style="font-size:5rem; margin-bottom:1rem;">🏆</div>
        <div style="font-family:'Playfair Display',serif; font-size:2.5rem; color:#b8860b; margin-bottom:1rem;">
            CASO ENCERRADO!
        </div>
        <div style="color:#999; font-size:1rem; max-width:500px; margin:0 auto 1.5rem; line-height:1.8;">
            <strong style="color:#f5ead0">{v['name']}</strong> foi capturado em Berlim com base nas 
            evidências de SQL Server que você coletou. O banco de dados mundial está salvo por mais um dia, Agente.
        </div>
        <div style="font-family:'Special Elite',cursive; color:#b8860b; font-size:1.8rem; margin-bottom:2rem;">
            Pontuação Final: {st.session_state.score}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔄 NOVO CASO", use_container_width=True, type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_lose():
    st.markdown("""
    <div style="text-align:center; padding:4rem 2rem;">
        <div style="font-size:5rem; margin-bottom:1rem;">💀</div>
        <div style="font-family:'Playfair Display',serif; font-size:2.5rem; color:#c0392b; margin-bottom:1rem;">
            CASO FRIO
        </div>
        <div style="color:#999; font-size:1rem; max-width:500px; margin:0 auto 2rem; line-height:1.8;">
            O suspeito desapareceu nas profundezas da dark web. Você cometeu erros demais.
            Estude mais SQL Server e tente novamente.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔄 TENTAR NOVAMENTE", use_container_width=True, type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
def main():
    screen = st.session_state.screen

    if screen == "intro":
        render_intro()
    elif screen == "game":
        render_game()
    elif screen == "win":
        render_win()
    elif screen == "lose":
        render_lose()


main()
