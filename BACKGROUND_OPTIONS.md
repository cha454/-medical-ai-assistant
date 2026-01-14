# 🎨 Options de Fonds Animés

Voici plusieurs options de fonds animés pour votre assistant médical. Choisissez celui qui vous plaît !

## Option 1 : Gradient Doux (ACTUEL) ✅

**Style** : Gradient pastel animé avec particules flottantes
**Couleurs** : Bleu clair, violet clair, vert clair, orange clair
**Animation** : Douce et apaisante (15s)
**Ambiance** : Professionnelle et médicale

```css
background: linear-gradient(-45deg, #e3f2fd, #f3e5f5, #e8f5e9, #fff3e0);
background-size: 400% 400%;
animation: gradientShift 15s ease infinite;
```

---

## Option 2 : Bulles Médicales

**Style** : Bulles flottantes comme des molécules
**Couleurs** : Blanc et bleu médical
**Animation** : Bulles qui montent lentement
**Ambiance** : Scientifique et moderne

```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    position: relative;
    overflow: hidden;
}

body::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px),
        radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 50px 50px, 80px 80px;
    background-position: 0 0, 40px 40px;
    animation: bubbleFloat 20s linear infinite;
}

@keyframes bubbleFloat {
    0% { transform: translateY(0); }
    100% { transform: translateY(-100px); }
}
```

---

## Option 3 : Vagues Douces

**Style** : Vagues ondulantes
**Couleurs** : Dégradé bleu/vert apaisant
**Animation** : Vagues qui ondulent
**Ambiance** : Calme et relaxante

```css
body {
    background: linear-gradient(to bottom, #e0f7fa, #b2ebf2);
    position: relative;
}

body::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 200%;
    height: 200px;
    background: linear-gradient(to right, 
        transparent, 
        rgba(0, 188, 212, 0.1), 
        transparent);
    animation: wave 10s ease-in-out infinite;
}

@keyframes wave {
    0%, 100% { transform: translateX(0) translateY(0); }
    50% { transform: translateX(-25%) translateY(-20px); }
}
```

---

## Option 4 : Particules Lumineuses

**Style** : Particules brillantes qui flottent
**Couleurs** : Fond sombre avec particules lumineuses
**Animation** : Particules qui scintillent
**Ambiance** : Moderne et technologique

```css
body {
    background: #0f172a;
    position: relative;
}

body::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(2px 2px at 20% 30%, white, transparent),
        radial-gradient(2px 2px at 60% 70%, white, transparent),
        radial-gradient(1px 1px at 50% 50%, white, transparent),
        radial-gradient(1px 1px at 80% 10%, white, transparent);
    background-size: 200% 200%;
    animation: sparkle 3s ease-in-out infinite;
}

@keyframes sparkle {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}
```

---

## Option 5 : Mesh Gradient (Tendance 2024)

**Style** : Gradient mesh moderne
**Couleurs** : Multicolore doux
**Animation** : Morphing fluide
**Ambiance** : Ultra-moderne et élégante

```css
body {
    background: 
        radial-gradient(at 40% 20%, hsla(28,100%,74%,0.3) 0px, transparent 50%),
        radial-gradient(at 80% 0%, hsla(189,100%,56%,0.3) 0px, transparent 50%),
        radial-gradient(at 0% 50%, hsla(355,100%,93%,0.3) 0px, transparent 50%),
        radial-gradient(at 80% 50%, hsla(340,100%,76%,0.3) 0px, transparent 50%),
        radial-gradient(at 0% 100%, hsla(22,100%,77%,0.3) 0px, transparent 50%),
        radial-gradient(at 80% 100%, hsla(242,100%,70%,0.3) 0px, transparent 50%),
        radial-gradient(at 0% 0%, hsla(343,100%,76%,0.3) 0px, transparent 50%);
    animation: meshMove 15s ease infinite;
}

@keyframes meshMove {
    0%, 100% { filter: hue-rotate(0deg); }
    50% { filter: hue-rotate(20deg); }
}
```

---

## Option 6 : Minimaliste Élégant

**Style** : Fond blanc avec subtiles animations
**Couleurs** : Blanc avec touches de couleur
**Animation** : Très subtile
**Ambiance** : Propre et professionnelle

```css
body {
    background: #ffffff;
    position: relative;
}

body::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: 
        radial-gradient(circle at 30% 40%, rgba(99, 102, 241, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 70% 60%, rgba(236, 72, 153, 0.03) 0%, transparent 50%);
    animation: subtleMove 20s ease-in-out infinite;
}

@keyframes subtleMove {
    0%, 100% { transform: translate(0, 0); }
    50% { transform: translate(5%, 5%); }
}
```

---

## 🎯 Recommandation

**Pour un assistant médical**, je recommande :
1. **Option 1** (actuel) - Professionnel et apaisant ✅
2. **Option 6** - Si vous préférez plus sobre
3. **Option 3** - Si vous voulez quelque chose de relaxant

## 📝 Comment changer

Pour changer de fond, remplacez le CSS du `body` dans `templates/chat.html` avec l'option de votre choix !
