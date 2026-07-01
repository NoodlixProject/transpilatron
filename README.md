
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

<p>Verified on the same machine. Same output. Fully static binaries.</p>

<pre><code>Benchmarker's PC:
CPU: Ryzen 5 5500
Python 3.14
Zorin OS 18</code></pre>

<h2>Demo: Flask app → C web server</h2>

<p>This Flask app:</p>

<pre><code>from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from the webserver!'

@app.route('/ping')
def ping():
    return 'pong'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)</code></pre>

<p>Becomes a native C HTTP server with one command:</p>

<pre><code>uvx transpilatron web.py</code></pre>

<pre><code>$ ./out/web &
Server running on http://0.0.0.0:8080

$ curl http://localhost:8080/
Hello from the webserver!

$ curl http://localhost:8080/ping
pong</code></pre>

<p>
No Flask. No Python runtime. No dependencies. Verified memory-safe by valgrind
(<code>0 errors, 0 leaks</code>).
</p>

<h2>Demo: It transpiles itself</h2>

<p>
transpilatron is written in Python. So we transpiled it.
</p>

<pre><code>uvx transpilatron src/transpilatron/agent.py</code></pre>

<p>
The result is a fully working C binary that does exactly what the Python version does —
reads your entry file, invokes the AI agent, and produces a C binary. Verified valgrind-clean.
</p>

<pre><code>$ ./out/agent --help
Usage: ./agent [--minimal|--full] &lt;entry_file&gt;
  --minimal  Use minimal mode: static linking, raw sockets only
  --full     Use full mode (default): dynamic linking, libcurl, etc.

$ ./out/agent examples/web.py
Thinking...
I'll help you convert the Python project to C...
</code></pre>

<p>
A C binary, orchestrating an AI agent, transpiling Python to C.
</p>

<h2>How it works</h2>

<p>
transpilatron uses an AI agent to convert your Python project into C,
compiles it (using -O2 or -O3 flags), and hands you a native binary.
No runtime, no interpreter, no dependencies.
</p>

<ol>
    <li>Reads your Python entry file and follows all imports</li>
    <li>Transpiles the full project to C</li>
    <li>Writes a Makefile and compiles (static for <code>--minimal</code>, dynamic for <code>--full</code>)</li>
    <li>Automatically installs any missing build tools via your system package manager (with sudo)</li>
    <li>Runs the binary under valgrind to verify zero memory leaks and zero segfaults</li>
    <li>Audits the generated C for race conditions, NULL dereferences, and logic bugs</li>
    <li>Drops the verified binary in <code>out/</code></li>
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
That's it. The AI agent automatically detects, installs, and configures all other
dependencies (C compilers, make, valgrind, system headers, and the Poolside CLI itself)
on first run.
</p>

<h2>Install</h2>

<pre><code># Run without installing
uvx transpilatron your_code.py

# Or install globally
uv tool install transpilatron</code></pre>

<p>
On first run, the tool bootstraps all its dependencies and asks you to
authenticate with <a href="https://poolside.ai/">Poolside</a> (free).
</p>

<h2>Usage</h2>

<pre><code># Default (full mode) — dynamic linking, libcurl, torch/tflite, web frameworks
uvx transpilatron your_code.py

# Minimal mode — fully static, raw sockets, initramfs-safe
uvx transpilatron --minimal your_code.py</code></pre>

<p>The binary lands at <code>out/&lt;your_code&gt;</code>. That's it.</p>

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
        <td><code>--minimal</code></td>
        <td></td>
        <td>Static only</td>
        <td>Raw BSD sockets</td>
        <td>Aborts with error</td>
        <td>Not supported</td>
        <td>initramfs, scratch containers, embedded, zero-dependency binaries</td>
    </tr>
    <tr>
        <td><code>--full</code></td>
        <td><strong>✓</strong></td>
        <td>Dynamic permitted</td>
        <td>libcurl</td>
        <td>libtorch / TFLite C API</td>
        <td>libmicrohttpd</td>
        <td>General use, speed + versatility, web apps</td>
    </tr>
</table>

<h2>What it handles</h2>

<ul>
    <li>Pure Python logic → idiomatic C</li>
    <li>HTTP (<code>requests</code>, <code>urllib3</code>) → raw BSD sockets (<code>--minimal</code>) or libcurl (<code>--full</code>)</li>
    <li>JSON → cJSON</li>
    <li>Threading → pthreads</li>
    <li>File I/O → POSIX syscalls</li>
    <li>Multi-file projects → one binary</li>
    <li>Web frameworks (flask, fastapi, django) → libmicrohttpd (<code>--full</code> only)</li>
    <li>torch / tensorflow → libtorch / TFLite C API (<code>--full</code> only)</li>
    <li>Detects and fixes common Python bugs during transpilation</li>
    <li>Memory-safe output verified by valgrind on every build</li>
</ul>

<h2>Quality &amp; Safety</h2>

<p>Every build goes through an automatic quality pipeline:</p>

<ul>
    <li><strong>Compile errors</strong> — if <code>make</code> fails, the agent reads the errors, fixes the C source, and retries up to 3 times</li>
    <li><strong>Memory safety</strong> — the binary is run under <code>valgrind --leak-check=full</code> to catch leaks and segfaults before delivery</li>
    <li><strong>Logic audit</strong> — the agent reviews the generated C for race conditions, NULL pointer dereferences, off-by-one errors, and semantic bugs</li>
    <li><strong>Missing deps</strong> — build tools and headers are auto-installed via your system package manager with sudo. If sudo fails, you'll get a clear message with instructions to re-run with <code>sudo uvx transpilatron ...</code></li>
</ul>

<h2>Limitations</h2>

<ul>
    <li>Linux and macOS only</li>
    <li>torch / tensorflow not supported in <code>--minimal</code> mode</li>
    <li>Some dynamic Python patterns (metaclasses, heavy monkey-patching) may not translate cleanly</li>
    <li>Complex projects may occasionally require manual fixes</li>
</ul>

<h2>Examples</h2>

<pre><code>examples/
├── sieve.py      # Prime number sieve — 24x speedup
├── sort.py       # Selection sort — 58x speedup
└── web.py        # Flask app → C HTTP server, valgrind clean</code></pre>

<h2>Comparison</h2>

<p>
While tools like Nuitka and PyInstaller package the CPython interpreter to guarantee
compatibility, <strong>transpilatron completely strips the CPython runtime</strong>.
By translating Python logic into pure C, it produces binaries that run in environments
with zero external libraries.
</p>

<table border="1">
    <tr>
        <th>Tool</th>
        <th>Approach</th>
        <th>CPython Runtime?</th>
        <th>Fully Static Binaries?</th>
        <th>Output Size</th>
        <th>Ideal For</th>
    </tr>
    <tr>
        <td><strong>transpilatron</strong></td>
        <td>Source-to-source C translation via LLM</td>
        <td><strong>No</strong></td>
        <td><strong>Yes (--minimal) / Optional (--full)</strong></td>
        <td>&lt; 1MB</td>
        <td>CLI tools, microservices, serverless, initramfs, scratch containers, embedded, web apps</td>
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
        <td>~30MB–100MB+</td>
        <td>Desktop app distribution</td>
    </tr>
    <tr>
        <td>Cython</td>
        <td>Compiles Python/Cython to extension modules</td>
        <td>Yes</td>
        <td>No</td>
        <td>N/A</td>
        <td>Accelerating hot paths in Python</td>
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


<a href="https://www.star-history.com/?repos=NoodlixProject%2Ftranspilatron&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=NoodlixProject/transpilatron&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=NoodlixProject/transpilatron&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=NoodlixProject/transpilatron&type=date&legend=top-left" />
 </picture>
</a>
<hr>
<p>
<em>
transpilatron was originally created to compile standalone initramfs boot scripts for
<a href="https://github.com/NoodlixProject">Noodlix</a>, a Python-only operating system —
but works for many Python applications.
</em>
</p>

<p>
<em>
<code>--minimal</code> mode outputs fully static binaries.
Runs even in initramfs. No dynamic linker required.
</em>
</p>
