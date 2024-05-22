class OffsetPagination:
    def __init__(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> None:
        self.offset = offset
        self.limit = limit


class PagePagination:
    def __init__(
        self,
        size: int = 10,
        page: int = 1,
    ) -> None:
        self.page = page
        self.size = size
