

class Pagination:
    def __init__(self, data, per_page):
        self.data = data
        self.per_page = per_page

    def get_page(self, page):
        start = (page - 1) * self.per_page
        end = start + self.per_page
        return self.data[start:end]

    def get_total_pages(self):
        return len(self.data) // self.per_page + 1