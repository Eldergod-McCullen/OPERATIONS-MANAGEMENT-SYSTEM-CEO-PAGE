

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


# ── Shared palette ────────────────────────────────────────────────────────────
_NAVY      = "#0d1b3e"
_ACCENT    = "#5870ff"
_BG        = "#f0f2f5"
_WHITE     = "#ffffff"
_BORDER    = "#e5e7eb"
_TEXT_DARK = "#1a1a2e"
_TEXT_GREY = "#6b7280"
_TEXT_MID  = "#374151"

# ── Priority colours ──────────────────────────────────────────────────────────
PRIORITY_COLOURS = {
    "High":   ("#b91c1c", "#fee2e2"),
    "Medium": ("#d97706", "#fef3c7"),
    "Low":    ("#15803d", "#dcfce7"),
}

# ── Status colours ────────────────────────────────────────────────────────────
STATUS_COLOURS = {
    "In Progress": ("#1d4ed8", "#dbeafe"),
    "Pending":     ("#d97706", "#fef3c7"),
    "Completed":   ("#15803d", "#dcfce7"),
    "Overdue":     ("#b91c1c", "#fee2e2"),
}

# ── Sample task data ──────────────────────────────────────────────────────────
# (task_id, title, assigned_to, department, priority, status, due_date,
#  created_by, created_on, last_updated, description)
SAMPLE_TASKS = [
    ("TSK-2025-0001","Prepare Q2 Performance Report",  "John Kamau",    "Finance",        "High",  "In Progress","24 Jun 2025","System Administrator","15 Jun 2025 09:30 AM","21 Jun 2025 11:15 AM","Prepare and submit the Q2 performance report for review by the executive team."),
    ("TSK-2025-0002","Review IT Security Policy",      "David Mwangi",  "IT Department",  "High",  "In Progress","23 Jun 2025","System Administrator","14 Jun 2025 08:00 AM","20 Jun 2025 03:00 PM","Review and update the company IT security policy document."),
    ("TSK-2025-0003","Employee Training Program",      "Grace Njeri",   "HR Department",  "Medium","Pending",    "25 Jun 2025","System Administrator","13 Jun 2025 10:00 AM","19 Jun 2025 09:00 AM","Coordinate the Q2 employee training and development program."),
    ("TSK-2025-0004","Office Equipment Maintenance",   "Joseph Kiprono","Maintenance",    "Medium","In Progress","22 Jun 2025","System Administrator","12 Jun 2025 11:00 AM","18 Jun 2025 02:00 PM","Schedule and oversee routine office equipment maintenance."),
    ("TSK-2025-0005","Marketing Campaign Planning",    "Susan Akinyi",  "Marketing",      "High",  "Pending",    "26 Jun 2025","System Administrator","11 Jun 2025 09:00 AM","17 Jun 2025 04:00 PM","Plan and prepare assets for the upcoming Q3 marketing campaign."),
    ("TSK-2025-0006","Budget Review and Approval",     "Peter Ochieng", "Finance",        "High",  "Completed",  "18 Jun 2025","System Administrator","10 Jun 2025 08:30 AM","18 Jun 2025 05:00 PM","Review departmental budgets and approve allocations for Q3."),
    ("TSK-2025-0007","System Backup and Recovery Test","James Mutua",   "IT Department",  "Medium","Completed",  "17 Jun 2025","System Administrator","09 Jun 2025 10:00 AM","17 Jun 2025 03:30 PM","Perform full system backup and test recovery procedures."),
    ("TSK-2025-0008","Supplier Contract Review",       "Mary Wanjiku",  "Procurement",    "Low",   "Pending",    "28 Jun 2025","System Administrator","08 Jun 2025 09:00 AM","16 Jun 2025 01:00 PM","Review and renew supplier contracts due for expiry in Q3."),
    ("TSK-2025-0009","Monthly Department Meeting",     "Brian Otieno",  "Operations",     "Low",   "Completed",  "20 Jun 2025","System Administrator","07 Jun 2025 08:00 AM","20 Jun 2025 12:00 PM","Facilitate the monthly cross-department operations meeting."),
    ("TSK-2025-0010","Update Employee Handbook",       "Lilian Moraa",  "HR Department",  "Medium","In Progress","27 Jun 2025","System Administrator","06 Jun 2025 11:00 AM","15 Jun 2025 10:00 AM","Update the employee handbook with new HR policies and procedures."),
]

DEPARTMENTS = [
    "Finance","IT Department","HR Department","Maintenance",
    "Marketing","Procurement","Operations","Administration",
    "Management","Executive Office",
]

# Overdue tasks for right panel
OVERDUE_TASKS = [
    ("Review IT Security Policy",    "23 Jun 2025", "Overdue by 1 day"),
    ("Office Equipment Maintenance", "22 Jun 2025", "Overdue by 2 days"),
    ("Submit Monthly Sales Report",  "21 Jun 2025", "Overdue by 3 days"),
]

# Priority bar data: (label, value, total, colour)
PRIORITY_BARS = [
    ("High",   60, 146, "#ef4444"),
    ("Medium", 60, 146, "#f59e0b"),
    ("Low",    26, 146, "#10b981"),
]


# ==============================================================================
# BADGE helper
# ==============================================================================
class _Badge(QtWidgets.QLabel):
    def __init__(self, text: str, fg: str, bg: str, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(20)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                           QtWidgets.QSizePolicy.Policy.Fixed)
        self.setStyleSheet(f"""
            QLabel {{
                color: {fg};
                background-color: {bg};
                border-radius: 9px;
                padding: 0px 9px;
                font-size: 10px;
                font-weight: 700;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)


# ==============================================================================
# DONUT CHART  (Tasks by Status)
# ==============================================================================
class _DonutChart(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(160, 160)
        self._slices = [
            ("Completed",  64, "#10b981"),
            ("In Progress",52, "#3b82f6"),
            ("Pending",    22, "#f59e0b"),
            ("Overdue",     8, "#ef4444"),
        ]
        self._total = sum(s[1] for s in self._slices)

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        w, h   = self.width(), self.height()
        size   = min(w, h) - 16
        x      = (w - size) // 2
        y      = (h - size) // 2
        rect   = QtCore.QRectF(x, y, size, size)
        start  = 90 * 16
        for _, value, colour in self._slices:
            span = int(round(value / self._total * 360 * 16))
            p.setBrush(QtGui.QColor(colour))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawPie(rect, start, -span)
            start -= span
        # Hollow centre
        hole = size * 0.56
        hx   = (w - hole) / 2
        hy   = (h - hole) / 2
        p.setBrush(QtGui.QColor(_WHITE))
        p.drawEllipse(QtCore.QRectF(hx, hy, hole, hole))
        # Centre text
        p.setPen(QtGui.QColor(_TEXT_DARK))
        p.setFont(QtGui.QFont("Segoe UI", 17, QtGui.QFont.Weight.Bold))
        p.drawText(QtCore.QRectF(hx, hy - 8, hole, hole / 2 + 8),
                   Qt.AlignmentFlag.AlignCenter, str(self._total))
        p.setFont(QtGui.QFont("Segoe UI", 9))
        p.setPen(QtGui.QColor(_TEXT_GREY))
        p.drawText(QtCore.QRectF(hx, hy + hole / 2 - 12, hole, 18),
                   Qt.AlignmentFlag.AlignCenter, "Total")
        p.end()


# ==============================================================================
# STAT CARD
# ==============================================================================
class _StatCard(QtWidgets.QFrame):
    def __init__(self, icon, icon_bg, label, value, sublabel, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {_WHITE};
                border: 1px solid {_BORDER};
                border-radius: 10px;
            }}
        """)
        hl = QtWidgets.QHBoxLayout(self)
        hl.setContentsMargins(14, 12, 14, 12)
        hl.setSpacing(12)

        ico_lbl = QtWidgets.QLabel(icon)
        ico_lbl.setFixedSize(40, 40)
        ico_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ico_lbl.setStyleSheet(f"""
            QLabel {{
                background-color: {icon_bg};
                border-radius: 20px;
                font-size: 18px;
            }}
        """)

        vl = QtWidgets.QVBoxLayout()
        vl.setSpacing(2)
        top = QtWidgets.QLabel(label)
        top.setStyleSheet(f"color:{_TEXT_GREY}; font-size:11px;")
        val = QtWidgets.QLabel(value)
        val.setStyleSheet(f"""
            color:{_TEXT_DARK}; font-size:24px; font-weight:bold;
            font-family:'Segoe UI',Arial;
        """)
        sub = QtWidgets.QLabel(sublabel)
        sub.setStyleSheet(f"color:{_TEXT_GREY}; font-size:10px;")
        vl.addWidget(top); vl.addWidget(val); vl.addWidget(sub)

        hl.addWidget(ico_lbl)
        hl.addLayout(vl)
        hl.addStretch()


# ==============================================================================
# ADD TASK DIALOG
# ==============================================================================
class AddTaskDialog(QtWidgets.QDialog):
    task_saved = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None, task_data: dict = None):
        super().__init__(parent)
        self._edit = task_data is not None
        self.setWindowTitle("Edit Task" if self._edit else "Add New Task")
        self.setModal(True)
        self.setFixedSize(500, 580)
        self.setStyleSheet(f"""
            QDialog {{ background:{_WHITE}; font-family:'Segoe UI',Arial; }}
            QLabel#hdrTitle {{ color:{_TEXT_DARK}; font-size:15px; font-weight:bold; }}
            QLabel#hdrSub   {{ color:{_TEXT_GREY}; font-size:12px; }}
            QLabel#fldLbl   {{ color:{_TEXT_MID};  font-size:12px; font-weight:600; }}
            QLineEdit, QComboBox, QDateEdit, QTextEdit {{
                border:1px solid {_BORDER}; border-radius:6px;
                padding:7px 10px; font-size:12px;
                color:{_TEXT_DARK}; background:#f9fafb;
            }}
            QLineEdit:focus, QComboBox:focus,
            QDateEdit:focus, QTextEdit:focus {{
                border:1.5px solid {_ACCENT}; background:{_WHITE};
            }}
            QPushButton#cancelBtn {{
                background:{_WHITE}; border:1px solid {_BORDER};
                border-radius:6px; padding:8px 22px;
                font-size:12px; color:{_TEXT_MID};
            }}
            QPushButton#cancelBtn:hover {{ background:#f9fafb; }}
            QPushButton#saveBtn {{
                background:{_ACCENT}; border:none; border-radius:6px;
                padding:8px 26px; font-size:12px;
                font-weight:bold; color:{_WHITE};
            }}
            QPushButton#saveBtn:hover {{ background:#4a60ee; }}
            QFrame#div {{ border:none; border-top:1px solid {_BORDER}; }}
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(26, 22, 26, 18)
        root.setSpacing(0)

        # Header
        hdr_hl = QtWidgets.QHBoxLayout()
        ico = QtWidgets.QLabel("✅")
        ico.setFixedSize(40, 40)
        ico.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ico.setStyleSheet("background:#eff0ff;border-radius:20px;font-size:18px;")
        hdr_vl = QtWidgets.QVBoxLayout(); hdr_vl.setSpacing(2)
        t = QtWidgets.QLabel("Edit Task" if self._edit else "Add New Task")
        t.setObjectName("hdrTitle")
        s = QtWidgets.QLabel("Update task details below." if self._edit
                             else "Fill in the details to create a new task.")
        s.setObjectName("hdrSub")
        hdr_vl.addWidget(t); hdr_vl.addWidget(s)
        hdr_hl.addWidget(ico); hdr_hl.addSpacing(10)
        hdr_hl.addLayout(hdr_vl); hdr_hl.addStretch()
        root.addLayout(hdr_hl)
        root.addSpacing(14)

        div0 = QtWidgets.QFrame(); div0.setObjectName("div"); div0.setFixedHeight(1)
        root.addWidget(div0); root.addSpacing(14)

        def lbl(txt):
            l = QtWidgets.QLabel(txt); l.setObjectName("fldLbl"); return l

        form = QtWidgets.QFormLayout()
        form.setVerticalSpacing(12); form.setHorizontalSpacing(14)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.title_edit = QtWidgets.QLineEdit()
        self.title_edit.setPlaceholderText("e.g. Prepare Q2 Performance Report")
        form.addRow(lbl("Task Title *"), self.title_edit)

        self.assigned_edit = QtWidgets.QLineEdit()
        self.assigned_edit.setPlaceholderText("e.g. John Kamau")
        form.addRow(lbl("Assigned To *"), self.assigned_edit)

        self.dept_combo = QtWidgets.QComboBox()
        self.dept_combo.addItem("— Select Department —")
        self.dept_combo.addItems(DEPARTMENTS)
        form.addRow(lbl("Department *"), self.dept_combo)

        self.priority_combo = QtWidgets.QComboBox()
        self.priority_combo.addItems(["High", "Medium", "Low"])
        form.addRow(lbl("Priority *"), self.priority_combo)

        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(["In Progress", "Pending", "Completed", "Overdue"])
        form.addRow(lbl("Status"), self.status_combo)

        self.due_date = QtWidgets.QDateEdit()
        self.due_date.setCalendarPopup(True)
        self.due_date.setDisplayFormat("dd MMM yyyy")
        self.due_date.setDate(QtCore.QDate.currentDate().addDays(7))
        form.addRow(lbl("Due Date *"), self.due_date)

        self.desc_edit = QtWidgets.QTextEdit()
        self.desc_edit.setPlaceholderText("Describe the task in detail...")
        self.desc_edit.setFixedHeight(70)
        form.addRow(lbl("Description"), self.desc_edit)

        root.addLayout(form)

        # Pre-fill for edit mode
        if self._edit and task_data:
            self.title_edit.setText(task_data.get("title", ""))
            self.assigned_edit.setText(task_data.get("assigned_to", ""))
            idx = self.dept_combo.findText(task_data.get("department", ""))
            if idx >= 0: self.dept_combo.setCurrentIndex(idx)
            idx = self.priority_combo.findText(task_data.get("priority", ""))
            if idx >= 0: self.priority_combo.setCurrentIndex(idx)
            idx = self.status_combo.findText(task_data.get("status", ""))
            if idx >= 0: self.status_combo.setCurrentIndex(idx)
            self.desc_edit.setPlainText(task_data.get("description", ""))

        root.addStretch()

        self.err_lbl = QtWidgets.QLabel("")
        self.err_lbl.setStyleSheet("color:#b91c1c; font-size:11px;")
        self.err_lbl.setVisible(False)
        root.addWidget(self.err_lbl)
        root.addSpacing(8)

        div1 = QtWidgets.QFrame(); div1.setObjectName("div"); div1.setFixedHeight(1)
        root.addWidget(div1); root.addSpacing(12)

        btn_hl = QtWidgets.QHBoxLayout(); btn_hl.addStretch()
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.setFixedHeight(36)
        self.cancel_btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QtWidgets.QPushButton(
            "💾  Save Changes" if self._edit else "✚  Add Task")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.setFixedHeight(36)
        self.save_btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        self.save_btn.clicked.connect(self._on_save)

        btn_hl.addWidget(self.cancel_btn)
        btn_hl.addSpacing(8)
        btn_hl.addWidget(self.save_btn)
        root.addLayout(btn_hl)

    def _on_save(self):
        title  = self.title_edit.text().strip()
        asgn   = self.assigned_edit.text().strip()
        dept   = self.dept_combo.currentText()
        errs   = []
        if not title: errs.append("Task Title is required.")
        if not asgn:  errs.append("Assigned To is required.")
        if dept.startswith("—"): errs.append("Please select a Department.")
        if errs:
            self.err_lbl.setText("⚠  " + "  •  ".join(errs))
            self.err_lbl.setVisible(True)
            return
        self.err_lbl.setVisible(False)
        self.task_saved.emit({
            "title":       title,
            "assigned_to": asgn,
            "department":  dept,
            "priority":    self.priority_combo.currentText(),
            "status":      self.status_combo.currentText(),
            "due_date":    self.due_date.date().toString("dd MMM yyyy"),
            "description": self.desc_edit.toPlainText().strip(),
        })
        self.accept()


# ==============================================================================
# TASKS PAGE
# ==============================================================================
class TasksPage(QtWidgets.QWidget):
    """
    Full Tasks page — slots into stackedWidget index 5.

    Layout
    ──────
    Left scroll area
      • Page header + action buttons
      • 5 stat cards
      • Tab bar (All Tasks / My Tasks / Assigned to Others / Overdue Tasks)
      • Task table + pagination
      • Bottom row: donut chart | priority bar chart | overdue list
    Right panel (fixed 268px)
      • Task Details card for the selected/highlighted task
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Tasks_Page")
        self.setStyleSheet(f"background-color:{_BG};")
        self._tasks = list(SAMPLE_TASKS)
        self._active_tab = "All Tasks"
        self._selected_row = 0
        self._build_ui()
        self._populate_table()

    # ──────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = QtWidgets.QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ════════════════════════════════════════════════════════════════
        # LEFT SCROLL AREA
        # ════════════════════════════════════════════════════════════════
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background:transparent; border:none;")

        lc = QtWidgets.QWidget()
        lc.setStyleSheet(f"background:{_BG};")
        lv = QtWidgets.QVBoxLayout(lc)
        lv.setContentsMargins(22, 18, 14, 18)
        lv.setSpacing(14)

        # ── Page header ───────────────────────────────────────────────
        hdr = QtWidgets.QHBoxLayout(); hdr.setSpacing(12)
        ico = QtWidgets.QLabel("✅")
        ico.setFixedSize(44, 44)
        ico.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ico.setStyleSheet("background:#eff0ff;border-radius:22px;font-size:20px;")

        tvl = QtWidgets.QVBoxLayout(); tvl.setSpacing(2)
        pg_t = QtWidgets.QLabel("Tasks")
        pg_t.setStyleSheet(f"color:{_TEXT_DARK};font-size:20px;font-weight:bold;"
                           "font-family:'Segoe UI',Arial;")
        pg_s = QtWidgets.QLabel("Manage, assign and track all tasks across the organization.")
        pg_s.setStyleSheet(f"color:{_TEXT_GREY};font-size:11px;")
        tvl.addWidget(pg_t); tvl.addWidget(pg_s)
        hdr.addWidget(ico); hdr.addLayout(tvl); hdr.addStretch()

        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("🔍  Search tasks...")
        self.search_edit.setFixedHeight(34)
        self.search_edit.setMinimumWidth(200)
        self.search_edit.setStyleSheet(f"""
            QLineEdit {{
                border:1px solid {_BORDER}; border-radius:6px;
                padding:0 12px; font-size:12px;
                color:{_TEXT_MID}; background:{_WHITE};
            }}
            QLineEdit:focus {{ border:1.5px solid {_ACCENT}; }}
        """)
        self.search_edit.textChanged.connect(self._apply_filters)

        self.filter_btn  = self._outline_btn("▼  Filter")
        self.export_btn  = self._outline_btn("↓  Export")
        self.add_btn     = self._primary_btn("＋  Add Task")
        self.filter_btn.clicked.connect(self._on_filter_menu)
        self.export_btn.clicked.connect(self._on_export)
        self.add_btn.clicked.connect(self._on_add_task)

        hdr.addWidget(self.search_edit)
        hdr.addWidget(self.filter_btn)
        hdr.addWidget(self.export_btn)
        hdr.addWidget(self.add_btn)
        lv.addLayout(hdr)

        # ── Stat cards ────────────────────────────────────────────────
        cards_hl = QtWidgets.QHBoxLayout(); cards_hl.setSpacing(10)
        for icon, ibg, label, val, sub in [
            ("📋","#eff0ff","Total Tasks",  "146","All tasks in system"),
            ("✅","#dcfce7","Completed",     "64", "43.84% of total"),
            ("⏳","#fff7e0","In Progress",   "52", "35.62% of total"),
            ("🕐","#f3e8ff","Pending",       "22", "15.07% of total"),
            ("⚠️","#fee2e2","Overdue",       "8",  "5.48% of total"),
        ]:
            cards_hl.addWidget(_StatCard(icon, ibg, label, val, sub))
        lv.addLayout(cards_hl)

        # ── Section title ─────────────────────────────────────────────
        sec_vl = QtWidgets.QVBoxLayout(); sec_vl.setSpacing(2)
        sec_t = QtWidgets.QLabel("Tasks List")
        sec_t.setStyleSheet(f"color:{_TEXT_DARK};font-size:14px;font-weight:bold;"
                            "font-family:'Segoe UI',Arial;")
        sec_s = QtWidgets.QLabel("View, filter and manage tasks.")
        sec_s.setStyleSheet(f"color:{_TEXT_GREY};font-size:11px;")
        sec_vl.addWidget(sec_t); sec_vl.addWidget(sec_s)
        lv.addLayout(sec_vl)

        # ── Tab bar ───────────────────────────────────────────────────
        tabs_hl = QtWidgets.QHBoxLayout(); tabs_hl.setSpacing(0)
        self._tab_btns: dict[str, QtWidgets.QPushButton] = {}
        for tab in ["All Tasks", "My Tasks", "Assigned to Others", "Overdue Tasks"]:
            btn = QtWidgets.QPushButton(tab)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setFixedHeight(34)
            btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(self._tab_style(False))
            btn.clicked.connect(lambda _, t=tab: self._on_tab(t))
            self._tab_btns[tab] = btn
            tabs_hl.addWidget(btn)
        tabs_hl.addStretch()
        self._tab_btns["All Tasks"].setChecked(True)
        self._tab_btns["All Tasks"].setStyleSheet(self._tab_style(True))
        lv.addLayout(tabs_hl)

        # ── Table card ────────────────────────────────────────────────
        tcard = self._card()
        tcvl  = QtWidgets.QVBoxLayout(tcard)
        tcvl.setContentsMargins(0, 0, 0, 0)
        tcvl.setSpacing(0)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "#", "Task Title", "Assigned To", "Department",
            "Priority", "Status", "Due Date", "Actions"
        ])
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        for i, w in enumerate([30, 220, 120, 120, 75, 95, 105, 90]):
            self.table.setColumnWidth(i, w)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.table.setStyleSheet(f"""
            QTableWidget {{
                border:none; background:{_WHITE};
                alternate-background-color:#fafbfc;
                font-size:12px; color:{_TEXT_MID};
                font-family:'Segoe UI',Arial; outline:none;
            }}
            QTableWidget::item {{
                padding:4px 6px;
                border-bottom:1px solid #f3f4f6;
            }}
            QTableWidget::item:selected {{
                background:#eff6ff; color:{_TEXT_DARK};
            }}
            QHeaderView::section {{
                background:#f9fafb; color:{_TEXT_GREY};
                font-size:10px; font-weight:bold;
                border:none; border-bottom:1px solid {_BORDER}; padding:7px;
            }}
            QScrollBar:vertical {{
                border:none; background:#f0f2f5;
                width:7px; border-radius:3px;
            }}
            QScrollBar::handle:vertical {{
                background:#d1d5db; border-radius:3px;
            }}
        """)
        self.table.cellClicked.connect(self._on_row_click)
        tcvl.addWidget(self.table)

        # Pagination bar
        pg_bar = QtWidgets.QWidget()
        pg_bar.setFixedHeight(44)
        pg_bar.setStyleSheet(f"""
            QWidget {{
                background:{_WHITE};
                border-top:1px solid {_BORDER};
                border-bottom-left-radius:10px;
                border-bottom-right-radius:10px;
            }}
        """)
        pg_hl = QtWidgets.QHBoxLayout(pg_bar)
        pg_hl.setContentsMargins(14, 0, 14, 0); pg_hl.setSpacing(4)

        self.showing_lbl = QtWidgets.QLabel("Showing 1 to 10 of 146 tasks")
        self.showing_lbl.setStyleSheet(f"color:{_TEXT_GREY};font-size:11px;")
        pg_hl.addWidget(self.showing_lbl); pg_hl.addStretch()

        for txt, act in [("«",False),("‹",False),
                         ("1",True),("2",False),("3",False),
                         ("›",False),("»",False)]:
            b = QtWidgets.QPushButton(txt)
            b.setFixedSize(26, 26)
            b.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
            b.setStyleSheet(f"""
                QPushButton {{
                    background:{"#1e3a6e" if act else _WHITE};
                    color:{"#fff" if act else _TEXT_MID};
                    border:1px solid {"#1e3a6e" if act else _BORDER};
                    border-radius:4px; font-size:11px;
                }}
                QPushButton:hover {{
                    background:{"#254d91" if act else "#f9fafb"};
                }}
            """)
            pg_hl.addWidget(b)

        pg_hl.addSpacing(10)
        pp = QtWidgets.QLabel("10 / page  ▾")
        pp.setStyleSheet(f"color:{_TEXT_GREY};font-size:11px;")
        pg_hl.addWidget(pp)
        tcvl.addWidget(pg_bar)
        lv.addWidget(tcard)

        # ── Bottom analytics row ──────────────────────────────────────
        bot = QtWidgets.QHBoxLayout(); bot.setSpacing(12)

        # Donut chart — Tasks by Status
        dc = self._card()
        dc_vl = QtWidgets.QVBoxLayout(dc)
        dc_vl.setContentsMargins(14, 14, 14, 14); dc_vl.setSpacing(10)
        dc_t = QtWidgets.QLabel("Tasks by Status")
        dc_t.setStyleSheet(f"color:{_TEXT_DARK};font-size:13px;font-weight:bold;"
                           "font-family:'Segoe UI',Arial;")
        dc_vl.addWidget(dc_t)

        donut_row = QtWidgets.QHBoxLayout(); donut_row.setSpacing(14)
        self._donut = _DonutChart()
        self._donut.setFixedSize(150, 150)
        donut_row.addWidget(self._donut)

        leg_vl = QtWidgets.QVBoxLayout(); leg_vl.setSpacing(7)
        for lname, lval, lpct, lcol in [
            ("Completed",  64, "43.84%","#10b981"),
            ("In Progress",52, "35.62%","#3b82f6"),
            ("Pending",    22, "15.07%","#f59e0b"),
            ("Overdue",     8,  "5.48%","#ef4444"),
        ]:
            row = QtWidgets.QHBoxLayout(); row.setSpacing(6)
            dot = QtWidgets.QLabel("●")
            dot.setStyleSheet(f"color:{lcol};font-size:12px;")
            dot.setFixedWidth(14)
            nl = QtWidgets.QLabel(lname)
            nl.setStyleSheet(f"color:{_TEXT_MID};font-size:11px;")
            vr = QtWidgets.QLabel(f"{lval} ({lpct})")
            vr.setStyleSheet(f"color:{_TEXT_GREY};font-size:11px;")
            vr.setAlignment(Qt.AlignmentFlag.AlignRight)
            row.addWidget(dot); row.addWidget(nl)
            row.addStretch(); row.addWidget(vr)
            leg_vl.addLayout(row)
        donut_row.addLayout(leg_vl)
        dc_vl.addLayout(donut_row)
        bot.addWidget(dc, stretch=3)

        # Priority bar chart
        bc = self._card()
        bc_vl = QtWidgets.QVBoxLayout(bc)
        bc_vl.setContentsMargins(14, 14, 14, 14); bc_vl.setSpacing(10)
        bc_t = QtWidgets.QLabel("Tasks by Priority")
        bc_t.setStyleSheet(f"color:{_TEXT_DARK};font-size:13px;font-weight:bold;"
                           "font-family:'Segoe UI',Arial;")
        bc_vl.addWidget(bc_t)

        for pri, val, total, col in PRIORITY_BARS:
            row = QtWidgets.QHBoxLayout(); row.setSpacing(8)
            lbl = QtWidgets.QLabel(pri)
            lbl.setFixedWidth(50)
            lbl.setStyleSheet(f"color:{_TEXT_MID};font-size:11px;")

            bar_bg = QtWidgets.QFrame()
            bar_bg.setFixedHeight(12)
            bar_bg.setStyleSheet("background:#f3f4f6;border-radius:6px;")
            bar_bg_hl = QtWidgets.QHBoxLayout(bar_bg)
            bar_bg_hl.setContentsMargins(0,0,0,0); bar_bg_hl.setSpacing(0)
            fill = QtWidgets.QFrame()
            fill.setFixedHeight(12)
            fill.setStyleSheet(f"background:{col};border-radius:6px;")
            pct = int(val / total * 100)
            bar_bg_hl.addWidget(fill, stretch=pct)
            bar_bg_hl.addStretch(100 - pct)

            vl_lbl = QtWidgets.QLabel(f"{val} ({val/total*100:.2f}%)")
            vl_lbl.setFixedWidth(90)
            vl_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            vl_lbl.setStyleSheet(f"color:{_TEXT_GREY};font-size:11px;")

            row.addWidget(lbl); row.addWidget(bar_bg, stretch=1); row.addWidget(vl_lbl)
            bc_vl.addLayout(row)

        bc_vl.addStretch()
        total_lbl = QtWidgets.QLabel("Total Tasks: 146")
        total_lbl.setStyleSheet(f"color:{_TEXT_DARK};font-size:12px;font-weight:bold;")
        bc_vl.addWidget(total_lbl)
        bot.addWidget(bc, stretch=3)

        # Overdue tasks list
        od = self._card()
        od_vl = QtWidgets.QVBoxLayout(od)
        od_vl.setContentsMargins(14, 14, 14, 14); od_vl.setSpacing(10)

        od_hdr = QtWidgets.QHBoxLayout()
        od_t = QtWidgets.QLabel("Overdue Tasks")
        od_t.setStyleSheet(f"color:{_TEXT_DARK};font-size:13px;font-weight:bold;"
                           "font-family:'Segoe UI',Arial;")
        va = QtWidgets.QLabel("View All")
        va.setStyleSheet(f"color:{_ACCENT};font-size:11px;")
        va.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        od_hdr.addWidget(od_t); od_hdr.addStretch(); od_hdr.addWidget(va)
        od_vl.addLayout(od_hdr)

        for title, date, sub in OVERDUE_TASKS:
            row_w = QtWidgets.QWidget()
            row_w.setStyleSheet("background:#fff8f8;border-radius:7px;")
            row_vl = QtWidgets.QVBoxLayout(row_w)
            row_vl.setContentsMargins(8, 6, 8, 6); row_vl.setSpacing(2)

            top_hl = QtWidgets.QHBoxLayout()
            warn = QtWidgets.QLabel("⚠")
            warn.setStyleSheet("color:#ef4444;font-size:12px;")
            warn.setFixedWidth(18)
            tl = QtWidgets.QLabel(title)
            tl.setStyleSheet(f"color:{_TEXT_DARK};font-size:11px;font-weight:600;")
            dl = QtWidgets.QLabel(date)
            dl.setStyleSheet("color:#ef4444;font-size:10px;")
            dl.setAlignment(Qt.AlignmentFlag.AlignRight)
            top_hl.addWidget(warn); top_hl.addWidget(tl)
            top_hl.addStretch(); top_hl.addWidget(dl)

            sl = QtWidgets.QLabel(sub)
            sl.setStyleSheet(f"color:{_TEXT_GREY};font-size:10px;padding-left:20px;")

            row_vl.addLayout(top_hl); row_vl.addWidget(sl)
            od_vl.addWidget(row_w)

        od_vl.addStretch()
        total_od = QtWidgets.QLabel("Total Overdue Tasks: 8")
        total_od.setStyleSheet("color:#ef4444;font-size:12px;font-weight:bold;")
        od_vl.addWidget(total_od)
        bot.addWidget(od, stretch=3)

        lv.addLayout(bot)
        lv.addStretch()
        scroll.setWidget(lc)
        outer.addWidget(scroll, stretch=1)

        # ════════════════════════════════════════════════════════════════
        # RIGHT PANEL — Task Details
        # ════════════════════════════════════════════════════════════════
        rp = QtWidgets.QWidget()
        rp.setFixedWidth(268)
        rp.setStyleSheet(f"background:{_BG};border-left:1px solid {_BORDER};")

        rp_scroll = QtWidgets.QScrollArea()
        rp_scroll.setWidgetResizable(True)
        rp_scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        rp_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        rp_scroll.setStyleSheet("background:transparent;border:none;")

        ri = QtWidgets.QWidget(); ri.setStyleSheet(f"background:{_BG};")
        rv = QtWidgets.QVBoxLayout(ri)
        rv.setContentsMargins(10, 16, 10, 16); rv.setSpacing(12)

        # Task Details card
        td_card = self._card()
        self._td_vl = QtWidgets.QVBoxLayout(td_card)
        self._td_vl.setContentsMargins(14, 14, 14, 14)
        self._td_vl.setSpacing(10)
        self._build_detail_panel(SAMPLE_TASKS[0])
        rv.addWidget(td_card)
        rv.addStretch()

        rp_scroll.setWidget(ri)
        rp_vl = QtWidgets.QVBoxLayout(rp)
        rp_vl.setContentsMargins(0, 0, 0, 0)
        rp_vl.addWidget(rp_scroll)
        outer.addWidget(rp)

    # ──────────────────────────────────────────────────────────────────────────
    # DETAIL PANEL
    # ──────────────────────────────────────────────────────────────────────────
    def _build_detail_panel(self, task: tuple):
        # Clear existing widgets
        while self._td_vl.count():
            item = self._td_vl.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        (task_id, title, assigned_to, department, priority,
         status, due_date, created_by, created_on, last_updated, description) = task

        # Header label
        hdr_lbl = QtWidgets.QLabel("Task Details")
        hdr_lbl.setStyleSheet(f"color:{_TEXT_DARK};font-size:13px;font-weight:bold;"
                              "font-family:'Segoe UI',Arial;")
        self._td_vl.addWidget(hdr_lbl)

        # Icon + title + status badge
        ico = QtWidgets.QLabel("📋")
        ico.setFixedSize(52, 52)
        ico.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ico.setStyleSheet("background:#eff0ff;border-radius:26px;font-size:24px;")
        self._td_vl.addWidget(ico, alignment=Qt.AlignmentFlag.AlignCenter)

        tl = QtWidgets.QLabel(title)
        tl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tl.setWordWrap(True)
        tl.setStyleSheet(f"color:{_TEXT_DARK};font-size:12px;font-weight:bold;"
                         "font-family:'Segoe UI',Arial;")
        self._td_vl.addWidget(tl)

        sfg, sbg = STATUS_COLOURS.get(status, (_TEXT_MID, "#f3f4f6"))
        st_badge = _Badge(status, sfg, sbg)
        st_row = QtWidgets.QHBoxLayout()
        st_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        st_row.addWidget(st_badge)
        self._td_vl.addLayout(st_row)

        # Divider
        dv = QtWidgets.QFrame()
        dv.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        dv.setStyleSheet(f"color:{_BORDER};")
        self._td_vl.addWidget(dv)

        # Detail rows
        details = [
            ("📋","Task ID",      task_id),
            ("👤","Assigned To",  assigned_to),
            ("🏢","Department",   department),
            ("⚡","Priority",     priority),
            ("📅","Due Date",     due_date),
            ("📊","Status",       status),
            ("👥","Created By",   created_by),
            ("🕐","Created On",   created_on),
            ("🔄","Last Updated", last_updated),
        ]
        for d_ico, d_lbl, d_val in details:
            row = QtWidgets.QHBoxLayout(); row.setSpacing(6)
            il = QtWidgets.QLabel(d_ico)
            il.setFixedWidth(18)
            il.setStyleSheet("font-size:11px;")
            ll = QtWidgets.QLabel(d_lbl)
            ll.setFixedWidth(80)
            ll.setStyleSheet(f"color:{_TEXT_GREY};font-size:10px;")

            if d_lbl == "Priority":
                pfg, pbg = PRIORITY_COLOURS.get(d_val, (_TEXT_MID, "#f3f4f6"))
                vw = _Badge(d_val, pfg, pbg)
            elif d_lbl == "Status":
                sfg2, sbg2 = STATUS_COLOURS.get(d_val, (_TEXT_MID, "#f3f4f6"))
                vw = _Badge(d_val, sfg2, sbg2)
            else:
                vw = QtWidgets.QLabel(d_val)
                vw.setStyleSheet(f"color:{_TEXT_DARK};font-size:10px;font-weight:600;")
                vw.setWordWrap(True)

            row.addWidget(il); row.addWidget(ll); row.addWidget(vw); row.addStretch()
            self._td_vl.addLayout(row)

        # Description
        desc_lbl = QtWidgets.QLabel("Description")
        desc_lbl.setStyleSheet(f"color:{_TEXT_GREY};font-size:10px;")
        self._td_vl.addWidget(desc_lbl)

        desc_txt = QtWidgets.QLabel(description)
        desc_txt.setWordWrap(True)
        desc_txt.setStyleSheet(f"color:{_TEXT_MID};font-size:10px;"
                               "background:#f9fafb;border-radius:5px;padding:6px;")
        self._td_vl.addWidget(desc_txt)

        # View Full Details button
        vfd = QtWidgets.QPushButton("View Full Details")
        vfd.setFixedHeight(34)
        vfd.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        vfd.setStyleSheet(f"""
            QPushButton {{
                background:{_ACCENT}; color:{_WHITE}; border:none;
                border-radius:6px; font-size:12px; font-weight:bold;
            }}
            QPushButton:hover {{ background:#4a60ee; }}
        """)
        self._td_vl.addWidget(vfd)

    # ──────────────────────────────────────────────────────────────────────────
    # TABLE POPULATION
    # ──────────────────────────────────────────────────────────────────────────
    def _populate_table(self, data: list = None):
        rows = data if data is not None else self._tasks
        self.table.setRowCount(0)
        for i, task in enumerate(rows):
            task_id, title, assigned_to, dept, priority, status, due_date, *_ = task
            self.table.insertRow(i)
            self.table.setRowHeight(i, 46)

            self._set_item(i, 0, str(i + 1))
            self._set_item(i, 1, title)
            self._set_item(i, 2, assigned_to)
            self._set_item(i, 3, dept)

            pfg, pbg = PRIORITY_COLOURS.get(priority, (_TEXT_MID, "#f3f4f6"))
            self.table.setCellWidget(i, 4, self._centre(_Badge(priority, pfg, pbg)))

            sfg, sbg = STATUS_COLOURS.get(status, (_TEXT_MID, "#f3f4f6"))
            self.table.setCellWidget(i, 5, self._centre(_Badge(status, sfg, sbg)))

            self._set_item(i, 6, due_date)
            self.table.setCellWidget(i, 7, self._action_widget(i))

        count = len(rows)
        self.showing_lbl.setText(
            f"Showing 1 to {min(10, count)} of {count} tasks")

    def _set_item(self, row, col, text):
        it = QtWidgets.QTableWidgetItem(text)
        it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, col, it)

    @staticmethod
    def _centre(widget) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        hl = QtWidgets.QHBoxLayout(w)
        hl.addWidget(widget)
        hl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        hl.setContentsMargins(6, 0, 0, 0)
        return w

    def _action_widget(self, row: int) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        hl = QtWidgets.QHBoxLayout(w)
        hl.setContentsMargins(4, 0, 4, 0); hl.setSpacing(4)
        for ico, tip, col, slot in [
            ("👁","View",  "#64748b", lambda _, r=row: self._on_view(r)),
            ("✏","Edit",  "#2563eb", lambda _, r=row: self._on_edit(r)),
            ("🗑","Delete","#dc2626", lambda _, r=row: self._on_delete(r)),
        ]:
            b = QtWidgets.QPushButton(ico)
            b.setFixedSize(26, 26)
            b.setToolTip(tip)
            b.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
            b.setStyleSheet(f"""
                QPushButton {{
                    background:{col}22; color:{col};
                    border:1px solid {col}44;
                    border-radius:5px; font-size:12px;
                }}
                QPushButton:hover {{ background:{col}44; }}
            """)
            b.clicked.connect(slot)
            hl.addWidget(b)
        hl.addStretch()
        return w

    # ──────────────────────────────────────────────────────────────────────────
    # SLOTS
    # ──────────────────────────────────────────────────────────────────────────
    def _on_tab(self, tab: str):
        self._active_tab = tab
        for name, btn in self._tab_btns.items():
            btn.setStyleSheet(self._tab_style(name == tab))
        self._apply_filters()

    def _apply_filters(self):
        text = self.search_edit.text().lower()
        results = []
        for task in self._tasks:
            task_id, title, assigned_to, dept, priority, status, due_date, *_ = task
            if self._active_tab == "My Tasks" and assigned_to != "John Kamau":
                continue
            if self._active_tab == "Assigned to Others" and assigned_to == "John Kamau":
                continue
            if self._active_tab == "Overdue Tasks" and status != "Overdue":
                continue
            if text and not any(text in v.lower() for v in
                                (task_id, title, assigned_to, dept, priority, status)):
                continue
            results.append(task)
        self._populate_table(results)

    def _on_row_click(self, row, col):
        visible = [t for t in self._tasks
                   if self._active_tab in ("All Tasks", t[5]) or
                   (self._active_tab == "My Tasks" and t[2] == "John Kamau") or
                   (self._active_tab == "Overdue Tasks" and t[5] == "Overdue")]
        if row < len(visible):
            self._build_detail_panel(visible[row])

    def _on_add_task(self):
        dlg = AddTaskDialog(self)
        dlg.task_saved.connect(self._append_task)
        dlg.exec()

    def _append_task(self, data: dict):
        new_id = f"TSK-2025-{len(self._tasks) + 1:04d}"
        self._tasks.insert(0, (
            new_id, data["title"], data["assigned_to"], data["department"],
            data["priority"], data["status"], data["due_date"],
            "System Administrator", "Just now", "Just now", data["description"]
        ))
        self._apply_filters()
        QtWidgets.QMessageBox.information(
            self, "Task Added",
            f"✅  '{data['title']}' has been added successfully."
        )

    def _on_view(self, row: int):
        if row < len(self._tasks):
            self._build_detail_panel(self._tasks[row])

    def _on_edit(self, row: int):
        if row >= len(self._tasks): return
        t = self._tasks[row]
        dlg = AddTaskDialog(self, task_data={
            "title": t[1], "assigned_to": t[2], "department": t[3],
            "priority": t[4], "status": t[5], "description": t[10],
        })
        dlg.task_saved.connect(lambda data, r=row: self._save_edit(r, data))
        dlg.exec()

    def _save_edit(self, row: int, data: dict):
        old = self._tasks[row]
        self._tasks[row] = (
            old[0], data["title"], data["assigned_to"], data["department"],
            data["priority"], data["status"], data["due_date"],
            old[7], old[8], "Just now", data["description"]
        )
        self._apply_filters()

    def _on_delete(self, row: int):
        if row >= len(self._tasks): return
        name = self._tasks[row][1]
        reply = QtWidgets.QMessageBox.question(
            self, "Delete Task",
            f"Delete <b>{name}</b>? This cannot be undone.",
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self._tasks.pop(row)
            self._apply_filters()

    def _on_filter_menu(self):
        QtWidgets.QMessageBox.information(
            self, "Advanced Filters",
            "Advanced filter panel will be available in the next sprint."
        )

    def _on_export(self):
        QtWidgets.QMessageBox.information(
            self, "Export",
            "Export functionality will be connected in the next sprint."
        )

    # ──────────────────────────────────────────────────────────────────────────
    # STYLE HELPERS
    # ──────────────────────────────────────────────────────────────────────────
    @staticmethod
    def _card() -> QtWidgets.QFrame:
        f = QtWidgets.QFrame()
        f.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        f.setStyleSheet(f"""
            QFrame {{
                background:{_WHITE};
                border:1px solid {_BORDER};
                border-radius:10px;
            }}
        """)
        return f

    @staticmethod
    def _outline_btn(text: str) -> QtWidgets.QPushButton:
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(34)
        btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet(f"""
            QPushButton {{
                background:{_WHITE}; color:{_TEXT_MID};
                border:1px solid {_BORDER}; border-radius:6px;
                padding:0 14px; font-size:12px;
                font-family:'Segoe UI',Arial;
            }}
            QPushButton:hover {{ background:#f9fafb; }}
        """)
        return btn

    @staticmethod
    def _primary_btn(text: str) -> QtWidgets.QPushButton:
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(34)
        btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet(f"""
            QPushButton {{
                background:{_ACCENT}; color:{_WHITE}; border:none;
                border-radius:6px; padding:0 16px;
                font-size:12px; font-weight:bold;
                font-family:'Segoe UI',Arial;
            }}
            QPushButton:hover {{ background:#4a60ee; }}
        """)
        return btn

    @staticmethod
    def _tab_style(active: bool) -> str:
        if active:
            return f"""
                QPushButton {{
                    background:transparent; color:{_ACCENT};
                    border:none; border-bottom:2px solid {_ACCENT};
                    padding:0 14px; font-size:12px; font-weight:bold;
                    font-family:'Segoe UI',Arial;
                }}
            """
        return f"""
            QPushButton {{
                background:transparent; color:{_TEXT_GREY};
                border:none; border-bottom:2px solid transparent;
                padding:0 14px; font-size:12px;
                font-family:'Segoe UI',Arial;
            }}
            QPushButton:hover {{ color:{_TEXT_DARK}; }}
        """