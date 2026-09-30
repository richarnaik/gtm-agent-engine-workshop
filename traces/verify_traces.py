"""Assert that the representative trace fixture is complete and connected."""

import json
from collections import Counter
from pathlib import Path


EXPECTED_RUN_COUNT = 43
EXPECTED_LLM_COUNT = 4


def verify_representative_trace():
    runs = json.loads((Path(__file__).with_name("traces.json")).read_text())
    traces = {}
    for run in runs:
        traces.setdefault(run["trace_id"], []).append(run)

    representative = min(traces.values(), key=lambda trace: trace[0]["trace_id"])
    if len(representative) != EXPECTED_RUN_COUNT:
        raise AssertionError(
            f"representative trace has {len(representative)} runs, "
            f"expected {EXPECTED_RUN_COUNT}"
        )
    counts = Counter(run["run_type"] for run in representative)
    if counts["llm"] != EXPECTED_LLM_COUNT:
        raise AssertionError(
            f"representative trace has {counts['llm']} llm runs, "
            f"expected {EXPECTED_LLM_COUNT}"
        )

    run_ids = {run["id"] for run in representative}
    missing_parents = {
        run["parent_run_id"]
        for run in representative
        if run["parent_run_id"] and run["parent_run_id"] not in run_ids
    }
    if missing_parents:
        raise AssertionError(f"unresolved parent_run_id values: {sorted(missing_parents)}")


if __name__ == "__main__":
    verify_representative_trace()
