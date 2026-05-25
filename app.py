"""
QUANT MEMORIA — v2.0 FINAL
============================
Plataforma integrada de aprendizaje cuantitativo para el programa BCRP.
Conecta master_cards.py + SRS engine + 5 modos de pregunta + gráficos.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import random
import json
import math
from datetime import datetime
from pathlib import Path

from core.srs_engine import SRSEngine, Rating, CardState
from core.store import CardStore
from content.master_cards import get_all_cards, get_bus_cards, get_cards_by_domain
from utils.analytics import AnalyticsEngine

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quant Memoria",
    page_icon="∂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Space+Grotesk:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    background-color: #0a0e17 !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stApp { background-color: #0a0e17 !important; }
section[data-testid="stSidebar"] {
    background: #0d1321 !important;
    border-right: 1px solid #1e293b;
}
div[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 16px;
}
.stButton > button {
    background: #1a2235 !important;
    color: #00ff88 !important;
    border: 1px solid #00ff88 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #00ff88 !important;
    color: #0a0e17 !important;
}
.stButton > button[kind="primary"] {
    background: #00ff88 !important;
    color: #0a0e17 !important;
    font-weight: 700 !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #1a2235 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
}
.stRadio > div { background: transparent !important; }
.stTabs [data-baseweb="tab"] {
    background: #111827 !important;
    color: #64748b !important;
    border-radius: 8px 8px 0 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #00ff88 !important;
    border-bottom: 2px solid #00ff88 !important;
}
code, pre { background: #0d1321 !important; color: #00ff88 !important; }
hr { border-color: #1e293b !important; }
.card-box {
    background: #111827;
    border: 1px solid #1e293b;
    border-left: 4px solid #00ff88;
    border-radius: 12px;
    padding: 24px 28px;
    margin: 12px 0;
    font-size: 15px;
    line-height: 1.75;
}
.card-answer {
    border-left-color: #3b82f6;
    background: #1a2235;
}
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    margin: 2px;
    border: 1px solid #1e293b;
}
.title-main {
    font-family: 'JetBrains Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    color: #00ff88;
    letter-spacing: -1px;
}
.title-sub {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 24px;
}
.mcq-option {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
    cursor: pointer;
    font-size: 14px;
}
.mcq-correct { border-color: #00ff88 !important; background: #0a2a1a !important; }
.mcq-wrong   { border-color: #ef4444 !important; background: #2a0a0a !important; }
.progress-bar-bg {
    background: #1e293b; border-radius: 8px; height: 6px; margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────
def init():
    defs = {
        "page": "Dashboard",
        "queue": [], "q_idx": 0,
        "revealed": False,
        "mode": "bus",
        "q_domain": "All",
        "q_type": "Flashcard",
        "mcq_answered": None,
        "tf_answered": None,
        "fill_submitted": False,
        "fill_input": "",
        "session_total": 0,
        "session_correct": 0,
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

store     = CardStore()
engine    = SRSEngine()
analytics = AnalyticsEngine()
ALL_CARDS = get_all_cards()

DOMAINS = ["All"] + sorted(list({c["domain"] for c in ALL_CARDS}))


# ═══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 20px 0;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:20px;
                  font-weight:700;color:#00ff88;">∂ QUANT MEMORIA</div>
      <div style="font-size:11px;color:#64748b;margin-top:2px;">BCRP · Financial Engineering</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "📊 Dashboard":    "Dashboard",
        "🚌 Modo Bus":     "Bus",
        "🏠 Modo Casa":    "Home",
        "📚 Biblioteca":   "Library",
        "📈 Analytics":    "Analytics",
        "➕ Nueva Carta":  "AddCard",
    }
    for label, key in pages.items():
        is_active = st.session_state.page == key
        if st.button(label, use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.page = key
            st.session_state.queue = []
            st.session_state.q_idx = 0
            st.session_state.revealed = False
            st.rerun()

    st.divider()

    # Quick stats
    states = store.all_states()
    due_count = len([c for c in ALL_CARDS
                     if engine.is_due(states.get(c["id"], CardState(card_id=c["id"])))])
    streak = store.streak_days()

    st.markdown(f"""
    <div style="text-align:center;padding:6px 0;">
      <div style="font-size:28px;color:#00ff88;font-family:'JetBrains Mono',monospace;
                  font-weight:700;">{due_count}</div>
      <div style="font-size:11px;color:#64748b;">para revisar hoy</div>
    </div>
    <div style="text-align:center;padding:6px 0;">
      <div style="font-size:24px;color:#f59e0b;font-family:'JetBrains Mono',monospace;">
        🔥 {streak}</div>
      <div style="font-size:11px;color:#64748b;">días seguidos</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def mastery_color(pct):
    if pct < 33:  return "#ef4444"
    if pct < 66:  return "#f59e0b"
    return "#00ff88"

def render_tags(card):
    domain_colors = {
        "Financial Engineering":  "#3b82f6",
        "Interest Rate Models":   "#8b5cf6",
        "Financial Econometrics": "#f59e0b",
        "Portfolio Management":   "#00ff88",
        "Financial Stability":    "#ef4444",
    }
    c = domain_colors.get(card.get("domain",""), "#64748b")
    diff_c = {"Foundational":"#00ff88","Intermediate":"#3b82f6",
               "Advanced":"#f59e0b","Expert":"#ef4444"}.get(card.get("difficulty",""),"#64748b")
    tags_html = (
        f'<span class="badge" style="color:{c};">{card.get("domain","")}</span>'
        f'<span class="badge" style="color:#94a3b8;">{card.get("topic","")}</span>'
        f'<span class="badge" style="color:{diff_c};">{card.get("difficulty","")}</span>'
    )
    if "bus" in card.get("mode_tags",[]) and "home" in card.get("mode_tags",[]):
        tags_html += '<span class="badge" style="color:#06b6d4;">🚌🏠 ambos</span>'
    elif "bus" in card.get("mode_tags",[]):
        tags_html += '<span class="badge" style="color:#06b6d4;">🚌 bus</span>'
    else:
        tags_html += '<span class="badge" style="color:#a78bfa;">🏠 casa</span>'
    st.markdown(tags_html, unsafe_allow_html=True)


def render_graph(card):
    """Render interactive Plotly graphs based on graph_type field."""
    gtype = card.get("graph_type","")
    if not gtype:
        return

    try:
        import plotly.graph_objects as go
        import numpy as np

        LAYOUT = dict(
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(color="#94a3b8", size=11),
            margin=dict(l=10,r=10,t=30,b=10),
            height=320,
            xaxis=dict(gridcolor="#1e293b", zeroline=False),
            yaxis=dict(gridcolor="#1e293b", zeroline=False),
        )

        if gtype == "brownian_paths":
            np.random.seed(7)
            T, N = 1, 500
            dt = T/N
            t  = np.linspace(0, T, N+1)
            fig = go.Figure()
            colors = ["#00ff88","#3b82f6","#f59e0b","#ef4444","#8b5cf6"]
            for i,col in enumerate(colors):
                W = np.cumsum(np.insert(np.random.normal(0,math.sqrt(dt),N),0,0))
                fig.add_trace(go.Scatter(x=t,y=W,mode="lines",
                    line=dict(color=col,width=1.5),name=f"Path {i+1}",showlegend=False))
            fig.update_layout(**LAYOUT, title="Trayectorias del Movimiento Browniano")
            fig.update_xaxes(title="Tiempo t")
            fig.update_yaxes(title="W(t)")
            st.plotly_chart(fig, use_container_width=True)

        elif gtype == "vasicek_simulation":
            np.random.seed(42)
            kappa,theta,sigma,r0,T,N = 0.5,0.05,0.015,0.03,10,500
            dt = T/N
            t  = np.linspace(0,T,N+1)
            fig = go.Figure()
            colors = ["#00ff88","#3b82f6","#f59e0b","#ef4444","#8b5cf6"]
            for i,col in enumerate(colors):
                r = np.zeros(N+1); r[0] = r0
                for s in range(1,N+1):
                    r[s] = r[s-1]+kappa*(theta-r[s-1])*dt+sigma*np.random.normal(0,math.sqrt(dt))
                fig.add_trace(go.Scatter(x=t,y=r*100,mode="lines",
                    line=dict(color=col,width=1.5),name=f"Path {i+1}"))
            fig.add_hline(y=theta*100,line_dash="dash",line_color="#ffffff",
                         annotation_text=f"θ={theta*100:.0f}%",annotation_font_color="#ffffff")
            fig.update_layout(**LAYOUT, title="Vasicek: Reversión a la Media")
            fig.update_xaxes(title="Años")
            fig.update_yaxes(title="Tasa corta (%)")
            st.plotly_chart(fig, use_container_width=True)

        elif gtype == "cir_vs_vasicek":
            np.random.seed(1)
            kappa,theta,sigma,r0,T,N = 0.5,0.05,0.08,0.03,10,500
            dt = T/N; t = np.linspace(0,T,N+1)
            # Vasicek
            rv = np.zeros(N+1); rv[0]=r0
            rc = np.zeros(N+1); rc[0]=r0
            for s in range(1,N+1):
                dW = np.random.normal(0,math.sqrt(dt))
                rv[s] = rv[s-1]+kappa*(theta-rv[s-1])*dt+sigma*dW
                rc[s] = max(rc[s-1]+kappa*(theta-rc[s-1])*dt+sigma*math.sqrt(max(rc[s-1],0))*dW,0)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t,y=rv*100,name="Vasicek (puede ser <0)",
                line=dict(color="#ef4444",width=2)))
            fig.add_trace(go.Scatter(x=t,y=rc*100,name="CIR (≥0 siempre)",
                line=dict(color="#00ff88",width=2)))
            fig.add_hline(y=0,line_dash="dot",line_color="#64748b")
            fig.update_layout(**LAYOUT, title="CIR vs Vasicek: Tasas Negativas")
            fig.update_xaxes(title="Años"); fig.update_yaxes(title="Tasa (%)")
            st.plotly_chart(fig, use_container_width=True)

        elif gtype == "garch_volatility":
            np.random.seed(99)
            T2 = 800
            omega,alpha,beta_g = 0.00001,0.09,0.90
            eps = np.zeros(T2); sig2 = np.zeros(T2)
            sig2[0] = omega/(1-alpha-beta_g)
            for s in range(1,T2):
                eps[s] = np.random.normal(0,math.sqrt(sig2[s-1]))
                sig2[s] = omega+alpha*eps[s-1]**2+beta_g*sig2[s-1]
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=eps*100,name="Retornos %",
                line=dict(color="#3b82f6",width=1),opacity=0.5))
            fig.add_trace(go.Scatter(y=np.sqrt(sig2)*100*math.sqrt(252),
                name="Vol anualizada %",line=dict(color="#f59e0b",width=2)))
            fig.update_layout(**LAYOUT, title="GARCH(1,1): Clustering de Volatilidad")
            fig.update_yaxes(title="% ")
            st.plotly_chart(fig, use_container_width=True)

        elif gtype == "sabr_smile":
            K_range = np.linspace(0.01, 0.10, 60)
            F0, T2, alpha_s, beta_s, rho_s, nu = 0.05, 1.0, 0.20, 0.5, -0.30, 0.40
            # Simplified SABR Hagan approximation
            vols = []
            for K in K_range:
                if abs(F0-K) < 1e-6:
                    vol = alpha_s / (F0**(1-beta_s)) * (1 + ((1-beta_s)**2/24*alpha_s**2/F0**(2-2*beta_s)
                          + rho_s*beta_s*nu*alpha_s/(4*F0**(1-beta_s)) + (2-3*rho_s**2)/24*nu**2)*T2)
                else:
                    FK = F0*K
                    z  = nu/alpha_s * FK**((1-beta_s)/2) * math.log(F0/K)
                    xz = math.log((math.sqrt(1-2*rho_s*z+z**2)+z-rho_s)/(1-rho_s))
                    num = alpha_s * (z/xz if abs(xz)>1e-8 else 1.0)
                    den = FK**((1-beta_s)/2) * (1 + (1-beta_s)**2/24*math.log(F0/K)**2
                          + (1-beta_s)**4/1920*math.log(F0/K)**4)
                    vol = num/den * (1 + ((1-beta_s)**2/24*alpha_s**2/FK**(1-beta_s)
                          + rho_s*beta_s*nu*alpha_s/(4*FK**((1-beta_s)/2))
                          + (2-3*rho_s**2)/24*nu**2)*T2)
                vols.append(max(vol*100, 0))
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=K_range*100,y=vols,mode="lines",
                line=dict(color="#00ff88",width=2.5),name="SABR vol implícita"))
            fig.add_vline(x=F0*100,line_dash="dash",line_color="#f59e0b",
                         annotation_text="ATM",annotation_font_color="#f59e0b")
            fig.update_layout(**LAYOUT, title="SABR: Sonrisa de Volatilidad Implícita")
            fig.update_xaxes(title="Strike K (%)")
            fig.update_yaxes(title="Vol Implícita (%)")
            st.plotly_chart(fig, use_container_width=True)

        elif gtype == "efficient_frontier":
            np.random.seed(5)
            n_assets = 5
            mu_a = np.array([0.08,0.12,0.15,0.07,0.10])
            cov  = np.array([
                [0.04,0.012,0.008,0.005,0.010],
                [0.012,0.09,0.020,0.008,0.015],
                [0.008,0.020,0.16,0.010,0.018],
                [0.005,0.008,0.010,0.03,0.006],
                [0.010,0.015,0.018,0.006,0.06],
            ])
            # Monte Carlo portfolios
            n_port = 3000
            rets,vols = [],[]
            for _ in range(n_port):
                w = np.random.dirichlet(np.ones(n_assets))
                rets.append(w@mu_a)
                vols.append(math.sqrt(w@cov@w))
            fig = go.Figure()
            sharpes = [r/v for r,v in zip(rets,vols)]
            fig.add_trace(go.Scatter(x=[v*100 for v in vols],y=[r*100 for r in rets],
                mode="markers",marker=dict(color=sharpes,colorscale="Viridis",size=3,
                opacity=0.6,colorbar=dict(title="Sharpe")),name="Portafolios"))
            fig.update_layout(**LAYOUT, title="Frontera Eficiente de Markowitz")
            fig.update_xaxes(title="Volatilidad (%)"); fig.update_yaxes(title="Retorno esperado (%)")
            st.plotly_chart(fig, use_container_width=True)

        elif gtype == "ito_lognormal":
            np.random.seed(3)
            mu_d,sigma_d,S0,T3,N3 = 0.10,0.20,100,1,252
            dt3 = T3/N3
            t3  = np.linspace(0,T3,N3+1)
            fig = go.Figure()
            colors2 = ["#00ff88","#3b82f6","#f59e0b","#ef4444","#8b5cf6"]
            for i,col in enumerate(colors2):
                S = np.zeros(N3+1); S[0]=S0
                for s in range(1,N3+1):
                    S[s]=S[s-1]*math.exp((mu_d-0.5*sigma_d**2)*dt3+sigma_d*math.sqrt(dt3)*np.random.normal())
                fig.add_trace(go.Scatter(x=t3,y=S,mode="lines",
                    line=dict(color=col,width=1.5),name=f"S path {i+1}",showlegend=False))
            # Theoretical mean
            S_mean = [S0*math.exp(mu_d*tt) for tt in t3]
            fig.add_trace(go.Scatter(x=t3,y=S_mean,mode="lines",
                line=dict(color="#ffffff",width=2,dash="dash"),name="E[S_t]=S₀e^{μt}"))
            fig.update_layout(**LAYOUT, title="GBM: d(ln S) = (μ-σ²/2)dt + σdW (Itô)")
            fig.update_xaxes(title="Tiempo"); fig.update_yaxes(title="Precio S_t")
            st.plotly_chart(fig, use_container_width=True)

    except ImportError:
        st.info("Instala plotly para ver gráficos interactivos.")
    except Exception as e:
        st.caption(f"Gráfico no disponible: {e}")


def render_question_modes(card, state):
    """Render the appropriate question type based on session mode."""
    qtype = st.session_state.q_type

    # ── FLASHCARD ────────────────────────────────────────────────────
    if qtype == "Flashcard":
        st.markdown(f'<div class="card-box">{card["front"]}</div>', unsafe_allow_html=True)
        if card.get("latex"):
            st.latex(card["latex"])

        if not st.session_state.revealed:
            if st.button("👁 Ver Respuesta", type="primary", use_container_width=True):
                st.session_state.revealed = True
                st.rerun()
        else:
            st.markdown(f'<div class="card-box card-answer">{card["back"]}</div>',
                       unsafe_allow_html=True)
            if card.get("latex"):
                st.latex(card["latex"])
            render_graph(card)
            _render_tabs(card)
            _render_rating_buttons(card, state)

    # ── MULTIPLE CHOICE ──────────────────────────────────────────────
    elif qtype == "MCQ":
        mcq = card.get("mcq")
        if not mcq:
            st.info("Esta carta no tiene MCQ. Cargando flashcard...")
            st.session_state.q_type = "Flashcard"
            st.rerun()
        st.markdown(f'<div class="card-box">{mcq["question"]}</div>', unsafe_allow_html=True)
        if card.get("latex"):
            st.latex(card["latex"])
        render_graph(card)

        if st.session_state.mcq_answered is None:
            for opt in mcq["options"]:
                letter = opt[0]
                if st.button(opt, use_container_width=True, key=f"mcq_{letter}"):
                    st.session_state.mcq_answered = letter
                    if letter == mcq["answer"]:
                        st.session_state.session_correct += 1
                    st.rerun()
        else:
            chosen = st.session_state.mcq_answered
            correct = mcq["answer"]
            for opt in mcq["options"]:
                letter = opt[0]
                if letter == correct:
                    st.markdown(f'<div class="mcq-option mcq-correct">✅ {opt}</div>',
                               unsafe_allow_html=True)
                elif letter == chosen and chosen != correct:
                    st.markdown(f'<div class="mcq-option mcq-wrong">❌ {opt}</div>',
                               unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="mcq-option">{opt}</div>', unsafe_allow_html=True)

            result_ok = (chosen == correct)
            if result_ok:
                st.success(f"✅ Correcto! — {mcq['explanation']}")
            else:
                st.error(f"❌ Incorrecto. Respuesta: **{correct}** — {mcq['explanation']}")

            _render_next_button(card, state, correct=result_ok)

    # ── TRUE / FALSE ─────────────────────────────────────────────────
    elif qtype == "True/False":
        tf = card.get("true_false")
        if not tf:
            st.session_state.q_type = "Flashcard"; st.rerun()

        st.markdown(f'<div class="card-box">{tf["statement"]}</div>', unsafe_allow_html=True)
        render_graph(card)

        if st.session_state.tf_answered is None:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ VERDADERO", use_container_width=True, type="primary"):
                    st.session_state.tf_answered = True
                    if True == tf["answer"]: st.session_state.session_correct += 1
                    st.rerun()
            with c2:
                if st.button("❌ FALSO", use_container_width=True):
                    st.session_state.tf_answered = False
                    if False == tf["answer"]: st.session_state.session_correct += 1
                    st.rerun()
        else:
            answered = st.session_state.tf_answered
            correct  = tf["answer"]
            result_ok = (answered == correct)
            label = "VERDADERO" if correct else "FALSO"
            if result_ok:
                st.success(f"✅ Correcto — La afirmación es **{label}**")
            else:
                st.error(f"❌ Incorrecto — La afirmación es **{label}**")
            st.info(f"💡 {tf['explanation']}")
            _render_next_button(card, state, correct=result_ok)

    # ── FILL IN THE BLANK ────────────────────────────────────────────
    elif qtype == "Fill-in-blank":
        fb = card.get("fill_blank")
        if not fb:
            st.session_state.q_type = "Flashcard"; st.rerun()

        st.markdown(f'<div class="card-box">{card["front"]}</div>', unsafe_allow_html=True)
        st.markdown(f"**Completa:** `{fb['template']}`")

        if not st.session_state.fill_submitted:
            user_input = st.text_input("Tu respuesta:", key="fill_input_field",
                                       placeholder="Escribe aquí...")
            if st.button("✔ Verificar", type="primary", use_container_width=True):
                st.session_state.fill_submitted = True
                st.session_state.fill_input = user_input
                answers = [a.lower().strip() for a in fb["answers"]]
                if any(a in user_input.lower() for a in answers):
                    st.session_state.session_correct += 1
                st.rerun()
        else:
            answers = fb["answers"]
            user    = st.session_state.fill_input
            ok = any(a.lower() in user.lower() for a in answers)
            if ok:
                st.success(f"✅ Correcto! Respuesta: **{' / '.join(answers)}**")
            else:
                st.error(f"❌ Respuestas esperadas: **{' / '.join(answers)}**")
                st.caption(f"Tu respuesta: {user}")
            _render_next_button(card, state, correct=ok)

    # ── INTERPRETAR GRÁFICO ──────────────────────────────────────────
    elif qtype == "Gráfico":
        if not card.get("graph_type"):
            st.session_state.q_type = "Flashcard"; st.rerun()

        st.markdown("**Observa el gráfico y responde:**")
        render_graph(card)
        st.markdown(f'<div class="card-box">{card["front"]}</div>', unsafe_allow_html=True)

        if not st.session_state.revealed:
            if st.button("👁 Ver Explicación", type="primary", use_container_width=True):
                st.session_state.revealed = True
                st.rerun()
        else:
            st.markdown(f'<div class="card-box card-answer">{card["back"]}</div>',
                       unsafe_allow_html=True)
            _render_rating_buttons(card, state)


def _render_tabs(card):
    """Render detail tabs (Intuition / Derivation / Code / Connections)."""
    has = lambda k: bool(card.get(k,"").strip()) if isinstance(card.get(k), str) else bool(card.get(k))
    labels = []
    if has("intuition"):    labels.append("💡 Intuición")
    if has("derivation"):   labels.append("🔢 Derivación")
    if has("code_python"):  labels.append("🐍 Python")
    if has("code_matlab"):  labels.append("📐 MATLAB")
    if card.get("connections"): labels.append("🔗 Conexiones")
    if card.get("exam_question"): labels.append("📝 Examen")

    if not labels:
        return
    tabs = st.tabs(labels)
    idx = 0
    if has("intuition"):
        with tabs[idx]: st.markdown(card["intuition"])
        idx+=1
    if has("derivation"):
        with tabs[idx]: st.markdown(card["derivation"])
        idx+=1
    if has("code_python"):
        with tabs[idx]: st.code(card["code_python"], language="python")
        idx+=1
    if has("code_matlab"):
        with tabs[idx]: st.code(card["code_matlab"], language="matlab")
        idx+=1
    if card.get("connections"):
        with tabs[idx]:
            for conn in card["connections"]:
                st.markdown(f"→ **{conn}**")
        idx+=1
    if card.get("exam_question"):
        with tabs[idx]:
            st.markdown("**Pregunta de examen:**")
            st.markdown(card["exam_question"])


def _advance():
    """Move to next card, resetting all answer state."""
    st.session_state.q_idx      += 1
    st.session_state.revealed    = False
    st.session_state.mcq_answered = None
    st.session_state.tf_answered  = None
    st.session_state.fill_submitted = False
    st.session_state.fill_input  = ""


def _render_rating_buttons(card, state):
    """SM-2 rating buttons — only shown for flashcard/graph modes."""
    st.divider()
    st.markdown("**¿Qué tan bien lo recordaste?**")
    cols = st.columns(6)
    ratings = [
        (0,"⬛ Nada","#ef4444"),(1,"🔴 Mal","#f97316"),
        (2,"🟡 Difícil","#f59e0b"),(3,"🟢 Bien","#22c55e"),
        (4,"💙 Fácil","#3b82f6"),(5,"⚡ Perfecto","#00ff88"),
    ]
    for col,(score,label,_) in zip(cols,ratings):
        with col:
            if st.button(label, use_container_width=True, key=f"rate_{score}_{card['id']}"):
                new_state = engine.update(state, Rating(score))
                store.save_state(new_state)
                store.log_review(card["id"], score, card.get("domain",""), card.get("topic",""))
                st.session_state.session_total += 1
                if score >= 3: st.session_state.session_correct += 1
                _advance()
                st.rerun()


def _render_next_button(card, state, correct: bool):
    """Next button for auto-rated question types (MCQ, T/F, Fill)."""
    st.divider()
    if st.button("→ Siguiente carta", type="primary", use_container_width=True):
        rating = Rating.EASY if correct else Rating.WRONG
        new_state = engine.update(state, rating)
        store.save_state(new_state)
        store.log_review(card["id"], int(rating), card.get("domain",""), card.get("topic",""))
        st.session_state.session_total += 1
        _advance()
        st.rerun()


def build_queue(domain_filter, mode_filter, question_type):
    """Build and shuffle study queue based on filters."""
    cards = ALL_CARDS
    if domain_filter != "All":
        cards = [c for c in cards if c["domain"] == domain_filter]
    if mode_filter == "🚌 Bus":
        cards = [c for c in cards if "bus" in c.get("mode_tags",[])]
    if question_type in ("MCQ","True/False","Fill-in-blank"):
        key = {"MCQ":"mcq","True/False":"true_false","Fill-in-blank":"fill_blank"}[question_type]
        cards = [c for c in cards if c.get(key)]
    elif question_type == "Gráfico":
        cards = [c for c in cards if c.get("graph_type")]

    # Prioritize due cards
    states = store.all_states()
    due   = [c for c in cards if engine.is_due(states.get(c["id"], CardState(card_id=c["id"])))]
    other = [c for c in cards if c not in due]
    random.shuffle(due); random.shuffle(other)
    return due + other


def render_study_session(mode_label):
    """Core study session renderer — used by both Bus and Home pages."""
    is_bus = (mode_label == "Bus")

    st.markdown(
        f'<div class="title-main">{"🚌 MODO BUS" if is_bus else "🏠 MODO CASA"}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="title-sub">{"Estudio ligero — sin papel ni lápiz necesario" if is_bus else "Estudio profundo — derivaciones, código, preguntas de examen"}</div>',
        unsafe_allow_html=True
    )

    # ── Controls ─────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1.5,1.5,1])
    with col1:
        domain = st.selectbox("Dominio", DOMAINS, key=f"dom_{mode_label}")
    with col2:
        if is_bus:
            q_types = ["Flashcard","MCQ","True/False","Fill-in-blank","Gráfico"]
        else:
            q_types = ["Flashcard","MCQ","True/False","Fill-in-blank","Gráfico"]
        q_type = st.selectbox("Tipo de pregunta", q_types, key=f"qt_{mode_label}")
        st.session_state.q_type = q_type
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶ Cargar sesión", type="primary", use_container_width=True,
                     key=f"load_{mode_label}"):
            queue = build_queue(domain, "🚌 Bus" if is_bus else "All", q_type)
            st.session_state.queue    = queue
            st.session_state.q_idx    = 0
            st.session_state.revealed = False
            st.session_state.mcq_answered  = None
            st.session_state.tf_answered   = None
            st.session_state.fill_submitted = False
            st.session_state.session_total  = 0
            st.session_state.session_correct = 0
            if not queue:
                st.warning("No hay cartas con ese filtro. Prueba 'All'.")
            st.rerun()

    queue = st.session_state.queue
    idx   = st.session_state.q_idx

    if not queue:
        st.markdown("""
        <div style="background:#111827;border:1px solid #1e293b;border-radius:16px;
                    padding:48px;text-align:center;margin-top:24px;">
          <div style="font-size:40px;margin-bottom:12px;">📚</div>
          <div style="color:#00ff88;font-size:18px;font-weight:600;">Configura y carga una sesión</div>
          <div style="color:#64748b;font-size:13px;margin-top:8px;">
            Elige dominio y tipo de pregunta, luego presiona ▶ Cargar sesión
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    if idx >= len(queue):
        # Session complete
        total   = st.session_state.session_total
        correct = st.session_state.session_correct
        pct     = int(correct/max(total,1)*100)
        st.markdown(f"""
        <div style="background:#111827;border:1px solid #1e293b;border-radius:16px;
                    padding:48px;text-align:center;">
          <div style="font-size:40px;margin-bottom:12px;">🎓</div>
          <div style="color:#00ff88;font-size:20px;font-weight:700;margin-bottom:16px;">
            ¡Sesión completa!
          </div>
          <div style="display:flex;justify-content:center;gap:40px;">
            <div>
              <div style="font-size:36px;color:#00ff88;font-family:'JetBrains Mono',monospace;">
                {total}</div>
              <div style="font-size:12px;color:#64748b;">revisadas</div>
            </div>
            <div>
              <div style="font-size:36px;color:#3b82f6;font-family:'JetBrains Mono',monospace;">
                {pct}%</div>
              <div style="font-size:12px;color:#64748b;">precisión</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔁 Nueva sesión", type="primary", use_container_width=True):
            st.session_state.queue = []
            st.session_state.q_idx = 0
            st.rerun()
        return

    # ── Active card ───────────────────────────────────────────────────
    card  = queue[idx]
    state = store.get_state(card["id"])

    # Progress
    pct_prog = idx / len(queue)
    m_score  = engine.mastery_score(state)
    m_pct    = int(m_score*100)
    m_col    = mastery_color(m_pct)

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;font-size:12px;
                color:#64748b;margin-bottom:4px;">
      <span>{idx+1} / {len(queue)}</span>
      <span>Dominio actual de esta carta: <span style="color:{m_col};">{m_pct}%</span></span>
    </div>
    <div class="progress-bar-bg">
      <div style="background:#00ff88;width:{pct_prog*100:.1f}%;height:100%;border-radius:8px;"></div>
    </div>
    """, unsafe_allow_html=True)

    render_tags(card)
    st.markdown("")
    render_question_modes(card, state)


# ═══════════════════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════════════════

# ── DASHBOARD ─────────────────────────────────────────────────────────
if st.session_state.page == "Dashboard":
    st.markdown('<div class="title-main">∂ QUANT MEMORIA</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-sub">Plataforma de aprendizaje cuantitativo · Programa BCRP</div>',
               unsafe_allow_html=True)

    # Sync master_cards into store on first load
    stored_ids = {c.id for c in store.all_cards()}
    for card in ALL_CARDS:
        if card["id"] not in stored_ids:
            from core.card_model import Flashcard
            fc = Flashcard(
                id=card["id"], domain=card.get("domain",""),
                topic=card.get("topic",""), card_type="Formula",
                difficulty=card.get("difficulty","Intermediate"),
                front=card.get("front",""), back=card.get("back",""),
                latex_formula=card.get("latex",""),
                tags=card.get("mode_tags",[]),
                source=card.get("source",""),
            )
            store.save_card(fc)

    summ = analytics.summary()
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Cartas totales", len(ALL_CARDS))
    c2.metric("Para hoy",       summ["due_today"])
    c3.metric("Dominio medio",  f"{summ['mean_mastery']*100:.0f}%")
    c4.metric("Precisión",      f"{summ['accuracy']*100:.0f}%")
    c5.metric("Streak 🔥",      f"{summ['streak_days']}d")

    st.divider()
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("#### 🎯 Temas más débiles")
        weak = analytics.weak_topics(6)
        for t in weak:
            pct = int(t["mastery"]*100)
            col = mastery_color(pct)
            st.markdown(f"""
            <div style="margin-bottom:10px;">
              <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:3px;">
                <span>{t['topic']}</span>
                <span style="color:{col};font-family:'JetBrains Mono',monospace;">{pct}%</span>
              </div>
              <div style="background:#1e293b;border-radius:6px;height:5px;">
                <div style="background:{col};width:{pct}%;height:100%;border-radius:6px;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown("#### 📋 Cobertura por dominio")
        domain_counts = {}
        for c in ALL_CARDS:
            d = c.get("domain","Other")
            domain_counts[d] = domain_counts.get(d,0) + 1
        for dom, cnt in sorted(domain_counts.items(), key=lambda x:-x[1]):
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:13px;
                        padding:6px 0;border-bottom:1px solid #1e293b;">
              <span>{dom}</span>
              <span style="font-family:'JetBrains Mono',monospace;color:#3b82f6;">{cnt} cartas</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    c_bus, c_home = st.columns(2)
    with c_bus:
        bus_n = len([c for c in ALL_CARDS if "bus" in c.get("mode_tags",[])])
        if st.button(f"🚌 Iniciar Modo Bus ({bus_n} cartas)", use_container_width=True, type="primary"):
            st.session_state.page = "Bus"
            st.session_state.queue = []
            st.rerun()
    with c_home:
        if st.button(f"🏠 Iniciar Modo Casa ({len(ALL_CARDS)} cartas)", use_container_width=True):
            st.session_state.page = "Home"
            st.session_state.queue = []
            st.rerun()


# ── BUS MODE ──────────────────────────────────────────────────────────
elif st.session_state.page == "Bus":
    render_study_session("Bus")


# ── HOME MODE ─────────────────────────────────────────────────────────
elif st.session_state.page == "Home":
    render_study_session("Home")


# ── LIBRARY ───────────────────────────────────────────────────────────
elif st.session_state.page == "Library":
    st.markdown('<div class="title-main">📚 BIBLIOTECA</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-sub">Todas las cartas del sistema</div>', unsafe_allow_html=True)

    col_s, col_d, col_m = st.columns([2,1.5,1])
    with col_s:
        search = st.text_input("🔍 Buscar", placeholder="vasicek, GARCH, martingala...")
    with col_d:
        f_domain = st.selectbox("Dominio", DOMAINS)
    with col_m:
        f_mode = st.selectbox("Modo", ["Todos","🚌 Bus","🏠 Casa"])

    filtered = ALL_CARDS
    if f_domain != "All":
        filtered = [c for c in filtered if c["domain"] == f_domain]
    if f_mode == "🚌 Bus":
        filtered = [c for c in filtered if "bus" in c.get("mode_tags",[])]
    elif f_mode == "🏠 Casa":
        filtered = [c for c in filtered if "home" in c.get("mode_tags",[])]
    if search:
        q = search.lower()
        filtered = [c for c in filtered if
                    q in c.get("front","").lower() or
                    q in c.get("topic","").lower() or
                    q in c.get("back","").lower()]

    st.markdown(f"**{len(filtered)} cartas**")
    states = store.all_states()

    for card in filtered:
        state  = states.get(card["id"], CardState(card_id=card["id"]))
        m_pct  = int(engine.mastery_score(state)*100)
        m_col  = mastery_color(m_pct)
        with st.expander(f"[{card.get('topic','')}] {card['front'][:75]}"):
            cc1, cc2 = st.columns([3,1])
            with cc1:
                render_tags(card)
                st.markdown(f"**Respuesta:** {card['back'][:300]}")
                if card.get("latex"): st.latex(card["latex"])
                render_graph(card)
                _render_tabs(card)
            with cc2:
                st.markdown(f"""
                <div style="text-align:center;background:#0d1321;border:1px solid #1e293b;
                            border-radius:8px;padding:16px;">
                  <div style="font-size:28px;color:{m_col};
                              font-family:'JetBrains Mono',monospace;font-weight:700;">
                    {m_pct}%</div>
                  <div style="font-size:11px;color:#64748b;">dominio</div>
                  <div style="margin-top:10px;font-size:11px;color:#64748b;line-height:1.8;">
                    {state.repetitions} repasos<br>
                    {state.error_count} errores<br>
                    vence en {engine.days_until_due(state):.0f}d
                  </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Estudiar", key=f"lib_{card['id']}", use_container_width=True):
                    st.session_state.queue   = [card]
                    st.session_state.q_idx   = 0
                    st.session_state.q_type  = "Flashcard"
                    st.session_state.revealed = False
                    st.session_state.page    = "Home"
                    st.rerun()


# ── ANALYTICS ─────────────────────────────────────────────────────────
elif st.session_state.page == "Analytics":
    st.markdown('<div class="title-main">📈 ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-sub">Curvas de olvido · Heatmaps · Métricas de retención</div>',
               unsafe_allow_html=True)

    summ = analytics.summary()
    c1,c2,c3 = st.columns(3)
    c1.metric("Streak",  f"{summ['streak_days']} días 🔥")
    c2.metric("Precisión global", f"{summ['accuracy']*100:.1f}%")
    c3.metric("Dominio medio",    f"{summ['mean_mastery']*100:.1f}%")

    try:
        import plotly.graph_objects as go
        import numpy as np

        LAYOUT2 = dict(
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(color="#94a3b8", size=11),
            margin=dict(l=0,r=0,t=30,b=0), height=300,
            xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="#1e293b"),
        )

        st.divider()
        st.markdown("### 📅 Actividad diaria (últimos 14 días)")
        rpd = analytics.reviews_per_day(14)
        dates  = [d["date"][-5:] for d in rpd]
        counts = [d["count"]     for d in rpd]
        fig = go.Figure(go.Bar(x=dates, y=counts, marker_color="#00ff88"))
        fig.update_layout(**LAYOUT2, title="Repasos por día")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🧠 Curvas de olvido proyectadas")
        curves = analytics.projected_forgetting_curves()
        if curves:
            fig2 = go.Figure()
            colors_fc = ["#00ff88","#3b82f6","#f59e0b","#ef4444","#8b5cf6","#06b6d4"]
            for i,item in enumerate(curves[:6]):
                xs = [p[0] for p in item["curve"]]
                ys = [p[1]*100 for p in item["curve"]]
                fig2.add_trace(go.Scatter(x=xs,y=ys,mode="lines",
                    name=item["front"][:30],
                    line=dict(color=colors_fc[i%len(colors_fc)],width=2)))
            fig2.update_layout(**LAYOUT2,
                title="Retención proyectada (%)",
                height=350,
                xaxis=dict(title="Días",gridcolor="#1e293b"),
                yaxis=dict(title="Retención %",gridcolor="#1e293b",range=[0,105]),
                legend=dict(bgcolor="#1e293b"))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 🗺️ Heatmap de dominio por tópico")
        hdata = analytics.topic_mastery_heatmap()
        if hdata:
            domains_h = sorted(list({d["domain"] for d in hdata}))
            topics_h  = sorted(list({d["topic"]  for d in hdata}))
            zm = []
            for dom in domains_h:
                row = []
                for top in topics_h:
                    match = next((d for d in hdata if d["domain"]==dom and d["topic"]==top),None)
                    row.append(match["mastery"]*100 if match else None)
                zm.append(row)
            fig3 = go.Figure(go.Heatmap(
                z=zm, x=topics_h, y=domains_h,
                colorscale=[[0,"#0a0e17"],[0.33,"#ef4444"],[0.66,"#f59e0b"],[1,"#00ff88"]],
                zmin=0,zmax=100,
                text=[[f"{v:.0f}%" if v is not None else "" for v in row] for row in zm],
                texttemplate="%{text}",
            ))
            fig3.update_layout(paper_bgcolor="#111827",plot_bgcolor="#111827",
                font=dict(color="#94a3b8",size=10),
                height=max(200,len(domains_h)*60),
                margin=dict(l=0,r=0,t=10,b=0),
                xaxis=dict(tickangle=-40))
            st.plotly_chart(fig3, use_container_width=True)

    except ImportError:
        st.info("Instala plotly para ver gráficos de analytics.")

    col_w, col_s = st.columns(2)
    with col_w:
        st.markdown("### ⚠️ Más débiles")
        for t in analytics.weak_topics(5):
            st.markdown(f"- **{t['topic']}** ({t['mastery']*100:.0f}%)")
    with col_s:
        st.markdown("### ✅ Más fuertes")
        for t in analytics.strong_topics(5):
            st.markdown(f"- **{t['topic']}** ({t['mastery']*100:.0f}%)")


# ── ADD CARD ──────────────────────────────────────────────────────────
elif st.session_state.page == "AddCard":
    st.markdown('<div class="title-main">➕ NUEVA CARTA</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-sub">Agrega al archivo master_cards.py o usa este formulario rápido</div>',
               unsafe_allow_html=True)

    st.info(
        "💡 **Tip:** Para cartas permanentes, edita directamente `content/master_cards.py` "
        "y sube a GitHub — se sincronizan automáticamente. Este formulario agrega al JSON local."
    )

    with st.form("add_card"):
        c1,c2 = st.columns(2)
        with c1:
            domain = st.selectbox("Dominio", [d for d in DOMAINS if d != "All"])
        with c2:
            topic = st.text_input("Tópico", placeholder="Vasicek Model")

        c3,c4 = st.columns(2)
        with c3:
            diff = st.selectbox("Dificultad", ["Foundational","Intermediate","Advanced","Expert"])
        with c4:
            mode_tag = st.selectbox("Modo", ["both","bus","home"])

        front = st.text_area("Pregunta *", height=80)
        back  = st.text_area("Respuesta *", height=120)
        latex = st.text_input("Fórmula LaTeX (sin $)")
        intuition = st.text_area("Intuición financiera", height=70)
        code_py   = st.text_area("Código Python", height=80)
        source    = st.text_input("Fuente")

        submitted = st.form_submit_button("💾 Guardar carta", type="primary",
                                          use_container_width=True)

    if submitted:
        if not front or not back:
            st.error("Pregunta y respuesta son obligatorias.")
        else:
            import uuid
            new_card = {
                "id": f"user_{str(uuid.uuid4())[:8]}",
                "domain": domain, "topic": topic,
                "difficulty": diff, "mode_tags": [mode_tag],
                "front": front, "back": back,
                "latex": latex, "intuition": intuition,
                "code_python": code_py, "source": source,
            }
            ALL_CARDS.append(new_card)
            from core.card_model import Flashcard
            fc = Flashcard(
                id=new_card["id"], domain=domain, topic=topic,
                front=front, back=back, latex_formula=latex,
                source=source,
            )
            store.save_card(fc)
            st.success(f"✅ Carta guardada. Para que persista en producción, agrégala a `content/master_cards.py`.")

