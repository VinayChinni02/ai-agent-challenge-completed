import os
import subprocess
import pandas as pd
from typing import Dict, Any

from langgraph.graph import StateGraph, END

# --- Agent state ---
class AgentState(Dict[str, Any]):
    attempt: int
    target: str
    success: bool
    error: str

# --- Nodes ---
def planner(state: AgentState) -> AgentState:
    print(f"\n=== Attempt {state['attempt']}/3 ===")
    state["plan"] = f"Generate parser for {state['target']}"
    return state

def codegen(state: AgentState) -> AgentState:
    target = state["target"]
    parser_path = f"custom_parsers/{target}_parser.py"

    # Dynamically detect schema from CSV in data/<target>/
    csv_file = next((f for f in os.listdir(f"data/{target}") if f.endswith(".csv")), None)
    if csv_file:
        expected = pd.read_csv(f"data/{target}/{csv_file}")
        columns = list(expected.columns)
    else:
        # Fallback schema
        columns = ["Date", "Description", "Debit Amt", "Credit Amt", "Balance"]

    # Parser template using extract_table()
    code = f"""
import pandas as pd
import pdfplumber

COLUMNS = {columns}

def parse(pdf_path: str) -> pd.DataFrame:
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:  # skip header row
                    if row and len(row) == len(COLUMNS):
                        rows.append(row)
    return pd.DataFrame(rows, columns=COLUMNS)
"""
    os.makedirs("custom_parsers", exist_ok=True)
    with open(parser_path, "w") as f:
        f.write(code)

    print(f"Generated parser at {parser_path}")
    return state

def tester(state: AgentState) -> AgentState:
    result = subprocess.run(
        ["pytest", "-q"],
        capture_output=True, text=True
    )
    print(result.stdout)

    if result.returncode == 0:
        state["success"] = True
        print("✅ Success: Parser passed all tests!")
        return state
    else:
        state["success"] = False
        state["error"] = result.stdout
        print("❌ Test failed.")
        return state

def refiner(state: AgentState) -> AgentState:
    # For now: stop after first failure to avoid infinite loop
    state["attempt"] += 1
    print("❌ Parser failed, not retrying further in this simplified version.")
    state["success"] = False
    return state

# --- Build LangGraph ---
graph = StateGraph(AgentState)

graph.add_node("planner", planner)
graph.add_node("codegen", codegen)
graph.add_node("tester", tester)
graph.add_node("refiner", refiner)

graph.add_edge("planner", "codegen")
graph.add_edge("codegen", "tester")

# If success -> END, else stop
graph.add_conditional_edges(
    "tester",
    lambda s: END if s["success"] else "refiner",
    {"refiner": END, END: END}
)

graph.set_entry_point("planner")
agent = graph.compile()

# --- CLI ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Bank name, e.g. icici or sbi")
    args = parser.parse_args()

    state = {"attempt": 1, "target": args.target, "success": False, "error": ""}
    agent.invoke(state)
