from dataclasses import dataclass


@dataclass
class Category:
    id: int | None
    name: str
    description: str | None
    is_active: bool = True

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        
        if not self.name:
            raise ValueError("Category name cannot be empty")