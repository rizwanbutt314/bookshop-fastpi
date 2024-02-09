from sqlalchemy import func


def paginate_query(query, page_number=1, items_per_page=10):
    pagination = query.paginate(page_number, items_per_page, error_out=False)
    results = pagination.items
    total_pages = pagination.pages
    total_items = pagination.total
    return results, total_pages, total_items


async def async_paginate(query, page, per_page):
    total_count = await query.with_only_columns(func.count()).order_by(None).all()
    total_count = total_count[0][0]
    total_pages = (total_count - 1) // per_page + 1
    offset = (page - 1) * per_page

    result = await query.limit(per_page).offset(offset).all()
    return result, total_count, total_pages
