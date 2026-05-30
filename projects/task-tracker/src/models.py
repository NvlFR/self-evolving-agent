import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Task:
    """
    Represents a Task object in the Task Tracker application.
    
    Attributes:
        description (str): A short description of the task.
        id (str): Unique identifier for the task (UUID).
        status (str): The current state of the task (todo, in-progress, done).
        created_at (datetime): Timestamp when the task was initialized.
        updated_at (datetime): Timestamp when the task was last modified.
    """
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "todo"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the Task object into a dictionary format compatible with JSON.
        """
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Creates a Task instance from a dictionary representation.
        """
        return cls(
            id=data["id"],
            description=data["description"],
            status=data["status"],
            created_at=datetime.fromisoformat(data["createdAt"]),
            updated_at=datetime.fromisoformat(data["updatedAt"])
        )

    def update(self, description: str = None, status: str = None):
        """
        Updates task attributes and refreshes the updatedAt timestamp.
        """
        if description:
            self.description = description
        if status:
            self.status = status
        self.updated_at = datetime.now()