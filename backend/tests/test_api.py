"""
Tests API TaskFlow - Atelier 1 Starter

Apprenez en faisant ! Ce fichier vous montre comment écrire des tests, puis vous en écrirez de similaires.

Structure de chaque test :
1. ARRANGE - Préparer les données de test
2. ACT - Faire la requête API
3. ASSERT - Vérifier la réponse
"""

import pytest


# =============================================================================
# PARTIE 1 : TESTS EXEMPLES (Apprenez de ceux-ci !)
# =============================================================================

def test_root_endpoint(client):
    """
    EXEMPLE : Tester un point de terminaison GET simple.

    Ce test vous montre le pattern de base :
    1. Faire une requête avec client.get()
    2. Vérifier le code de statut
    3. Vérifier les données de la réponse
    """
    # ACT : Faire une requête GET
    response = client.get("/")

    # ASSERT : Vérifier la réponse
    assert response.status_code == 200
    assert "Welcome to TaskFlow API" in response.json()["message"]


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"  # ✅ Correct

def test_create_task(client):
    """
    EXEMPLE : Tester un point de terminaison POST (création de données).

    Pattern pour les requêtes POST :
    1. Préparer les données comme un dictionnaire Python
    2. Les envoyer avec client.post()
    3. Vérifier le code de statut (201 = Créé)
    4. Vérifier les données retournées
    """
    # ARRANGE : Préparer les données
    new_task = {
        "title": "Acheter des courses",
        "description": "Lait, œufs, pain"
    }

    # ACT : Envoyer la requête POST
    response = client.post("/tasks", json=new_task)

    # ASSERT : Vérifier la réponse
    assert response.status_code == 201  # 201 = Créé

    task = response.json()
    assert task["title"] == "Acheter des courses"
    assert task["description"] == "Lait, œufs, pain"
    assert task["status"] == "todo"  # Valeur par défaut
    assert "id" in task  # Le serveur génère un ID


def test_list_tasks(client):
    """
    EXEMPLE : Tester GET avec préparation de données.

    Parfois vous devez créer des données d'abord, puis tester leur listage.
    """
    # ARRANGE : Créer quelques tâches d'abord
    client.post("/tasks", json={"title": "Tâche 1"})
    client.post("/tasks", json={"title": "Tâche 2"})

    # ACT : Obtenir la liste des tâches
    response = client.get("/tasks")

    # ASSERT : Vérifier qu'on a bien les deux tâches
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_task_by_id(client):
    """
    EXEMPLE : Tester GET pour une ressource spécifique.

    Pattern :
    1. Créer une tâche d'abord
    2. Obtenir son ID depuis la réponse
    3. Utiliser cet ID pour récupérer la tâche
    """
    # ARRANGE : Créer une tâche
    create_response = client.post("/tasks", json={"title": "Trouve-moi"})
    task_id = create_response.json()["id"]

    # ACT : Obtenir la tâche spécifique
    response = client.get(f"/tasks/{task_id}")

    # ASSERT : Vérifier qu'on a la bonne tâche
    assert response.status_code == 200
    assert response.json()["title"] == "Trouve-moi"


# =============================================================================
# PARTIE 2 : À VOUS ! Complétez ces tests
# =============================================================================

# EXERCICE 1 : Écrire un test pour SUPPRIMER une tâche
# Pattern : Créer → Supprimer → Vérifier qu'elle a disparu
def test_delete_task(client):
    """
    Teste la suppression d'une tâche existante :
    - Crée une tâche
    - Supprime la tâche
    - Vérifie qu'elle a bien disparu
    """

    # Créer une tâche
    response = client.post("/tasks/", json={"title": "Tâche à supprimer", "description": "Test de suppression"})
    assert response.status_code == 201
    task = response.json()
    task_id = task["id"]

    # Supprimer la tâche
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204  # No Content

    # Vérifier qu’elle n’existe plus
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404  # Not Found

def test_delete_nonexistent_task_returns_404(client):
    """Deleting a task that doesn't exist should return 404."""
    # TODO: Votre code ici
    # 1. Essayer de supprimer une tâche avec un ID qui n'existe pas (ex: 9999)
    # 2. Vérifier que ça retourne 404
    # 3. Vérifier le message d'erreur contient "not found"

# EXERCICE 2 : Écrire un test pour METTRE À JOUR une tâche
# Pattern : Créer → Mettre à jour → Vérifier les changements
def test_update_task(client):
    """
    VOTRE TÂCHE : Écrire un test qui met à jour le titre d'une tâche.

    Étapes :
    1. Créer une tâche avec le titre "Titre Original"
    2. Obtenir son ID
    3. Envoyer une requête PUT : client.put(f"/tasks/{task_id}", json={"title": "Nouveau Titre"})
    4. Vérifier que le code de statut est 200
    5. Vérifier que la réponse contient le nouveau titre

    Astuce : Les requêtes PUT sont comme les POST, mais elles modifient des données existantes
    """
    # TODO : Écrivez votre test ici !
    pass


# EXERCICE 3 : Tester la validation - un titre vide devrait échouer
def test_create_task_empty_title(client):
    """
    VOTRE TÂCHE : Tester que créer une tâche avec un titre vide échoue.

    Étapes :
    1. Essayer de créer une tâche avec title = ""
    2. Vérifier que le code de statut est 422 (Erreur de Validation)

    Astuce : Regardez test_create_task, mais attendez-vous à un échec !
    """
    # TODO : Écrivez votre test ici !
    pass


# EXERCICE 4 : Tester la validation - priorité invalide
def test_update_task_with_invalid_priority(client):
    """
    Teste qu'on ne peut pas mettre à jour une tâche avec une priorité invalide.
    """

    # Créer une tâche valide
    response = client.post("/tasks/", json={"title": "Tâche test", "description": "Priorité invalide"})
    assert response.status_code == 201
    task = response.json()
    task_id = task["id"]

    # Essayer de la mettre à jour avec une priorité invalide
    update_response = client.put(f"/tasks/{task_id}", json={"priority": "urgent"})  # "urgent" n'est pas une priorité valide

    # Vérifier que c’est une erreur de validation
    assert update_response.status_code == 422  # Erreur de validation (Unprocessable Entity)



# EXERCICE 5 : Tester l'erreur 404
def test_get_nonexistent_task(client):
    """
    VOTRE TÂCHE : Tester qu'obtenir une tâche qui n'existe pas retourne 404.

    Étapes :
    1. Essayer d'obtenir une tâche avec un faux ID : client.get("/tasks/999")
    2. Vérifier que le code de statut est 404 (Not Found)
    """
    # TODO : Écrivez votre test ici !
    pass

def test_filter_by_multiple_criteria(client):
    """
    Filtering by status AND priority should work.
    """

    # Créer plusieurs tâches avec différents statuts et priorités
    client.post("/tasks/", json={"title": "Tâche 1", "description": "todo + high", "status": "todo", "priority": "high"})
    client.post("/tasks/", json={"title": "Tâche 2", "description": "in_progress + high", "status": "in_progress", "priority": "high"})
    client.post("/tasks/", json={"title": "Tâche 3", "description": "todo + low", "status": "todo", "priority": "low"})

    # Filtrer par status=todo et priority=high
    response = client.get("/tasks?status=todo&priority=high")
    assert response.status_code == 200

    tasks = response.json()

    # Vérifier qu'on reçoit uniquement la tâche correspondante
    assert len(tasks) == 1
    assert tasks[0]["status"] == "todo"
    assert tasks[0]["priority"] == "high"
    assert tasks[0]["title"] == "Tâche 1"


# =============================================================================
# EXERCICES BONUS (Si vous finissez en avance !)
# =============================================================================

# BONUS 1 : Tester le filtrage par statut
def test_filter_tasks_by_status(client):
    """
    BONUS : Tester le filtrage des tâches par statut.

    Étapes :
    1. Créer 2 tâches : une avec status="todo", une avec status="done"
    2. Obtenir les tâches avec le filtre : client.get("/tasks?status=done")
    3. Vérifier que seule la tâche "done" est retournée
    """
    # TODO : Écrivez votre test ici !
    pass


# BONUS 2 : Tester la mise à jour d'un seul champ
def test_update_only_status(client):
    """
    BONUS : Tester que mettre à jour seulement le statut ne change pas les autres champs.

    Étapes :
    1. Créer une tâche avec title="Test" et status="todo"
    2. Mettre à jour seulement le statut à "done"
    3. Vérifier que le statut a changé MAIS le titre est resté le même
    """
    # TODO : Écrivez votre test ici !
    pass


# BONUS 3 : Tester le cycle de vie complet d'une tâche
def test_task_lifecycle(client):
    """
    BONUS : Tester le cycle de vie complet : Créer → Lire → Mettre à jour → Supprimer

    Étapes :
    1. Créer une tâche
    2. La lire (GET par ID)
    3. La mettre à jour (changer le statut à "done")
    4. La supprimer
    5. Vérifier qu'elle a disparu (GET devrait retourner 404)
    """
    # TODO : Écrivez votre test ici !
    pass


# =============================================================================
# ASTUCES & CONSEILS
# =============================================================================

"""
PATTERNS COURANTS :

1. Tester POST (Créer) :
   response = client.post("/tasks", json={"title": "..."})
   assert response.status_code == 201

2. Tester GET (Lire) :
   response = client.get("/tasks")
   assert response.status_code == 200

3. Tester PUT (Mettre à jour) :
   response = client.put(f"/tasks/{id}", json={"title": "..."})
   assert response.status_code == 200

4. Tester DELETE (Supprimer) :
   response = client.delete(f"/tasks/{id}")
   assert response.status_code == 204

5. Tester les erreurs de validation :
   response = client.post("/tasks", json={"bad": "data"})
   assert response.status_code == 422

6. Tester les erreurs 404 :
   response = client.get("/tasks/999")
   assert response.status_code == 404

CODES DE STATUT COURANTS :
- 200 : OK (GET/PUT réussi)
- 201 : Créé (POST réussi)
- 204 : Pas de Contenu (DELETE réussi)
- 404 : Non Trouvé (la ressource n'existe pas)
- 422 : Erreur de Validation (données invalides)

RAPPELEZ-VOUS :
- La fixture `client` est automatiquement fournie par conftest.py
- La base de données est automatiquement nettoyée avant/après chaque test
- Les tests doivent être indépendants (ne pas dépendre d'autres tests)
"""
@pytest.mark.e2e
def test_complete_task_lifecycle(client):
    """Test E2E : Créer plusieurs tâches et les lister."""
    # Créer la première tâche
    response = client.post("/tasks", json={
        "title": "Tâche E2E 1",
        "description": "Première tâche"
    })
    assert response.status_code == 201
    task1_id = response.json()["id"]

    # Créer la deuxième tâche
    response = client.post("/tasks", json={
        "title": "Tâche E2E 2",
        "description": "Deuxième tâche"
    })
    assert response.status_code == 201
    task2_id = response.json()["id"]

    # Lister toutes les tâches
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2

    # Vérifier que nos deux tâches sont dans la liste
    task_ids = [task["id"] for task in tasks]
    assert task1_id in task_ids
    assert task2_id in task_ids

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
