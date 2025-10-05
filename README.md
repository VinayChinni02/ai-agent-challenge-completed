🧑‍💻 Agent-as-Coder Challenge

This project implements an autonomous coding agent that can generate custom parsers for bank statement PDFs.

##The agent automatically:##

**Reads a sample bank PDF and its expected CSV output.
 Generates a parser under custom_parsers/.
 Validates the parser by running tests (pytest).
 If tests fail, it can refine and retry (up to 3 attempts).**


**🚀 Features**

Agent loop: plan → generate → test → refine (up to 3 retries).
CLI support: Run with python agent.py --target <bank_name>.
Parser contract: Every parser exposes

 **parse(pdf_path) -> pd.DataFrame**
 
Testing: Verifies parser output matches expected CSV with DataFrame.equals().
Lightweight design: Built using Python, LangGraph, and pytest.

## Project Structure ##

ai-agent-challenge/
│
├── agent.py                  # Main coding agent
├── custom_parsers/           # Auto-generated bank parsers
│   └── icici_parser.py
├── data/                     # Sample PDFs and expected CSVs
│   └── icici/
│       ├── icici sample.pdf
│       └── result.csv
├── tests/                    # Test cases
│   └── test_icici.py
├── README.md                 # Documentation
└── requirements.txt

## 🔄 Agent Workflow Diagram ##

 ┌─────────────┐
 │   Planner   │  (decide what code to write)
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Code Writer │  (writes parser into custom_parsers/)
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │   Tester    │  (runs pytest to validate parser)
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │   Refiner   │  (fixes code if tests fail, retries ≤3)
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │   Success   │  ✅ Parser passes all tests!
 └─────────────┘


## 🏃 Run Instructions ##
1. Clone Repo
   git clone <your-fork-url>
   cd ai-agent-challenge

2.Create virtual environment

python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

3.Install dependencies
 pip install -r requirements.txt 

4.Run the agent
python agent.py --target icici


