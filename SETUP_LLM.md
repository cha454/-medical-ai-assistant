# 🤖 Configuration du LLM pour l'Assistant Médical IA

## Options disponibles (par ordre de recommandation)

### 1. 🆓 Groq (GRATUIT - Recommandé)
**Le plus rapide et gratuit!**

1. Créez un compte sur https://console.groq.com
2. Générez une clé API
3. Ajoutez dans Render: `GROQ_API_KEY=votre_clé`

### 2. 🆓 HuggingFace (GRATUIT)
1. Créez un compte sur https://huggingface.co
2. Générez un token: Settings → Access Tokens
3. Ajoutez: `HUGGINGFACE_API_KEY=votre_token`

### 3. 💰 OpenAI GPT-4 (Payant ~$0.01/requête)
1. Créez un compte sur https://platform.openai.com
2. Ajoutez des crédits et générez une clé API
3. Ajoutez: `OPENAI_API_KEY=votre_clé`

### 4. 💰 Anthropic Claude (Payant)
1. Créez un compte sur https://console.anthropic.com
2. Générez une clé API
3. Ajoutez: `ANTHROPIC_API_KEY=votre_clé`

## Configuration sur Render

1. Dashboard Render → Votre service
2. Environment → Add Environment Variable
3. Ajoutez la clé de votre choix
4. Redéployez

## Test
Après configuration, l'API `/api/health` affichera le LLM actif.
