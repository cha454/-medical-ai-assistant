# 🏥 Assistant Médical IA

Un assistant médical intelligent basé sur l'IA qui permet de discuter en langage naturel sur des questions de santé.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📚 Documentation

**🗂️ [INDEX COMPLET DE LA DOCUMENTATION](INDEX_DOCUMENTATION.md)** - Accédez à tous les guides (80+ fichiers organisés)

**Guides rapides :**
- 🚀 [Démarrage Rapide](DEMARRAGE_RAPIDE.md)
- 🎤 [Système Vocal v2.0](GUIDE_VOCAL_AMELIORE.md)
- 🔧 [Configuration](SETUP_LLM.md)
- 🚢 [Déploiement](DEPLOIEMENT_RENDER.md)

## 🌐 Démo en ligne

**🔗 Application:** https://medical-ai-assistant-2k1a.onrender.com/

## ⚠️ Avertissement Important

**Cet assistant est un outil d'information uniquement. Il ne remplace EN AUCUN CAS une consultation médicale professionnelle. Consultez toujours un médecin qualifié pour tout problème de santé.**

## ✨ Fonctionnalités

### 🆕 NOUVELLES FONCTIONNALITÉS

#### 🌤️ Météo en Temps Réel (OpenWeather API)
- Demandez la météo de n'importe quelle ville
- Température, humidité, vent, conditions
- Conseils santé adaptés à la météo
- Exemples: "Quelle est la météo à Paris ?"

#### 🔍 Recherche Web Multi-Sources (Version 2.0) 🆕
- **7 moteurs de recherche** : Google, Wikipedia, DuckDuckGo, PubMed, Bing, Brave, Google Scholar
- **Système de fiabilité** avec notation ⭐⭐⭐
- **Croisement automatique** des sources pour garantir la fiabilité
- **Jusqu'à 8 sources** affichées avec détails complets
- **14 sources médicales prioritaires** (OMS, PubMed, etc.)
- **Statistiques de qualité** (nombre de sources, fiabilité)
- **Informations détaillées** : titre, extrait, auteurs, date, URL
- Exemples: "Fais une recherche poussée sur le diabète"
- **Voir** : `AMELIORATIONS_RECHERCHE_WEB.md` pour les détails

### 💬 Chat Intelligent
- Interface conversationnelle style ChatGPT
- Réponses en temps réel avec effet de typing
- Historique des conversations sauvegardé
- Actions: Copier, Régénérer les réponses

### 🎤 Reconnaissance Vocale
- Parlez au lieu de taper
- Support multilingue (FR, EN, ES)
- Activation simple par bouton micro

### 🌍 Multilingue
- **Français** 🇫🇷
- **English** 🇬🇧
- **Español** 🇪🇸
- Changement de langue instantané

### 🤖 Intelligence Artificielle
- **LLM intégré** : Google Gemini, OpenAI GPT, Anthropic Claude, Groq, HuggingFace
- **Recherche web multi-sources (v2.0)** 🆕 : 
  - 7 moteurs : Google, Wikipedia, DuckDuckGo, PubMed, Bing, Brave, Google Scholar
  - Système de fiabilité ⭐⭐⭐
  - Croisement automatique des sources
  - 14 sources médicales prioritaires
- **API Météo** : OpenWeather (1000 appels/jour gratuit)
- **55+ maladies** dans la base de connaissances
- **60+ médicaments** avec interactions
- **Machine Learning** (scikit-learn) pour la classification
- **Base de données SQLite** pour l'historique
- **Réponses vérifiées** avec sources citées

### 📊 Dashboard Admin (optionnel)
- Statistiques en temps réel
- Graphiques interactifs (Charts.js)
- Gestion des maladies et médicaments
- Accès: `/admin`

## 🚀 Installation

### Prérequis
- Python 3.9+
- pip

### Installation locale

```bash
# Cloner le repository
git clone https://github.com/cha454/-medical-ai-assistant.git
cd medical-ai-assistant

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 🔑 Configuration des APIs (Optionnel)

Pour activer les fonctionnalités avancées, créez un fichier `.env` à la racine :

```env
# LLM Provider (choisissez-en un)
GOOGLE_API_KEY=votre_cle_google_gemini
OPENAI_API_KEY=votre_cle_openai
ANTHROPIC_API_KEY=votre_cle_anthropic
GROQ_API_KEY=votre_cle_groq
HUGGINGFACE_API_KEY=votre_cle_huggingface

# Météo (NOUVEAU - Gratuit)
OPENWEATHER_API_KEY=votre_cle_openweather

# Recherche Web - Sources Gratuites (déjà actives sans config)
# Wikipedia, DuckDuckGo, PubMed = 3 sources gratuites illimitées

# Recherche Web - Sources Optionnelles (pour améliorer la qualité)
GOOGLE_SEARCH_API_KEY=votre_cle_google_search  # 100/jour gratuit
GOOGLE_SEARCH_CX=votre_search_engine_id
BING_SEARCH_API_KEY=votre_cle_bing            # 1000/mois gratuit
BRAVE_SEARCH_API_KEY=votre_cle_brave          # 2000/mois gratuit
SERPAPI_KEY=votre_cle_serpapi                 # 100/mois gratuit (Google Scholar)

# Email (optionnel)
SENDGRID_API_KEY=votre_cle_sendgrid
SENDGRID_FROM_EMAIL=votre_email@exemple.com
```

**📖 Guides détaillés:**
- [AMELIORATIONS_RECHERCHE_WEB.md](AMELIORATIONS_RECHERCHE_WEB.md) 🆕 - Documentation complète recherche multi-sources
- [CONFIGURATION_SOURCES_RECHERCHE.md](CONFIGURATION_SOURCES_RECHERCHE.md) 🆕 - Guide configuration des sources
- [RESUME_AMELIORATIONS.md](RESUME_AMELIORATIONS.md) 🆕 - Résumé visuel avant/après
- [GUIDE_RENDER_COMPLET.md](GUIDE_RENDER_COMPLET.md) - Déploiement sur Render avec toutes les clés API
- [NOUVELLES_FONCTIONNALITES.md](NOUVELLES_FONCTIONNALITES.md) - Documentation des nouvelles fonctionnalités
- [GOOGLE_SEARCH_SETUP.md](GOOGLE_SEARCH_SETUP.md) - Configuration recherche Google

**Sans configuration:** L'assistant fonctionne avec Wikipedia, DuckDuckGo et PubMed (3 sources gratuites illimitées)

## 📁 Structure du Projet

```
medical-ai-assistant/
├── app.py                      # Application Flask principale
├── requirements.txt            # Dépendances Python
├── render.yaml                 # Configuration Render
├── src/
│   ├── chatbot.py             # Chatbot conversationnel
│   ├── disease_classifier.py  # Classification ML des maladies
│   ├── drug_interactions.py   # Vérification médicaments
│   ├── medical_knowledge.py   # Base de connaissances (55+ maladies, 60+ médicaments)
│   └── database.py            # Gestion base de données SQLite
├── templates/
│   ├── index.html             # Page d'accueil
│   ├── chat.html              # Interface chat style ChatGPT
│   └── admin.html             # Dashboard admin
└── README.md
```

## 🎯 Utilisation

### Interface Chat

1. Accédez à https://medical-ai-assistant-2k1a.onrender.com/
2. Cliquez sur "💬 Commencer la conversation"
3. Posez vos questions en langage naturel

**Exemples de questions:**
- "J'ai de la fièvre et de la toux, qu'est-ce que ça peut être?"
- "Quels sont les symptômes du diabète?"
- "Puis-je prendre ibuprofène et aspirine ensemble?"
- "Comment traiter une migraine?"
- **🆕 "Quelle est la météo à Paris ?"**
- **🆕 "Fais une recherche poussée sur le diabète"**
- **🆕 "Explique en détail le système immunitaire"**

### Reconnaissance Vocale

1. Cliquez sur le bouton micro 🎤
2. Autorisez l'accès au microphone
3. Parlez votre question
4. Le texte apparaît automatiquement

### Changer de Langue

1. En bas de la sidebar, sélectionnez la langue
2. L'interface se traduit instantanément

## 🛠️ Technologies Utilisées

### Backend
- **Flask** - Framework web Python
- **scikit-learn** - Machine Learning
- **TensorFlow** - Deep Learning (préparé pour analyse d'images)
- **SQLite** - Base de données
- **Gunicorn** - Serveur WSGI

### Frontend
- **HTML5/CSS3** - Interface moderne
- **JavaScript** - Interactivité
- **Chart.js** - Graphiques interactifs
- **Web Speech API** - Reconnaissance vocale

### Déploiement
- **Render** - Hébergement cloud
- **GitHub** - Contrôle de version

## 📊 Base de Connaissances

### Maladies (55+)
- Infectieuses: grippe, COVID-19, angine, bronchite, pneumonie...
- Cardiovasculaires: hypertension, infarctus, AVC...
- Neurologiques: migraine, épilepsie, Parkinson, Alzheimer...
- Digestives: gastro-entérite, ulcère, appendicite...
- Et bien plus...

### Médicaments (60+)
- Antalgiques: paracétamol, tramadol, morphine...
- Anti-inflammatoires: ibuprofène, aspirine, naproxène...
- Antibiotiques: amoxicilline, azithromycine...
- Antihypertenseurs: amlodipine, ramipril...
- Et bien plus...

## 🔒 Sécurité et Confidentialité

- ✅ Aucune donnée personnelle n'est collectée
- ✅ Historique sauvegardé localement (localStorage)
- ✅ Pas de tracking
- ✅ Code open source

## 🚧 Roadmap

- [ ] Analyse d'images médicales (Deep Learning)
- [ ] Authentification utilisateurs
- [ ] Export PDF des consultations
- [ ] Application mobile (React Native)
- [ ] API publique
- [ ] Plus de langues (Arabe, Chinois, etc.)

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**cha454**
- GitHub: [@cha454](https://github.com/cha454)
- Projet: [medical-ai-assistant](https://github.com/cha454/-medical-ai-assistant)

## 🙏 Remerciements

- Données médicales basées sur des sources publiques
- Interface inspirée de ChatGPT
- Communauté open source

## 📞 Support

Pour toute question ou problème:
- Ouvrir une [issue](https://github.com/cha454/-medical-ai-assistant/issues)
- Consulter la [documentation](https://github.com/cha454/-medical-ai-assistant/wiki)

---

**⚠️ Rappel:** Cet outil est à but éducatif et informatif uniquement. Consultez toujours un professionnel de santé pour un diagnostic médical.

**Made with ❤️ for better healthcare access**
