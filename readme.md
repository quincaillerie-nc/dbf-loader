# 📦 DBF LOADER

## Module Python de chargement automatique des fichiers DBF via SMB

---

# 📖 Présentation

`dbf_loader` est un module Python permettant de charger automatiquement des fichiers `.DBF` depuis un serveur réseau SMB.

Le module est compatible :

* ✅ Windows
* ✅ Linux / Ubuntu
* ✅ environnements serveurs
* ✅ scripts ETL
* ✅ reporting automatisé
* ✅ pipelines Power BI

Il permet de simplifier l’accès aux anciennes bases de données `.DBF` utilisées dans :

* les ERP historiques,
* les logiciels de caisse,
* les logiciels de stock,
* les systèmes de gestion legacy.

---

# 🎯 Objectif du module

Le module a été conçu pour :

✅ centraliser la lecture des DBF
✅ uniformiser les accès réseau
✅ gérer automatiquement Windows/Linux
✅ retourner directement un DataFrame pandas
✅ simplifier les scripts métiers

---

# ⚙️ Fonctionnement général

Le module détecte automatiquement le système d’exploitation :

| OS      | Fonctionnement                     |
| ------- | ---------------------------------- |
| Windows | lecture directe via partage réseau |
| Linux   | copie temporaire via SMB           |

---

# 🏗️ Architecture

```bash
modules/
└── dbf-loader/
    └── dbf_loader.py
```

---

# 📦 Dépendances

---

# Installation Python

```bash
pip install pandas
pip install dbfread
```

---

# Installation Linux (Ubuntu)

Le module Linux nécessite :

```bash
sudo apt install smbclient
```

---

# 📁 Configuration SMB

Le module utilise une connexion SMB réseau.

---

# 📌 Configuration actuelle

```python
SMB_HOST     = "//192.168.0.250/bases"
SMB_USER     = "supportserv"
SMB_PASSWORD = "********"
```

---

# ⚠️ Sécurité importante

⚠️ Il est fortement déconseillé de stocker les mots de passe directement dans le code source.

---

# ✅ Bonne pratique recommandée

Utiliser un fichier `.env`

Exemple :

```env
SMB_HOST=//192.168.0.250/bases
SMB_USER=supportserv
SMB_PASSWORD=motdepasse
```

---

# 🧠 Détection automatique du système

Le module détecte automatiquement l’OS :

```python
platform.system()
```

---

# 📌 Résultat

| OS détecté | Traitement      |
| ---------- | --------------- |
| Windows    | lecture directe |
| Linux      | copie SMB       |

---

# 🚀 Fonction principale

---

# `get_dbf()`

## 📌 Description

Fonction principale du module.

Elle permet de charger un fichier `.DBF` depuis le réseau.

---

# 📌 Syntaxe

```python
get_dbf(chemin_relatif)
```

---

# 📌 Paramètres

| Paramètre      | Type | Description           |
| -------------- | ---- | --------------------- |
| chemin_relatif | str  | chemin du fichier DBF |

---

# 📌 Exemple

```python
df = get_dbf("qc/article.dbf")
```

---

# 📊 Résultat

Retourne :

```python
pandas.DataFrame
```

---

# 🖥️ Fonctionnement Windows

---

# 📌 Méthode utilisée

Sous Windows :

* le partage réseau est utilisé directement,
* aucun fichier temporaire n’est créé.

---

# 📌 Exemple de chemin

```bash
\\192.168.0.250\Bases\qc\article.dbf
```

---

# 📌 Fonction utilisée

```python
_load_windows()
```

---

# 🔄 Étapes réalisées

1. conversion des `/` en `\`
2. création du chemin complet
3. vérification du fichier
4. lecture du DBF
5. retour du DataFrame

---

# 🐧 Fonctionnement Linux / Ubuntu

---

# 📌 Méthode utilisée

Sous Linux :

* le fichier est copié temporairement,
* la copie utilise `smbclient`,
* le fichier est stocké dans `/tmp`.

---

# 📌 Fonction utilisée

```python
_load_linux()
```

---

# 🔄 Étapes réalisées

1. connexion SMB
2. copie du DBF
3. stockage temporaire
4. lecture du DBF
5. retour du DataFrame

---

# 📌 Exemple de commande SMB

```bash
smbclient //192.168.0.250/bases \
-U supportserv%motdepasse \
-c "get qc/article.dbf /tmp/article.dbf"
```

---

# 📂 Dossier temporaire Linux

```python
LINUX_TMP = "/tmp"
```

---

# 📌 Exemple de fichier temporaire

```bash
/tmp/article.dbf
```

---

# 📖 Lecture du DBF

---

# 📌 Fonction utilisée

```python
_read_dbf()
```

---

# 📌 Librairie utilisée

```python
dbfread
```

---

# 📌 Encodage utilisé

```python
encoding="cp1252"
```

Cet encodage est souvent utilisé dans :

* les anciens ERP,
* les logiciels de caisse,
* les logiciels de stock français.

---

# 📌 Gestion des erreurs caractères

```python
char_decode_errors="ignore"
```

Permet d’éviter les crashs liés aux caractères invalides.

---

# 📊 Conversion en DataFrame

Le DBF est automatiquement converti :

```python
pd.DataFrame(iter(table))
```

---

# 📌 Exemple complet

```python
from dbf_loader import get_dbf

df = get_dbf("qc/article.dbf")

print(df.head())
```

---

# 📊 Exemple de filtrage

```python
df_filtered = df[df["NART"] == "710092"]
```

---

# 📈 Exemple de statistiques

```python
print(len(df))
print(df.columns)
```

---

# 📝 Logs du module

Le module affiche plusieurs logs :

---

# Exemple Windows

```bash
[DBF_LOADER] Windows → lecture directe :
\\192.168.0.250\Bases\qc\article.dbf
```

---

# Exemple Linux

```bash
[DBF_LOADER] Linux → copie SMB vers /tmp/article.dbf
```

---

# Exemple chargement réussi

```bash
[DBF_LOADER] 15420 lignes chargées depuis article.dbf
```

---

# ❌ Gestion des erreurs

---

# 📌 Fichier introuvable

```python
FileNotFoundError
```

---

# 📌 Exemple

```python
raise FileNotFoundError(
    f"Fichier introuvable : {full_path}"
)
```

---

# 📌 Erreurs possibles

| Erreur            | Cause                   |
| ----------------- | ----------------------- |
| FileNotFoundError | fichier absent          |
| smbclient error   | accès réseau impossible |
| Permission denied | mauvais droits          |
| DBF decode error  | encodage corrompu       |

---

# 🔐 Sécurité

---

# ⚠️ Attention

Le module contient actuellement :

* un utilisateur SMB,
* un mot de passe SMB.

---

# ❌ Risques

Cela peut entraîner :

* fuite de credentials,
* accès réseau non sécurisé,
* compromission serveur.

---

# ✅ Recommandations

Utiliser :

* `.env`
* variables système
* vault
* secrets manager

---

# 🛠️ Évolutions possibles

---

# Fonctionnalités futures recommandées

✅ cache local
✅ suppression auto des fichiers `/tmp`
✅ retries automatiques
✅ logs avancés
✅ gestion multi-serveurs
✅ support PostgreSQL
✅ export SQL direct
✅ monitoring réseau

---

# 📊 Cas d’utilisation métier

Le module est particulièrement utile pour :

---

# 🏪 Quincailleries

* lecture articles,
* suivi stock,
* extraction ventes.

---

# 📦 ERP historiques

* migration DBF,
* synchronisation SQL,
* ETL.

---

# 📈 Reporting Power BI

* alimentation SQL,
* nettoyage données,
* automatisation reporting.

---

# 🧪 Exemple Workflow Réel

---

# Étape 1

Chargement DBF :

```python
df = get_dbf("qc/article.dbf")
```

---

# Étape 2

Nettoyage :

```python
df = df.dropna()
```

---

# Étape 3

Filtrage :

```python
df_filtered = df[df["FAM"] == "OUTILLAGE"]
```

---

# Étape 4

Export :

```python
df_filtered.to_excel("rapport.xlsx")
```

---

# 👨‍💻 Public cible

Ce module est destiné :

* aux développeurs Python,
* aux data analysts,
* aux administrateurs systèmes,
* aux entreprises utilisant des DBF.

---

# 📜 Conclusion

`dbf_loader` permet de simplifier considérablement l’exploitation des anciennes bases DBF dans des environnements modernes.

Grâce à sa compatibilité Windows/Linux et son intégration pandas, il constitue une excellente base pour :

* les ETL,
* les migrations SQL,
* les automatisations,
* les dashboards Power BI,
* les systèmes de reporting.

---
