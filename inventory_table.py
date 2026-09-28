from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QMenu,
    QMessageBox
)


class InventoryTable(QTableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QTableWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.inventory_name = ""
        self.inventory_items = []

    def startDrag(self, supportedActions):
        index = self.currentIndex()

        if not index.isValid():
            return

        item = self.item(index.row(), index.column())

        if item is None:
            return

        row = index.row()
        column = index.column()

        drag = QDrag(self)
        mime = QMimeData()

        mime.setText(f"{self.inventory_name}|{row}|{column}")
        drag.setMimeData(mime)

        # Simple drag image
        pixmap = QPixmap(150, 35)
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        painter.setPen(Qt.black)
        painter.drawRect(0, 0, 149, 34)
        painter.drawText(
            pixmap.rect().adjusted(5, 0, -5, 0),
            Qt.AlignCenter,
            item.text()
        )
        painter.end()

        drag.setPixmap(pixmap)

        drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):

        try:
            source_name, source_row, source_column = \
                event.mimeData().text().split("|")

            source_row = int(source_row)
            source_column = int(source_column)

        except Exception:
            event.ignore()
            return

        # Find the source table
        source_table = None

        for table in self.window().findChildren(InventoryTable):
            if table.inventory_name == source_name:
                source_table = table
                break

        if source_table is None:
            event.ignore()
            return

        # Determine where we dropped
        target_index = self.indexAt(event.pos())

        if not target_index.isValid():
            event.ignore()
            return

        target_row = target_index.row()
        target_column = target_index.column()

        # Get the items
        source_index = source_row + (
            source_column * source_table.rowCount()
        )

        target_index_num = target_row + (
            target_column * self.rowCount()
        )

        if source_index >= len(source_table.inventory_items):
            event.ignore()
            return

        source_item = source_table.inventory_items[source_index]

        # Empty target slot
        target_item = None

        if target_index_num < len(self.inventory_items):
            target_item = self.inventory_items[target_index_num]

        # Same table
        if source_table is self:

            self.inventory_items[source_index], \
            self.inventory_items[target_index_num] = \
                self.inventory_items[target_index_num], \
                self.inventory_items[source_index]

        # Different tables
        else:

            # Remove source
            source_table.inventory_items[source_index] = target_item

            # Put source into target
            if target_index_num < len(self.inventory_items):
                self.inventory_items[target_index_num] = source_item
            else:
                while len(self.inventory_items) <= target_index_num:
                    self.inventory_items.append(None)

                self.inventory_items[target_index_num] = source_item

        # Redraw both tables
        source_table.refresh_inventory()
        self.refresh_inventory()

        event.acceptProposedAction()

    def refresh_inventory(self):

        self.clearContents()

        for index, item in enumerate(self.inventory_items):

            if item is None:
                continue

            row = index % self.rowCount()
            column = index // self.rowCount()

            if column >= self.columnCount():
                continue

            self.setItem(
                row,
                column,
                QTableWidgetItem(item["name"])
            )
    def show_context_menu(self, position):

        index = self.indexAt(position)

        # Nothing was clicked
        if not index.isValid():
            return

        row = index.row()
        column = index.column()

        item_index = row + (column * self.rowCount())

        # Slot doesn't exist in the inventory list
        if item_index >= len(self.inventory_items):
            return

        # Slot is empty
        item = self.inventory_items[item_index]
        if item is None:
            return

        # Only show the menu if there is actually an item
        menu = QMenu(self)
        delete_action = menu.addAction("Delete Item")

        action = menu.exec_(
            self.viewport().mapToGlobal(position)
        )

        if action == delete_action:
            self.delete_inventory_item(item_index)
        
    def delete_inventory_item(self, item_index):

        item = self.inventory_items[item_index]

        if item is None:
            return

        item_name = item.get("name", "this item")

        reply = QMessageBox.question(
            self,
            "Delete Item",
            f"Are you sure you want to delete '{item_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.inventory_items[item_index] = None
            self.refresh_inventory()



