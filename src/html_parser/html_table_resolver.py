from bs4 import Tag

class TableResolver:
    def __init__(self, table, include_header=True):
        if table.tbody is not None:
            tbody = table.tbody
        else:
            tbody = table

        cols_iter = filter(lambda x: x.name == 'tr', tbody.children)

        if include_header:
            self._header = next(cols_iter)
        else:
            self._header = None
        self._cols = cols_iter
        self.rowspan_save = dict()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        next_col = next(self._cols, None)
        if next_col is None:
            raise StopIteration()

        next_iter = filter(lambda x: x.name == 'td', next_col.children)
        return TableResolver_col(next_iter, self)


class TableResolver_col:
    def __init__(self, inner_iter, parent_instalce):
        self._inner_iter = inner_iter
        self._parent = parent_instalce
        self._colspan_count = 0
        self._idx = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._colspan_count != 0:
            self._colspan_count -= 1
            self._idx += 1
            return None
        
        next_item = None
        if self._idx in self._parent.rowspan_save and self._parent.rowspan_save[self._idx]['count'] != 0:
            self._parent.rowspan_save[self._idx]['count'] -= 1
            next_item = self._parent.rowspan_save[self._idx]['item']
        else:
            next_item = next(self._inner_iter, None)

        if next_item is None:
            raise StopIteration()

        if 'colspan' in next_item.attrs:
            self._colspan_count = int(next_item['colspan']) - 1
        
        if 'rowspan' in next_item.attrs:
            count = int(next_item['rowspan']) - 1
            del next_item.attrs['rowspan']
            self._parent.rowspan_save[self._idx] = { 'count': count, 'item': next_item }
        
        self._idx += 1
        return next_item
