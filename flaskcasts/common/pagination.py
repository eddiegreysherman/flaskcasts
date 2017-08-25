from math import ceil


class Pagination:

    def __init__(self, items, page, per_page, total_items):
        self.items = items
        self.page = page
        self.per_page = float(per_page)
        self.num_pages = int(ceil(total_items / float(per_page)))

    @property
    def has_next(self):
        return self.page < self.num_pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def next_page(self):
        return self.page + 1

    @property
    def prev_page(self):
        return self.page - 1


def paginate(queryset, page=1, per_page=5):
    skip = (page-1)*per_page
    limit = per_page

    return Pagination(queryset.limit(limit).skip(skip),
                      page=page,
                      per_page=per_page,
                      total_items=queryset.count())