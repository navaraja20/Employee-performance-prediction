from typing import List, Tuple
from sqlalchemy.orm import Query

# ✅ Pagination Utility
def get_pagination(query: Query, page: int, page_size: int) -> Tuple[int, List[dict]]:
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return total, items
