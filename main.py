
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import numpy as np
import pandas as pd

app = FastAPI(title="Python Apps Script API")

EDITOR_HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RIVOX Python Editor</title>

<script src="https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js"></script>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 20px;
    background: #101827;
    color: white;
    font-family: Arial, sans-serif;
}

.container {
    max-width: 950px;
    margin: auto;
}

h1 { color: #60a5fa; }

.subtitle { color: #94a3b8; }

textarea {
    width: 100%;
    height: 330px;
    padding: 16px;
    background: #080d18;
    color: #a7f3d0;
    border: 1px solid #334155;
    border-radius: 10px;
    direction: ltr;
    text-align: left;
    font: 15px monospace;
    resize: vertical;
}

button {
    padding: 12px 18px;
    margin: 8px 4px;
    border: 0;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
}

button:disabled {
    opacity: .5;
    cursor: not-allowed;
}

#run { background: #2563eb; color: white; }
#packages { background: #059669; color: white; }
#clear { background: #475569; color: white; }

pre {
    min-height: 120px;
    padding: 16px;
    background: #080d18;
    color: #a7f3d0;
    border-radius: 10px;
    direction: ltr;
    text-align: left;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

#status {
    padding: 12px;
    background: #1e293b;
    border-radius: 8px;
    color: #fbbf24;
}

.footer {
    margin-top: 25px;
    color: #64748b;
    font-size: 13px;
}
</style>
</head>

<body>
<div class="container">

<h1>🐍 محرر Python</h1>
<p class="subtitle">اكتب كود Python وشغّله مباشرة من المتصفح.</p>

<p id="status">جارٍ تحميل محرك Python...</p>

<textarea id="code">print("Hello Python!")

x = 10
y = 20

print("المجموع:", x + y)
</textarea>

<div>
    <button id="run" onclick="runCode()" disabled>
        ▶ تشغيل Python
    </button>

    <button id="packages" onclick="loadPackages()" disabled>
        تحميل NumPy و Pandas
    </button>

    <button id="clear" onclick="clearOutput()">
        مسح النتيجة
    </button>
</div>

<h3>النتيجة:</h3>
<pre id="output">ستظهر النتائج هنا...</pre>

<p class="footer">
    Python يعمل داخل متصفحك باستخدام Pyodide.
    لا يتم إرسال الكود إلى الخادم.
</p>

</div>

<script>
let pyodide = null;

async function initialize() {
    const status = document.getElementById("status");

    try {
        status.textContent = "جارٍ تشغيل محرك Python...";

        if (typeof loadPyodide !== "function") {
            throw new Error("تعذّر تحميل مكتبة Pyodide");
        }

        pyodide = await loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"
        });

        status.textContent = "✅ Python جاهز للتشغيل";

        document.getElementById("run").disabled = false;
        document.getElementById("packages").disabled = false;

    } catch (error) {
        status.textContent =
            "❌ خطأ التحميل: " +
            (error.message || String(error));

        console.error(error);
    }
}

async function runCode() {
    const code = document.getElementById("code").value;
    const output = document.getElementById("output");
    const button = document.getElementById("run");

    button.disabled = true;
    output.textContent = "جارٍ التنفيذ...";

    try {
        pyodide.globals.set("user_code", code);

        const result = await pyodide.runPythonAsync(`
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr

_buffer = io.StringIO()

try:
    with redirect_stdout(_buffer), redirect_stderr(_buffer):
        exec(user_code, globals())

    _result = _buffer.getvalue() or "تم التنفيذ بنجاح."

except Exception:
    _result = _buffer.getvalue() + traceback.format_exc()

_result
        `);

        output.textContent = result;

    } catch (error) {
        output.textContent = String(error);
    }

    button.disabled = false;
}

async function loadPackages() {
    const status = document.getElementById("status");
    const button = document.getElementById("packages");

    button.disabled = true;
    status.textContent = "جارٍ تحميل NumPy و Pandas...";

    try {
        await pyodide.loadPackage(["numpy", "pandas"]);

        status.textContent = "✅ تم تحميل NumPy و Pandas بنجاح";

    } catch (error) {
        status.textContent =
            "❌ تعذّر تحميل المكتبات: " + String(error);
    }

    button.disabled = false;
}

function clearOutput() {
    document.getElementById("output").textContent =
        "ستظهر النتائج هنا...";
}

initialize();
</script>

</body>
</html>
"""


@app.get("/")
def home():
    return {"status": "Python server is running"}


@app.get("/editor", response_class=HTMLResponse)
def editor():
    return EDITOR_HTML


@app.get("/calculate")
def calculate():
    numbers = np.array([10, 20, 30])
    data = pd.DataFrame({"numbers": numbers})

    return {
        "total": int(data["numbers"].sum()),
        "average": float(data["numbers"].mean())
    }
