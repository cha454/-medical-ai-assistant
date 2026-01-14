# ⚡ Fix Rapide SendGrid sur Render

## 🎯 Tu as l'erreur : "Render bloque SMTP"

### ✅ Solution en 3 Étapes

---

## Étape 1️⃣ : Vérifier un Email dans SendGrid

1. Va sur : https://app.sendgrid.com/settings/sender_auth/senders

2. Clique **"Create New Sender"**

3. Remplis :
   - **From Email** : `ton_email@gmail.com` (ou autre)
   - **From Name** : `Assistant Medical IA`
   - **Reply To** : `ton_email@gmail.com`
   - Remplis les autres champs

4. Clique **"Create"**

5. **IMPORTANT** : Va dans ta boîte email et clique sur le lien de vérification

6. Attends que le statut devienne **"Verified"** ✅

---

## Étape 2️⃣ : Ajouter la Variable sur Render

1. Va sur : https://dashboard.render.com/

2. Sélectionne ton service **medical-ai-assistant**

3. Va dans **Environment**

4. Ajoute cette nouvelle variable :

```
Variable Name: SENDGRID_FROM_EMAIL
Value: ton_email_verifie@gmail.com
```

**⚠️ Utilise EXACTEMENT l'email que tu as vérifié à l'étape 1 !**

5. Clique **"Save Changes"**

---

## Étape 3️⃣ : Vérifier que ça Marche

1. Attends 2-3 minutes que Render redémarre

2. Va dans **Logs** sur Render

3. Cherche cette ligne :
   ```
   ✓ Email: SendGrid activé (expéditeur: ton_email@gmail.com)
   ```

4. Teste l'envoi d'email depuis ton app !

---

## 📋 Récapitulatif des Variables Render

Tu dois avoir ces 2 variables dans **Render → Environment** :

```
SENDGRID_API_KEY=SG.xxxxxxxxxx (tu l'as déjà ✅)
SENDGRID_FROM_EMAIL=ton_email_verifie@gmail.com (à ajouter ⚠️)
```

---

## 🎉 C'est Tout !

Après ces 3 étapes, l'envoi d'email devrait fonctionner !

---

## 🆘 Ça ne Marche Toujours Pas ?

### Vérifie :

1. ✅ Email vérifié dans SendGrid (statut "Verified")
2. ✅ `SENDGRID_FROM_EMAIL` = email vérifié (exactement pareil)
3. ✅ Service Render redémarré
4. ✅ Logs montrent "SendGrid activé"

### Erreurs Courantes :

**"Email expéditeur non vérifié"**
→ Vérifie ton email dans SendGrid et clique sur le lien de vérification

**"API key invalide"**
→ Recrée une clé API sur SendGrid et mets-la dans Render

**"Service email non configuré"**
→ Vérifie que les 2 variables sont bien dans Render Environment

---

## 📖 Guide Complet

Pour plus de détails, consulte : **CONFIGURER_SENDGRID.md**

---

**Made with ❤️ pour résoudre ton problème rapidement !**
