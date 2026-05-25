"""
Seed Data: Curated Quantitative Finance Flashcards
====================================================
High-quality starter deck covering all five domains.
Run this once to populate the library.
"""

from core.card_model import Flashcard, Domain, CardType, DifficultyLevel
from core.store import CardStore

SEED_CARDS = [

    # ── FINANCIAL ENGINEERING ─────────────────────────────────────────

    Flashcard(
        domain="Financial Engineering",
        topic="Black-Scholes Model",
        card_type=CardType.FORMULA,
        difficulty=DifficultyLevel.INTERMEDIATE,
        front="Write the Black-Scholes PDE and explain what each term represents.",
        back=(
            "$$\\frac{\\partial V}{\\partial t} + \\frac{1}{2}\\sigma^2 S^2 \\frac{\\partial^2 V}{\\partial S^2} "
            "+ rS\\frac{\\partial V}{\\partial S} - rV = 0$$\n\n"
            "**Terms:**\n"
            "- $\\partial V/\\partial t$: time decay (theta)\n"
            "- $\\frac{1}{2}\\sigma^2 S^2 V_{SS}$: convexity gain (gamma)\n"
            "- $rS V_S$: drift of underlying\n"
            "- $rV$: risk-free discounting"
        ),
        latex_formula=r"\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0",
        intuition=(
            "The PDE says: **options are locally risk-free**. "
            "The gamma gain from convexity exactly offsets the theta decay at the risk-free rate. "
            "This is the Black-Scholes 'magic': you can hedge perfectly in continuous time."
        ),
        derivation=(
            "1. Construct a delta-hedged portfolio Π = V − ΔS\n"
            "2. Apply Itô's lemma to V(S,t)\n"
            "3. Set dΠ = rΠ dt (no-arbitrage, risk-free return)\n"
            "4. Choose Δ = ∂V/∂S to eliminate stochastic term\n"
            "5. Collect terms → BS PDE"
        ),
        assumptions=(
            "• Geometric Brownian Motion for S\n"
            "• Constant σ, r\n"
            "• No dividends\n"
            "• Continuous trading, no transaction costs\n"
            "• European exercise only"
        ),
        limitations=(
            "• Volatility smile violates constant σ assumption\n"
            "• Fat tails in real returns\n"
            "• Cannot handle jumps (Merton extension needed)\n"
            "• Continuous hedging is impossible in practice"
        ),
        code_snippet='''import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Black-Scholes closed-form option price.
    S: spot, K: strike, T: maturity, r: rate, sigma: vol
    """
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == "call":
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

# Example
price = black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2)
print(f"Call price: {price:.4f}")''',
        connections=["Itô's Lemma", "Risk-Neutral Pricing", "Greeks & Sensitivities"],
        tags=["black-scholes", "PDE", "options", "pricing", "derivatives"],
        source="Hull - Options, Futures & Other Derivatives"
    ),

    Flashcard(
        domain="Financial Engineering",
        topic="Stochastic Calculus & Itô's Lemma",
        card_type=CardType.FORMULA,
        difficulty=DifficultyLevel.ADVANCED,
        front="State Itô's Lemma for a function f(S,t) where S follows GBM.",
        back=(
            "If $dS = \\mu S\\,dt + \\sigma S\\,dW_t$, then for $f(S,t)$:\n\n"
            "$$df = \\left(\\frac{\\partial f}{\\partial t} + \\mu S\\frac{\\partial f}{\\partial S} "
            "+ \\frac{1}{2}\\sigma^2 S^2 \\frac{\\partial^2 f}{\\partial S^2}\\right)dt "
            "+ \\sigma S\\frac{\\partial f}{\\partial S}dW_t$$\n\n"
            "The key insight: the **second-order term** $\\frac{1}{2}\\sigma^2 S^2 f_{SS}$ "
            "arises because $(dW_t)^2 = dt$ (quadratic variation of BM)."
        ),
        latex_formula=r"df = \left(f_t + \mu S f_S + \frac{1}{2}\sigma^2 S^2 f_{SS}\right)dt + \sigma S f_S\,dW_t",
        intuition=(
            "Itô's Lemma is the **chain rule for stochastic processes**. "
            "Unlike ordinary calculus, you keep the second-order term because Brownian motion "
            "has non-zero quadratic variation: (dW)² = dt. "
            "This extra term is why options have value through convexity (gamma)."
        ),
        assumptions="• Continuous semimartingale process\n• f twice continuously differentiable",
        connections=["Black-Scholes Model", "Martingales & Risk-Neutral Pricing"],
        tags=["ito", "stochastic calculus", "GBM", "brownian motion"],
        source="Shreve - Stochastic Calculus for Finance II"
    ),

    Flashcard(
        domain="Financial Engineering",
        topic="Martingales & Risk-Neutral Pricing",
        card_type=CardType.CONCEPT,
        difficulty=DifficultyLevel.ADVANCED,
        front="What is the Fundamental Theorem of Asset Pricing (FTAP)? State both parts.",
        back=(
            "**Part 1:** A market is arbitrage-free if and only if there exists at least one "
            "**Equivalent Martingale Measure (EMM)** Q ~ P.\n\n"
            "**Part 2:** The market is complete if and only if the EMM is **unique**.\n\n"
            "Under Q: $\\tilde{S}_t = e^{-rt}S_t$ is a martingale, and\n"
            "$$V_0 = e^{-rT}\\mathbb{E}^Q[V_T]$$"
        ),
        intuition=(
            "Under the real-world measure P, investors demand risk premia. "
            "The risk-neutral measure Q tweaks probabilities so that all assets grow at r. "
            "This lets us price by taking expectations — no equilibrium model needed. "
            "The Radon-Nikodym derivative dQ/dP is the **Girsanov kernel** (market price of risk)."
        ),
        connections=["Black-Scholes Model", "Stochastic Calculus & Itô's Lemma"],
        tags=["martingale", "risk-neutral", "FTAP", "no-arbitrage", "EMM"],
        source="Shreve - Stochastic Calculus for Finance II"
    ),

    # ── INTEREST RATE MODELS ──────────────────────────────────────────

    Flashcard(
        domain="Interest Rate Models",
        topic="Vasicek Model",
        card_type=CardType.FORMULA,
        difficulty=DifficultyLevel.INTERMEDIATE,
        front="Write the Vasicek short rate SDE. What is mean reversion and why does it matter?",
        back=(
            "$$dr_t = \\kappa(\\theta - r_t)\\,dt + \\sigma\\,dW_t$$\n\n"
            "- $\\kappa > 0$: speed of mean reversion\n"
            "- $\\theta$: long-run mean\n"
            "- $\\sigma$: volatility\n\n"
            "**Mean Reversion:** When $r_t > \\theta$, drift is negative (rate pulled down). "
            "When $r_t < \\theta$, drift is positive. This prevents rates drifting to ±∞."
        ),
        latex_formula=r"dr_t = \kappa(\theta - r_t)\,dt + \sigma\,dW_t",
        intuition=(
            "Interest rates in reality revert to long-run economic equilibria. "
            "Vasicek captures this with an Ornstein-Uhlenbeck process. "
            "The model is analytically tractable (affine structure) but allows negative rates — "
            "this was a 'flaw' until negative rates became reality in Europe/Japan."
        ),
        code_snippet='''import numpy as np

def simulate_vasicek(r0, kappa, theta, sigma, T, n_steps, n_paths):
    """Simulate Vasicek short rate paths via Euler-Maruyama."""
    dt = T / n_steps
    rates = np.zeros((n_paths, n_steps + 1))
    rates[:, 0] = r0
    for t in range(1, n_steps + 1):
        dW = np.random.normal(0, np.sqrt(dt), n_paths)
        rates[:, t] = (rates[:, t-1]
                       + kappa * (theta - rates[:, t-1]) * dt
                       + sigma * dW)
    return rates

paths = simulate_vasicek(r0=0.03, kappa=0.5, theta=0.05,
                          sigma=0.01, T=5, n_steps=252, n_paths=100)''',
        assumptions=(
            "• Constant κ, θ, σ\n"
            "• Risk-neutral dynamics specified\n"
            "• Negative rates possible (not bounded below)"
        ),
        limitations=(
            "• Negative rates (CIR fixes this)\n"
            "• Cannot fit initial term structure exactly (Hull-White extends)\n"
            "• Constant volatility (doesn't match vol smile)"
        ),
        connections=["Cox-Ingersoll-Ross (CIR)", "Hull-White Model", "Yield Curve Construction"],
        tags=["vasicek", "short rate", "mean reversion", "interest rates", "OU process"],
        source="Brigo & Mercurio - Interest Rate Models"
    ),

    Flashcard(
        domain="Interest Rate Models",
        topic="Cox-Ingersoll-Ross (CIR)",
        card_type=CardType.FORMULA,
        difficulty=DifficultyLevel.INTERMEDIATE,
        front="How does CIR fix Vasicek's negative rate problem? Write the SDE.",
        back=(
            "$$dr_t = \\kappa(\\theta - r_t)\\,dt + \\sigma\\sqrt{r_t}\\,dW_t$$\n\n"
            "The $\\sqrt{r_t}$ diffusion term ensures:\n"
            "- When $r_t \\to 0$, volatility $\\to 0$ → rates can't go negative\n"
            "- **Feller condition** $2\\kappa\\theta > \\sigma^2$ guarantees $r_t > 0$ a.s."
        ),
        latex_formula=r"dr_t = \kappa(\theta - r_t)\,dt + \sigma\sqrt{r_t}\,dW_t",
        intuition=(
            "The square-root diffusion naturally kills volatility near zero. "
            "CIR has a non-central chi-squared distribution analytically. "
            "Bond prices remain in closed form (affine term structure). "
            "Still can't match an arbitrary initial curve without extensions."
        ),
        connections=["Vasicek Model", "Hull-White Model"],
        tags=["CIR", "cox ingersoll ross", "short rate", "positive rates", "feller"],
        source="Brigo & Mercurio - Interest Rate Models"
    ),

    # ── FINANCIAL ECONOMETRICS ────────────────────────────────────────

    Flashcard(
        domain="Financial Econometrics",
        topic="ARCH & GARCH Models",
        card_type=CardType.FORMULA,
        difficulty=DifficultyLevel.INTERMEDIATE,
        front="Write the GARCH(1,1) model. What stylized facts of financial returns does it capture?",
        back=(
            "**Return:** $r_t = \\mu + \\epsilon_t$, where $\\epsilon_t = \\sigma_t z_t$, $z_t \\sim N(0,1)$\n\n"
            "**Conditional variance:**\n"
            "$$\\sigma_t^2 = \\omega + \\alpha \\epsilon_{t-1}^2 + \\beta \\sigma_{t-1}^2$$\n\n"
            "**Constraints:** $\\omega > 0$, $\\alpha,\\beta \\geq 0$, $\\alpha+\\beta < 1$ (stationarity)\n\n"
            "**Stylized facts captured:**\n"
            "• Volatility clustering\n"
            "• Fat tails (leptokurtosis)\n"
            "• Leverage effect (via EGARCH/GJR extension)"
        ),
        latex_formula=r"\sigma_t^2 = \omega + \alpha\epsilon_{t-1}^2 + \beta\sigma_{t-1}^2",
        intuition=(
            "GARCH says: **today's variance depends on yesterday's shock and yesterday's variance**. "
            "Large shocks → high variance tomorrow (clustering). "
            "The ratio α/(1−α−β) gives the half-life of a variance shock. "
            "Persistence = α+β: near 1 means shocks decay slowly (common in equity markets)."
        ),
        code_snippet='''# Using arch library (pip install arch)
from arch import arch_model
import yfinance as yf

data = yf.download("SPY", start="2010-01-01", end="2023-01-01")["Close"]
returns = 100 * data.pct_change().dropna()

model = arch_model(returns, vol="Garch", p=1, q=1, dist="normal")
result = model.fit(disp="off")
print(result.summary())
forecasts = result.forecast(horizon=5)''',
        assumptions=(
            "• Stationarity: α+β < 1\n"
            "• Symmetric: shocks of equal magnitude have equal impact\n"
            "• i.i.d. innovations z_t"
        ),
        limitations=(
            "• No leverage effect (use EGARCH/GJR-GARCH)\n"
            "• Symmetric response to positive/negative shocks\n"
            "• Assumes normal innovations (use t-dist for fat tails)"
        ),
        connections=["Volatility Modeling", "Time Series Analysis (ARMA/ARIMA)"],
        tags=["GARCH", "ARCH", "volatility", "clustering", "econometrics"],
        source="Tsay - Analysis of Financial Time Series"
    ),

    Flashcard(
        domain="Financial Econometrics",
        topic="Cointegration & Error Correction",
        card_type=CardType.CONCEPT,
        difficulty=DifficultyLevel.ADVANCED,
        front="Define cointegration. What is the Engle-Granger representation theorem?",
        back=(
            "**Definition:** $X_t$ and $Y_t$ are cointegrated I(1) if there exists $\\beta$ such that "
            "$Y_t - \\beta X_t \\sim I(0)$ (stationary).\n\n"
            "**Engle-Granger Theorem:** If $X_t, Y_t$ are CI(1,1), then they have an **Error Correction Model (ECM):**\n\n"
            "$$\\Delta Y_t = \\alpha(Y_{t-1} - \\beta X_{t-1}) + \\text{lagged } \\Delta\\text{s} + \\epsilon_t$$\n\n"
            "where $\\alpha < 0$ is the **adjustment speed** back to equilibrium."
        ),
        intuition=(
            "Cointegration = **long-run equilibrium** between non-stationary series. "
            "Individual series wander (random walk), but they don't drift apart too far. "
            "Classic examples: interest rates at different maturities, spot vs futures prices. "
            "ECM says: short-run deviations get corrected at speed α."
        ),
        connections=["Time Series Analysis (ARMA/ARIMA)", "Yield Curve Construction"],
        tags=["cointegration", "error correction", "ECM", "unit root", "Engle-Granger"],
        source="Hamilton - Time Series Analysis"
    ),

    # ── PORTFOLIO MANAGEMENT ──────────────────────────────────────────

    Flashcard(
        domain="Portfolio Management",
        topic="Mean-Variance Optimization",
        card_type=CardType.FORMULA,
        difficulty=DifficultyLevel.INTERMEDIATE,
        front="State the Markowitz mean-variance optimization problem in matrix form.",
        back=(
            "**Minimize:** $\\frac{1}{2}\\mathbf{w}^\\top \\Sigma \\mathbf{w}$\n\n"
            "**Subject to:**\n"
            "- $\\mathbf{w}^\\top \\boldsymbol{\\mu} = \\mu_p$ (target return)\n"
            "- $\\mathbf{w}^\\top \\mathbf{1} = 1$ (fully invested)\n\n"
            "**Solution (unconstrained):** $\\mathbf{w}^* = \\frac{\\mu_p}{A}\\Sigma^{-1}\\boldsymbol{\\mu} + \\frac{1}{B}\\Sigma^{-1}\\mathbf{1}$\n\n"
            "where $A = \\boldsymbol{\\mu}^\\top\\Sigma^{-1}\\mathbf{1}$, $B = \\mathbf{1}^\\top\\Sigma^{-1}\\mathbf{1}$"
        ),
        latex_formula=r"\min_{\mathbf{w}} \frac{1}{2}\mathbf{w}^\top\Sigma\mathbf{w} \quad\text{s.t.}\quad \mathbf{w}^\top\boldsymbol{\mu}=\mu_p,\;\mathbf{w}^\top\mathbf{1}=1",
        intuition=(
            "Find weights that minimize portfolio variance for a given return target. "
            "The efficient frontier is the set of all such optimal portfolios. "
            "Critical problem: Σ⁻¹ amplifies estimation errors → garbage in, garbage out. "
            "In practice: shrinkage estimators (Ledoit-Wolf), Black-Litterman, or robust optimization."
        ),
        code_snippet='''import numpy as np
from scipy.optimize import minimize

def min_variance_portfolio(mu, Sigma, target_return):
    """Find minimum variance portfolio for a target return."""
    n = len(mu)
    constraints = [
        {"type": "eq", "fun": lambda w: w @ mu - target_return},
        {"type": "eq", "fun": lambda w: w.sum() - 1}
    ]
    result = minimize(
        lambda w: 0.5 * w @ Sigma @ w,
        x0=np.ones(n)/n,
        method="SLSQP",
        constraints=constraints
    )
    return result.x, np.sqrt(result.fun * 2)''',
        limitations=(
            "• Sensitive to input estimation errors\n"
            "• Corner solutions (concentrated portfolios)\n"
            "• Static: ignores time-varying covariances\n"
            "• Does not account for higher moments (skew, kurtosis)"
        ),
        connections=["Capital Asset Pricing Model", "Risk Measures (VaR, CVaR)", "Factor Models"],
        tags=["markowitz", "mean-variance", "portfolio", "optimization", "efficient frontier"],
        source="Fabozzi - Robust Portfolio Optimization"
    ),

    # ── FINANCIAL STABILITY ───────────────────────────────────────────

    Flashcard(
        domain="Financial Stability",
        topic="Systemic Risk Measures",
        card_type=CardType.CONCEPT,
        difficulty=DifficultyLevel.ADVANCED,
        front="Define CoVaR and MES. How do they differ as systemic risk measures?",
        back=(
            "**CoVaR (Adrian & Brunnermeier, 2011):**\n"
            "$\\text{CoVaR}_{q}^{i|j}$ = VaR of institution $i$ conditional on institution $j$ being at its VaR:\n"
            "$$\\Delta\\text{CoVaR}^i = \\text{CoVaR}^{i|j \\text{ at VaR}} - \\text{CoVaR}^{i|j \\text{ at median}}$$\n\n"
            "**MES (Acharya et al., 2012):**\n"
            "$$\\text{MES}_i = E[r_i | r_m < \\text{VaR}_q^m]$$\n"
            "Expected loss of institution $i$ when market is in tail distress.\n\n"
            "**Difference:** CoVaR measures spillover *from* a firm; MES measures *exposure* to systemic crisis."
        ),
        intuition=(
            "Traditional VaR looks at individual institutions in isolation. "
            "Systemic risk is about *interconnectedness*: a firm can be individually safe "
            "but still pose systemic risk (TBTF). "
            "CoVaR asks: 'if Goldman fails, how does that affect the system?' "
            "MES asks: 'which firms bleed most when the system crashes?'"
        ),
        connections=["Macroprudential Policy", "SIFI Identification", "Stress Testing Methodologies"],
        tags=["systemic risk", "CoVaR", "MES", "macroprudential", "TBTF", "financial stability"],
        source="Adrian & Brunnermeier (2011) AER; Acharya et al (2012)"
    ),

    Flashcard(
        domain="Financial Stability",
        topic="Macroprudential Policy",
        card_type=CardType.CENTRAL_BANK,
        difficulty=DifficultyLevel.INTERMEDIATE,
        front="What are the main macroprudential instruments? Classify them by target.",
        back=(
            "**Capital-based:**\n"
            "• Countercyclical capital buffer (CCyB)\n"
            "• Systemic risk buffer (SRB)\n"
            "• SIFI surcharges (G-SIB, D-SIB)\n\n"
            "**Borrower-based:**\n"
            "• Loan-to-Value (LTV) limits\n"
            "• Debt-to-Income (DTI) limits\n"
            "• Debt Service Coverage Ratios (DSCR)\n\n"
            "**Liquidity-based:**\n"
            "• Liquidity Coverage Ratio (LCR)\n"
            "• Net Stable Funding Ratio (NSFR)\n\n"
            "**Exposure-based:**\n"
            "• Large exposure limits\n"
            "• Concentration risk charges"
        ),
        intuition=(
            "Microprudential = safety of individual institutions. "
            "Macroprudential = safety of the *system*. "
            "The distinction matters: individually rational behavior (deleveraging in a crisis) "
            "can be collectively destabilizing (fire sales, credit crunch). "
            "Central banks use macroprudential tools to lean against the financial cycle."
        ),
        connections=["Systemic Risk Measures", "Basel III/IV Framework", "Central Bank Toolkits"],
        tags=["macroprudential", "CCyB", "LTV", "Basel III", "financial stability", "central bank"],
        source="BIS - Macroprudential Frameworks; FSB Reports"
    ),
]


def seed_database():
    """Populate the card library with starter content."""
    store = CardStore()
    existing = {c.id for c in store.all_cards()}
    added = 0
    for card in SEED_CARDS:
        if card.id not in existing:
            store.save_card(card)
            added += 1
    print(f"Seeded {added} new cards. Total: {len(store.all_cards())} cards.")


if __name__ == "__main__":
    seed_database()
