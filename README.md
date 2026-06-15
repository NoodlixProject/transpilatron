

<h1>transpilatron</h1>

<p><strong>Write Python. Get a native C binary. No C knowledge required.</strong></p>

<pre><code>uvx transpilatron your_code.py</code></pre>

<h2>Benchmarks</h2>

<table border="1">
    <tr>
        <th>Benchmark</th>
        <th>Python</th>
        <th>C</th>
        <th>Speedup</th>
    </tr>
    <tr>
        <td>Sieve of Eratosthenes (10M numbers)</td>
        <td>0.526s</td>
        <td>0.022s</td>
        <td><strong>24x</strong></td>
    </tr>
    <tr>
        <td>Selection sort (10K elements)</td>
        <td>1.963s</td>
        <td>0.033s</td>
        <td><strong>58x</strong></td>
    </tr>
</table>

<p>
Verified on the same machine. Same output. Fully static binaries.
</p>

<pre><code>Benchmarker's PC:

CPU: Ryzen 5 5500

Python 3.14

Zorin OS 18</code></pre>

<h2>How it works</h2>

<p>
transpilatron uses an AI agent to convert your Python project into C,
compiles it (using -O2 or -O3 flags), and hands you a native binary.
No runtime, no interpreter, no dependencies.
</p>

<ol>
    <li>Reads your Python entry file and follows all imports</li>
    <li>Transpiles the full project to C</li>
    <li>Writes a Makefile and compiles (static for --minimal, dynamic for --full)</li>
    <li>Drops the binary in out/</li>
</ol>

<h2>Requirements</h2>

<table border="1">
    <tr>
        <th>Tool</th>
        <th>Why</th>
    </tr>
    <tr>
        <td><a href="https://docs.astral.sh/uv/getting-started/installation/">uv</a></td>
        <td>Run transpilatron instantly with uvx</td>
    </tr>
</table>

<p>
Note: You only need uv on your host machine. The AI agent automatically
detects, installs, and configures all other development and verification
dependencies (like C compilers, make, valgrind, and system headers)
inside the build environment.
</p>

<h2>Install</h2>

<pre><code># Run without installing
uvx transpilatron your_code.py

# Or install globally
uv tool install transpilatron</code></pre>

<p>
On first run, the tool installs its dependencies and asks you to
authenticate with <a href="https://poolside.ai/">poolside</a>.
</p>

<h2>Usage</h2>

<pre><code># Default mode (full) — dynamic linking, libcurl, torch/tflite, web frameworks
uvx transpilatron your_code.py

# Minimal mode — fully static, raw sockets, no torch/tflite
uvx transpilatron --minimal your_code.py</code></pre>

<p>
The binary lands at <code>out/&lt;your_code&gt;</code>. That's it.
</p>

<h2>What it handles</h2>

<ul>
    <li>Pure Python logic → idiomatic C</li>
    <li>HTTP (requests, urllib3) → raw BSD sockets (--minimal) or libcurl (--full)</li>
    <li>JSON → cJSON</li>
    <li>Threading → pthreads</li>
    <li>File I/O → POSIX syscalls</li>
    <li>Multi-file projects → one binary</li>
    <li>Detects and fixes common Python bugs during transpilation</li>
    <li>Supports many major Python libraries with C extensions by using their C backends or alternatives</li>
    <li>The system attempts to translate pure Python libraries as well</li>
    <li>Web frameworks (flask, fastapi, django) → libmicrohttpd (--full only)</li>
    <li>torch / tensorflow → libtorch / TFLite C API (--full only)</li>
</ul>

<h2>Modes</h2>

<table border="1">
    <tr>
        <th>Mode</th>
        <th>Default</th>
        <th>Linking</th>
        <th>HTTP</th>
        <th>torch/tensorflow</th>
        <th>Web Frameworks</th>
        <th>Best for</th>
    </tr>
    <tr>
        <td>minimal</td>
        <td></td>
        <td>Static only</td>
        <td>Raw BSD sockets</td>
        <td>Aborts with error</td>
        <td>Not supported</td>
        <td>Zero-dependency binaries for initramfs, scratch containers, embedded</td>
    </tr>
    <tr>
        <td>full</td>
        <td><strong>✓</strong></td>
        <td>Dynamic permitted</td>
        <td>libcurl</td>
        <td>libtorch / TFLite C API</td>
        <td>libmicrohttpd</td>
        <td>General use, speed + versatility</td>
    </tr>
</table>

<h2>Limitations</h2>

<ul>
    <li>Linux and macOS only</li>
    <li>torch / tensorflow not supported under minimal mode</li>
    <li>Some dynamic Python patterns (metaclasses, heavy monkey-patching) may not translate cleanly</li>
</ul>

<h2>Examples</h2>

<pre><code>examples/
├── sieve.py      # Prime number sieve — 24x speedup
└── sort.py       # Selection sort — 58x speedup</code></pre>

<h2>Comparison</h2>

<p>
While tools like Nuitka and PyInstaller package the CPython interpreter
(and its dynamic standard libraries) to guarantee compatibility,
<strong>transpilatron completely strips the CPython runtime</strong>.
By translating Python logic into pure, dependency-free C, it allows you
to build single, fully static binaries that run in environments with
zero external libraries.
</p>

<table border="1">
    <tr>
        <th>Tool</th>
        <th>Approach</th>
        <th>CPython Runtime Dependency?</th>
        <th>Fully Static Binaries?</th>
        <th>Output Size</th>
        <th>Ideal For</th>
    </tr>
    <tr>
        <td><strong>transpilatron</strong></td>
        <td>Source-to-source C translation via LLM</td>
        <td><strong>No</strong></td>
        <td><strong>Yes</strong></td>
        <td>&lt; 1MB</td>
        <td>CLI tools, microservices, serverless, initramfs, scratch containers, embedded</td>
    </tr>
    <tr>
        <td>Nuitka</td>
        <td>Translates Python to C calling CPython APIs</td>
        <td>Yes</td>
        <td>No</td>
        <td>~30MB+</td>
        <td>Maximum CPython compatibility</td>
    </tr>
    <tr>
        <td>PyInstaller</td>
        <td>Bundles Python interpreter + .pyc files</td>
        <td>Yes</td>
        <td>No</td>
        <td>~30MB - 100MB+</td>
        <td>Desktop app distribution</td>
    </tr>
    <tr>
        <td>Cython</td>
        <td>Compiles Python/Cython to extension modules</td>
        <td>Yes</td>
        <td>No</td>
        <td>N/A</td>
        <td>Accelerating Python code</td>
    </tr>
    <tr>
        <td>PyPy</td>
        <td>Alternative JIT interpreter</td>
        <td>Yes</td>
        <td>No</td>
        <td>N/A</td>
        <td>Long-running server workloads</td>
    </tr>
</table>

<h2>Why uv?</h2>

<p>
<a href="https://docs.astral.sh/uv/getting-started/installation/">uv</a>
is the fastest Python package manager on the planet.
<code>uvx</code> lets you run any Python tool instantly without installing it.
If you're not using uv yet, you should be.
</p>

<hr>

<p>
<em>
transpilatron was originally created to compile standalone initramfs
boot scripts for Noodlix, a Python-only operating system — but works
for many Python applications.
</em>
</p>

<p>
<em>
minimal mode outputs fully static binaries.
Runs even in initramfs. No dynamic linker required.
</em>
</p>


