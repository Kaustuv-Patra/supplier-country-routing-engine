import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from .decision_repository import DecisionRepository


class FileDecisionRepository(DecisionRepository):
    """
    Reads routing decisions from a JSONL (JSON Lines) file.
    Each line is a single JSON object.
    """

    def __init__(self, decisions_file: Path):
        self.decisions_file = decisions_file

    def get_all_decisions(self) -> Dict[str, Any]:
        decisions: List[Dict[str, Any]] = []

        if self.decisions_file.exists():
            with self.decisions_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    decisions.append(json.loads(line))

        return {
            "meta": {
                "source": "file",
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "count": len(decisions),
            },
            "decisions": decisions,
        }