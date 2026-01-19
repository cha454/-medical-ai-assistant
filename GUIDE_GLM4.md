# 🚀 Guide d'intégration GLM-4 (Zhipu AI)

GLM-4 est un excellent modèle de langage chinois développé par Zhipu AI. Il offre une API gratuite, rapide et performante.

## 📋 Avantages de GLM-4

- ✅ **Gratuit** : API gratuite avec quota généreux
- ✅ **Rapide** : Temps de réponse très court
- ✅ **Performant** : Qualité comparable à GPT-4
- ✅ **Multilingue** : Supporte français, anglais, chinois, etc.
- ✅ **Facile** : Intégration simple et compatible OpenAI

## 🔑 Étape 1 : Obtenir votre clé API

1. **Allez sur le site officiel** : https://open.bigmodel.cn/

2. **Créez un compte** (gratuit)
   - Cliquez sur "注册" (S'inscrire) en haut à droite
   - Utilisez votre email ou numéro de téléphone
   - Vérifiez votre compte

3. **Obtenez votre API Key**
   - Connectez-vous à votre compte
   - Allez dans "API Keys" ou "密钥管理"
   - Cliquez sur "创建新的API密钥" (Créer une nouvelle clé API)
   - Copiez votre clé API (elle commence généralement par des chiffres et lettres)

4. **Vérifiez votre quota**
   - Vous avez un quota gratuit pour commencer
   - Consultez votre tableau de bord pour voir votre utilisation

## ⚙️ Étape 2 : Configuration

1. **Ouvrez le fichier `.env`** dans votre projet

2. **Ajoutez votre clé API GLM-4** :
   ```env
   # Zhipu AI GLM-4 (GRATUIT - Excellent modèle chinois)
   # Site: https://open.bigmodel.cn/
   GLM_API_KEY=votre_cle_api_ici
   ```

3. **Commentez les autres clés** (optionnel) :
   ```env
   # GOOGLE_API_KEY=
   # OPENAI_API_KEY=
   ```

4. **Sauvegardez le fichier**

## 🧪 Étape 3 : Tester l'intégration

Exécutez le script de test :

```bash
python test_glm.py
```

Vous devriez voir :
```
✓ Clé API GLM-4 détectée
✓ Provider actif: glm
✓ LLM disponible: True
✅ Réponse reçue
```

## 🚀 Étape 4 : Lancer l'application

```bash
python app.py
```

Ouvrez votre navigateur sur : http://localhost:5000

## 📊 Modèles disponibles

GLM-4 propose plusieurs modèles :

| Modèle | Description | Vitesse | Coût |
|--------|-------------|---------|------|
| `glm-4-flash` | Rapide et léger (par défaut) | ⚡⚡⚡ | Gratuit |
| `glm-4` | Modèle standard | ⚡⚡ | Gratuit |
| `glm-4-plus` | Plus performant | ⚡ | Payant |

Le modèle `glm-4-flash` est utilisé par défaut car il offre le meilleur rapport vitesse/qualité.

## 🔧 Personnalisation

Pour changer de modèle, modifiez dans `src/llm_provider.py` :

```python
def _call_glm(self, messages):
    data = {
        "model": "glm-4",  # Changez ici : glm-4-flash, glm-4, glm-4-plus
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.7
    }
```

## 🌐 Paramètres avancés

Vous pouvez ajuster les paramètres de génération :

```python
data = {
    "model": "glm-4-flash",
    "messages": messages,
    "max_tokens": 2000,      # Longueur maximale de la réponse
    "temperature": 0.7,      # Créativité (0.0 = précis, 1.0 = créatif)
    "top_p": 0.9,           # Diversité des réponses
    "stream": False         # Streaming activé/désactivé
}
```

## ❓ Dépannage

### Erreur : "Invalid API Key"
- Vérifiez que votre clé API est correcte
- Assurez-vous qu'elle est bien copiée dans `.env`
- Vérifiez qu'il n'y a pas d'espaces avant/après

### Erreur : "Quota exceeded"
- Vous avez dépassé votre quota gratuit
- Attendez le renouvellement ou ajoutez du crédit
- Consultez votre tableau de bord : https://open.bigmodel.cn/

### Erreur : "Connection timeout"
- Vérifiez votre connexion internet
- Le service peut être temporairement indisponible
- Réessayez dans quelques minutes

### Le provider n'est pas "glm"
- Vérifiez que `GLM_API_KEY` est bien définie dans `.env`
- Redémarrez l'application
- GLM-4 a la priorité sur les autres providers

## 📚 Documentation officielle

- Site officiel : https://open.bigmodel.cn/
- Documentation API : https://open.bigmodel.cn/dev/api
- Exemples de code : https://github.com/zhipuai

## 💡 Conseils

1. **Quota gratuit** : Utilisez-le intelligemment pour vos tests
2. **Cache** : Implémentez un cache pour éviter les appels répétés
3. **Fallback** : Gardez un autre provider (Google Gemini) en backup
4. **Monitoring** : Surveillez votre utilisation dans le dashboard

## 🎉 Félicitations !

Vous avez maintenant intégré GLM-4 dans votre assistant médical IA !

Pour toute question, consultez la documentation officielle ou ouvrez une issue sur GitHub.
