# transpilatron

> Write Python. Get a native C binary. No C knowledge required.

```bash
uvx transpilatron your_code.py
```

## Benchmarks

| Benchmark | Python | C | Speedup |
|-----------|--------|---|---------|
| Sieve of Eratosthenes (10M numbers) | 0.526s | 0.022s | **24x** |
| Selection sort (10K elements) | 1.963s | 0.033s | **58x** |

*Verified on the same machine. Same output. Fully static binaries.*

## How it works

transpilatron uses an AI agent to convert your Python project into C, compiles it (using `-O2` or `-O3` flags), and hands you a fully static binary. No runtime, no interpreter, no dependencies.

1. Reads your Python entry file and follows all imports
2. Transpiles the full project to C
3. Writes a Makefile and compiles with static linking
4. Drops the binary in `out/`

## Requirements

| Tool | Why |
|------|-----|
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | Run transpilatron instantly with `uvx` |

*Note: You only need `uv` on your host machine. The AI agent automatically detects, installs, and configures all other development and verification dependencies (like C compilers, `make`, `valgrind`, and system headers) inside the build environment.*


## Install

```bash
# Run without installing
uvx transpilatron your_code.py

# Or install globally
uv tool install transpilatron
```

On first run, the tool installs its dependencies, and asks you to authenticate with [poolside](https://poolside.ai/).

## Usage

```bash
uvx transpilatron your_code.py
```

The binary lands at `out/<your_code>`. That's it.

## What it handles

- Pure Python logic → idiomatic C
- HTTP (`requests`, `urllib3`) → raw BSD sockets
- JSON → cJSON
- Threading → pthreads  
- File I/O → POSIX syscalls
- Multi-file projects → one binary
- Detects and fixes common Python bugs during transpilation
- Supports many major Python libraries with C extensions by simply using their C backends or alternatives
- The system attempts to translate pure Python libraries as well

## Limitations

- Linux and macOS only
- `torch` / `tensorflow` — not supported (aborts with a clear error)
- Some dynamic Python patterns (metaclasses, heavy monkey-patching) may not translate cleanly

## Examples

```
examples/
├── sieve.py      # Prime number sieve — 24x speedup
└── sort.py       # Selection sort — 58x speedup
```

## Comparison

While tools like Nuitka and PyInstaller package the CPython interpreter (and its dynamic standard libraries) to guarantee compatibility, **transpilatron completely strips the CPython runtime**. By translating Python logic into pure, dependency-free C, it allows you to build single, fully static binaries that run in environments with zero external libraries.

| Tool | Approach | CPython Runtime Dependency? | Fully Static Binaries? | Output Size | Ideal For |
|---|---|---|---|---|---|
| **transpilatron** | Source-to-source C translation via LLM | **No** | **Yes** (trivial) | **< 1MB** | **Any Python application** (CLI tools, microservices, serverless, initramfs, scratch containers, embedded) |
| **Nuitka** | Translates Python to C calling CPython APIs | **Yes** | **No** (requires "shared libs galore" and dynamic loading) | **~30MB+** | 100% CPython compatibility for desktop/server applications |
| **PyInstaller** | Bundles Python interpreter + `.pyc` files into a zip | **Yes** | **No** (unpacks dynamic libraries to `/tmp` at runtime) | **~30MB - 100MB+** | Distributing desktop apps where size and startup speed don't matter |
| **Cython** | Compiles Python/Cython to a C extension module | **Yes** | **No** (produces a `.so` file that must be imported inside Python) | N/A (requires python host) | Speeding up hot paths inside an existing Python project |
| **PyPy** | Alternative JIT-compiled interpreter | **Yes** | **No** | N/A (it's a heavy runtime) | Long-running Python server applications needing JIT speedups |

## Why uv?

[uv](https://docs.astral.sh/uv/getting-started/installation/) is the fastest Python package manager on the planet. `uvx` lets you run any Python tool instantly without installing it. If you're not using uv yet, you should be.

---

*Outputs fully static binaries. Runs even in initramfs. No dynamic linker required.*