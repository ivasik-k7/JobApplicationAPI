class JobApplicationsFiltration:
    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        status: str | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.status = status
