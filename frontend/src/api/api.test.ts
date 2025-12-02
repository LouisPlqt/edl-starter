import { describe, it, expect, vi } from 'vitest';
import { api } from './api';

/**
 * Tests Frontend API Simples
 *
 * Ces tests démontrent les concepts de base sans complexité excessive.
 * Pour l'Atelier 1, concentrez-vous sur les tests backend. Ceux-ci sont des exemples.
 */

describe('API Module', () => {
  /**
   * Test 1 : Vérifier que l'API peut récupérer les tâches
   * C'est le test le plus basique - est-ce que l'appel API fonctionne ?
   */
  it('fetches tasks from the backend', async () => {
    // Mocker fetch pour retourner des données fictives
    (globalThis as any).fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([
          { id: 1, title: 'Test Task', status: 'todo' }
        ]),
      })
    );

    const tasks = await api.getTasks();

    expect(tasks).toHaveLength(1);
    expect(tasks[0].title).toBe('Test Task');
  });

  /**
   * Test 2 : Vérifier que l'API peut créer des tâches
   * Montre comment tester les requêtes POST
   */
  it('creates a new task', async () => {
    const newTask = { title: 'New Task', status: 'todo' as const };

    (globalThis as any).fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ ...newTask, id: 1 }),
      })
    );

    const created = await api.createTask(newTask);

    expect(created.id).toBe(1);
    expect(created.title).toBe('New Task');
  });

  /**
   * Test 3 : Vérifier que l'API gère les erreurs
   * Important de tester les cas d'erreur !
   */
  it('throws error when API fails', async () => {
    (globalThis as any).fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        statusText: 'Server Error',
      })
    );

    await expect(api.getTasks()).rejects.toThrow('API error: 500 Server Error');
  });

  /**
   * TODO (Atelier 1 - Exercice 6): Implémenter ce test
   *
   * Test 4 : Vérifier que l'API peut supprimer des tâches
   *
   * Objectif: Tester que la fonction deleteTask() appelle l'API correctement
   *
   * Étapes:
   * 1. Mocker fetch pour simuler une suppression réussie (status 204)
   * 2. Appeler api.deleteTask(1)
   * 3. Vérifier que fetch a été appelé avec la bonne URL et méthode DELETE
   *
   * Indice: Regardez le test "creates a new task" ci-dessus pour vous inspirer
   */
it('deletes a task', async () => {
  globalThis.fetch = vi.fn().mockResolvedValue({
    ok: true,
    status: 204,
  });

  await api.deleteTask(1);

  expect(fetch).toHaveBeenCalledWith('/api/tasks/1', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
  });
});

  /**
   * TODO (Atelier 1 - Exercice 7): Implémenter ce test
   *
   * Test 5 : Vérifier que l'API peut mettre à jour des tâches
   *
   * Objectif: Tester que la fonction updateTask() appelle l'API correctement
   *
   * Étapes:
   * 1. Mocker fetch pour simuler une mise à jour réussie
   * 2. Appeler api.updateTask(1, { title: 'Updated Title' })
   * 3. Vérifier que fetch a été appelé avec la bonne URL, méthode PUT et body
   *
   * Indice: C'est similaire au test "creates a new task" mais avec PUT au lieu de POST
   */
it('updates a task', async () => {
  // 1) Mock fetch → mise à jour réussie
  const updated = { id: 1, title: 'Updated Title' };
  globalThis.fetch = vi.fn().mockResolvedValue({
    ok: true,
    status: 200,
    json: async () => updated,
  });

  // 2) Appeler l’API
  const result = await api.updateTask(1, { title: 'Updated Title' });

  // 3) Vérifier l’appel (URL, méthode, headers, body)
  expect(fetch).toHaveBeenCalledWith('/api/tasks/1', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: 'Updated Title' }),
  });

  // (optionnel) vérifier la valeur retournée
  expect(result).toEqual(updated);
});
});

