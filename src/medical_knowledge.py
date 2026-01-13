"""
Base de connaissances médicales

⚠️ AVERTISSEMENT:
Les informations contenues dans ce fichier sont à but éducatif uniquement.
Elles ne remplacent pas l'avis d'un professionnel de santé.
Sources: Littérature médicale publique, recommandations de santé publique.
Dernière mise à jour: Janvier 2026

Pour les urgences médicales, appelez le 15 (SAMU) en France.
"""

# Métadonnées de la base de connaissances
KNOWLEDGE_BASE_INFO = {
    "version": "1.0.0",
    "last_updated": "2026-01-13",
    "total_diseases": 55,
    "total_drugs": 60,
    "languages": ["fr", "en", "es"],
    "disclaimer": "Informations à but éducatif uniquement. Consultez un médecin pour un diagnostic.",
    "sources": [
        "OMS - Organisation Mondiale de la Santé",
        "Santé Publique France",
        "Vidal (informations médicamenteuses)",
        "Littérature médicale publique"
    ]
}

# Base de données des maladies et symptômes (55+ maladies)
# Note: Ces informations sont générales et peuvent ne pas s'appliquer à tous les cas
DISEASES_DATABASE = {
    # Maladies infectieuses
    "rhume": {
        "symptoms": ["nez bouché", "écoulement nasal", "éternuements", "mal de gorge", "fatigue légère", "toux"],
        "description": "Infection virale bénigne des voies respiratoires supérieures (rhinopharyngite)",
        "recommendations": ["Repos", "Hydratation abondante", "Lavages nasaux au sérum physiologique", "Paracétamol si douleurs", "Miel pour la gorge", "Consulter si fièvre > 38.5°C ou symptômes > 10 jours"],
        "severity": "faible"
    },
    "grippe": {
        "symptoms": ["fièvre", "toux", "fatigue", "courbatures", "maux de tête"],
        "description": "Infection virale respiratoire courante",
        "recommendations": ["Repos au lit", "Hydratation abondante", "Paracétamol pour la fièvre", "Consulter si symptômes persistent > 7 jours"],
        "severity": "modérée"
    },
    "covid-19": {
        "symptoms": ["fièvre", "toux sèche", "fatigue", "perte goût", "perte odorat", "difficultés respiratoires"],
        "description": "Infection virale COVID-19",
        "recommendations": ["Isolement immédiat", "Test PCR recommandé", "Surveillance saturation oxygène", "Consulter urgence si difficultés respiratoires"],
        "severity": "élevée"
    },
    "angine": {
        "symptoms": ["mal de gorge", "fièvre", "difficultés à avaler", "ganglions gonflés"],
        "description": "Inflammation des amygdales",
        "recommendations": ["Consulter pour test streptocoque", "Antibiotiques si bactérienne", "Antalgiques", "Repos"],
        "severity": "modérée"
    },
    "bronchite": {
        "symptoms": ["toux grasse", "expectorations", "fatigue", "fièvre légère", "essoufflement"],
        "description": "Inflammation des bronches",
        "recommendations": ["Repos", "Hydratation", "Expectorants", "Consulter si persistant > 3 semaines"],
        "severity": "modérée"
    },
    "pneumonie": {
        "symptoms": ["fièvre élevée", "toux", "douleur thoracique", "difficultés respiratoires", "fatigue"],
        "description": "Infection pulmonaire grave",
        "recommendations": ["Consultation médicale urgente", "Antibiotiques", "Hospitalisation si sévère", "Radiographie thoracique"],
        "severity": "élevée"
    },
    "sinusite": {
        "symptoms": ["douleur faciale", "congestion nasale", "maux de tête", "écoulement nasal", "fièvre"],
        "description": "Inflammation des sinus",
        "recommendations": ["Lavages nasaux", "Décongestionnants", "Antalgiques", "Consulter si > 10 jours"],
        "severity": "modérée"
    },
    "otite": {
        "symptoms": ["douleur oreille", "fièvre", "troubles auditifs", "écoulement"],
        "description": "Infection de l'oreille",
        "recommendations": ["Consultation ORL", "Antalgiques", "Antibiotiques si bactérienne", "Éviter l'eau dans l'oreille"],
        "severity": "modérée"
    },
    "méningite": {
        "symptoms": ["maux de tête intenses", "fièvre élevée", "raideur nuque", "vomissements", "photophobie"],
        "description": "Inflammation des méninges - URGENCE",
        "recommendations": ["URGENCE IMMÉDIATE", "Appeler le 15", "Hospitalisation", "Traitement antibiotique urgent"],
        "severity": "critique"
    },
    
    # Maladies digestives
    "gastro-entérite": {
        "symptoms": ["diarrhée", "nausées", "vomissements", "douleurs abdominales", "fièvre"],
        "description": "Infection digestive",
        "recommendations": ["Hydratation importante (SRO)", "Repos digestif", "Réintroduction progressive aliments", "Consulter si déshydratation"],
        "severity": "modérée"
    },
    "reflux gastrique": {
        "symptoms": ["brûlures estomac", "remontées acides", "douleur thoracique", "toux nocturne"],
        "description": "Remontée acide de l'estomac",
        "recommendations": ["Éviter aliments gras", "Surélever tête de lit", "IPP si nécessaire", "Consulter si persistant"],
        "severity": "faible"
    },
    "ulcère gastrique": {
        "symptoms": ["douleur abdominale", "brûlures estomac", "nausées", "perte appétit", "sang dans selles"],
        "description": "Lésion de la muqueuse gastrique",
        "recommendations": ["Consultation gastro-entérologue", "Endoscopie", "IPP", "Traitement Helicobacter si présent"],
        "severity": "élevée"
    },
    "appendicite": {
        "symptoms": ["douleur abdominale droite", "nausées", "vomissements", "fièvre", "perte appétit"],
        "description": "Inflammation de l'appendice - URGENCE",
        "recommendations": ["URGENCE CHIRURGICALE", "Appeler le 15", "Ne rien manger", "Hospitalisation immédiate"],
        "severity": "critique"
    },
    "constipation": {
        "symptoms": ["difficultés défécation", "ballonnements", "douleurs abdominales", "selles dures"],
        "description": "Ralentissement du transit intestinal",
        "recommendations": ["Augmenter fibres", "Hydratation", "Activité physique", "Laxatifs doux si besoin"],
        "severity": "faible"
    },
    "syndrome intestin irritable": {
        "symptoms": ["douleurs abdominales", "ballonnements", "diarrhée", "constipation", "gaz"],
        "description": "Trouble fonctionnel intestinal",
        "recommendations": ["Régime FODMAP", "Gestion stress", "Probiotiques", "Consultation gastro-entérologue"],
        "severity": "modérée"
    },
    "hépatite": {
        "symptoms": ["jaunisse", "fatigue", "nausées", "douleur abdominale", "urines foncées"],
        "description": "Inflammation du foie",
        "recommendations": ["Consultation urgente", "Bilan hépatique", "Repos", "Éviter alcool et médicaments hépatotoxiques"],
        "severity": "élevée"
    },
    
    # Maladies cardiovasculaires
    "hypertension": {
        "symptoms": ["maux de tête", "vertiges", "vision trouble", "fatigue"],
        "description": "Pression artérielle élevée",
        "recommendations": ["Mesurer régulièrement tension", "Réduire sel", "Activité physique", "Consultation médicale obligatoire"],
        "severity": "élevée"
    },
    "infarctus": {
        "symptoms": ["douleur thoracique", "essoufflement", "sueurs", "nausées", "douleur bras gauche"],
        "description": "Crise cardiaque - URGENCE VITALE",
        "recommendations": ["URGENCE ABSOLUE", "Appeler 15 immédiatement", "Aspirine si disponible", "Ne pas bouger"],
        "severity": "critique"
    },
    "angine de poitrine": {
        "symptoms": ["douleur thoracique", "oppression", "essoufflement", "douleur irradiante"],
        "description": "Douleur cardiaque à l'effort",
        "recommendations": ["Consultation cardiologique urgente", "ECG", "Trinitrine", "Repos"],
        "severity": "élevée"
    },
    "arythmie": {
        "symptoms": ["palpitations", "vertiges", "essoufflement", "fatigue", "malaise"],
        "description": "Trouble du rythme cardiaque",
        "recommendations": ["Consultation cardiologique", "ECG", "Holter", "Traitement selon type"],
        "severity": "élevée"
    },
    "avc": {
        "symptoms": ["paralysie faciale", "faiblesse membre", "troubles parole", "confusion", "troubles vision"],
        "description": "Accident vasculaire cérébral - URGENCE",
        "recommendations": ["URGENCE ABSOLUE", "Appeler 15", "Noter heure début symptômes", "Ne rien donner à boire/manger"],
        "severity": "critique"
    },
    
    # Maladies métaboliques
    "diabète": {
        "symptoms": ["soif excessive", "fatigue", "vision trouble", "urines fréquentes", "perte de poids"],
        "description": "Trouble régulation glucose",
        "recommendations": ["Test glycémie à jeun", "Consultation endocrinologue", "Régime adapté", "Surveillance régulière"],
        "severity": "élevée"
    },
    "hypoglycémie": {
        "symptoms": ["tremblements", "sueurs", "faim", "confusion", "palpitations"],
        "description": "Baisse du taux de sucre",
        "recommendations": ["Sucre rapide immédiat", "Resucrage", "Consulter si fréquent", "Ajuster traitement diabète"],
        "severity": "modérée"
    },
    "hypothyroïdie": {
        "symptoms": ["fatigue", "prise de poids", "frilosité", "constipation", "peau sèche"],
        "description": "Insuffisance thyroïdienne",
        "recommendations": ["Bilan thyroïdien", "Consultation endocrinologue", "Lévothyroxine", "Surveillance régulière"],
        "severity": "modérée"
    },
    "hyperthyroïdie": {
        "symptoms": ["perte de poids", "nervosité", "palpitations", "tremblements", "sueurs"],
        "description": "Excès hormones thyroïdiennes",
        "recommendations": ["Bilan thyroïdien", "Consultation endocrinologue", "Antithyroïdiens", "Surveillance cardiaque"],
        "severity": "élevée"
    },
    
    # Maladies neurologiques
    "migraine": {
        "symptoms": ["maux de tête", "nausées", "sensibilité lumière", "vomissements"],
        "description": "Céphalée intense et récurrente",
        "recommendations": ["Repos pièce sombre", "Anti-inflammatoires", "Éviter déclencheurs", "Consulter neurologue si fréquent"],
        "severity": "modérée"
    },
    "épilepsie": {
        "symptoms": ["convulsions", "perte conscience", "mouvements involontaires", "confusion"],
        "description": "Trouble neurologique avec crises",
        "recommendations": ["Consultation neurologique", "EEG", "Antiépileptiques", "Éviter déclencheurs"],
        "severity": "élevée"
    },
    "sclérose en plaques": {
        "symptoms": ["fatigue", "troubles vision", "faiblesse musculaire", "troubles équilibre", "engourdissements"],
        "description": "Maladie auto-immune neurologique",
        "recommendations": ["Consultation neurologique", "IRM", "Traitement immunomodulateur", "Rééducation"],
        "severity": "élevée"
    },
    "parkinson": {
        "symptoms": ["tremblements repos", "rigidité", "lenteur mouvements", "troubles équilibre"],
        "description": "Maladie neurodégénérative",
        "recommendations": ["Consultation neurologique", "Dopaminergiques", "Kinésithérapie", "Suivi régulier"],
        "severity": "élevée"
    },
    "alzheimer": {
        "symptoms": ["pertes mémoire", "confusion", "désorientation", "troubles langage", "changements humeur"],
        "description": "Démence neurodégénérative",
        "recommendations": ["Consultation mémoire", "Bilan neuropsychologique", "Traitement symptomatique", "Accompagnement famille"],
        "severity": "élevée"
    },
    
    # Maladies respiratoires
    "asthme": {
        "symptoms": ["essoufflement", "sifflements", "toux", "oppression thoracique"],
        "description": "Maladie respiratoire chronique",
        "recommendations": ["Consultation pneumologue", "Bronchodilatateurs", "Corticoïdes inhalés", "Éviter allergènes"],
        "severity": "modérée"
    },
    "bpco": {
        "symptoms": ["essoufflement", "toux chronique", "expectorations", "fatigue"],
        "description": "Bronchopneumopathie chronique obstructive",
        "recommendations": ["Arrêt tabac", "Bronchodilatateurs", "Réhabilitation respiratoire", "Oxygénothérapie si besoin"],
        "severity": "élevée"
    },
    "apnée du sommeil": {
        "symptoms": ["ronflements", "fatigue diurne", "somnolence", "maux de tête matinaux"],
        "description": "Pauses respiratoires nocturnes",
        "recommendations": ["Polysomnographie", "PPC si sévère", "Perte de poids", "Éviter alcool"],
        "severity": "modérée"
    },
    
    # Maladies dermatologiques
    "eczéma": {
        "symptoms": ["démangeaisons", "rougeurs", "peau sèche", "vésicules", "croûtes"],
        "description": "Dermatite inflammatoire",
        "recommendations": ["Émollients", "Corticoïdes topiques", "Éviter irritants", "Consultation dermatologue"],
        "severity": "faible"
    },
    "psoriasis": {
        "symptoms": ["plaques rouges", "squames", "démangeaisons", "peau épaissie"],
        "description": "Maladie inflammatoire cutanée",
        "recommendations": ["Consultation dermatologue", "Corticoïdes", "Photothérapie", "Biothérapies si sévère"],
        "severity": "modérée"
    },
    "acné": {
        "symptoms": ["boutons", "points noirs", "inflammation", "cicatrices"],
        "description": "Affection cutanée des follicules",
        "recommendations": ["Nettoyage doux", "Rétinoïdes topiques", "Antibiotiques si sévère", "Consultation dermatologue"],
        "severity": "faible"
    },
    "zona": {
        "symptoms": ["éruption cutanée", "douleur", "vésicules", "brûlures", "démangeaisons"],
        "description": "Réactivation virus varicelle",
        "recommendations": ["Consultation rapide", "Antiviraux", "Antalgiques", "Éviter contact personnes fragiles"],
        "severity": "modérée"
    },
    
    # Maladies rhumatologiques
    "arthrose": {
        "symptoms": ["douleurs articulaires", "raideur matinale", "gonflement", "craquements"],
        "description": "Usure du cartilage articulaire",
        "recommendations": ["Activité physique adaptée", "Antalgiques", "Anti-inflammatoires", "Kinésithérapie"],
        "severity": "modérée"
    },
    "polyarthrite rhumatoïde": {
        "symptoms": ["douleurs articulaires", "gonflement", "raideur matinale", "fatigue"],
        "description": "Maladie auto-immune articulaire",
        "recommendations": ["Consultation rhumatologue", "Méthotrexate", "Biothérapies", "Kinésithérapie"],
        "severity": "élevée"
    },
    "goutte": {
        "symptoms": ["douleur articulaire intense", "gonflement", "rougeur", "chaleur"],
        "description": "Excès acide urique",
        "recommendations": ["Colchicine", "Anti-inflammatoires", "Régime pauvre purines", "Allopurinol au long cours"],
        "severity": "modérée"
    },
    "ostéoporose": {
        "symptoms": ["fractures", "douleurs dorsales", "perte taille", "dos voûté"],
        "description": "Fragilité osseuse",
        "recommendations": ["Densitométrie", "Calcium et vitamine D", "Bisphosphonates", "Activité physique"],
        "severity": "modérée"
    },
    
    # Maladies urinaires
    "infection urinaire": {
        "symptoms": ["brûlures mictionnelles", "urines fréquentes", "douleur bas ventre", "urines troubles"],
        "description": "Infection des voies urinaires",
        "recommendations": ["Hydratation abondante", "Antibiotiques", "Cranberry", "Consulter si fièvre"],
        "severity": "modérée"
    },
    "calculs rénaux": {
        "symptoms": ["douleur intense flanc", "nausées", "vomissements", "sang dans urines"],
        "description": "Lithiase rénale",
        "recommendations": ["Antalgiques puissants", "Hydratation", "Scanner", "Lithotritie si nécessaire"],
        "severity": "élevée"
    },
    "insuffisance rénale": {
        "symptoms": ["fatigue", "œdèmes", "urines rares", "nausées", "confusion"],
        "description": "Défaillance fonction rénale",
        "recommendations": ["Consultation néphrologique urgente", "Bilan rénal", "Dialyse si sévère", "Régime adapté"],
        "severity": "critique"
    },
    
    # Maladies psychiatriques
    "dépression": {
        "symptoms": ["tristesse", "perte intérêt", "fatigue", "troubles sommeil", "idées noires"],
        "description": "Trouble de l'humeur",
        "recommendations": ["Consultation psychiatre/psychologue", "Antidépresseurs", "Psychothérapie", "Soutien social"],
        "severity": "élevée"
    },
    "anxiété": {
        "symptoms": ["inquiétude excessive", "tension", "palpitations", "troubles sommeil", "irritabilité"],
        "description": "Trouble anxieux",
        "recommendations": ["Psychothérapie", "Anxiolytiques si besoin", "Relaxation", "Activité physique"],
        "severity": "modérée"
    },
    "burn-out": {
        "symptoms": ["épuisement", "cynisme", "baisse performance", "troubles sommeil", "irritabilité"],
        "description": "Épuisement professionnel",
        "recommendations": ["Arrêt travail", "Consultation psychologue", "Repos", "Réorganisation professionnelle"],
        "severity": "élevée"
    },
    
    # Maladies allergiques
    "rhinite allergique": {
        "symptoms": ["éternuements", "nez qui coule", "démangeaisons", "yeux rouges"],
        "description": "Allergie respiratoire",
        "recommendations": ["Antihistaminiques", "Corticoïdes nasaux", "Éviter allergènes", "Désensibilisation"],
        "severity": "faible"
    },
    "allergie alimentaire": {
        "symptoms": ["démangeaisons", "urticaire", "gonflement", "troubles digestifs", "choc anaphylactique"],
        "description": "Réaction allergique alimentaire",
        "recommendations": ["Éviction allergène", "Antihistaminiques", "Adrénaline auto-injectable", "Consultation allergologue"],
        "severity": "élevée"
    },
    
    # Maladies ophtalmologiques
    "conjonctivite": {
        "symptoms": ["œil rouge", "larmoiement", "démangeaisons", "sécrétions"],
        "description": "Inflammation de la conjonctive",
        "recommendations": ["Lavages oculaires", "Collyres", "Éviter frottements", "Consulter si persistant"],
        "severity": "faible"
    },
    "glaucome": {
        "symptoms": ["perte vision périphérique", "douleur oculaire", "vision floue", "halos lumineux"],
        "description": "Hypertension oculaire",
        "recommendations": ["Consultation ophtalmologique urgente", "Collyres hypotonisants", "Surveillance régulière", "Chirurgie si besoin"],
        "severity": "élevée"
    },
    "cataracte": {
        "symptoms": ["vision floue", "éblouissement", "baisse acuité visuelle", "vision double"],
        "description": "Opacification du cristallin",
        "recommendations": ["Consultation ophtalmologique", "Chirurgie si gênante", "Lunettes adaptées"],
        "severity": "modérée"
    },
    
    # Maladies gynécologiques
    "endométriose": {
        "symptoms": ["douleurs pelviennes", "règles douloureuses", "douleurs rapports", "infertilité"],
        "description": "Tissu endométrial hors utérus",
        "recommendations": ["Consultation gynécologique", "Échographie", "Traitement hormonal", "Chirurgie si sévère"],
        "severity": "élevée"
    },
    "syndrome prémenstruel": {
        "symptoms": ["irritabilité", "ballonnements", "douleurs seins", "fatigue", "troubles humeur"],
        "description": "Symptômes avant règles",
        "recommendations": ["Activité physique", "Magnésium", "Vitamine B6", "Contraception si sévère"],
        "severity": "faible"
    },
    
    # Maladies hématologiques
    "anémie": {
        "symptoms": ["fatigue", "pâleur", "essoufflement", "vertiges", "palpitations"],
        "description": "Manque de globules rouges",
        "recommendations": ["Bilan sanguin", "Fer si carence", "Recherche cause", "Alimentation riche en fer"],
        "severity": "modérée"
    },
    "leucémie": {
        "symptoms": ["fatigue", "infections fréquentes", "saignements", "pâleur", "fièvre"],
        "description": "Cancer des cellules sanguines",
        "recommendations": ["Consultation hématologique urgente", "Chimiothérapie", "Greffe si nécessaire", "Hospitalisation"],
        "severity": "critique"
    }
}

# Base de données des médicaments (50+ médicaments)
DRUGS_DATABASE = {
    # Antalgiques / Antipyrétiques
    "paracétamol": {
        "category": "antalgique/antipyrétique",
        "interactions": ["alcool"],
        "contraindications": ["insuffisance hépatique"],
        "dosage": "1g toutes les 6h, max 4g/jour"
    },
    "tramadol": {
        "category": "antalgique opioïde",
        "interactions": ["alcool", "antidépresseurs", "benzodiazépines"],
        "contraindications": ["insuffisance respiratoire", "épilepsie non contrôlée"],
        "dosage": "50-100mg toutes les 6h, max 400mg/jour"
    },
    "codéine": {
        "category": "antalgique opioïde",
        "interactions": ["alcool", "sédatifs"],
        "contraindications": ["insuffisance respiratoire", "enfants < 12 ans"],
        "dosage": "30-60mg toutes les 4-6h"
    },
    "morphine": {
        "category": "antalgique opioïde fort",
        "interactions": ["alcool", "benzodiazépines", "autres opioïdes"],
        "contraindications": ["insuffisance respiratoire sévère"],
        "dosage": "Sur prescription stricte uniquement"
    },
    
    # Anti-inflammatoires
    "ibuprofène": {
        "category": "anti-inflammatoire AINS",
        "interactions": ["aspirine", "anticoagulants", "corticoïdes"],
        "contraindications": ["ulcère gastrique", "insuffisance rénale", "grossesse 3e trimestre"],
        "dosage": "400mg toutes les 6-8h, max 1200mg/jour"
    },
    "aspirine": {
        "category": "antalgique/antiagrégant/AINS",
        "interactions": ["ibuprofène", "anticoagulants", "méthotrexate"],
        "contraindications": ["ulcère gastrique", "hémophilie", "enfants < 16 ans"],
        "dosage": "500mg-1g toutes les 4-6h ou 75-160mg/jour (antiagrégant)"
    },
    "naproxène": {
        "category": "anti-inflammatoire AINS",
        "interactions": ["anticoagulants", "autres AINS"],
        "contraindications": ["ulcère gastrique", "insuffisance rénale", "grossesse"],
        "dosage": "500mg 2 fois/jour"
    },
    "diclofénac": {
        "category": "anti-inflammatoire AINS",
        "interactions": ["anticoagulants", "lithium"],
        "contraindications": ["ulcère gastrique", "insuffisance cardiaque", "grossesse"],
        "dosage": "50mg 2-3 fois/jour"
    },
    "kétoprofène": {
        "category": "anti-inflammatoire AINS",
        "interactions": ["anticoagulants", "autres AINS"],
        "contraindications": ["ulcère gastrique", "insuffisance rénale"],
        "dosage": "100mg 2 fois/jour"
    },
    
    # Antibiotiques
    "amoxicilline": {
        "category": "antibiotique pénicilline",
        "interactions": ["pilule contraceptive", "méthotrexate"],
        "contraindications": ["allergie pénicilline"],
        "dosage": "500mg-1g 3 fois/jour, 7-10 jours"
    },
    "azithromycine": {
        "category": "antibiotique macrolide",
        "interactions": ["anticoagulants", "statines"],
        "contraindications": ["allergie macrolides", "troubles hépatiques"],
        "dosage": "500mg jour 1, puis 250mg jours 2-5"
    },
    "ciprofloxacine": {
        "category": "antibiotique fluoroquinolone",
        "interactions": ["théophylline", "anticoagulants"],
        "contraindications": ["enfants", "grossesse", "tendinopathies"],
        "dosage": "500mg 2 fois/jour"
    },
    "doxycycline": {
        "category": "antibiotique tétracycline",
        "interactions": ["antiacides", "fer"],
        "contraindications": ["grossesse", "enfants < 8 ans"],
        "dosage": "100mg 2 fois/jour"
    },
    "métronidazole": {
        "category": "antibiotique/antiparasitaire",
        "interactions": ["alcool", "anticoagulants"],
        "contraindications": ["grossesse 1er trimestre"],
        "dosage": "500mg 2-3 fois/jour"
    },
    
    # Antiviraux
    "aciclovir": {
        "category": "antiviral",
        "interactions": ["néphrotoxiques"],
        "contraindications": ["insuffisance rénale sévère"],
        "dosage": "200-800mg 5 fois/jour selon indication"
    },
    "oseltamivir": {
        "category": "antiviral anti-grippe",
        "interactions": ["peu d'interactions"],
        "contraindications": ["allergie"],
        "dosage": "75mg 2 fois/jour, 5 jours"
    },
    
    # Antihypertenseurs
    "amlodipine": {
        "category": "antihypertenseur inhibiteur calcique",
        "interactions": ["jus pamplemousse", "simvastatine"],
        "contraindications": ["choc cardiogénique"],
        "dosage": "5-10mg 1 fois/jour"
    },
    "ramipril": {
        "category": "antihypertenseur IEC",
        "interactions": ["AINS", "diurétiques épargneurs potassium"],
        "contraindications": ["grossesse", "sténose artères rénales"],
        "dosage": "2.5-10mg 1 fois/jour"
    },
    "losartan": {
        "category": "antihypertenseur ARA2",
        "interactions": ["AINS", "lithium"],
        "contraindications": ["grossesse", "insuffisance hépatique sévère"],
        "dosage": "50-100mg 1 fois/jour"
    },
    "bisoprolol": {
        "category": "bêta-bloquant",
        "interactions": ["vérapamil", "diltiazem"],
        "contraindications": ["asthme", "bloc AV", "bradycardie"],
        "dosage": "5-10mg 1 fois/jour"
    },
    "hydrochlorothiazide": {
        "category": "diurétique thiazidique",
        "interactions": ["lithium", "digitaliques"],
        "contraindications": ["insuffisance rénale sévère", "hypokaliémie"],
        "dosage": "12.5-25mg 1 fois/jour"
    },
    
    # Antidiabétiques
    "metformine": {
        "category": "antidiabétique biguanide",
        "interactions": ["produits de contraste iodés", "alcool"],
        "contraindications": ["insuffisance rénale", "acidose"],
        "dosage": "500-1000mg 2-3 fois/jour"
    },
    "gliclazide": {
        "category": "antidiabétique sulfamide",
        "interactions": ["alcool", "AINS"],
        "contraindications": ["insuffisance rénale/hépatique sévère"],
        "dosage": "30-120mg 1 fois/jour"
    },
    "insuline": {
        "category": "hormone antidiabétique",
        "interactions": ["bêta-bloquants"],
        "contraindications": ["hypoglycémie"],
        "dosage": "Selon schéma personnalisé"
    },
    
    # Anticoagulants
    "warfarine": {
        "category": "anticoagulant AVK",
        "interactions": ["AINS", "antibiotiques", "nombreux médicaments"],
        "contraindications": ["hémorragie active", "grossesse"],
        "dosage": "Selon INR cible"
    },
    "rivaroxaban": {
        "category": "anticoagulant AOD",
        "interactions": ["antifongiques azolés", "inhibiteurs protéase"],
        "contraindications": ["hémorragie active", "insuffisance rénale sévère"],
        "dosage": "10-20mg 1 fois/jour"
    },
    "héparine": {
        "category": "anticoagulant injectable",
        "interactions": ["AINS", "antiagrégants"],
        "contraindications": ["thrombopénie", "hémorragie active"],
        "dosage": "Selon protocole hospitalier"
    },
    
    # Antiagrégants
    "clopidogrel": {
        "category": "antiagrégant plaquettaire",
        "interactions": ["anticoagulants", "AINS", "IPP"],
        "contraindications": ["hémorragie active", "ulcère gastrique"],
        "dosage": "75mg 1 fois/jour"
    },
    
    # Hypolipémiants
    "atorvastatine": {
        "category": "hypolipémiant statine",
        "interactions": ["jus pamplemousse", "fibrates", "macrolides"],
        "contraindications": ["insuffisance hépatique", "grossesse"],
        "dosage": "10-80mg 1 fois/jour le soir"
    },
    "simvastatine": {
        "category": "hypolipémiant statine",
        "interactions": ["jus pamplemousse", "amlodipine", "amiodarone"],
        "contraindications": ["insuffisance hépatique", "grossesse"],
        "dosage": "20-40mg 1 fois/jour le soir"
    },
    
    # Inhibiteurs pompe à protons
    "oméprazole": {
        "category": "IPP antiulcéreux",
        "interactions": ["clopidogrel", "antifongiques azolés"],
        "contraindications": ["allergie"],
        "dosage": "20-40mg 1 fois/jour"
    },
    "pantoprazole": {
        "category": "IPP antiulcéreux",
        "interactions": ["warfarine", "méthotrexate"],
        "contraindications": ["allergie"],
        "dosage": "20-40mg 1 fois/jour"
    },
    "ésoméprazole": {
        "category": "IPP antiulcéreux",
        "interactions": ["clopidogrel", "diazépam"],
        "contraindications": ["allergie"],
        "dosage": "20-40mg 1 fois/jour"
    },
    
    # Antihistaminiques
    "cétirizine": {
        "category": "antihistaminique H1",
        "interactions": ["alcool", "sédatifs"],
        "contraindications": ["insuffisance rénale sévère"],
        "dosage": "10mg 1 fois/jour"
    },
    "loratadine": {
        "category": "antihistaminique H1",
        "interactions": ["peu d'interactions"],
        "contraindications": ["allergie"],
        "dosage": "10mg 1 fois/jour"
    },
    "desloratadine": {
        "category": "antihistaminique H1",
        "interactions": ["peu d'interactions"],
        "contraindications": ["allergie"],
        "dosage": "5mg 1 fois/jour"
    },
    
    # Corticoïdes
    "prednisone": {
        "category": "corticoïde",
        "interactions": ["AINS", "anticoagulants", "antidiabétiques"],
        "contraindications": ["infections non contrôlées", "ulcère gastrique"],
        "dosage": "5-60mg/jour selon indication"
    },
    "dexaméthasone": {
        "category": "corticoïde",
        "interactions": ["AINS", "anticoagulants"],
        "contraindications": ["infections non contrôlées"],
        "dosage": "0.5-9mg/jour selon indication"
    },
    
    # Bronchodilatateurs
    "salbutamol": {
        "category": "bronchodilatateur bêta-2",
        "interactions": ["bêta-bloquants"],
        "contraindications": ["hypersensibilité"],
        "dosage": "100-200µg par inhalation, max 8 fois/jour"
    },
    "tiotropium": {
        "category": "bronchodilatateur anticholinergique",
        "interactions": ["autres anticholinergiques"],
        "contraindications": ["glaucome", "rétention urinaire"],
        "dosage": "18µg 1 inhalation/jour"
    },
    
    # Antidépresseurs
    "sertraline": {
        "category": "antidépresseur ISRS",
        "interactions": ["IMAO", "tramadol", "anticoagulants"],
        "contraindications": ["IMAO < 14 jours"],
        "dosage": "50-200mg 1 fois/jour"
    },
    "escitalopram": {
        "category": "antidépresseur ISRS",
        "interactions": ["IMAO", "médicaments allongeant QT"],
        "contraindications": ["IMAO < 14 jours", "allongement QT"],
        "dosage": "10-20mg 1 fois/jour"
    },
    "venlafaxine": {
        "category": "antidépresseur IRSN",
        "interactions": ["IMAO", "tramadol"],
        "contraindications": ["IMAO < 14 jours", "HTA non contrôlée"],
        "dosage": "75-225mg/jour"
    },
    "mirtazapine": {
        "category": "antidépresseur tétracyclique",
        "interactions": ["IMAO", "sédatifs"],
        "contraindications": ["IMAO < 14 jours"],
        "dosage": "15-45mg 1 fois/jour le soir"
    },
    
    # Anxiolytiques
    "alprazolam": {
        "category": "anxiolytique benzodiazépine",
        "interactions": ["alcool", "opioïdes", "antifongiques azolés"],
        "contraindications": ["insuffisance respiratoire", "myasthénie"],
        "dosage": "0.25-0.5mg 2-3 fois/jour"
    },
    "lorazépam": {
        "category": "anxiolytique benzodiazépine",
        "interactions": ["alcool", "opioïdes"],
        "contraindications": ["insuffisance respiratoire", "myasthénie"],
        "dosage": "1-2mg 2-3 fois/jour"
    },
    "diazépam": {
        "category": "anxiolytique benzodiazépine",
        "interactions": ["alcool", "opioïdes", "oméprazole"],
        "contraindications": ["insuffisance respiratoire", "myasthénie"],
        "dosage": "2-10mg 2-4 fois/jour"
    },
    
    # Hypnotiques
    "zolpidem": {
        "category": "hypnotique",
        "interactions": ["alcool", "opioïdes", "antidépresseurs"],
        "contraindications": ["insuffisance respiratoire", "myasthénie"],
        "dosage": "10mg au coucher"
    },
    "zopiclone": {
        "category": "hypnotique",
        "interactions": ["alcool", "opioïdes"],
        "contraindications": ["insuffisance respiratoire", "myasthénie"],
        "dosage": "7.5mg au coucher"
    },
    
    # Antiépileptiques
    "lévétiracétam": {
        "category": "antiépileptique",
        "interactions": ["peu d'interactions"],
        "contraindications": ["allergie"],
        "dosage": "500-1500mg 2 fois/jour"
    },
    "valproate": {
        "category": "antiépileptique",
        "interactions": ["lamotrigine", "carbamazépine"],
        "contraindications": ["grossesse", "troubles hépatiques"],
        "dosage": "500-2000mg/jour en 2 prises"
    },
    
    # Antiparkinsoniens
    "lévodopa": {
        "category": "antiparkinsonien",
        "interactions": ["antipsychotiques", "IMAO"],
        "contraindications": ["glaucome angle fermé"],
        "dosage": "Selon schéma personnalisé"
    },
    
    # Autres
    "lévothyroxine": {
        "category": "hormone thyroïdienne",
        "interactions": ["fer", "calcium", "IPP"],
        "contraindications": ["thyrotoxicose"],
        "dosage": "25-200µg 1 fois/jour à jeun"
    },
    "allopurinol": {
        "category": "anti-goutteux",
        "interactions": ["azathioprine", "warfarine"],
        "contraindications": ["crise de goutte aiguë"],
        "dosage": "100-300mg 1 fois/jour"
    },
    "colchicine": {
        "category": "anti-goutteux",
        "interactions": ["statines", "macrolides"],
        "contraindications": ["insuffisance rénale/hépatique sévère"],
        "dosage": "0.5-1mg/jour"
    },
    "méthotrexate": {
        "category": "immunosuppresseur/antirhumatismal",
        "interactions": ["AINS", "triméthoprime"],
        "contraindications": ["grossesse", "insuffisance rénale/hépatique"],
        "dosage": "7.5-25mg 1 fois/semaine"
    }
}

# Symptômes d'urgence
EMERGENCY_SYMPTOMS = [
    "douleur thoracique",
    "difficultés respiratoires",
    "perte de conscience",
    "hémorragie importante",
    "paralysie",
    "confusion mentale",
    "convulsions",
    "douleur abdominale intense"
]

def get_disease_info(disease_name):
    """Récupère les informations sur une maladie"""
    return DISEASES_DATABASE.get(disease_name.lower())

def get_drug_info(drug_name):
    """Récupère les informations sur un médicament"""
    return DRUGS_DATABASE.get(drug_name.lower())

def check_emergency(symptoms):
    """Vérifie si les symptômes nécessitent une urgence"""
    for symptom in symptoms:
        if any(emergency in symptom.lower() for emergency in EMERGENCY_SYMPTOMS):
            return True
    return False

def get_all_diseases():
    """Retourne la liste de toutes les maladies"""
    return list(DISEASES_DATABASE.keys())

def get_all_drugs():
    """Retourne la liste de tous les médicaments"""
    return list(DRUGS_DATABASE.keys())


# Fonction pour obtenir les métadonnées
def get_knowledge_base_info():
    """Retourne les informations sur la base de connaissances"""
    return KNOWLEDGE_BASE_INFO

# Fonction pour obtenir le disclaimer
def get_medical_disclaimer():
    """Retourne l'avertissement médical"""
    return {
        "fr": "⚠️ Ces informations sont à but éducatif uniquement. Consultez toujours un médecin pour un diagnostic médical. En cas d'urgence, appelez le 15 (SAMU).",
        "en": "⚠️ This information is for educational purposes only. Always consult a doctor for medical diagnosis. In case of emergency, call 15 (SAMU).",
        "es": "⚠️ Esta información es solo para fines educativos. Siempre consulte a un médico para un diagnóstico médico. En caso de emergencia, llame al 15 (SAMU)."
    }

# Fonction pour vérifier la fraîcheur des données
def check_data_freshness():
    """Vérifie si les données sont à jour (< 6 mois)"""
    from datetime import datetime, timedelta
    
    last_update = datetime.strptime(KNOWLEDGE_BASE_INFO["last_updated"], "%Y-%m-%d")
    now = datetime.now()
    age_days = (now - last_update).days
    
    return {
        "is_fresh": age_days < 180,  # Moins de 6 mois
        "age_days": age_days,
        "last_updated": KNOWLEDGE_BASE_INFO["last_updated"],
        "warning": "Les données ont plus de 6 mois. Vérifiez avec des sources récentes." if age_days >= 180 else None
    }
