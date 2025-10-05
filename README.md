
# Agent-as-Coder Challenge

## Goal
Develop an autonomous coding agent that writes custom parsers for Bank Statement PDFs.  
When run, the agent should generate a new parser, test it against expected CSVs, and refine until the tests pass.

---

## How It Works
The agent is built using **LangGraph** and follows an autonomous loop:

1. **Plan (Codegen)** – Generate initial parser template.
2. **Act** – Save parser file into `custom_parsers/`.
3. **Test** – Run `pytest` to compare parser output against expected CSV.
4. **Observe** – Capture test results and errors.
5. **Refine** – Retry parser generation (≤3 attempts).

This loop mimics a **junior software engineer** that writes → tests → fixes → succeeds.

---

## Run Instructions (5 Steps)

1. **Clone the repo**
   ```bash
   git clone <your-fork-url>
   cd ai-agent-challenge


Setup virtual environment

python -m venv .venv

.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac


Install requirements :

pip install -r requirements.txt

Run the agent :

python agent.py --target icici

Verify tests :

pytest -q


✅ You should see:

.                        [100%]
1 passed in 1.3s


Agent Diagram

The agent flow is:

codegen → tester → refiner → tester → ... until tests pass ✅
