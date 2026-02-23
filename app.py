"""
SQL Detective — Streamlit App
Onde no Mundo está o Hacker das Queries?
"""

import random
import streamlit as st
from game_data import CASES, LEVEL_LABELS
from player_store import (
    player_exists, create_player, load_player,
    save_player, record_game_result, list_all_players, format_player_card,
)

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
