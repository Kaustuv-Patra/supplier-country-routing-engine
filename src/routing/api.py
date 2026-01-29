from pathlib import Path
from fastapi import APIRouter

from .file_repository import FileDecisionRepository

router = APIRouter(prefix="/decisions", tags=["Routing Decisions"])

# Must match where decisions are written
DECISIONS_FILE_PATH = Path("outputs/routing_decisions.jsonl")

repository = FileDecisionRepository(DECISIONS_FILE_PATH)


@router.get("")
def get_decisions():
    """
    Returns all routing decisions.
    Read-only endpoint.
    """
    return repository.get_all_decisions()