from PyQt5.QtCore import Qt, QSortFilterProxyModel, QTime, QStringListModel, QAbstractTableModel
from PyQt5.QtWidgets import QCompleter, QComboBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTimeEdit, QTableView, QHeaderView, QTextEdit
from london_metro import create_summary, dijkstra_search, reconstruct_path


class ExtendedComboBox(QComboBox):
    """
    The original source code is from
    https://stackoverflow.com/a/50639066
    """
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)


class TableModel(QAbstractTableModel):
    """
    Creates a Table Model for PyQt with a custom header
    """
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        columns = ["Station", "Line", "Travel time to\nnext station", "Total time"]
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return columns[section]


class App(QMainWindow):
    def __init__(self, metro_graph, parent=None):
        QMainWindow.__init__(self, parent)
        self.metro_graph = metro_graph
        self.available_stations = metro_graph.get_station_names()
        self.setWindowTitle("London Tube Planner")
        self.path_steps = [["", "", "", ""]]
        main_frame = QWidget()
        vbox = self.create_main_frame()
        main_frame.setLayout(vbox)
        self.setCentralWidget(main_frame)

    def calculate_necessary(self, start_station, end_station, leaving_time):
        """
        Runs Dijkstra's search algorithm with the user input,
        and runs the necessary functions to obtain the path, line_changes, cost_so_far
        $:returns True for succesful operation, False for error
        """
        start = self.metro_graph.get_station(start_station)
        end = self.metro_graph.get_station(end_station)
        if start and end:
            came_from, cost_so_far = dijkstra_search(start, end, leaving_time)
            self.total_time = cost_so_far[end]
            path = reconstruct_path(came_from, start, end)
            self.path_steps, self.line_changes = create_summary(path, cost_so_far, leaving_time)
            return True
        else:
            self.summary.setText("Wrong stations")
            return False

    def draw_table(self):
        """
        Draws a table with the selected data
        """
        self.model = TableModel(self.path_steps)
        self.table.setModel(self.model)

    def update_summary(self):
        """
        Updates summary text with the latest information
        """
        summary_text = "\nchange\n".join((f"{line}: {fr} to {to}" for line, fr, to in self.line_changes))
        summary_text += f"\nTotal journey time: {self.total_time} minutes"
        self.summary.setText(summary_text)

    def on_plan_press(self):
        """
        Parses the user input and if everything is okay
        Calls the functions for drawing the table and updating the summary
        """
        start_station = str(self.from_station_edit.currentText())
        end_station = str(self.to_station_edit.currentText())
        leaving_time = self.start_time_edit.time().toPyTime()
        if start_station.lower() == end_station.lower():
            return
        succesful = self.calculate_necessary(start_station, end_station, leaving_time)
        if succesful:
            self.draw_table()
            self.update_summary()

    def create_main_frame(self):
        time_options = {
            "displayFormat": "hh:mm AP",
            "minimumTime": QTime.fromString("05:00", "hh:mm"),
            "maximumTime": QTime.fromString("24:00", "hh:mm")
        }

        # Create the time input
        start_time_label = QLabel("Start time:")
        self.start_time_edit = QTimeEdit(**time_options)
        self.start_time_edit.setTime(self.start_time_edit.minimumTime())
        self.start_time_edit.setMinimumWidth(100)

        # Create the text input for source station
        from_station_label = QLabel("From:")
        self.from_station_edit = ExtendedComboBox()
        self.from_station_edit.setModel(QStringListModel(self.available_stations))

        # Create the text input for target station
        to_station_label = QLabel("To:")
        self.to_station_edit = ExtendedComboBox()
        self.to_station_edit.setModel(QStringListModel(self.available_stations))

        # Button when pressed will update the table and summary
        self.plan_button = QPushButton("Plan")
        self.plan_button.setCheckable(True)
        self.plan_button.toggle()
        self.plan_button.clicked.connect(self.on_plan_press)

        # Create the table to show the steps
        self.table = QTableView()
        self.table.setMinimumHeight(200)
        self.model = TableModel(self.path_steps)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        # Create the text box for summary information
        self.summary = QTextEdit()
        self.summary.setReadOnly(True)

        # Layout with box sizers
        hbox = QHBoxLayout()

        for w in [start_time_label,
                  self.start_time_edit,
                  from_station_label,
                  self.from_station_edit,
                  to_station_label,
                  self.to_station_edit,
                  self.plan_button]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.table)
        vbox.addWidget(self.summary)

        return vbox
