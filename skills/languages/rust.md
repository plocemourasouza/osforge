# Rust Pro

**Trigger:** Rust, cargo, ownership, borrowing, lifetimes, async Rust

---

## Core Concepts

### Ownership
```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;  // s1 is moved, no longer valid
    // println!("{}", s1);  // Error!
    println!("{}", s2);

    let s3 = s2.clone();  // Explicit copy
    println!("{} {}", s2, s3);  // Both valid
}
```

### Borrowing
```rust
fn main() {
    let s = String::from("hello");

    // Immutable borrow (many allowed)
    let len = calculate_length(&s);
    println!("{} has length {}", s, len);

    // Mutable borrow (only one at a time)
    let mut s2 = String::from("hello");
    change(&mut s2);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &mut String) {
    s.push_str(", world");
}
```

### Lifetimes
```rust
// Explicit lifetime annotations
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with lifetime
struct ImportantExcerpt<'a> {
    part: &'a str,
}
```

---

## Error Handling

### Result and Option
```rust
use std::fs::File;
use std::io::Read;

fn read_file(path: &str) -> Result<String, std::io::Error> {
    let mut file = File::open(path)?;  // ? propagates error
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

fn find_user(id: u32) -> Option<User> {
    users.iter().find(|u| u.id == id).cloned()
}

// Using them
match read_file("config.txt") {
    Ok(contents) => println!("{}", contents),
    Err(e) => eprintln!("Error: {}", e),
}

if let Some(user) = find_user(42) {
    println!("Found: {}", user.name);
}
```

### Custom Errors
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Validation error: {0}")]
    Validation(String),
}
```

---

## Async Rust (Tokio)

### Basic Async
```rust
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data().await;
    println!("{:?}", result);
}

async fn fetch_data() -> Result<String, reqwest::Error> {
    let response = reqwest::get("https://api.example.com/data")
        .await?
        .text()
        .await?;
    Ok(response)
}
```

### Concurrent Tasks
```rust
use tokio::join;

async fn main() {
    // Run concurrently
    let (a, b, c) = join!(
        fetch_users(),
        fetch_orders(),
        fetch_products()
    );

    // Or spawn tasks
    let handle = tokio::spawn(async {
        expensive_computation().await
    });

    let result = handle.await.unwrap();
}
```

### Channels
```rust
use tokio::sync::mpsc;

async fn main() {
    let (tx, mut rx) = mpsc::channel(32);

    tokio::spawn(async move {
        tx.send("hello").await.unwrap();
    });

    while let Some(message) = rx.recv().await {
        println!("Received: {}", message);
    }
}
```

---

## Axum Web Framework

```rust
use axum::{
    routing::{get, post},
    Router, Json, extract::Path,
};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct User {
    id: u32,
    name: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
}

async fn get_user(Path(id): Path<u32>) -> Json<User> {
    Json(User { id, name: "John".into() })
}

async fn create_user(Json(payload): Json<CreateUser>) -> Json<User> {
    Json(User { id: 1, name: payload.name })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/users/:id", get(get_user))
        .route("/users", post(create_user));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

---

## Common Patterns

### Builder Pattern
```rust
#[derive(Default)]
struct RequestBuilder {
    url: Option<String>,
    method: Option<String>,
    headers: Vec<(String, String)>,
}

impl RequestBuilder {
    fn new() -> Self {
        Self::default()
    }

    fn url(mut self, url: &str) -> Self {
        self.url = Some(url.to_string());
        self
    }

    fn method(mut self, method: &str) -> Self {
        self.method = Some(method.to_string());
        self
    }

    fn build(self) -> Result<Request, &'static str> {
        Ok(Request {
            url: self.url.ok_or("URL required")?,
            method: self.method.unwrap_or_else(|| "GET".to_string()),
            headers: self.headers,
        })
    }
}

// Usage
let request = RequestBuilder::new()
    .url("https://api.example.com")
    .method("POST")
    .build()?;
```

### Type State Pattern
```rust
struct Locked;
struct Unlocked;

struct Door<State> {
    _state: std::marker::PhantomData<State>,
}

impl Door<Locked> {
    fn unlock(self) -> Door<Unlocked> {
        Door { _state: std::marker::PhantomData }
    }
}

impl Door<Unlocked> {
    fn lock(self) -> Door<Locked> {
        Door { _state: std::marker::PhantomData }
    }

    fn open(&self) {
        println!("Opening door");
    }
}

// Can only open unlocked door
let door: Door<Locked> = Door { _state: std::marker::PhantomData };
// door.open();  // Error! Not available on Locked
let door = door.unlock();
door.open();  // Works!
```

---

## Cargo Commands

```bash
# Create project
cargo new my_project
cargo new --lib my_library

# Build
cargo build
cargo build --release

# Run
cargo run
cargo run --release

# Test
cargo test
cargo test -- --nocapture  # Show println output

# Check (fast, no codegen)
cargo check

# Format
cargo fmt

# Lint
cargo clippy

# Documentation
cargo doc --open

# Add dependency
cargo add tokio --features full
cargo add serde --features derive
```

---

## Best Practices

1. **Prefer `&str` over `String` in function parameters**
2. **Use `clippy` and fix all warnings**
3. **Implement `From` for error conversions**
4. **Use `#[derive]` liberally**
5. **Prefer composition over inheritance**
6. **Use `Option` and `Result`, avoid panics**
7. **Document public APIs with `///`**
