"""Smoke tests for the calculator back-end API (Flask test client)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import create_app  # noqa: E402

app = create_app()
client = app.test_client()

failures = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print("%s %s %s" % (status, name, detail))
    if not condition:
        failures.append(name)


# 1. basic operations
r = client.post("/api/calculate", json={"expression": "12+8"})
check("add 12+8", r.status_code == 200 and r.get_json()["result"] == "20",
      str(r.get_json()))

r = client.post("/api/calculate", json={"expression": "10-25"})
check("sub 10-25", r.get_json()["result"] == "-15", str(r.get_json()))

r = client.post("/api/calculate", json={"expression": "5*8"})
check("mul 5*8", r.get_json()["result"] == "40", str(r.get_json()))

r = client.post("/api/calculate", json={"expression": "10/4"})
check("div 10/4", r.get_json()["result"] == "2.5", str(r.get_json()))

# 2. compound expressions
cases = {
    "1+2*3": "7",
    "(1+2)*3": "9",
    "10/2+7": "12",
    "8-3*2": "2",
    "-5+8": "3",
    "3*-2": "-6",
    "3.14+2.86": "6",
    "((1+2)*(3+4))/7": "3",
}
for expr, expected in cases.items():
    r = client.post("/api/calculate", json={"expression": expr})
    check("expr %s" % expr,
          r.status_code == 200 and r.get_json()["result"] == expected,
          str(r.get_json()))

# 3. invalid expressions and division by zero
for expr in ["1++", "abc", "1/0", "(1+2", "1 2 3", ""]:
    r = client.post("/api/calculate", json={"expression": expr})
    check("error [%s]" % expr,
          r.status_code == 400 and r.get_json()["success"] is False,
          str(r.get_json()))

r = client.post("/api/calculate", json={})
check("missing expression", r.status_code == 400, str(r.get_json()))

# 4. history
r = client.get("/api/history")
history = r.get_json()["history"]
check("history list", r.status_code == 200 and len(history) == len(cases) + 4,
      "count=%d" % len(history))
check("history order desc", history[0]["id"] > history[-1]["id"])
check("history fields",
      all(set(h) >= {"id", "expression", "result", "created_at"} for h in history))

# 5. delete one record
target = history[0]["id"]
r = client.delete("/api/history/%d" % target)
check("delete existing", r.status_code == 204)
r = client.get("/api/history")
check("record removed",
      all(h["id"] != target for h in r.get_json()["history"]))

# 6. delete non-existing
r = client.delete("/api/history/999999")
check("delete missing -> 404", r.status_code == 404)

# 7. clear all
r = client.delete("/api/history")
check("clear all", r.status_code == 200 and r.get_json()["deleted"] >= 1)
r = client.get("/api/history")
check("history empty", r.get_json()["history"] == [])

# 8. health
r = client.get("/api/health")
check("health", r.status_code == 200 and r.get_json()["success"] is True)

print("\n%d failures" % len(failures))
sys.exit(1 if failures else 0)
