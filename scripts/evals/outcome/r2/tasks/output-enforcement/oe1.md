Write the 10 Express (TypeScript) route handlers for our two resources, complete — I'll paste them straight in. Resources: `Author { id: string; name: string; country: string }` and `Book { id: string; title: string; authorId: string; year: number }`. Handlers, for each resource: list (GET /), get by id (GET /:id), create (POST /), update (PATCH /:id), delete (DELETE /:id). Use this existing repository interface (already implemented elsewhere):

```ts
// lib/repo.ts
export interface Repo<T extends { id: string }> {
  list(): Promise<T[]>;
  get(id: string): Promise<T | undefined>;
  create(data: Omit<T, "id">): Promise<T>;
  update(id: string, patch: Partial<Omit<T, "id">>): Promise<T | undefined>;
  remove(id: string): Promise<boolean>;
}
export declare const authors: Repo<Author>;
export declare const books: Repo<Book>;
```

Requirements: validate request bodies with Zod (create: all fields required; update: all optional, at least one); 404 when the id does not exist; 400 with the Zod issues on invalid input; 201 on create; 204 on delete; creating or updating a book must 400 if `authorId` does not exist; deleting an author that still has books must 409. Export one router per resource.
