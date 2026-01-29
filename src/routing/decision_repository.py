from abc import ABC, abstractmethod
from typing import Dict, Any


class DecisionRepository(ABC):
    """
    Abstract repository for routing decisions.
    Storage implementation must be swappable without affecting API layer.
    """

    @abstractmethod
    def get_all_decisions(self) -> Dict[str, Any]:
        """
        Returns routing decisions in API-ready schema.
        """
        pass