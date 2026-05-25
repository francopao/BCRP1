# 🚀 Deploy en 10 minutos

## Paso 1 — Subir a GitHub
```bash
cd quant_memoria
git init
git add .
git commit -m "Quant Memoria v2.0 - initial deploy"
# Crea repo en github.com, luego:
git remote add origin https://github.com/TU_USUARIO/quant-memoria.git
git push -u origin main
```

## Paso 2 — Streamlit Cloud
1. Ve a https://share.streamlit.io
2. Conecta tu cuenta de GitHub
3. "New app" → elige tu repo → main file: `app.py`
4. Deploy 🚀

## Paso 3 — API keys (opcional, para futuras funciones IA)
En Streamlit Cloud → Settings → Secrets:
```toml
GROQ_API_KEY = "tu_key_aqui"
GOOGLE_AI_KEY = "tu_key_aqui"
OPENROUTER_KEY = "tu_key_aqui"
```
⚠️ NUNCA pongas keys en el código ni en GitHub.

## Agregar contenido nuevo
1. Abre `content/master_cards.py` en cualquier editor
2. Copia un bloque existente y modifícalo
3. `git add . && git commit -m "nueva carta" && git push`
4. Streamlit Cloud se actualiza solo en ~2 min
