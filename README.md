# PharmAPI

API REST de gestion de pharmacies, d'utilisateurs et de médicaments, construite avec **FastAPI**, **SQLAlchemy** et **SQLite**.

Elle permet de gérer les utilisateurs, les pharmacies et leurs médicaments, avec une authentification par email et token.

---

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Stack technique](#stack-technique)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Lancer l'API](#lancer-lapi)
- [Documentation interactive](#documentation-interactive)
- [Authentification](#authentification)
- [Endpoints](#endpoints)
- [Base de données](#base-de-données)
- [Accéder à la base SQLite](#accéder-à-la-base-sqlite)
- [Structure du projet](#structure-du-projet)
- [Configuration](#configuration)
- [Réinitialiser la base](#réinitialiser-la-base)
- [Notes de sécurité](#notes-de-sécurité)

---

## Fonctionnalités

- Inscription et connexion par email, sans mot de passe.
- Génération de tokens d'accès stockés en base.
- Protection des routes : les endpoints métier renvoient `401` sans token valide.
- CRUD complet pour les utilisateurs, les pharmacies et les médicaments.
- Relations :
  - utilisateurs ↔ pharmacies : plusieurs-à-plusieurs ;
  - pharmacies → médicaments : un-à-plusieurs.
- Association et dissociation d'un utilisateur à une pharmacie.
- Filtrage des médicaments par pharmacie.
- Base SQLite créée automatiquement au démarrage.

---

## Stack technique

- **Python** 3.13+
- **FastAPI** (API et validation)
- **SQLAlchemy** (ORM)
- **SQLite** (base de données)
- **Pydantic** (schémas de données)
- **uv** (gestion des dépendances et exécution)

---

## Prérequis

- Python **3.13** ou supérieur
- [uv](https://docs.astral.sh/uv/) installé

---

## Installation

```bash
git clone https://github.com/SakaizaNomena/pharmapi.git
cd pharmapi
uv sync
```

`uv sync` installe les dépendances dans le virtualenv local `.venv`.

---

## Lancer l'API

### Mode développement

```bash
uv run fastapi dev
```

L'API démarre par défaut sur :

```
http://127.0.0.1:8000
```

Le rechargement automatique est activé : le serveur redémarre à chaque modification du code.

### Mode production

```bash
uv run fastapi run main.py
```

### Changer de port

```bash
uv run fastapi dev --port 8080
```

---

## Documentation interactive

Une fois le serveur lancé :

| Interface | URL |
|-----------|-----|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |

Dans Swagger UI, cliquez sur **Authorize** et saisissez votre token pour tester les routes protégées.

---

## Authentification

L'authentification fonctionne sans mot de passe :

1. `POST /auth/register` crée un utilisateur si l'email est disponible et renvoie un token.
2. `POST /auth/login` vérifie que l'email existe et renvoie un nouveau token.
3. Le token doit être envoyé dans le header HTTP :

```
Authorization: Bearer <access_token>
```

4. `POST /auth/logout` supprime le token utilisé.

### Inscription

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com"
  }'
```

Réponse :

```json
{
  "access_token": "VOTRE_TOKEN",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```

### Connexion

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com"}'
```

### Appel d'une route protégée

```bash
curl http://127.0.0.1:8000/users/ \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

### Déconnexion

```bash
curl -X POST http://127.0.0.1:8000/auth/logout \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

---

## Endpoints

### Auth

| Méthode | Route | Token requis | Description |
|---------|-------|--------------|-------------|
| POST | `/auth/register` | Non | Créer un compte et obtenir un token |
| POST | `/auth/login` | Non | Se connecter avec un email |
| GET | `/auth/me` | Oui | Utilisateur actuellement connecté |
| POST | `/auth/logout` | Oui | Supprimer le token courant |

### Users

| Méthode | Route | Token requis | Description |
|---------|-------|--------------|-------------|
| GET | `/users/` | Oui | Liste des utilisateurs |
| GET | `/users/{user_id}` | Oui | Détail d'un utilisateur avec ses pharmacies |
| POST | `/users/` | Oui | Créer un utilisateur |
| PUT | `/users/{user_id}` | Oui | Modifier un utilisateur |
| DELETE | `/users/{user_id}` | Oui | Supprimer un utilisateur |
| GET | `/users/{user_id}/pharmacies` | Oui | Pharmacies liées à un utilisateur |
| POST | `/users/{user_id}/pharmacies/{pharmacy_id}` | Oui | Lier une pharmacie à un utilisateur |
| DELETE | `/users/{user_id}/pharmacies/{pharmacy_id}` | Oui | Retirer le lien |

### Pharmacies

| Méthode | Route | Token requis | Description |
|---------|-------|--------------|-------------|
| GET | `/pharmacies/` | Oui | Liste des pharmacies |
| GET | `/pharmacies/{pharmacy_id}` | Oui | Détail d'une pharmacie |
| POST | `/pharmacies/` | Oui | Créer une pharmacie |
| PUT | `/pharmacies/{pharmacy_id}` | Oui | Modifier une pharmacie |
| DELETE | `/pharmacies/{pharmacy_id}` | Oui | Supprimer une pharmacie |
| GET | `/pharmacies/{pharmacy_id}/users` | Oui | Utilisateurs liés à une pharmacie |
| POST | `/pharmacies/{pharmacy_id}/users/{user_id}` | Oui | Lier un utilisateur |
| DELETE | `/pharmacies/{pharmacy_id}/users/{user_id}` | Oui | Retirer le lien |
| GET | `/pharmacies/{pharmacy_id}/medicaments` | Oui | Médicaments d'une pharmacie |

### Medicaments

| Méthode | Route | Token requis | Description |
|---------|-------|--------------|-------------|
| GET | `/medicaments/` | Oui | Liste des médicaments (`?pharmacy_id=` pour filtrer) |
| GET | `/medicaments/{medicament_id}` | Oui | Détail d'un médicament |
| POST | `/medicaments/` | Oui | Créer un médicament |
| PUT | `/medicaments/{medicament_id}` | Oui | Modifier un médicament |
| DELETE | `/medicaments/{medicament_id}` | Oui | Supprimer un médicament |

### Exemples

Créer une pharmacie :

```bash
curl -X POST http://127.0.0.1:8000/pharmacies/ \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pharmacie Centrale",
    "address": "1 rue de la Paix",
    "city": "Paris",
    "phone": "0102030405"
  }'
```

Créer un médicament :

```bash
curl -X POST http://127.0.0.1:8000/medicaments/ \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Doliprane",
    "description": "Anti-douleur",
    "price": 2.5,
    "stock": 50,
    "pharmacy_id": 1
  }'
```

Lister les médicaments d'une pharmacie :

```bash
curl "http://127.0.0.1:8000/medicaments/?pharmacy_id=1" \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

---

## Base de données

La base est une base **SQLite** nommée `app.db`, créée automatiquement à la racine du projet au démarrage de l'application.

### Tables

| Table | Description |
|-------|-------------|
| `users` | Utilisateurs (`id`, `name`, `email`) |
| `pharmacies` | Pharmacies (`id`, `name`, `address`, `city`, `phone`) |
| `medicaments` | Médicaments (`id`, `name`, `description`, `price`, `stock`, `pharmacy_id`) |
| `user_pharmacy` | Table d'association utilisateurs ↔ pharmacies (`user_id`, `pharmacy_id`) |
| `auth_tokens` | Tokens de connexion (`id`, `token`, `user_id`, `created_at`) |

### Relations

```
User  <-- user_pharmacy -->  Pharmacy  <-- medicaments
  |
  +-- auth_tokens
```

- Un utilisateur peut être lié à plusieurs pharmacies, et inversement.
- Une pharmacie possède plusieurs médicaments.
- Un médicament appartient à une seule pharmacie.
- Supprimer une pharmacie supprime ses médicaments et ses liens d'association.
- Supprimer un utilisateur supprime ses tokens et ses liens d'association.

---

## Accéder à la base SQLite

Le fichier de base se trouve à la racine du projet :

```
./app.db
```

### Avec le client SQLite

Si `sqlite3` est installé :

```bash
sqlite3 app.db
```

Puis :

```sql
.tables
SELECT * FROM users;
SELECT * FROM pharmacies;
SELECT * FROM medicaments;
SELECT * FROM user_pharmacy;
SELECT * FROM auth_tokens;
.quit
```

### Sans client SQLite (via Python)

Lister les tables :

```bash
uv run python -c "import sqlite3; c=sqlite3.connect('app.db'); print(c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall())"
```

Ouvrir une session interactive :

```bash
uv run python
```

```python
import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

conn.close()
```

### Avec un outil graphique

Le fichier `app.db` peut être ouvert avec des outils comme **DB Browser for SQLite**, **DBeaver** ou l'extension SQLite de VS Code.

> Le fichier `app.db` est ignoré par Git et ne fait pas partie du dépôt.

---

## Structure du projet

```
.
├── main.py                         # Point d'entrée FastAPI
├── pyproject.toml                  # Dépendances et configuration du projet
├── uv.lock                         # Versions verrouillées des dépendances
├── .gitignore
└── src/
    └── app/
        ├── api/                    # Routes HTTP
        │   ├── auth.py
        │   ├── users.py
        │   ├── pharmacies.py
        │   └── medicaments.py
        ├── core/
        │   ├── database.py         # Connexion SQLite + session SQLAlchemy
        │   └── security.py         # Vérification du token et utilisateur courant
        ├── models/                 # Tables SQLAlchemy
        │   ├── association.py
        │   ├── auth_token_model.py
        │   ├── medicament_model.py
        │   ├── pharmacy_model.py
        │   └── user_model.py
        ├── schemas/                # Schémas Pydantic (entrée/sortie)
        │   ├── auth_schema.py
        │   ├── medicament_schema.py
        │   ├── pharmacy_schema.py
        │   └── user_schema.py
        └── services/               # Logique métier et requêtes SQL
            ├── auth_services.py
            ├── medicament_services.py
            ├── pharmacy_services.py
            └── user_services.py
```

---

## Configuration

L'URL de la base de données est définie dans `src/app/core/database.py` :

```python
DATABASE_URL = "sqlite:///./app.db"
```

Pour utiliser un autre fichier SQLite :

```python
DATABASE_URL = "sqlite:///./ma_base.db"
```

Les tables sont créées automatiquement au démarrage via `Base.metadata.create_all(bind=engine)`.

---

## Réinitialiser la base

1. Arrêter le serveur.
2. Supprimer le fichier de base.
3. Relancer l'API : les tables seront recréées vides.

```bash
rm app.db
uv run fastapi dev
```

> Important : arrêtez toujours le serveur avant de supprimer `app.db`. Sur certains systèmes de fichiers, supprimer une base encore ouverte peut rendre le fichier inaccessible en écriture.

---

## Notes de sécurité

- L'authentification est basée uniquement sur l'email : **aucun mot de passe n'est demandé**.
- L'email est validé au niveau du format et de son existence en base, mais **aucun email de confirmation n'est envoyé**.
- Les tokens n'expirent pas automatiquement : ils restent valides jusqu'à `/auth/logout` ou jusqu'à la suppression de l'utilisateur.
- Toutes les routes métier (`/users`, `/pharmacies`, `/medicaments`) nécessitent un token valide.
- Pour un usage en production, ajoutez une vérification d'email, une expiration des tokens et des règles de permissions par utilisateur.
