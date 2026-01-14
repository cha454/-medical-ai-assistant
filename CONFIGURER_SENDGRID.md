# 📧 Configuration SendGrid pour Render - Guide Complet

## 🎯 Problème Résolu

Tu as l'erreur : **"Render bloque les connexions SMTP"**

✅ **Solution** : Utiliser SendGrid API (pas SMTP)

---

## 📋 Étapes de Configuration

### Étape 1️⃣ : Obtenir la Clé API SendGrid

Tu l'as déjà fait ✅

1. Va sur https://app.sendgrid.com/settings/api_keys
2. Clique "Create API Key"
3. Nom : "Medical AI Assistant"
4. Permissions : **Full Access**
5. Copie la clé (commence par `SG.`)

---

### Étape 2️⃣ : Vérifier un Email Expéditeur (IMPORTANT!)

**C'est l'étape que tu as peut-être oubliée !**

#### Option A : Vérification d'un Email Unique (Recommandé)

1. Va sur https://app.sendgrid.com/settings/sender_auth/senders
2. Clique **"Create New Sender"** ou **"Verify Single Sender"**
3. Remplis le formulaire :
   ```
   From Name: Assistant Medical IA
   From Email: TON_EMAIL@gmail.com (ou autre)
   Reply To: TON_EMAIL@gmail.com
   Company Address: (remplis avec tes infos)
   ```
4. Clique **"Create"**
5. **IMPORTANT** : Va dans ta boîte email et clique sur le lien de vérification
6. Attends que le statut devienne **"Verified"** ✅

#### Option B : Vérification de Domaine (Avancé)

Si tu as un domaine (ex: medical-ai.com) :
1. Va sur https://app.sendgrid.com/settings/sender_auth
2. Clique **"Authenticate Your Domain"**
3. Suis les instructions DNS

---

### Étape 3️⃣ : Configurer les Variables d'Environnement sur Render

1. Va sur ton dashboard Render : https://dashboard.render.com/
2. Sélectionne ton service **medical-ai-assistant**
3. Va dans **Environment**
4. Ajoute/Modifie ces variables :

```env
SENDGRID_API_KEY=SG.ta_cle_ici
SENDGRID_FROM_EMAIL=ton_email_verifie@gmail.com
```

**⚠️ IMPORTANT** : `SENDGRID_FROM_EMAIL` doit être **exactement** l'email que tu as vérifié à l'étape 2 !

#### Exemple de Configuration Render

```
Variable Name: SENDGRID_API_KEY
Value: SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Variable Name: SENDGRID_FROM_EMAIL  
Value: contact@medical-ai.com
```

---

### Étape 4️⃣ : Sauvegarder et Redémarrer

1. Clique **"Save Changes"** sur Render
2. Render va automatiquement redémarrer ton service
3. Attends 2-3 minutes que le service redémarre

---

### Étape 5️⃣ : Tester l'Envoi d'Email

#### Test depuis l'Interface Web

1. Va sur https://medical-ai-assistant-2k1a.onrender.com/
2. Commence une conversation
3. Demande : "Envoie-moi un résumé par email à noir1777@gmail.com"
4. Tu devrais recevoir l'email ! 🎉

#### Test avec cURL

```bash
curl -X POST https://medical-ai-assistant-2k1a.onrender.com/api/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "noir1777@gmail.com",
    "subject": "Test SendGrid",
    "body": "Ceci est un test depuis Render avec SendGrid API"
  }'
```

---

## 🔍 Vérification de la Configuration

### Vérifier les Logs Render

1. Va sur Render Dashboard
2. Clique sur ton service
3. Va dans **Logs**
4. Cherche cette ligne au démarrage :

```
✓ Email: SendGrid activé (expéditeur: ton_email@gmail.com)
```

Si tu vois :
- ✅ `✓ Email: SendGrid activé` → Tout est bon !
- ❌ `⚠️ Email: Non configuré` → Vérifie SENDGRID_API_KEY
- ❌ `⚠️ Email: SMTP` → Tu utilises encore SMTP, pas SendGrid

---

## 🆘 Résolution des Erreurs

### Erreur : "Email expéditeur non vérifié"

**Cause** : L'email dans `SENDGRID_FROM_EMAIL` n'est pas vérifié dans SendGrid

**Solution** :
1. Va sur https://app.sendgrid.com/settings/sender_auth/senders
2. Vérifie que ton email a le statut **"Verified"** ✅
3. Si non, clique sur "Resend Verification"
4. Vérifie ta boîte email et clique sur le lien

### Erreur : "API key invalide"

**Cause** : La clé `SENDGRID_API_KEY` est incorrecte

**Solution** :
1. Va sur https://app.sendgrid.com/settings/api_keys
2. Crée une nouvelle clé API
3. Copie-la entièrement (commence par `SG.`)
4. Mets-la dans Render → Environment → SENDGRID_API_KEY
5. Sauvegarde et redémarre

### Erreur : "Render bloque SMTP"

**Cause** : Tu utilises encore SMTP au lieu de SendGrid API

**Solution** :
1. Vérifie que `SENDGRID_API_KEY` est bien configuré dans Render
2. Vérifie que `sendgrid>=6.9.0` est dans requirements.txt
3. Redémarre le service Render
4. Vérifie les logs : tu dois voir "SendGrid activé"

### Erreur : "Service email non configuré"

**Cause** : Les variables d'environnement ne sont pas chargées

**Solution** :
1. Vérifie que les variables sont dans Render → Environment
2. Pas d'espaces avant/après les valeurs
3. Sauvegarde et redémarre le service

---

## ✅ Checklist Complète

- [ ] Clé API SendGrid créée
- [ ] Email expéditeur vérifié dans SendGrid (statut "Verified")
- [ ] `SENDGRID_API_KEY` ajouté dans Render Environment
- [ ] `SENDGRID_FROM_EMAIL` ajouté dans Render Environment (email vérifié)
- [ ] Service Render redémarré
- [ ] Logs montrent "✓ Email: SendGrid activé"
- [ ] Test d'envoi réussi

---

## 📊 Configuration Finale dans Render

Voici ce que tu dois avoir dans **Render → Environment** :

```env
# Clé API SendGrid (obligatoire)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Email expéditeur vérifié (obligatoire)
SENDGRID_FROM_EMAIL=ton_email_verifie@gmail.com

# Autres variables (optionnelles)
SECRET_KEY=ta-cle-secrete-production
PORT=10000
```

---

## 🎯 Exemple Complet

### 1. Dans SendGrid

**Sender vérifié** :
```
From Name: Assistant Medical IA
From Email: contact@medical-ai.com
Status: ✅ Verified
```

### 2. Dans Render Environment

```
SENDGRID_API_KEY=SG.abc123xyz...
SENDGRID_FROM_EMAIL=contact@medical-ai.com
```

### 3. Dans les Logs Render

```
✓ Email: SendGrid activé (expéditeur: contact@medical-ai.com)
```

### 4. Test Réussi

```json
{
  "success": true,
  "message": "Email envoyé à noir1777@gmail.com via SendGrid"
}
```

---

## 💡 Conseils

### Pour le Développement Local

Crée un fichier `.env` :
```env
SENDGRID_API_KEY=SG.ta_cle_ici
SENDGRID_FROM_EMAIL=ton_email_verifie@gmail.com
```

### Pour la Production (Render)

Utilise les variables d'environnement Render (plus sécurisé)

### Limites SendGrid Gratuit

- ✅ 100 emails/jour
- ✅ Suffisant pour tester et petite utilisation
- 💰 Plans payants si besoin de plus

---

## 📞 Support SendGrid

Si tu as encore des problèmes :

1. **Documentation** : https://docs.sendgrid.com/
2. **Support** : https://support.sendgrid.com/
3. **Status** : https://status.sendgrid.com/

---

## 🎉 Résultat Attendu

Après configuration, quand un utilisateur demande un email :

```
✅ Email envoyé avec succès !
📧 Un résumé de consultation a été envoyé à noir1777@gmail.com
```

Et l'utilisateur reçoit :

```
De: Assistant Medical IA <ton_email@gmail.com>
À: noir1777@gmail.com
Sujet: Résumé consultation - 14/01/2026

RESUME DE CONSULTATION - ASSISTANT MEDICAL IA

Date: 14/01/2026 à 15:30

SYMPTOMES MENTIONNES:
  - fièvre
  - toux

HISTORIQUE DE LA CONVERSATION:
...
```

---

**🎊 Félicitations ! Ton service email est maintenant opérationnel sur Render !**
