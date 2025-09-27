<h1>SafeSpace AI Agent</h1>
<p>
  <strong>AI-powered mental health chat app</strong> built with FastAPI, Streamlit, and LangGraph.
</p>

<h2>Features</h2>
<ul>
  <li>JWT registration/login for secure user access</li>
  <li>Therapy chatbot with session history and emergency calling (Twilio)</li>
  <li>Usage tracking and subscription-ready logic</li>
  <li>Environment-based secret management (<code>.env</code>)</li>
  <li>Clean separation of backend (FastAPI) and frontend (Streamlit)</li>
</ul>

<h2>Quick Start</h2>
<ol>
  <li>Install dependencies with <code>uv</code>:
    <pre><code>uv pip install -r requirements.txt</code></pre>
  </li>
  <li>Configure your <code>.env</code> with API keys and secrets</li>
  <li>Run backend:
    <pre><code>uv run uvicorn main:app --reload</code></pre>
  </li>
  <li>Run frontend:
    <pre><code>streamlit run frontend.py</code></pre>
  </li>
</ol>

<h2>Structure</h2>
<pre>
main.py       # FastAPI app
models.py     # User/auth/chat models
auth.py       # JWT logic
database.py   # Persistence
aiagent.py    # LangGraph agent
tools.py      # MedGemma, Twilio
frontend.py   # Streamlit UI
.env          # Secrets (private)
</pre>

<h2>Next Steps</h2>
<ul>
  <li>Add premium features/subscription middleware</li>
  <li>Switch to a persistent database for user/chat data</li>
  <li>Deploy with secure settings for production</li>
</ul>
