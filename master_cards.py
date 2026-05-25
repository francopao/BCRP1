"""
QUANT MEMORIA — Master Content Library
=======================================
Hardcoded, curated content derived from:
  - Interest Rate Models (HJM, LMM, SABR, xVA chapters)
  - Stochastic Calculus foundations
  - Financial Econometrics
  - Portfolio Management & Financial Stability

Each entry is a rich card dict with ALL pedagogical layers:
  front, back, latex, intuition, derivation, code_python,
  code_matlab, graph_type, assumptions, limitations,
  connections, mcq_options, mcq_answer, true_false,
  fill_blank, exam_question, difficulty, mode_tags

mode_tags:
  "bus"  → lightweight, no paper/pen needed
  "home" → derivations, code, complex graphs
  "both" → works in either context
"""

CARDS = [

# ══════════════════════════════════════════════════════
# DOMAIN 1: STOCHASTIC CALCULUS FOUNDATIONS
# ══════════════════════════════════════════════════════

{
  "id": "sc_01",
  "domain": "Financial Engineering",
  "topic": "Brownian Motion",
  "difficulty": "Intermediate",
  "mode_tags": ["both"],
  "front": "¿Cuáles son las 4 propiedades formales del Movimiento Browniano estándar $W_t$?",
  "back": (
    "1. $W_0 = 0$\n"
    "2. **Incrementos independientes**: $W_t - W_s \\perp W_s$ para $t > s$\n"
    "3. **Incrementos estacionarios**: $W_t - W_s \\sim N(0, t-s)$\n"
    "4. **Trayectorias continuas** pero **no diferenciables** en ningún punto"
  ),
  "latex": r"W_t - W_s \sim \mathcal{N}(0,\, t-s), \quad 0 \le s < t",
  "intuition": (
    "El BM es el límite de una caminata aleatoria con pasos infinitesimales. "
    "La no-diferenciabilidad es contraintuitiva pero crucial: significa que la volatilidad "
    "instantánea es infinita, lo que hace que (dW)² = dt (variación cuadrática no nula). "
    "Esto rompe el cálculo clásico y da origen al término de Itô."
  ),
  "graph_type": "brownian_paths",
  "true_false": {
    "statement": "El Movimiento Browniano tiene variación cuadrática igual a cero.",
    "answer": False,
    "explanation": "La variación cuadrática de W_t en [0,T] es T, no cero. Esto es fundamental y diferencia al BM de funciones ordinarias."
  },
  "mcq": {
    "question": "Si $W_t$ es un BM estándar, ¿cuál es $\\text{Var}(W_5 - W_2)$?",
    "options": ["A) 2", "B) 3", "C) 5", "D) 7"],
    "answer": "B",
    "explanation": "Var(W_t - W_s) = t - s = 5 - 2 = 3. Los incrementos son N(0, t-s)."
  },
  "fill_blank": {
    "template": "La variación cuadrática del BM en [0,T] es ___, lo que implica que (dW_t)² = ___.",
    "answers": ["T", "dt"]
  },
  "connections": ["Itô's Lemma", "Stochastic Integrals", "GBM"],
  "source": "Veronesi Ch.1 / Shreve Vol.II",
},

{
  "id": "sc_02",
  "domain": "Financial Engineering",
  "topic": "Itô's Lemma",
  "difficulty": "Advanced",
  "mode_tags": ["both"],
  "front": "Enuncia el Lema de Itô para $f(S_t, t)$ donde $dS = \\mu S\\,dt + \\sigma S\\,dW$.",
  "back": (
    "$$df = \\underbrace{f_t\\,dt}_{\\text{tiempo}} "
    "+ \\underbrace{f_S\\,dS}_{\\text{delta}} "
    "+ \\underbrace{\\tfrac{1}{2}f_{SS}\\sigma^2 S^2\\,dt}_{\\text{término Itô (gamma)}}$$\n\n"
    "Expandido:\n"
    "$$df = \\left(f_t + \\mu S f_S + \\tfrac{1}{2}\\sigma^2 S^2 f_{SS}\\right)dt + \\sigma S f_S\\,dW_t$$"
  ),
  "latex": r"df = \left(f_t + \mu S f_S + \frac{1}{2}\sigma^2 S^2 f_{SS}\right)dt + \sigma S f_S\,dW_t",
  "intuition": (
    "Es la regla de la cadena para procesos estocásticos. "
    "El término extra ½σ²S²f_SS aparece porque (dW)²=dt ≠ 0, a diferencia del cálculo ordinario. "
    "Financieramente: este término ES el valor de la convexidad (gamma). "
    "Por eso las opciones valen más que una posición lineal."
  ),
  "derivation": (
    "Taylor de segundo orden: df = f_t dt + f_S dS + ½f_SS(dS)² + ...\n"
    "dS = μS dt + σS dW  →  (dS)² = σ²S²(dW)² = σ²S² dt\n"
    "Sustituyendo y tomando (dt)² → 0, dt·dW → 0:\n"
    "df = (f_t + μSf_S + ½σ²S²f_SS)dt + σSf_S dW"
  ),
  "code_python": '''\
import numpy as np

# Verificación numérica del Lema de Itô: d(ln S)
# Analítico: d(ln S) = (μ - σ²/2)dt + σ dW
# Esto explica por qué GBM tiene drift ajustado

def simulate_log_verification(mu, sigma, S0, T, n):
    dt = T / n
    S = np.zeros(n+1); S[0] = S0
    lnS = np.zeros(n+1); lnS[0] = np.log(S0)
    
    for i in range(n):
        dW = np.random.normal(0, np.sqrt(dt))
        S[i+1] = S[i] * np.exp((mu - 0.5*sigma**2)*dt + sigma*dW)
        lnS[i+1] = np.log(S[i+1])
    
    # Drift real de ln(S) ≈ μ - σ²/2
    realized_drift = (lnS[-1] - lnS[0]) / T
    theoretical   = mu - 0.5*sigma**2
    print(f"Drift realizado: {realized_drift:.4f}")
    print(f"Teórico (μ-σ²/2): {theoretical:.4f}")

simulate_log_verification(mu=0.1, sigma=0.2, S0=100, T=1, n=10000)
''',
  "code_matlab": '''\
% Verificación del Lema de Itô: d(ln S) = (mu - sigma^2/2)dt + sigma*dW
mu = 0.1; sigma = 0.2; S0 = 100; T = 1; n = 10000;
dt = T/n;
dW = sqrt(dt) * randn(1, n);
S  = S0 * cumprod(exp((mu - 0.5*sigma^2)*dt + sigma*dW));
lnS_final = log(S(end));
fprintf("ln(S_T): %.4f | Teórico: %.4f\\n", lnS_final, log(S0)+(mu-0.5*sigma^2)*T);
''',
  "graph_type": "ito_lognormal",
  "mcq": {
    "question": "Aplicando Itô a $f(S)=\\ln S$ con $dS=\\mu S\\,dt+\\sigma S\\,dW$, ¿cuál es $d(\\ln S)$?",
    "options": [
        "A) $\\mu\\,dt + \\sigma\\,dW$",
        "B) $(\\mu - \\frac{\\sigma^2}{2})\\,dt + \\sigma\\,dW$",
        "C) $(\\mu + \\frac{\\sigma^2}{2})\\,dt + \\sigma\\,dW$",
        "D) $\\frac{1}{S}dS$"
    ],
    "answer": "B",
    "explanation": "f_S=1/S, f_SS=-1/S². El término Itô contribuye -½σ² al drift. Este ajuste es el 'Itô correction'."
  },
  "true_false": {
    "statement": "En el Lema de Itô, el término de segundo orden desaparece igual que en el cálculo ordinario.",
    "answer": False,
    "explanation": "No. El término ½σ²S²f_SS dt NO desaparece porque (dW)²=dt. Esta es la diferencia fundamental con el cálculo clásico."
  },
  "connections": ["Brownian Motion", "Black-Scholes PDE", "GBM", "Martingales"],
  "source": "Veronesi Ch.1.3",
},

# ══════════════════════════════════════════════════════
# DOMAIN 2: INTEREST RATE MODELS
# ══════════════════════════════════════════════════════

{
  "id": "irm_01",
  "domain": "Interest Rate Models",
  "topic": "Vasicek Model",
  "difficulty": "Intermediate",
  "mode_tags": ["both"],
  "front": "Escribe el SDE de Vasicek. ¿Qué implica cada parámetro económicamente?",
  "back": (
    "$$dr_t = \\kappa(\\theta - r_t)\\,dt + \\sigma\\,dW_t$$\n\n"
    "- $\\kappa$: **velocidad de reversión** — qué tan rápido vuelve la tasa al equilibrio\n"
    "- $\\theta$: **tasa de largo plazo** (media incondicional)\n"
    "- $\\sigma$: **volatilidad** de la tasa corta\n\n"
    "Distribución: $r_t | r_0 \\sim N\\left(\\theta + (r_0-\\theta)e^{-\\kappa t},\\; \\frac{\\sigma^2}{2\\kappa}(1-e^{-2\\kappa t})\\right)$"
  ),
  "latex": r"dr_t = \kappa(\theta - r_t)\,dt + \sigma\,dW_t",
  "intuition": (
    "Las tasas de interés no pueden crecer indefinidamente ni colapsar a -∞ permanentemente — "
    "existe un equilibrio macroeconómico de largo plazo θ. "
    "κ mide la 'elasticidad' de la tasa hacia ese equilibrio. "
    "Si κ es muy pequeño, la tasa tarda mucho en revertir (persistencia alta). "
    "La distribución normal permite tasas negativas — que parecía un defecto hasta que Europa/Japón lo hicieron realidad."
  ),
  "graph_type": "vasicek_simulation",
  "code_python": '''\
import numpy as np
import matplotlib.pyplot as plt

def vasicek_paths(r0, kappa, theta, sigma, T, n_steps, n_paths, seed=42):
    """Simula trayectorias del modelo Vasicek (Euler-Maruyama)."""
    np.random.seed(seed)
    dt = T / n_steps
    r  = np.zeros((n_paths, n_steps + 1))
    r[:, 0] = r0
    for t in range(1, n_steps + 1):
        dW = np.random.normal(0, np.sqrt(dt), n_paths)
        r[:, t] = r[:, t-1] + kappa*(theta - r[:, t-1])*dt + sigma*dW
    return r

r = vasicek_paths(r0=0.03, kappa=0.5, theta=0.05, sigma=0.015, T=10, n_steps=500, n_paths=5)
t = np.linspace(0, 10, 501)
for path in r:
    plt.plot(t, path*100, alpha=0.7)
plt.axhline(5, color="red", linestyle="--", label="θ = 5%")
plt.xlabel("Años"); plt.ylabel("Tasa corta (%)"); plt.legend()
plt.title("Vasicek: reversión a la media"); plt.tight_layout()
''',
  "code_matlab": '''\
% Vasicek - Euler-Maruyama
r0=0.03; kappa=0.5; theta=0.05; sigma=0.015; T=10; N=500; M=5;
dt=T/N; t=linspace(0,T,N+1);
r=zeros(M,N+1); r(:,1)=r0;
for i=2:N+1
    dW=sqrt(dt)*randn(M,1);
    r(:,i)=r(:,i-1)+kappa*(theta-r(:,i-1))*dt+sigma*dW;
end
plot(t, r\'*100); hold on;
yline(theta*100,\'r--\',\'theta\'); xlabel(\'Years\'); ylabel(\'Rate (%)\');
title(\'Vasicek Short Rate Paths\');
''',
  "mcq": {
    "question": "En Vasicek, si $r_t > \\theta$, ¿qué ocurre con el drift?",
    "options": [
        "A) Es positivo → la tasa sigue subiendo",
        "B) Es negativo → la tasa tiende a bajar hacia θ",
        "C) Es cero → la tasa se estabiliza inmediatamente",
        "D) Depende solo de σ"
    ],
    "answer": "B",
    "explanation": "κ(θ - r_t) < 0 cuando r_t > θ. El drift negativo jala la tasa hacia abajo. Esto es la reversión a la media."
  },
  "true_false": {
    "statement": "El modelo Vasicek garantiza tasas de interés siempre positivas.",
    "answer": False,
    "explanation": "No. Al ser distribución normal, permite tasas negativas. El modelo CIR resuelve esto con difusión √r_t."
  },
  "fill_blank": {
    "template": "En Vasicek, la varianza incondicional de largo plazo es ___.",
    "answers": ["σ²/(2κ)"]
  },
  "exam_question": (
    "Dado κ=0.4, θ=0.05, σ=0.02, r₀=0.08:\n"
    "a) Calcule E[r₁] y Var(r₁)\n"
    "b) ¿En qué dirección va el drift en t=0? ¿Por qué?\n"
    "c) ¿Cuál es la distribución límite (t→∞)?\n"
    "d) ¿Qué implica κ pequeño para la estructura temporal?"
  ),
  "assumptions": "κ, θ, σ constantes. Proceso de Ornstein-Uhlenbeck. Mercado completo con un factor.",
  "limitations": "Tasas negativas posibles. No calibra curva inicial exactamente (Hull-White lo resuelve). σ constante.",
  "connections": ["CIR Model", "Hull-White Model", "HJM Framework", "Yield Curve"],
  "source": "Veronesi Ch.5",
},

{
  "id": "irm_02",
  "domain": "Interest Rate Models",
  "topic": "Cox-Ingersoll-Ross (CIR)",
  "difficulty": "Intermediate",
  "mode_tags": ["both"],
  "front": "¿Cómo evita el modelo CIR las tasas negativas? Escribe el SDE y la condición de Feller.",
  "back": (
    "$$dr_t = \\kappa(\\theta - r_t)\\,dt + \\sigma\\sqrt{r_t}\\,dW_t$$\n\n"
    "**Condición de Feller:** $2\\kappa\\theta > \\sigma^2$\n\n"
    "→ Si se cumple, $r_t > 0$ con probabilidad 1\n\n"
    "**Distribución:** no-central chi-cuadrado (analítica)\n\n"
    "**Precio de bono:** $P(t,T) = A(t,T)\\,e^{-B(t,T)r_t}$ (forma afín)"
  ),
  "latex": r"dr_t = \kappa(\theta - r_t)\,dt + \sigma\sqrt{r_t}\,dW_t",
  "intuition": (
    "La difusión √r_t se apaga cuando r_t → 0, haciendo que el drift positivo κθ domine. "
    "Cuando la tasa está cerca de cero, el proceso se empuja hacia arriba y no puede cruzar. "
    "Es como un resorte que se vuelve más fuerte cuanto más cerca está del suelo."
  ),
  "graph_type": "cir_vs_vasicek",
  "mcq": {
    "question": "¿Cuál es la condición de Feller en CIR para garantizar r_t > 0 a.s.?",
    "options": [
        "A) $2\\kappa\\theta < \\sigma^2$",
        "B) $2\\kappa\\theta > \\sigma^2$",
        "C) $\\kappa > \\sigma$",
        "D) $\\theta > \\sigma^2$"
    ],
    "answer": "B",
    "explanation": "2κθ > σ² garantiza que el proceso de difusión cuadrada (χ²-no-central) nunca toca cero."
  },
  "true_false": {
    "statement": "CIR y Vasicek pertenecen ambos a la familia de modelos afines de estructura temporal.",
    "answer": True,
    "explanation": "Sí. En ambos, el precio del bono tiene forma P(t,T) = exp(A - B·r_t), lo que los clasifica como Affine Term Structure Models (ATSM)."
  },
  "connections": ["Vasicek Model", "Affine Term Structure Models", "Hull-White Model"],
  "source": "Veronesi Ch.5 / Brigo-Mercurio",
},

{
  "id": "irm_03",
  "domain": "Interest Rate Models",
  "topic": "Hull-White Model",
  "difficulty": "Advanced",
  "mode_tags": ["both"],
  "front": "¿Cuál es la ventaja clave del modelo Hull-White sobre Vasicek? Escribe su SDE.",
  "back": (
    "$$dr_t = [\\theta(t) - \\kappa r_t]\\,dt + \\sigma\\,dW_t$$\n\n"
    "**Ventaja clave:** $\\theta(t)$ es una **función del tiempo** calibrada para reproducir "
    "exactamente la curva de tasas observada en el mercado.\n\n"
    "Vasicek solo tiene $\\theta$ constante → no puede ajustar la curva inicial.\n\n"
    "Hull-White = **Vasicek extendido** = Ho-Lee con reversión a la media."
  ),
  "latex": r"dr_t = [\theta(t) - \kappa r_t]\,dt + \sigma\,dW_t",
  "intuition": (
    "Vasicek dice 'las tasas revierten a un nivel constante θ'. "
    "Pero en la realidad, la curva de tasas de hoy ya contiene información sobre niveles futuros. "
    "Hull-White calibra θ(t) para que el modelo reproduzca exactamente los precios de bonos observados. "
    "Esto lo hace el modelo estándar para pricing de derivados de tasa en la práctica."
  ),
  "mcq": {
    "question": "¿Por qué Hull-White puede calibrar exactamente la curva de tasas inicial y Vasicek no?",
    "options": [
        "A) Hull-White tiene volatilidad estocástica",
        "B) Hull-White usa θ(t) función del tiempo, no constante",
        "C) Hull-White no permite reversión a la media",
        "D) Hull-White es un modelo multi-factor"
    ],
    "answer": "B",
    "explanation": "θ(t) es determinista pero dependiente del tiempo. Se calibra numéricamente para que P(0,T) del modelo = P(0,T) del mercado para todo T."
  },
  "true_false": {
    "statement": "El modelo Ho-Lee es un caso especial de Hull-White con κ=0.",
    "answer": True,
    "explanation": "Con κ=0, no hay reversión: dr = θ(t)dt + σ dW. Esto es exactamente Ho-Lee (Veronesi Cap.4.3.1)."
  },
  "connections": ["Vasicek Model", "HJM Framework", "Ho-Lee Model", "Yield Curve Construction"],
  "source": "Veronesi Ch.4.3.2 / Ch.5.4",
},

{
  "id": "irm_04",
  "domain": "Interest Rate Models",
  "topic": "HJM Framework",
  "difficulty": "Expert",
  "mode_tags": ["home"],
  "front": "Enuncia la condición de no-arbitraje HJM para la dinámica de las forward rates.",
  "back": (
    "HJM modela directamente las **forward rates** $f(t,T)$:\n\n"
    "$$df(t,T) = \\alpha(t,T)\\,dt + \\sigma(t,T)\\,dW_t$$\n\n"
    "**Condición de no-arbitraje (drift restriction):**\n\n"
    "$$\\alpha(t,T) = \\sigma(t,T)\\int_t^T \\sigma(t,s)\\,ds$$\n\n"
    "Bajo la medida de riesgo neutro, el drift está completamente determinado por la volatilidad. "
    "No hay libertad en α — solo en σ(t,T)."
  ),
  "latex": r"\alpha(t,T) = \sigma(t,T)\int_t^T \sigma(t,s)\,ds",
  "intuition": (
    "En HJM no se modela la tasa corta directamente, sino toda la curva forward de una vez. "
    "El insight genial: bajo no-arbitraje, una vez que eliges cómo va a fluctuar la curva (σ), "
    "el drift queda completamente determinado. "
    "Vasicek, CIR y Hull-White son casos especiales de HJM con estructuras σ específicas."
  ),
  "derivation": (
    "1. El precio del bono: P(t,T) = exp(-∫_t^T f(t,s)ds)\n"
    "2. Aplicar Itô a P(t,T)\n"
    "3. Exigir que P(t,T)/B(t) sea martingala bajo Q (no-arbitraje)\n"
    "4. Igualar el drift a cero → condición HJM"
  ),
  "exam_question": (
    "a) ¿Por qué HJM es un 'framework' y no un 'modelo'?\n"
    "b) ¿Qué modelo de tasa corta emerge cuando σ(t,T) = σ·e^{-κ(T-t)}?\n"
    "c) Explique el problema de 'explosión' en algunos modelos HJM."
  ),
  "mcq": {
    "question": "En HJM bajo medida de riesgo neutro, ¿qué determina completamente el drift α(t,T)?",
    "options": [
        "A) Las condiciones iniciales del mercado",
        "B) La función de volatilidad σ(t,T)",
        "C) La tasa corta r_t",
        "D) El precio de los swaps"
    ],
    "answer": "B",
    "explanation": "La restricción de drift HJM: α(t,T) = σ(t,T)∫_t^T σ(t,s)ds. El drift no es libre — lo dicta σ."
  },
  "connections": ["Hull-White Model", "LIBOR Market Model", "Forward Rates", "Vasicek Model"],
  "source": "Veronesi Ch.4",
},

{
  "id": "irm_05",
  "domain": "Interest Rate Models",
  "topic": "LIBOR Market Model",
  "difficulty": "Expert",
  "mode_tags": ["home"],
  "front": "¿Cuál es la dinámica del LMM (BGM) bajo la medida forward $Q^{T_{i+1}}$?",
  "back": (
    "$$dL_i(t) = L_i(t)\\,\\sigma_i(t)\\,dW_t^{T_{i+1}}$$\n\n"
    "Donde $L_i(t)$ es la **tasa LIBOR forward** para el período $[T_i, T_{i+1}]$.\n\n"
    "Bajo la **spot LIBOR measure**, la dinámica se convierte en:\n\n"
    "$$dL_i = L_i\\left(-\\sum_{j=\\beta(t)}^{i} \\frac{\\delta_j L_j \\rho_{ij}\\sigma_j\\sigma_i}{1+\\delta_j L_j}\\,dt + \\sigma_i\\,dW\\right)$$\n\n"
    "**Key result:** Las tasas LIBOR tienen distribución **lognormal** bajo su medida forward → "
    "la fórmula de Black aplica exactamente para caps/floors."
  ),
  "latex": r"dL_i(t) = L_i(t)\,\sigma_i(t)\,dW_t^{T_{i+1}}",
  "intuition": (
    "El LMM resolvió el gran problema de los '90: los traders usaban la fórmula de Black para "
    "caps y swaptions, pero no existía un modelo consistente que la justificara. "
    "El LMM/BGM construyó ese modelo: cada tasa LIBOR es lognormal bajo su propia medida forward. "
    "El precio de caps sale exacto con Black. Para swaptions requiere aproximación."
  ),
  "mcq": {
    "question": "¿Por qué el LMM puede pricear caps exactamente con la fórmula de Black pero swaptions solo aproximadamente?",
    "options": [
        "A) Porque los caps son más líquidos",
        "B) Las tasas LIBOR son lognormales bajo su medida forward, pero la swap rate no lo es simultáneamente",
        "C) Porque los swaptions tienen mayor duración",
        "D) El LMM no puede pricear swaptions"
    ],
    "answer": "B",
    "explanation": "No se puede tener todas las tasas LIBOR lognormales Y la swap rate lognormal al mismo tiempo. Por eso swaptions requieren aproximaciones (Rebonato, Hull-White)."
  },
  "true_false": {
    "statement": "En el LMM, la dinámica de L_i bajo su propia medida forward no tiene término de drift.",
    "answer": True,
    "explanation": "Bajo Q^{T_{i+1}}, L_i(t) es una martingala: dL_i = L_i σ_i dW^{T_{i+1}}. El drift es cero."
  },
  "connections": ["HJM Framework", "Cap Pricing", "Swaption Pricing", "Forward Measure", "SABR Model"],
  "source": "Veronesi Ch.6",
},

{
  "id": "irm_06",
  "domain": "Interest Rate Models",
  "topic": "SABR Model",
  "difficulty": "Expert",
  "mode_tags": ["both"],
  "front": "Escribe el sistema de SDEs del modelo SABR. ¿Por qué es importante en la práctica?",
  "back": (
    "$$dF_t = \\sigma_t F_t^\\beta\\,dW_t^1$$\n"
    "$$d\\sigma_t = \\alpha\\sigma_t\\,dW_t^2$$\n"
    "$$dW_t^1\\cdot dW_t^2 = \\rho\\,dt$$\n\n"
    "**Parámetros:**\n"
    "- $\\beta \\in [0,1]$: elasticidad (β=0: normal, β=1: lognormal)\n"
    "- $\\alpha$: vol-of-vol\n"
    "- $\\rho$: correlación forward-vol (suele ser negativa en equity)\n\n"
    "**Importancia:** Genera una **sonrisa de volatilidad implícita** analítica (fórmula Hagan et al.)"
  ),
  "latex": r"dF = \sigma F^\beta dW^1, \quad d\sigma = \alpha\sigma dW^2, \quad dW^1 dW^2 = \rho\,dt",
  "intuition": (
    "Black-Scholes asume volatilidad constante → smile plano. "
    "La realidad muestra una sonrisa: las opciones OTM tienen mayor vol implícita. "
    "SABR hace que la volatilidad misma sea estocástica (vol-of-vol = α). "
    "La correlación ρ inclina la sonrisa (skew). El parámetro β controla la forma del backbone. "
    "El gran avance: existe una fórmula analítica aproximada para la vol implícita."
  ),
  "graph_type": "sabr_smile",
  "mcq": {
    "question": "En el modelo SABR, ¿qué parámetro controla principalmente el skew (asimetría) de la sonrisa de volatilidad?",
    "options": [
        "A) β (elasticidad)",
        "B) α (vol-of-vol)",
        "C) ρ (correlación forward-volatilidad)",
        "D) F₀ (forward inicial)"
    ],
    "answer": "C",
    "explanation": "ρ < 0 produce skew negativo (put OTM más caros). ρ > 0 produce skew positivo. β también afecta el skew pero ρ es el driver principal."
  },
  "true_false": {
    "statement": "En SABR con β=1, el forward F sigue un proceso lognormal puro (como GBM).",
    "answer": False,
    "explanation": "Con β=1, dF = σF dW¹, pero σ es estocástica (d σ = ασ dW²). No es GBM puro porque la volatilidad fluctúa."
  },
  "connections": ["LIBOR Market Model", "Volatility Smile", "Cap Pricing", "Swaption Pricing"],
  "source": "Veronesi Ch.10",
},

{
  "id": "irm_07",
  "domain": "Interest Rate Models",
  "topic": "Affine Term Structure Models",
  "difficulty": "Advanced",
  "mode_tags": ["home"],
  "front": "¿Qué define a un modelo de estructura temporal afín (ATSM)? ¿Por qué son útiles?",
  "back": (
    "Un ATSM satisface que el precio del bono tiene la forma:\n\n"
    "$$P(t,T) = \\exp\\left(A(t,T) - B(t,T)^\\top X_t\\right)$$\n\n"
    "donde $X_t$ es el vector de factores y $A, B$ satisfacen las **ecuaciones de Riccati**.\n\n"
    "**Condición:** drift y varianza de $X_t$ deben ser afines en $X_t$.\n\n"
    "**Ejemplos:** Vasicek (A₀(1)), CIR (A₁(1)), modelos multifactor $A_m(n)$."
  ),
  "latex": r"P(t,T) = \exp\!\left(A(t,T) - \mathbf{B}(t,T)^\top \mathbf{X}_t\right)",
  "intuition": (
    "Los ATSM son el 'modelo estándar' de la academia porque tienen soluciones analíticas. "
    "La forma exponencial-afín viene del hecho de que la función generadora de momentos de "
    "distribuciones afines es exponencial-cuadrática. "
    "La clasificación A_m(n) de Dai-Singleton: n factores, m con varianza estocástica."
  ),
  "mcq": {
    "question": "¿Cuál de estas NO es una propiedad de los ATSM?",
    "options": [
        "A) Precio de bonos en forma cerrada",
        "B) La yield curve es lineal en los factores X_t",
        "C) Siempre garantizan tasas positivas",
        "D) Los factores siguen procesos con drift y varianza afines"
    ],
    "answer": "C",
    "explanation": "Vasicek es ATSM y permite tasas negativas. CIR garantiza positividad con la condición de Feller, pero no todos los ATSM la tienen."
  },
  "connections": ["Vasicek Model", "CIR Model", "HJM Framework", "Riccati Equations"],
  "source": "Veronesi Ch.9",
},

# ══════════════════════════════════════════════════════
# DOMAIN 3: FINANCIAL ECONOMETRICS
# ══════════════════════════════════════════════════════

{
  "id": "eco_01",
  "domain": "Financial Econometrics",
  "topic": "GARCH Models",
  "difficulty": "Intermediate",
  "mode_tags": ["both"],
  "front": "GARCH(1,1): escribe el modelo completo. ¿Qué es la persistencia y qué implica?",
  "back": (
    "$r_t = \\mu + \\epsilon_t$, $\\;\\epsilon_t = \\sigma_t z_t$, $\\;z_t \\sim N(0,1)$\n\n"
    "$$\\sigma_t^2 = \\omega + \\alpha\\epsilon_{t-1}^2 + \\beta\\sigma_{t-1}^2$$\n\n"
    "**Persistencia:** $\\pi = \\alpha + \\beta$\n\n"
    "- $\\pi < 1$: varianza estacionaria\n"
    "- $\\pi \\to 1$: shocks de volatilidad son permanentes (IGARCH)\n"
    "- Varianza incondicional: $\\bar{\\sigma}^2 = \\omega/(1-\\alpha-\\beta)$\n\n"
    "**Half-life de un shock:** $t_{1/2} = \\ln(0.5)/\\ln(\\pi)$"
  ),
  "latex": r"\sigma_t^2 = \omega + \alpha\epsilon_{t-1}^2 + \beta\sigma_{t-1}^2",
  "intuition": (
    "α capta la reacción: qué tanto sube la volatilidad tras un shock grande. "
    "β capta la memoria: qué tan lento decae la volatilidad elevada. "
    "En acciones típicamente α≈0.05-0.10 y β≈0.85-0.90, dando π≈0.95. "
    "Eso significa que un shock de volatilidad tiene una vida media de ≈14 días."
  ),
  "graph_type": "garch_volatility",
  "code_python": '''\
# GARCH(1,1) manual para entender el mecanismo
import numpy as np

def garch_filter(returns, omega, alpha, beta):
    """Filtra la varianza condicional GARCH(1,1)."""
    T = len(returns)
    sigma2 = np.zeros(T)
    sigma2[0] = np.var(returns)  # inicializar en varianza incondicional
    
    for t in range(1, T):
        sigma2[t] = omega + alpha * returns[t-1]**2 + beta * sigma2[t-1]
    return sigma2

# Ejemplo con retornos simulados
np.random.seed(42)
T = 1000
# Parámetros típicos de equity
omega, alpha, beta = 0.00001, 0.08, 0.90
persistence = alpha + beta
print(f"Persistencia: {persistence:.2f}")
print(f"Varianza incondicional: {omega/(1-alpha-beta)*252:.4f} (anualizada)")
halflife = np.log(0.5) / np.log(persistence)
print(f"Half-life del shock: {halflife:.1f} días")
''',
  "mcq": {
    "question": "En un GARCH(1,1) con α=0.08, β=0.90. ¿Cuál es la varianza incondicional si ω=0.00002?",
    "options": [
        "A) 0.00002",
        "B) 0.001",
        "C) 0.00002/0.02 = 0.001",
        "D) No existe (proceso no estacionario)"
    ],
    "answer": "C",
    "explanation": "σ² = ω/(1-α-β) = 0.00002/(1-0.98) = 0.00002/0.02 = 0.001. La persistencia es 0.98 < 1, así que existe."
  },
  "true_false": {
    "statement": "En GARCH(1,1), si α+β=1, el proceso tiene varianza incondicional finita.",
    "answer": False,
    "explanation": "Con α+β=1 (IGARCH), la varianza incondicional es infinita. Los shocks son permanentes y el proceso no es covarianza-estacionario."
  },
  "connections": ["ARCH Models", "Volatility Clustering", "GJR-GARCH", "Stochastic Volatility"],
  "source": "Tsay - Analysis of Financial Time Series",
},

# ══════════════════════════════════════════════════════
# DOMAIN 4: PORTFOLIO MANAGEMENT
# ══════════════════════════════════════════════════════

{
  "id": "pm_01",
  "domain": "Portfolio Management",
  "topic": "Mean-Variance Optimization",
  "difficulty": "Intermediate",
  "mode_tags": ["both"],
  "front": "¿Qué es la frontera eficiente de Markowitz y cómo se construye?",
  "back": (
    "La **frontera eficiente** es el conjunto de portafolios que:\n"
    "- **Minimizan la varianza** para cada nivel de retorno esperado, O\n"
    "- **Maximizan el retorno** para cada nivel de varianza\n\n"
    "Se construye resolviendo para distintos $\\mu_p$:\n"
    "$$\\min_{\\mathbf{w}} \\mathbf{w}^\\top\\Sigma\\mathbf{w} \\quad \\text{s.t.} \\quad "
    "\\mathbf{w}^\\top\\boldsymbol{\\mu}=\\mu_p,\\; \\mathbf{w}^\\top\\mathbf{1}=1$$\n\n"
    "El **portafolio de mínima varianza global** (GMV) es el extremo izquierdo."
  ),
  "latex": r"\min_w \mathbf{w}^\top\Sigma\mathbf{w} \;\text{ s.t. }\; \mathbf{w}^\top\mu=\mu_p,\; \mathbf{1}^\top\mathbf{w}=1",
  "graph_type": "efficient_frontier",
  "intuition": (
    "La frontera eficiente muestra el trade-off riesgo/retorno óptimo. "
    "Ningún portafolio racional debería estar por debajo de la frontera. "
    "El problema práctico: Σ⁻¹ amplifica errores de estimación enormemente. "
    "En la práctica se usa shrinkage (Ledoit-Wolf), Black-Litterman, o restricciones de peso."
  ),
  "mcq": {
    "question": "¿Cuál portafolio sobre la frontera eficiente elige un inversor con aversión al riesgo infinita?",
    "options": [
        "A) El portafolio tangente",
        "B) El portafolio de máximo Sharpe ratio",
        "C) El portafolio de mínima varianza global (GMV)",
        "D) Un portafolio igualmente ponderado"
    ],
    "answer": "C",
    "explanation": "Aversión infinita → minimizar varianza independientemente del retorno → portafolio GMV."
  },
  "true_false": {
    "statement": "El portafolio tangente maximiza el Sharpe ratio y está sobre la frontera eficiente.",
    "answer": True,
    "explanation": "Correcto. El portafolio tangente es el punto donde la línea desde la tasa libre de riesgo es tangente a la frontera. Es único y maximiza el Sharpe ratio."
  },
  "connections": ["CAPM", "Factor Models", "Risk Measures", "Black-Litterman"],
  "source": "Fabozzi - Robust Portfolio Optimization",
},

# ══════════════════════════════════════════════════════
# DOMAIN 5: FINANCIAL STABILITY
# ══════════════════════════════════════════════════════

{
  "id": "fs_01",
  "domain": "Financial Stability",
  "topic": "Systemic Risk Measures",
  "difficulty": "Advanced",
  "mode_tags": ["both"],
  "front": "Define CoVaR y MES. ¿Cómo los usa un banco central para identificar riesgo sistémico?",
  "back": (
    "**ΔCoVaR** (Adrian & Brunnermeier 2011):\n"
    "$$\\Delta\\text{CoVaR}_q^i = \\text{CoVaR}_q^{i|j=\\text{VaR}} - \\text{CoVaR}_q^{i|j=\\text{mediana}}$$\n"
    "→ Contribución marginal de la institución j al riesgo del sistema\n\n"
    "**MES** (Acharya et al. 2012):\n"
    "$$\\text{MES}_i = E[r_i \\mid r_m < \\text{VaR}_q^m]$$\n"
    "→ Pérdida esperada de i cuando el sistema cae\n\n"
    "**Uso del BC:** rankear instituciones por contribución sistémica → calibrar surcharges de capital (D-SIB)"
  ),
  "latex": r"\text{MES}_i = \mathbb{E}[r_i \mid r_m < \text{VaR}_q^m]",
  "mcq": {
    "question": "¿Cuál es la diferencia conceptual entre CoVaR y MES?",
    "options": [
        "A) CoVaR mide riesgo individual; MES mide riesgo sistémico",
        "B) CoVaR mide spillover desde una firma; MES mide exposición al colapso sistémico",
        "C) Son equivalentes matemáticamente",
        "D) CoVaR es para bancos; MES para aseguradoras"
    ],
    "answer": "B",
    "explanation": "CoVaR: ¿cuánto sufre el sistema si la firma X colapsa? MES: ¿cuánto sufre la firma X si el sistema colapsa? Perspectivas opuestas."
  },
  "true_false": {
    "statement": "Una institución con VaR individual bajo nunca puede tener alto riesgo sistémico.",
    "answer": False,
    "explanation": "Una firma puede ser segura individualmente pero altamente interconectada (TBTF). Lehman tenía VaR 'manejable' individualmente pero era sistémicamente crítico."
  },
  "connections": ["Macroprudential Policy", "Basel III", "SIFI", "Network Contagion"],
  "source": "Adrian & Brunnermeier (2011) AER",
},

]  # END CARDS


def get_all_cards():
    return CARDS

def get_cards_by_domain(domain: str):
    return [c for c in CARDS if c["domain"] == domain]

def get_cards_by_topic(topic: str):
    return [c for c in CARDS if c["topic"] == topic]

def get_bus_cards():
    """Cards suitable for commute study (both or bus tagged)."""
    return [c for c in CARDS if any(t in c.get("mode_tags", []) for t in ("bus", "both"))]

def get_home_cards():
    """All cards including heavy derivations."""
    return CARDS

def get_cards_with_graphs():
    return [c for c in CARDS if c.get("graph_type")]
