from textual.widgets import DataTable
from textual.widgets.data_table import Column, ColumnKey, ColumnDoesNotExist

class DataTablePR(DataTable):


    def get_column_object(self, column_key: ColumnKey | str) -> Column:
        """Get the column object for a given column key"""

        if column_key not in self._column_locations:
            raise ColumnDoesNotExist(f"Column key {column_key!r} is not valid.")           

        column_index = self.get_column_index(column_key)
        return self.ordered_columns[column_index]