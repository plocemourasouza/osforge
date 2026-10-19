Deliverables expected: 10 handlers (authors: list, get, create, update, delete; books: list, get,
create, update, delete), in two exported routers, with Zod schemas.
Per-handler requirements: 404 on unknown id (get, update, delete); 400 with Zod issues on invalid
body (create, update; update rejects an empty object); 201 on create; 204 on delete; book create and
book update check `authorId` exists (update only when `authorId` is in the patch) -> 400; author delete
returns 409 while books reference the author (e.g. `(await books.list()).some(b => b.authorId === id)`).
Async errors should reach Express's error handling (Express 5 handles rejected promises; for Express 4
a wrapper or try/catch->next is needed — either is acceptable if consistent).
A handler counts as complete only if its code is fully written (no placeholder, no "same as above").
