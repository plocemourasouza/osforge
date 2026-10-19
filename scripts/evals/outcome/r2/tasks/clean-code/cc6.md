This legacy Node module is a mess (mixed concerns, `var`, console logging). Please clean it up. Existing callers must keep working — we have no tests for it.

```js
// userImport.js
const fs = require("fs");

var seen = {};

function importUsers(path, cb) {
  var data = fs.readFileSync(path, "utf8");
  var lines = data.split("\n");
  var out = [];
  for (var i = 1; i < lines.length; i++) { // skip header
    var l = lines[i];
    if (l == "") continue;
    var parts = l.split(",");
    var email = parts[1].trim().toLowerCase();
    if (seen[email]) continue;
    seen[email] = true;
    var age = parts[2] == "" ? null : parseInt(parts[2]);
    out.push({
      name: parts[0],
      email: email,
      age: age,
      vip: parts[3] == "1" || parts[3] == "true",
    });
    console.log("imported " + email);
  }
  cb(null, out);
}

module.exports = { importUsers };
```

For context, this is how the nightly job uses it:

```js
// nightly.js
const { importUsers } = require("./userImport");
for (const file of ["crm.csv", "shop.csv", "events.csv"]) {
  importUsers(file, (err, users) => {
    if (err) throw err;
    upsertAll(users);
  });
}
```
