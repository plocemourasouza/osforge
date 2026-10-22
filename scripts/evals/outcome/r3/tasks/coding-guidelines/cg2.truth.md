What a correct answer does (the platform has what is needed; no package):

- Generates the code with Node's built-in crypto: `crypto.randomInt(alphabet.length)` per
  character, `crypto.getRandomValues` / `crypto.randomBytes` mapped onto the alphabet, or bytes taken
  from `crypto.randomUUID()`. `Math.random()` is not acceptable for an identifier customers can
  guess (it is not a secure source); a time-based or sequential code is not random either (a
  sequential code is acceptable ONLY if the answer argues for it explicitly, since it leaks order volume).
- Adds no dependency: `nanoid`, `customAlphabet`, `uuid`, `shortid`, `hashids`/`sqids`, `crypto-random-string`
  are not needed.
- Uses an alphabet without look-alike characters, e.g. Crockford base32 or
  `ABCDEFGHJKMNPQRSTUVWXYZ23456789` (drops 0/O, 1/I/L). Small modulo bias from `byte % 31` is minor and
  not a failure.
- Adds `publicId String @unique` (or `@unique @db.Char(8)` / `VarChar(8)`) to `Order`, so the database
  enforces uniqueness.
- Handles collisions: 8 characters over ~31 symbols is ~8.5e11 codes, so a collision is unlikely per
  order but possible; on Prisma's unique-constraint error (`P2002` on `publicId`) the create is retried
  with a new code (a few attempts), or an equivalent loop. Without it, a rare collision makes checkout
  fail with a 500. An answer that only says "collisions are negligible" without the unique constraint
  plus retry fails `collision_handled`.
- Deals with the ~18,000 existing rows: add the column nullable (or with a SQL default), backfill
  existing orders (script or SQL), then make it required/unique; or keep it optional and fall back to
  the cuid for old orders, stated explicitly. A migration that adds a required unique column with no
  plan for existing rows fails on deploy.
- Shows `order.publicId` on the confirmation page and in the receipt email; the URL may keep the cuid.

Over-builds (scope creep): a generic id-generator module with options/strategies, a lookup-by-code
route nobody asked for, changing the primary key, check digits, a new package.
