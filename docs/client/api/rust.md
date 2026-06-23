# Rust API

The EdgeFirst Client Rust crate is the core library behind the CLI and all language bindings.

- **Full reference:** [docs.rs/edgefirst-client](https://docs.rs/edgefirst-client/latest/edgefirst_client/)
- **Crate:** [crates.io/crates/edgefirst-client](https://crates.io/crates/edgefirst-client)
- **Source:** [github.com/EdgeFirstAI/client](https://github.com/EdgeFirstAI/client)

## Quick start

```rust
use edgefirst_client::{Client, Error};

#[tokio::main]
async fn main() -> Result<(), Error> {
    let client = Client::new()?;
    let client = client.with_login("username", "password").await?;

    let projects = client.projects(None).await?;
    println!("Found {} projects", projects.len());

    Ok(())
}
```

## Optional features

| Feature | Description |
|---------|-------------|
| `polars` | Polars DataFrame integration (`samples_dataframe`) |
| `tracing` | Instrumentation hooks for profiling |

Enable features in `Cargo.toml`:

```toml
edgefirst-client = { version = "2", features = ["polars"] }
```

## COCO module

The Rust crate includes a `coco` module for COCO/LVIS format conversion and Studio import/export. CLI commands such as `import-coco` and `coco-to-arrow` call into this module. See the [dataset import guide](../import.md) for usage from the command line.

## See also

- [Python API](python.md)
- [Python tutorials](../tutorials/index.md)
- [CLI reference](../cli/reference.md)
