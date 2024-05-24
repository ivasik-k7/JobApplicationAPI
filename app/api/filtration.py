class JobApplicationsFiltration:
    def __init__(
        self,
        name: str | None = None,
        company: str | None = None,
        status: str | None = None,
    ) -> None:
        self.name = name
        self.company = company
        self.status = status
