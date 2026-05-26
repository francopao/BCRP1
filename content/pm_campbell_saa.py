"""
Strategic Asset Allocation — John Campbell
==========================================
Cartas generadas desde Prompt A + Prompt B del Capítulo.
Incluye: conceptos, trampas, cuándo-no-usar, lógicas implícitas,
sabiduría practitioner.

Agregar en master_cards.py al final:
    from content.pm_campbell_saa import CARDS as CAMPBELL_CARDS
    CARDS = CARDS + CAMPBELL_CARDS
"""

CARDS = [

# ══════════════════════════════════════════════════════════════════
# CAPA 1 — CONCEPTOS EXPLÍCITOS (Prompt A)
# ══════════════════════════════════════════════════════════════════

{
    "id": "saa_01",
    "domain": "Portfolio Management",
    "topic": "Utilidad Logarítmica",
    "difficulty": "Intermediate",
    "mode_tags": ["both"],
    "front": "Define la función de utilidad logarítmica. ¿Qué implica sobre la aversión al riesgo?",
    "back": (
        "$$U(W) = \\log(W)$$\n\n"
        "- **Aversión relativa al riesgo constante** (CRRA) con γ = 1\n"
        "- **Elasticidad de sustitución intertemporal** = 1\n"
        "- Caso particular de power utility $U(W) = W^{1-\\gamma}/(1-\\gamma)$ cuando γ → 1\n"
        "- Permite soluciones analíticas en modelos de asignación de activos"
    ),
    "latex": r"U(W) = \log(W)",
    "intuition": (
        "El agente con log-utility siempre invierte una fracción **constante** de su riqueza "
        "en cada activo, independientemente de su nivel de riqueza. "
        "Duplicar la riqueza produce el mismo incremento de utilidad que duplicarla desde cero — "
        "eso captura la idea de que $1M adicional importa menos si ya tienes $10M."
    ),
    "code_python": """\
import numpy as np

def utilidad_logaritmica(riqueza):
    \"\"\"U(W) = log(W). Indefinida para W <= 0.\"\"\"
    return np.log(riqueza)

# La utilidad marginal DECRECE — aversión al riesgo
W = np.array([1, 10, 100, 1000])
U = utilidad_logaritmica(W)
dU = np.diff(U) / np.diff(W)   # utilidad marginal

print("Riqueza:          ", W)
print("Utilidad:         ", np.round(U, 3))
print("Utilidad marginal:", np.round(dU, 4))
# La utilidad marginal cae → agente es averso al riesgo
""",
    "assumptions": (
        "• Agentes maximizan utilidad esperada de riqueza\n"
        "• Mercados completos, sin restricciones de liquidez\n"
        "• Aversión relativa al riesgo constante (γ = 1)"
    ),
    "limitations": (
        "• No captura γ ≠ 1 — muchos inversores institucionales tienen γ > 1\n"
        "• Puede sugerir apalancamiento excesivo (ver carta saa_trap_01)\n"
        "• Ignora asimetría downside y liabilities convexos"
    ),
    "mcq": {
        "question": "¿Cuál es la aversión relativa al riesgo (γ) implícita en la utilidad logarítmica?",
        "options": ["A) γ = 0", "B) γ = 0.5", "C) γ = 1", "D) γ = ∞"],
        "answer": "C",
        "explanation": "U(W)=log(W) es el caso límite de power utility W^(1-γ)/(1-γ) cuando γ→1. La aversión relativa al riesgo −W·U''/U' = 1."
    },
    "true_false": {
        "statement": "Con utilidad logarítmica, un inversor con $1M y otro con $1B invertirán la misma fracción de su riqueza en activos riesgosos.",
        "answer": True,
        "explanation": "Correcto. CRRA implica que la fracción óptima es independiente del nivel de riqueza. Solo depende de las características del activo (E[R], σ², r_f)."
    },
    "connections": ["Coeficiente de Aversión al Riesgo γ", "Elección de Portafolio Miópica", "Epstein-Zin Utility", "Kelly Criterion"],
    "source": "Campbell - Strategic Asset Allocation, Cap.1",
},

{
    "id": "saa_02",
    "domain": "Portfolio Management",
    "topic": "Coeficiente de Aversión al Riesgo γ",
    "difficulty": "Intermediate",
    "mode_tags": ["both"],
    "front": "Define γ (aversión relativa al riesgo). ¿Cómo afecta la asignación óptima?",
    "back": (
        "$$\\gamma = -\\frac{W \\cdot U''(W)}{U'(W)}$$\n\n"
        "En power utility $U(W) = \\frac{W^{1-\\gamma}}{1-\\gamma}$:\n\n"
        "| γ | Perfil | Asignación riesgosa |\n"
        "|---|--------|--------------------|\n"
        "| 1 | Log utility | Máxima (Kelly) |\n"
        "| 2–3 | Moderado | Alta |\n"
        "| 5–10 | Conservador | Baja |\n"
        "| → ∞ | Sin riesgo | → 0% |\n\n"
        "Fracción óptima: $\\pi^* = \\frac{E[R]-r_f}{\\gamma\\sigma^2}$"
    ),
    "latex": r"\gamma = -\frac{W \cdot U''(W)}{U'(W)}, \qquad \pi^* = \frac{E[R]-r_f}{\gamma\,\sigma^2}",
    "intuition": (
        "γ es el parámetro que 'frena' la agresividad del portafolio. "
        "Duplicar γ divide a la mitad la exposición al activo riesgoso. "
        "Los bancos centrales gestionando reservas usan γ entre 3 y 10 en la práctica — "
        "no el γ=1 que da soluciones limpias en el aula."
    ),
    "code_python": """\
import numpy as np
import matplotlib.pyplot as plt

def fraccion_optima(E_R, r_f, sigma2, gamma):
    \"\"\"Fracción óptima en activo riesgoso bajo CRRA.\"\"\"
    return (E_R - r_f) / (gamma * sigma2)

E_R, r_f, sigma2 = 0.08, 0.02, 0.04
gammas = np.linspace(0.5, 10, 100)
pis    = [fraccion_optima(E_R, r_f, sigma2, g) for g in gammas]

plt.figure(figsize=(8,4))
plt.plot(gammas, pis, color='#00ff88', linewidth=2)
plt.axhline(1.0, color='white', linestyle='--', alpha=0.4, label='100% riesgoso')
plt.axhline(0.0, color='red',   linestyle='--', alpha=0.4, label='0% riesgoso')
plt.axvline(1.0, color='yellow',linestyle=':',  alpha=0.6, label='γ=1 (log utility)')
plt.xlabel('γ (aversión al riesgo)')
plt.ylabel('π* (fracción óptima)')
plt.title('Asignación óptima vs. aversión al riesgo')
plt.legend(); plt.tight_layout()
print(f"γ=1 (log): π* = {fraccion_optima(E_R, r_f, sigma2, 1):.2f}")
print(f"γ=5 (conserv): π* = {fraccion_optima(E_R, r_f, sigma2, 5):.2f}")
""",
    "mcq": {
        "question": "Con E[R]=8%, r_f=2%, σ²=4%, ¿cuál es π* para un inversor con γ=2?",
        "options": ["A) 0.50", "B) 0.75", "C) 1.50", "D) 3.00"],
        "answer": "B",
        "explanation": "π* = (0.08−0.02)/(2×0.04) = 0.06/0.08 = 0.75. Con γ=1 sería 1.5 — el doble. Mayor γ → menos riesgo."
    },
    "true_false": {
        "statement": "Doblar γ de 1 a 2 reduce la asignación óptima al activo riesgoso a la mitad.",
        "answer": True,
        "explanation": "π* = (E[R]−r_f)/(γσ²). Si γ se duplica, π* se divide a la mitad. La relación es exactamente inversa."
    },
    "connections": ["Utilidad Logarítmica", "Epstein-Zin Utility", "Mean-Variance Optimization"],
    "source": "Campbell - Strategic Asset Allocation, Cap.1",
},

{
    "id": "saa_03",
    "domain": "Portfolio Management",
    "topic": "Elección de Portafolio Miópica",
    "difficulty": "Advanced",
    "mode_tags": ["both"],
    "front": "¿Qué es la elección miópica de portafolio? ¿Cuándo es óptima y cuándo falla?",
    "back": (
        "**Definición:** Asignación que maximiza utilidad en un solo período, "
        "ignorando cómo cambiarán las oportunidades de inversión futuras.\n\n"
        "$$\\pi^* = \\frac{E[R] - r_f}{\\gamma\\sigma^2}$$\n\n"
        "**Es óptima cuando:**\n"
        "- Retornos son IID (independientes e idénticamente distribuidos)\n"
        "- Utilidad es logarítmica (γ=1) — incluso con retornos NO-IID\n\n"
        "**Falla cuando:**\n"
        "- Retornos tienen predictibilidad (valuation ratios, mean reversion)\n"
        "- γ ≠ 1 y las oportunidades de inversión varían en el tiempo\n"
        "- Hay variables de estado que el inversor quiere cubrir (hedging demand)"
    ),
    "latex": r"\pi^* = \frac{E[R] - r_f}{\gamma\,\sigma^2}",
    "intuition": (
        "La miopía es óptima bajo log-utility porque el income effect y el substitution effect "
        "se cancelan exactamente. Intuitivamente: con log-utility, ganar más riqueza no cambia "
        "tu apetito relativo por riesgo. Para cualquier otro γ, el inversor también quiere "
        "cubrir cambios futuros en las oportunidades de inversión — eso introduce demanda "
        "de cobertura (hedging demand) que la miopía ignora."
    ),
    "mcq": {
        "question": "¿Bajo qué condición es la elección miópica óptima incluso con retornos NO-IID?",
        "options": [
            "A) Cuando γ > 1",
            "B) Cuando la utilidad es logarítmica (γ = 1)",
            "C) Cuando los mercados son completos",
            "D) Cuando el horizonte es suficientemente largo"
        ],
        "answer": "B",
        "explanation": "Con γ=1, income effect y substitution effect se cancelan exactamente. La demanda de cobertura es cero independientemente de la predictibilidad de retornos. Campbell lo demuestra formalmente."
    },
    "true_false": {
        "statement": "La elección miópica es siempre óptima cuando el horizonte de inversión es de un solo período.",
        "answer": True,
        "explanation": "Correcto. Con un solo período no hay oportunidades futuras que cubrir, así que la miopía es trivialmente óptima. El problema surge en múltiples períodos con γ ≠ 1."
    },
    "connections": ["Utilidad Logarítmica", "Hedging Demand", "IID Returns", "Epstein-Zin Utility"],
    "source": "Campbell - Strategic Asset Allocation, Cap.1",
},


# ══════════════════════════════════════════════════════════════════
# CAPA 2 — LÓGICA IMPLÍCITA (Prompt B: secciones 2, 3, 4)
# ══════════════════════════════════════════════════════════════════

{
    "id": "saa_04",
    "domain": "Portfolio Management",
    "topic": "Epstein-Zin vs Power Utility",
    "difficulty": "Advanced",
    "mode_tags": ["both"],
    "front": "¿Por qué Campbell prefiere Epstein-Zin sobre power utility? ¿Qué separa conceptualmente?",
    "back": (
        "**Power utility:** fuerza $\\psi = 1/\\gamma$ — aversión al riesgo y elasticidad "
        "de sustitución intertemporal son el **mismo parámetro** (recíproco).\n\n"
        "**Epstein-Zin:** separa los dos:\n"
        "- $\\gamma$: aversión al riesgo (cuánto odias la volatilidad *cross-sectional*)\n"
        "- $\\psi$: elasticidad de sustitución intertemporal (cuánto odias la volatilidad *en el tiempo*)\n\n"
        "**Por qué importa:** en power utility, si eres muy averso al riesgo (γ alto), "
        "automáticamente eres muy rígido intertemporalmente (ψ bajo). "
        "Eso no tiene justificación económica — son dos conceptos distintos."
    ),
    "latex": r"\psi = \frac{1}{\gamma} \text{ (power utility)} \qquad \gamma, \psi \text{ libres (Epstein-Zin)}",
    "intuition": (
        "Imagina dos preguntas distintas: \n"
        "1) ¿Preferirías $100 seguros o un 50/50 de $0 o $200? → mide γ\n"
        "2) ¿Preferirías $100 hoy o $110 el año que viene? → mide ψ\n\n"
        "Power utility obliga que la misma persona responda ambas con el mismo parámetro. "
        "Epstein-Zin permite que sean independientes — como deberían ser."
    ),
    "mcq": {
        "question": "En power utility U(W)=W^(1-γ)/(1-γ), ¿cuánto vale la elasticidad de sustitución intertemporal ψ?",
        "options": ["A) ψ = γ", "B) ψ = 1/γ", "C) ψ = γ²", "D) ψ es libre"],
        "answer": "B",
        "explanation": "Power utility impone ψ = 1/γ. Si γ=2 entonces ψ=0.5. Esta restricción es lo que Epstein-Zin elimina, permitiendo calibrar ambos parámetros independientemente."
    },
    "true_false": {
        "statement": "En Epstein-Zin, un agente puede tener alta aversión al riesgo (γ grande) y alta elasticidad de sustitución intertemporal (ψ grande) simultáneamente.",
        "answer": True,
        "explanation": "Correcto — esa es exactamente la ventaja. En power utility esto sería imposible porque ψ=1/γ. Epstein-Zin los desacopla."
    },
    "connections": ["Utilidad Logarítmica", "Coeficiente de Aversión al Riesgo γ", "Strategic Asset Allocation"],
    "source": "Campbell - SAA, Cap.1 — comparación implícita sección 3",
},

{
    "id": "saa_05",
    "domain": "Portfolio Management",
    "topic": "Time Diversification — La Falacia",
    "difficulty": "Advanced",
    "mode_tags": ["both"],
    "front": "¿Por qué 'el largo plazo reduce el riesgo' es una falacia según Campbell? ¿Cuándo SÍ es válido?",
    "back": (
        "**La falacia:** 'Invertir en acciones a largo plazo es seguro porque la volatilidad "
        "anualizada cae con √T.'\n\n"
        "**Por qué es falsa bajo IID + CRRA:**\n"
        "- La volatilidad total crece con √T, aunque la anualizada caiga\n"
        "- La probabilidad de pérdida cae, pero las pérdidas posibles *en valor absoluto* crecen\n"
        "- Bajo CRRA, lo que importa es la utilidad de la riqueza terminal, no la prob. de ganar\n\n"
        "**Cuándo SÍ hay horizon effects legítimos:**\n"
        "- Cuando los retornos **mean-revert** (predictibilidad)\n"
        "- Cuando existen variables de estado que hedgear\n"
        "- Cuando γ ≠ 1 y las oportunidades de inversión varían"
    ),
    "latex": r"\text{Var}(R_{1..T}) = T\sigma^2 \xrightarrow{\text{anualizado}} \sigma^2 \quad \text{pero riesgo total} \uparrow",
    "intuition": (
        "Diversificar en el tiempo no crea estados independientes nuevos — "
        "solo promedia resultados dentro de los mismos estados. "
        "Cross-sectional diversification sí reduce riesgo porque mezcla activos imperfectamente correlacionados. "
        "Time diversification es una ilusión: la distribución del valor terminal se ensancha con T, "
        "aunque el Sharpe ratio anualizado permanezca constante."
    ),
    "mcq": {
        "question": "¿Bajo qué condición SÍ existen horizon effects legítimos en la asignación de activos?",
        "options": [
            "A) Cuando los retornos son IID y el inversor tiene log-utility",
            "B) Cuando los retornos tienen mean-reversion y γ ≠ 1",
            "C) Cuando el horizonte supera los 10 años",
            "D) Cuando el activo riesgoso es un índice bursátil diversificado"
        ],
        "answer": "B",
        "explanation": "Campbell es explícito: 'legitimate arguments for horizon effects appear when the assumptions of this chapter fail' — es decir, cuando retornos no son IID y γ ≠ 1. Mean-reversion del mercado crea hedging demand real."
    },
    "true_false": {
        "statement": "Un inversor de largo plazo (30 años) debería invertir más agresivamente que uno de corto plazo (1 año) porque el tiempo diversifica el riesgo.",
        "answer": False,
        "explanation": "Bajo IID returns y CRRA utility, la asignación óptima es IDÉNTICA para ambos horizontes (myopic optimality). La 'time diversification' es una falacia bajo estos supuestos. Solo hay diferencia cuando hay predictibilidad en retornos."
    },
    "connections": ["Elección de Portafolio Miópica", "Hedging Demand", "IID Returns"],
    "source": "Campbell - SAA, Cap.1 — advertencia explícita del autor",
},

{
    "id": "saa_06",
    "domain": "Portfolio Management",
    "topic": "Growth-Optimal Portfolio vs Utility Maximization",
    "difficulty": "Advanced",
    "mode_tags": ["both"],
    "front": "El portafolio growth-optimal (Kelly) 'casi siempre gana'. ¿Por qué aun así puede destruir utilidad?",
    "back": (
        "**Kelly / Growth-optimal:** maximiza $E[\\log W_T]$ → "
        "gana a cualquier estrategia alternativa en probabilidad cuando T → ∞\n\n"
        "**El problema:**\n"
        "$$\\max P(\\text{outperform}) \\neq \\max E[U(W_T)]$$\n\n"
        "- Para γ > 1: Kelly **sobreinvierte** → drawdowns enormes en el camino\n"
        "- Para un inversor con γ=5: el portafolio Kelly puede sugerir "
        "200-300% en acciones → ruinoso en práctica\n"
        "- 'Ganar casi siempre' con drawdowns del 80% no maximiza utilidad esperada\n\n"
        "**Clave:** maximizar prob. de outperform es un objetivo de *ranking*, "
        "no de *utilidad*."
    ),
    "latex": r"\max_\pi \Pr(\text{outperform}) \neq \max_\pi \mathbb{E}[U(W_T)]",
    "intuition": (
        "El Kelly criterion es óptimo para alguien con log-utility (γ=1). "
        "Para cualquier γ > 1, Kelly sobreinvierte porque ignora el costo en utilidad "
        "de los drawdowns extremos. Un inversor con γ=3 debería usar 'fractional Kelly' "
        "(Kelly/γ). En la práctica institucional, nadie usa Kelly puro — precisamente "
        "porque los mandatos institucionales penalizan drawdowns más que lo que premia el upside."
    ),
    "mcq": {
        "question": "¿Para qué valor de γ el portafolio Kelly (growth-optimal) es exactamente óptimo?",
        "options": ["A) γ = 0", "B) γ = 1 (log utility)", "C) γ = 2", "D) Para todo γ > 0"],
        "answer": "B",
        "explanation": "Kelly maximiza E[log(W)], que es exactamente la utilidad logarítmica (γ=1). Para γ>1, el óptimo es 'fractional Kelly' = Kelly/γ, que invierte menos agresivamente."
    },
    "true_false": {
        "statement": "El portafolio Kelly maximiza la probabilidad de superar a cualquier estrategia alternativa en el largo plazo.",
        "answer": True,
        "explanation": "Correcto — pero esto no implica que maximice la utilidad esperada para inversores con γ>1. Son objetivos distintos. 'Ganar casi siempre' con drawdowns enormes puede destruir más utilidad que una estrategia más conservadora."
    },
    "connections": ["Utilidad Logarítmica", "Coeficiente de Aversión al Riesgo γ", "Elección de Portafolio Miópica"],
    "source": "Campbell - SAA, Cap.1 — intuición mencionada de pasada, sección 4",
},

{
    "id": "saa_07",
    "domain": "Portfolio Management",
    "topic": "Continuous-Time vs Discrete-Time Portfolio Theory",
    "difficulty": "Expert",
    "mode_tags": ["home"],
    "front": "¿Por qué la teoría de portafolio 'vive' en tiempo continuo según Campbell? ¿Qué pierde en discreto?",
    "back": (
        "**En tiempo discreto:**\n"
        "- Combinación lineal de lognormales ≠ lognormal → el portafolio no tiene distribución cerrada\n"
        "- Retornos multi-período son productos, no sumas → no se preserva normalidad\n"
        "- Aproximaciones log-lineales se deterioran en horizontes largos\n\n"
        "**En tiempo continuo (Itô):**\n"
        "- Itô's Lemma vuelve exactas varias relaciones clave\n"
        "- La lognormalidad del portafolio se preserva instantáneamente\n"
        "- La condición $dt \\to 0$ elimina las nonlinearidades incómodas\n\n"
        "**El costo:** el modelo continuo ignora jumps, market closures, "
        "liquidity spirals y margin calls — exactamente lo que importa en las crisis."
    ),
    "latex": r"\sum_i w_i \ln(1+R_i) \neq \ln\!\left(1+\sum_i w_i R_i\right)",
    "intuition": (
        "La elegancia matemática del tiempo continuo viene de que $dt \\to 0$ hace "
        "desaparecer los términos de segundo orden incómodos. "
        "El problema es que 2008 y 2020 son exactamente los escenarios donde "
        "el tiempo NO es continuo: hay gaps, halts, liquidity spirals y forced deleveraging. "
        "La teoría es más limpia precisamente cuando el mundo es más tranquilo."
    ),
    "true_false": {
        "statement": "Una combinación lineal de activos lognormales es también lognormal.",
        "answer": False,
        "explanation": "Falso — y esto es una trampa frecuente. La SUMA de lognormales no es lognormal. Solo el PRODUCTO lo es. Esto es por qué la teoría discreta de portafolio requiere aproximaciones, mientras que el tiempo continuo resuelve esto con Itô."
    },
    "connections": ["Itô's Lemma", "GBM", "Elección de Portafolio Miópica"],
    "source": "Campbell - SAA, Cap.1 — comparación implícita sección 3",
},


# ══════════════════════════════════════════════════════════════════
# CAPA 3 — SABIDURÍA PRACTITIONER (Prompt B: secciones 1, 5)
# ══════════════════════════════════════════════════════════════════

{
    "id": "saa_trap_01",
    "domain": "Portfolio Management",
    "topic": "Elección de Portafolio Miópica",
    "difficulty": "Advanced",
    "mode_tags": ["bus"],
    "front": "⚠️ TRAMPA: π* = 1.5 sale de la fórmula de log-utility. ¿Deberías implementarlo directamente en un fondo institucional?",
    "back": (
        "**NO.** π* = 1.5 significa 150% en el activo riesgoso → **apalancamiento**.\n\n"
        "El modelo ignora completamente:\n"
        "- Límites de leverage (restricciones regulatorias)\n"
        "- VaR limits y drawdown constraints\n"
        "- Margin calls en escenarios de stress\n"
        "- Liquidez y costos de transacción\n"
        "- Benchmark-relative risk (tracking error)\n\n"
        "**En práctica:** el resultado teórico da la *dirección*, no la magnitud. "
        "Los portfolios institucionales escalan hacia abajo y agregan restricciones. "
        "Un resultado > 100% es una señal de alerta, no una instrucción."
    ),
    "mcq": {
        "question": "Un modelo da π*=1.8 para el peso óptimo en acciones. ¿Cuál es la interpretación correcta para un gestor institucional?",
        "options": [
            "A) Invertir 180% en acciones usando apalancamiento",
            "B) El modelo sugiere máxima exposición permitida, aplicar restricciones institucionales",
            "C) El modelo está equivocado, nunca puede ser > 100%",
            "D) Reducir γ hasta que π* < 1"
        ],
        "answer": "B",
        "explanation": "π*>1 es matemáticamente válido pero operacionalmente requiere ajuste. El modelo dice 'sé tan agresivo como puedas' — las restricciones institucionales (VaR, leverage limits, regulación) determinan el techo real."
    },
    "connections": ["Utilidad Logarítmica", "Coeficiente de Aversión al Riesgo γ", "Mean-Variance Optimization"],
    "source": "Campbell - SAA, Cap.1 — advertencia practitioner sección 5",
},

{
    "id": "saa_trap_02",
    "domain": "Portfolio Management",
    "topic": "Mean-Variance Optimization",
    "difficulty": "Advanced",
    "mode_tags": ["bus"],
    "front": "⚠️ TRAMPA: La fórmula w* = Σ⁻¹μ da el portafolio óptimo. ¿Por qué es peligrosa en producción?",
    "back": (
        "**El problema:** $\\mathbf{w}^* = \\Sigma^{-1}\\boldsymbol{\\mu}$ amplifica "
        "**brutalmente** los errores de estimación.\n\n"
        "En la práctica:\n"
        "- $\\boldsymbol{\\mu}$ (retornos esperados) es casi imposible de estimar con precisión\n"
        "- $\\Sigma^{-1}$ invierte esas estimaciones, amplificando el error\n"
        "- El resultado: portafolios concentrados, inestables, con turnover altísimo\n\n"
        "**Soluciones usadas en práctica:**\n"
        "- Shrinkage estimators (Ledoit-Wolf)\n"
        "- Black-Litterman (combina prior de mercado con views)\n"
        "- Restricciones de peso (no shorting, límites por activo)\n"
        "- Portafolio de mínima varianza (ignora μ por completo)"
    ),
    "latex": r"\mathbf{w}^* = \Sigma^{-1}\boldsymbol{\mu} \quad \leftarrow \text{inestable en producción}",
    "mcq": {
        "question": "¿Por qué el portafolio de mínima varianza global (GMV) a veces supera en práctica al portafolio mean-variance óptimo?",
        "options": [
            "A) Porque tiene mayor retorno esperado",
            "B) Porque ignora μ, eliminando la principal fuente de error de estimación",
            "C) Porque tiene menor tracking error",
            "D) Porque es más fácil de implementar"
        ],
        "answer": "B",
        "explanation": "Estimar μ es mucho más difícil que estimar Σ. El GMV solo necesita Σ, evitando la amplificación de errores en μ. En datos históricos, el GMV frecuentemente outperforms el MVO precisamente por esto."
    },
    "true_false": {
        "statement": "El mayor problema práctico de la optimización de Markowitz es la complejidad computacional.",
        "answer": False,
        "explanation": "No — la computación es trivial. El problema real es la sensibilidad extrema a los inputs estimados, especialmente μ. Pequeños cambios en retornos esperados producen portafolios radicalmente distintos."
    },
    "connections": ["Mean-Variance Optimization", "Black-Litterman", "Coeficiente de Aversión al Riesgo γ"],
    "source": "Campbell - SAA — practitioner warning, sección 5",
},

{
    "id": "saa_nowhen_01",
    "domain": "Portfolio Management",
    "topic": "Elección de Portafolio Miópica",
    "difficulty": "Advanced",
    "mode_tags": ["bus"],
    "front": "¿Cuándo NO usar el modelo de portafolio miópico? Lista los 5 contextos críticos.",
    "back": (
        "1. **Retornos NO son IID:** si P/E, dividend yield o tasas predicen retornos, "
        "hay hedging demand que la miopía ignora\n\n"
        "2. **γ ≠ 1:** para γ > 1 (la mayoría de instituciones), el inversor quiere "
        "cubrir cambios en el opportunity set\n\n"
        "3. **Horizonte corto con constraints:** leverage limits, VaR, drawdown — "
        "la miopía asume que puedes siempre rebalancear sin fricciones\n\n"
        "4. **Liabilities convexos:** fondos de pensión, aseguradoras — "
        "el benchmark no es efectivo sino liabilities específicos\n\n"
        "5. **Presencia de jumps y crisis:** el modelo vive en tiempo continuo; "
        "en crises el tiempo es discontinuo (2008, 2020)"
    ),
    "true_false": {
        "statement": "El modelo de portafolio miópico es una buena aproximación para bancos centrales gestionando reservas internacionales.",
        "answer": False,
        "explanation": "Los bancos centrales tienen: (1) γ alto (muy conservadores), (2) liabilities específicos (importaciones, deuda), (3) restricciones regulatorias estrictas, (4) horizonte de largo plazo con predictibilidad macroeconómica. Todos estos factores violan los supuestos de la miopía."
    },
    "connections": ["Elección de Portafolio Miópica", "Hedging Demand", "IID Returns", "Time Diversification — La Falacia"],
    "source": "Campbell - SAA — secciones 1 y 5 Prompt B",
},

{
    "id": "saa_nowhen_02",
    "domain": "Portfolio Management",
    "topic": "Lognormal vs Normal Returns",
    "difficulty": "Advanced",
    "mode_tags": ["bus"],
    "front": "⚠️ ¿Por qué los modelos con retornos normales son inconsistentes en horizontes largos?",
    "back": (
        "**El problema fundamental:**\n\n"
        "Si $R_t \\sim N(\\mu, \\sigma^2)$ mensualmente, entonces $R_{1..T}$ es suma de normales → "
        "sigue siendo normal. Pero el retorno compuesto es:\n\n"
        "$$W_T = W_0 \\prod_{t=1}^T (1+R_t)$$\n\n"
        "Esto es un **producto**, no una suma. Los productos de normales no son normales.\n\n"
        "**Consecuencia práctica:**\n"
        "- Usar VaR basado en normalidad subestima pérdidas en horizontes largos\n"
        "- Los modelos de asset allocation discreto con normales son localmente válidos, "
        "no globalmente\n"
        "- La lognormal es consistente: $\\ln(W_T/W_0)$ sí es suma de normales"
    ),
    "latex": r"W_T = W_0\prod_t(1+R_t) \neq \text{normal aunque } R_t \sim N",
    "mcq": {
        "question": "¿Por qué el retorno compuesto de una estrategia no es normal aunque los retornos periódicos sí lo sean?",
        "options": [
            "A) Porque hay fat tails en los retornos periódicos",
            "B) Porque el retorno compuesto es un producto, no una suma, de variables normales",
            "C) Porque la varianza aumenta con el tiempo",
            "D) Porque los retornos tienen autocorrelación"
        ],
        "answer": "B",
        "explanation": "El teorema central del límite preserva normalidad bajo SUMAS. Pero W_T = W_0 × (1+R_1) × ... × (1+R_T) es un PRODUCTO. El logaritmo de ese producto sí es normal (lognormal), pero la riqueza terminal en sí no lo es."
    },
    "connections": ["GBM", "Continuous-Time vs Discrete-Time", "VaR"],
    "source": "Campbell - SAA — advertencia explícita, sección 1 Prompt B",
},

{
    "id": "saa_implicit_01",
    "domain": "Portfolio Management",
    "topic": "Strategic Asset Allocation",
    "difficulty": "Advanced",
    "mode_tags": ["both"],
    "front": "¿Cuál es el verdadero 'corazón' del resultado de miopía óptima según Campbell?",
    "back": (
        "No es simplemente que los retornos sean IID. El driver real es:\n\n"
        "> **Si las oportunidades de inversión no cambian de forma relevante "
        "para el consumo óptimo, entonces el horizonte no importa.**\n\n"
        "Formalmente: si la **razón consumo-riqueza** (c/W) es constante, "
        "el problema multiperiodo se separa en problemas de un período.\n\n"
        "Esto ocurre cuando:\n"
        "- Retornos IID (el caso clásico)\n"
        "- O γ = 1 (log utility), donde c/W = constante independientemente "
        "de las oportunidades de inversión\n\n"
        "**Implicación:** La miopía no es sobre el horizonte — es sobre la "
        "estacionariedad del opportunity set."
    ),
    "true_false": {
        "statement": "La razón consumo-riqueza constante es una condición suficiente para que la elección de portafolio sea miópica.",
        "answer": True,
        "explanation": "Correcto. Si c/W es constante, el problema intertemporal se descompone en problemas de un período. Esto es el verdadero mecanismo, no simplemente 'los retornos son IID'. Con log-utility, c/W es siempre constante independientemente de la estructura de retornos."
    },
    "connections": ["Elección de Portafolio Miópica", "Utilidad Logarítmica", "Epstein-Zin Utility"],
    "source": "Campbell - SAA — intuición implícita, sección 4 Prompt B",
},

]  # END CARDS
