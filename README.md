# 🚀 EDL Starter - Code de Démarrage

Bienvenue dans le code de démarrage pour les ateliers d'Environnement de Développement Logiciel (EDL) !

## 📦 Contenu

Ce starter contient une application **TaskFlow** complète avec :

- **Backend FastAPI** (Python) - API REST pour gérer des tâches
- **Frontend React** (TypeScript) - Interface utilisateur simple
- **Tests unitaires** - Backend (pytest) et Frontend (Vitest)

## 🎯 Pour Commencer

### Prérequis

- **Python 3.11+** (pour le backend)
- **Node.js 18+** (pour le frontend)
- **Git**

### Installation

#### Option 1 : Cloner depuis GitHub (Recommandé)

```bash
git clone https://github.com/umons-ig/edl-starter
cd edl-starter
```

#### Option 2 : Utiliser ce Dossier Local

```bash
cd edl-starter
```

## 📖 Suivre les Travaux Pratiques

### TP 1 : Tests Unitaires (3h)

**Objectif :** Apprendre à écrire des tests unitaires backend et frontend

📄 **Documentation :** Voir [`docs/TP-1.md`](../docs/TP-1.md) ou [`docs/TP-1.pdf`](../docs/TP-1.pdf)

**Ce que vous allez faire :**
- ✅ Installer les dépendances (UV ou pip)
- ✅ Lancer le backend et le frontend localement
- ✅ Écrire des tests backend avec pytest
- ✅ Écrire des tests frontend avec Vitest
- 🎁 **BONUS :** Exercices Java JUnit

**Démarrage rapide :**

```bash
# Backend
cd backend
uv venv && uv sync
uv run uvicorn src.app:app --reload

# Frontend (nouveau terminal)
cd frontend
npm install
npm run dev
```

---

### TP 2 : CI/CD avec GitHub Actions (3h)

**Objectif :** Automatiser les tests avec GitHub Actions

📄 **Documentation :** Voir [`docs/TP-2.md`](../docs/TP-2.md)

**Ce que vous allez faire :**
- ✅ Créer un workflow GitHub Actions
- ✅ Tester automatiquement backend + frontend
- ✅ Vérifier la couverture de code sur CI
- ✅ Comprendre le pipeline CI/CD

---

### TP 3 : Déploiement + Database (3h)

**Objectif :** Déployer l'application en production avec PostgreSQL

📄 **Documentation :** Voir [`docs/TP-3.md`](../docs/TP-3.md)

**Ce que vous allez faire :**
- ✅ Migrer de stockage en mémoire vers PostgreSQL
- ✅ Déployer sur Render
- ✅ Configurer les variables d'environnement
- ✅ Tester l'application en production

---

## 📂 Structure du Projet

```
edl-starter/
├── backend/
│   ├── src/
│   │   ├── app.py           # API FastAPI principale
│   │   └── __init__.py
│   ├── tests/
│   │   ├── conftest.py      # Fixtures pytest
│   │   └── test_api.py      # Tests API
│   ├── pyproject.toml       # Dépendances Python
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Composant principal
│   │   ├── api/
│   │   │   ├── api.ts       # Client API
│   │   │   └── api.test.ts  # Tests API
│   │   └── components/
│   │       ├── SimpleTaskList.tsx
│   │       └── TaskForm.tsx
│   ├── package.json         # Dépendances Node.js
│   └── vite.config.ts
│
├── .github/
│   └── workflows/           # Workflows à créer dans TP 2
│
└── README.md (ce fichier)
```

---

## 🧪 Lancer les Tests

### Backend

```bash
cd backend
uv run pytest -v                    # Tous les tests
uv run pytest --cov                 # Avec couverture
uv run pytest --cov-report=html     # Rapport HTML
```

### Frontend

```bash
cd frontend
npm test                            # Tests en mode watch
npm test -- --run                   # Tests une fois (pour CI)
npm run test:coverage               # Avec couverture
```

---

## 🚀 Lancer l'Application Complète

**Terminal 1 - Backend :**

```bash
cd backend
uv run uvicorn src.app:app --reload
# → http://localhost:8000
```

**Terminal 2 - Frontend :**

```bash
cd frontend
npm run dev
# → http://localhost:5173
```

**Ouvrir dans le navigateur :** <http://localhost:5173>

---

## 🔧 Configuration

### Backend

Le backend utilise un **stockage en mémoire** (dictionnaire Python) pour les TP 1 et 2.

**TP 3 :** Vous migrerez vers PostgreSQL.

**Fichier de config :** `backend/.env.example`

```env
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow
ENVIRONMENT=development
```

### Frontend

**Fichier de config :** `frontend/.env.example`

```env
VITE_API_URL=http://localhost:8000
```

---

## 📚 Technologies Utilisées

### Backend
- **FastAPI** - Framework web moderne et rapide
- **pytest** - Framework de tests Python
- **pytest-cov** - Couverture de code
- **Pydantic** - Validation de données
- **SQLAlchemy** - ORM (Atelier 3)
- **UV** - Gestionnaire de paquets Python moderne

### Frontend
- **React 18** - Framework UI
- **TypeScript** - Typage statique
- **Vitest** - Framework de tests
- **Vite** - Build tool rapide
- **React Testing Library** - Tests de composants

---

## 🆘 Problèmes Courants

### Backend ne démarre pas

```bash
# Vérifier que vous êtes dans backend/
cd backend

# Réinstaller les dépendances
uv sync
```

### Frontend ne démarre pas

```bash
# Vérifier que vous êtes dans frontend/
cd frontend

# Réinstaller les dépendances
rm -rf node_modules package-lock.json
npm install
```

### Tests qui échouent

```bash
# Backend : lancer un seul test
uv run pytest tests/test_api.py::test_create_task -v -s

# Frontend : mode verbose
npm test -- --reporter=verbose
```

---

## 🎓 Ressources Supplémentaires

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation pytest](https://docs.pytest.org/)
- [Documentation UV](https://docs.astral.sh/uv/)
- [Documentation React](https://react.dev/)
- [Documentation Vitest](https://vitest.dev/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 📝 Notes Importantes

### Stockage en Mémoire (TP 1-2)

⚠️ Les données sont **stockées en mémoire** (dictionnaire Python). Si vous redémarrez le backend, **toutes les données sont perdues**.

C'est **intentionnel** pour simplifier l'apprentissage des tests unitaires.

### Migration vers PostgreSQL (TP 3)

Dans le TP 3, vous allez :
1. Créer une base de données PostgreSQL
2. Configurer SQLAlchemy
3. Migrer le code pour utiliser la DB
4. Déployer en production

---

## 📧 Support

**Problèmes avec les travaux pratiques ?**

1. Vérifiez la documentation dans `docs/`
2. Relisez la section "🆘 Problèmes Courants"
3. Consultez votre professeur ou assistant

---

**Bon courage pour les travaux pratiques ! 🚀**

Version: 1.0 - EDL 2024-2025
"# Test PR" 
