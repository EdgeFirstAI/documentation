# API Reference

The EdgeFirst Client library is implemented in Rust with language bindings for Python, Swift, and Kotlin.

| Language | Documentation |
|----------|---------------|
| **Python** | [Python API](python.md) — generated from the installed `edgefirst_client` package |
| **Rust** | [Rust API](rust.md) — [docs.rs](https://docs.rs/edgefirst-client/latest/edgefirst_client/) |
| **Swift / iOS** | [APPLE.md on GitHub](https://github.com/EdgeFirstAI/client/blob/main/APPLE.md) |
| **Kotlin / Android** | [ANDROID.md on GitHub](https://github.com/EdgeFirstAI/client/blob/main/ANDROID.md) |

## Python

Install with `pip install edgefirst-client`. IDE autocompletion uses `edgefirst_client.pyi` stubs shipped in the wheel.

Start with the [Python tutorials](../tutorials/index.md) before diving into the full API surface.

## Rust

The Rust crate powers the CLI and all bindings. See [Rust API](rust.md) for a quick-start snippet and link to the full docs.rs reference.

## Swift and Kotlin

Mobile bindings are generated via UniFFI from the same Rust core. They expose the same Studio operations (datasets, annotations, training) with platform-idiomatic APIs. Progress callbacks are not available on all FFI methods — see the platform README files for details.
