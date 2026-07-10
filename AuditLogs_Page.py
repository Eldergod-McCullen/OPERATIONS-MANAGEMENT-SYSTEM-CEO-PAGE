from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


# ── Shared palette (matches CEO_Page.py / users_page.py) ─────────────────────
_NAVY      = "#0d1b3e"
_BLUE_ACT  = "#1e3a6e"
_ACCENT    = "#5870ff"
_BG        = "#f0f2f5"
_WHITE     = "#ffffff"
_BORDER    = "#e5e7eb"
_TEXT_DARK = "#1a1a2e"
_TEXT_GREY = "#6b7280"
_TEXT_MID  = "#374151"


# ── Action badge colours  {action: (text_colour, bg_colour)} ─────────────────
ACTION_COLOURS: dict[str, tuple[str, str]] = {
    "LOGIN":  ("#1d4ed8", "#dbeafe"),
    "LOGOUT": ("#374151", "#f3f4f6"),
    "VIEW":   ("#0369a1", "#e0f2fe"),
    "CREATE": ("#15803d", "#dcfce7"),
    "UPDATE": ("#d97706", "#fef3c7"),
    "DELETE": ("#b91c1c", "#fee2e2"),
    "EXPORT": ("#7c3aed", "#ede9fe"),
}

# ── Sample log data ───────────────────────────────────────────────────────────
# (log_id, timestamp, user_name, role, action, table_affected, record_id,
#  ip_address, details)
SAMPLE_LOGS = [
    ("10001","01 Jul 2025 10:45:32 AM","Jane Mwangi","Administrator","LOGIN", "-","-","192.168.1.101","User logged in successfully"),
    ("10000","01 Jul 2025 10:42:15 AM","Jane Mwangi","Administrator","VIEW","TASKS","58","192.168.1.101","Viewed task details"),
    ("9999", "01 Jul 2025 10:40:09 AM","John Kamau","CEO","UPDATE","USERS","14","192.168.1.105","Updated user role from Operations Manager to General Manager"),
    ("9998", "01 Jul 2025 10:35:47 AM","Jane Mwangi","Administrator","CREATE","ANNOUNCEMENTS","25","192.168.1.101","Created new announcement 'Staff Meeting on Friday'"),
    ("9997", "01 Jul 2025 10:20:31 AM","Peter Otieno","Operations Manager","UPDATE","MAINTENANCE_REQUESTS","102","192.168.1.112","Updated status to In Progress"),
    ("9996", "01 Jul 2025 10:18:16 AM","Mary Wanjiku","General Manager","DELETE","VISITORS","77","192.168.1.109","Deleted visitor record"),
    ("9995", "01 Jul 2025 10:10:05 AM","Samuel Mutua","IT Manager","CREATE","USERS","45","192.168.1.108","Created new user account"),
    ("9994", "30 Jun 2025 09:55:43 AM","Grace Njeri","Marketing Officer","EXPORT","REPORTS","-","192.168.1.114","Exported Marketing Report to PDF"),
    ("9993", "30 Jun 2025 09:50:21 AM","Jane Mwangi","Administrator","LOGOUT","-","-","192.168.1.101","User logged out"),
    ("9992", "30 Jun 2025 09:48:11 AM","Jane Mwangi","Administrator","LOGIN","-","-","192.168.1.101","User logged in successfully"),
]

TOP_USERS = [
    ("JM", "#c8a96e", "Jane Mwangi",   "Administrator",      "2,458"),
    ("JK", "#3b82f6", "John Kamau",    "CEO",                "1,876"),
    ("PO", "#10b981", "Peter Otieno",  "Operations Manager", "1,432"),
    ("SM", "#8b5cf6", "Samuel Mutua",  "IT Manager",         "1,210"),
    ("MW", "#f59e0b", "Mary Wanjiku",  "General Manager",    "987"),
]

CRITICAL_ACTIONS = [
    ("User role changed",         "10:40 AM"),
    ("Maintenance request deleted","09:18 AM"),
    ("User account deactivated",  "Yesterday, 04:30 PM"),
    ("Announcement deleted",      "Yesterday, 02:10 PM"),
]

ALL_TABLES = [
    "All Tables", "USERS", "TASKS", "ANNOUNCEMENTS",
    "VISITORS", "MAINTENANCE_REQUESTS", "REPORTS",
]

ALL_USERS = [
    "All Users", "Jane Mwangi", "John Kamau", "Peter Otieno",
    "Mary Wanjiku", "Samuel Mutua", "Grace Njeri",
]


# ==============================================================================
# BADGE  helper
# ==============================================================================
class _Badge(QtWidgets.QLabel):
    def __init__(self, text: str, fg: str, bg: str, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(22)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                           QtWidgets.QSizePolicy.Policy.Fixed)
        self.setStyleSheet(f"""
            QLabel {{
                color: {fg};
                background-color: {bg};
                border-radius: 10px;
                padding: 0px 10px;
                font-size: 11px;
                font-weight: 700;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)


# ==============================================================================
# SUMMARY STAT CARD  (right panel)
# ==============================================================================
class _SummaryCard(QtWidgets.QFrame):
    def __init__(self, icon: str, icon_bg: str, value: str,
                 label: str, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {_WHITE};
                border: 1px solid {_BORDER};
                border-radius: 8px;
            }}
        """)
        self.setFixedHeight(62)

        hl = QtWidgets.QHBoxLayout(self)
        hl.setContentsMargins(10, 0, 10, 0)
        hl.setSpacing(10)

        icon_lbl = QtWidgets.QLabel(icon)
        icon_lbl.setFixedSize(34, 34)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"""
            QLabel {{
                background-color: {icon_bg};
                border-radius: 17px;
                font-size: 15px;
            }}
        """)

        vl = QtWidgets.QVBoxLayout()
        vl.setSpacing(1)

        val_lbl = QtWidgets.QLabel(value)
        val_lbl.setStyleSheet(f"""
            color: {_TEXT_DARK};
            font-size: 18px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        lbl_lbl = QtWidgets.QLabel(label)
        lbl_lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 10px;")

        vl.addWidget(val_lbl)
        vl.addWidget(lbl_lbl)

        hl.addWidget(icon_lbl)
        hl.addLayout(vl)
        hl.addStretch()


# ==============================================================================
# AUDIT LOGS PAGE
# ==============================================================================
class AuditLogsPage(QtWidgets.QWidget):
    """
    Full Audit Logs page — slots into stackedWidget index 10.
    Left column  : filter bar + main table + pagination
    Right column : Log Summary cards + Top Users + Recent Critical Actions
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AuditLogs_Page")
        self.setStyleSheet(f"background-color: {_BG};")
        self._logs = list(SAMPLE_LOGS)
        self._build_ui()
        self._populate_table()

    # ──────────────────────────────────────────────────────────────────────────
    # UI CONSTRUCTION
    # ──────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Outer horizontal split: left content | right panel
        outer_hl = QtWidgets.QHBoxLayout(self)
        outer_hl.setContentsMargins(0, 0, 0, 0)
        outer_hl.setSpacing(0)

        # ── LEFT SCROLL AREA ──────────────────────────────────────────────────
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background-color: transparent; border: none;")

        left_container = QtWidgets.QWidget()
        left_container.setStyleSheet(f"background-color: {_BG};")
        left_vl = QtWidgets.QVBoxLayout(left_container)
        left_vl.setContentsMargins(24, 20, 16, 20)
        left_vl.setSpacing(14)

        # ── Page header ───────────────────────────────────────────────────────
        hdr_hl = QtWidgets.QHBoxLayout()
        hdr_hl.setSpacing(14)

        icon_lbl = QtWidgets.QLabel("🔍")
        icon_lbl.setFixedSize(44, 44)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"""
            QLabel {{
                background-color: #eff0ff;
                border-radius: 22px;
                font-size: 20px;
            }}
        """)

        title_vl = QtWidgets.QVBoxLayout()
        title_vl.setSpacing(2)
        pg_title = QtWidgets.QLabel("Audit Logs")
        pg_title.setStyleSheet(f"""
            color: {_TEXT_DARK};
            font-size: 20px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        pg_sub = QtWidgets.QLabel("Track and review all system activities and user actions")
        pg_sub.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 12px;")
        title_vl.addWidget(pg_title)
        title_vl.addWidget(pg_sub)

        hdr_hl.addWidget(icon_lbl)
        hdr_hl.addLayout(title_vl)
        hdr_hl.addStretch()

        # Export + Actions buttons
        self.export_btn  = self._outline_btn("  ↑  Export")
        self.actions_btn = self._outline_btn("  Actions  ▾")
        self.export_btn.clicked.connect(self._on_export)
        self.actions_btn.clicked.connect(self._on_actions)

        hdr_hl.addWidget(self.export_btn)
        hdr_hl.addWidget(self.actions_btn)
        left_vl.addLayout(hdr_hl)

        # ── Filter card ───────────────────────────────────────────────────────
        filter_card = self._card_frame()
        fc_vl = QtWidgets.QVBoxLayout(filter_card)
        fc_vl.setContentsMargins(16, 12, 16, 12)
        fc_vl.setSpacing(10)

        # Row 1 — search + combos + dates + buttons
        row1 = QtWidgets.QHBoxLayout()
        row1.setSpacing(10)

        # Search box
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("🔍  Search logs by user, action or record...")
        self.search_edit.setFixedHeight(36)
        self.search_edit.setMinimumWidth(260)
        self.search_edit.setStyleSheet(self._input_style())
        self.search_edit.textChanged.connect(self._on_filter)

        # Action Type combo
        self.action_combo = self._combo_with_label(
            "Action Type",
            ["All Actions","LOGIN","LOGOUT","VIEW","CREATE","UPDATE","DELETE","EXPORT"]
        )

        # User combo
        self.user_combo = self._combo_with_label("User", ALL_USERS)

        # Table Affected combo
        self.table_combo = self._combo_with_label("Table Affected", ALL_TABLES)

        # Date From
        self.date_from = self._date_widget("Date From", "01/06/2025")

        # Date To
        self.date_to = self._date_widget("Date To", "01/07/2025")

        # Filters + Reset buttons (stacked vertically)
        btn_vl = QtWidgets.QVBoxLayout()
        btn_vl.setSpacing(4)
        self.filter_btn = self._small_btn("▼  Filters")
        self.reset_btn  = self._small_btn("↺  Reset")
        self.filter_btn.clicked.connect(self._on_filter)
        self.reset_btn.clicked.connect(self._on_reset)
        btn_vl.addWidget(self.filter_btn)
        btn_vl.addWidget(self.reset_btn)

        row1.addWidget(self.search_edit)
        row1.addLayout(self.action_combo)
        row1.addLayout(self.user_combo)
        row1.addLayout(self.table_combo)
        row1.addLayout(self.date_from)
        row1.addLayout(self.date_to)
        row1.addLayout(btn_vl)
        row1.addStretch()

        fc_vl.addLayout(row1)
        left_vl.addWidget(filter_card)

        # ── Table card ────────────────────────────────────────────────────────
        table_card = self._card_frame()
        tc_vl = QtWidgets.QVBoxLayout(table_card)
        tc_vl.setContentsMargins(0, 0, 0, 0)
        tc_vl.setSpacing(0)

        # Table widget
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "", "Log ID", "Timestamp", "User",
            "Action", "Table Affected", "Record ID", "IP Address", "Details"
        ])
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setSortingEnabled(True)

        # Column widths
        self.table.setColumnWidth(0, 36)   # checkbox
        self.table.setColumnWidth(1, 70)   # log id
        self.table.setColumnWidth(2, 165)  # timestamp
        self.table.setColumnWidth(3, 185)  # user
        self.table.setColumnWidth(4, 90)   # action badge
        self.table.setColumnWidth(5, 165)  # table affected
        self.table.setColumnWidth(6, 80)   # record id
        self.table.setColumnWidth(7, 120)  # ip address
        self.table.horizontalHeader().setStretchLastSection(True)  # details stretches

        self.table.setStyleSheet(f"""
            QTableWidget {{
                border: none;
                background-color: {_WHITE};
                alternate-background-color: #fafbfc;
                font-size: 12px;
                color: {_TEXT_MID};
                font-family: 'Segoe UI', Arial, sans-serif;
                outline: none;
            }}
            QTableWidget::item {{
                padding: 4px 8px;
                border-bottom: 1px solid #f3f4f6;
            }}
            QTableWidget::item:selected {{
                background-color: #eff6ff;
                color: {_TEXT_DARK};
            }}
            QHeaderView::section {{
                background-color: #f9fafb;
                color: {_TEXT_GREY};
                font-size: 11px;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid {_BORDER};
                padding: 8px;
            }}
            QScrollBar:vertical {{
                border: none;
                background: #f0f2f5;
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: #d1d5db;
                border-radius: 4px;
            }}
        """)

        tc_vl.addWidget(self.table)

        # ── Pagination bar ────────────────────────────────────────────────────
        pg_bar = QtWidgets.QWidget()
        pg_bar.setFixedHeight(46)
        pg_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {_WHITE};
                border-top: 1px solid {_BORDER};
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }}
        """)
        pg_hl = QtWidgets.QHBoxLayout(pg_bar)
        pg_hl.setContentsMargins(16, 0, 16, 0)
        pg_hl.setSpacing(5)

        self.showing_lbl = QtWidgets.QLabel("Showing 1 to 10 of 12,458 logs")
        self.showing_lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 12px;")
        pg_hl.addWidget(self.showing_lbl)
        pg_hl.addStretch()

        for text, active in [("«",False),("‹",False),
                              ("1",True),("2",False),("3",False),
                              ("4",False),("5",False),
                              ("›",False),("»",False)]:
            btn = QtWidgets.QPushButton(text)
            btn.setFixedSize(28, 28)
            btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {"#1e3a6e" if active else _WHITE};
                    color: {"#ffffff" if active else _TEXT_MID};
                    border: 1px solid {"#1e3a6e" if active else _BORDER};
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: {"bold" if active else "normal"};
                }}
                QPushButton:hover {{
                    background-color: {"#254d91" if active else "#f9fafb"};
                }}
            """)
            pg_hl.addWidget(btn)

        tc_vl.addWidget(pg_bar)
        left_vl.addWidget(table_card)

        scroll.setWidget(left_container)
        outer_hl.addWidget(scroll, stretch=1)

        # ── RIGHT PANEL ───────────────────────────────────────────────────────
        right_panel = QtWidgets.QWidget()
        right_panel.setFixedWidth(272)
        right_panel.setStyleSheet(f"""
            QWidget {{
                background-color: {_BG};
                border-left: 1px solid {_BORDER};
            }}
        """)

        right_scroll = QtWidgets.QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        right_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        right_scroll.setStyleSheet("background: transparent; border: none;")

        right_inner = QtWidgets.QWidget()
        right_inner.setStyleSheet(f"background-color: {_BG};")
        right_vl = QtWidgets.QVBoxLayout(right_inner)
        right_vl.setContentsMargins(12, 20, 12, 20)
        right_vl.setSpacing(14)

        # ── Log Summary card ──────────────────────────────────────────────────
        summary_card = self._card_frame()
        sv_vl = QtWidgets.QVBoxLayout(summary_card)
        sv_vl.setContentsMargins(14, 14, 14, 14)
        sv_vl.setSpacing(10)

        sum_hdr = QtWidgets.QLabel("Log Summary")
        sum_hdr.setStyleSheet(f"""
            color: {_TEXT_DARK};
            font-size: 13px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        sv_vl.addWidget(sum_hdr)

        # 2-column grid of stat tiles
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(8)

        tiles = [
            ("📄", "#eff0ff", "12,458", "Total Logs"),
            ("✅", "#dcfce7", "4,231",  "Create Actions"),
            ("✏️", "#fef3c7", "5,102",  "Update Actions"),
            ("🗑", "#fee2e2", "1,203",  "Delete Actions"),
            ("🔐", "#ede9fe", "1,345",  "Logins"),
            ("📤", "#f0f2f5", "577",    "Logouts"),
        ]
        for i, (icon, bg, val, lbl) in enumerate(tiles):
            tile = _SummaryCard(icon, bg, val, lbl)
            grid.addWidget(tile, i // 2, i % 2)

        sv_vl.addLayout(grid)
        right_vl.addWidget(summary_card)

        # ── Top Users by Activity card ────────────────────────────────────────
        top_card = self._card_frame()
        tu_vl = QtWidgets.QVBoxLayout(top_card)
        tu_vl.setContentsMargins(14, 14, 14, 14)
        tu_vl.setSpacing(10)

        tu_hdr_hl = QtWidgets.QHBoxLayout()
        tu_title = QtWidgets.QLabel("Top Users by Activity")
        tu_title.setStyleSheet(f"""
            color: {_TEXT_DARK};
            font-size: 13px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        tu_view = QtWidgets.QLabel("View All")
        tu_view.setStyleSheet(f"color: {_ACCENT}; font-size: 11px;")
        tu_view.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        tu_hdr_hl.addWidget(tu_title)
        tu_hdr_hl.addStretch()
        tu_hdr_hl.addWidget(tu_view)
        tu_vl.addLayout(tu_hdr_hl)

        for initials, av_col, name, role, logs in TOP_USERS:
            row_hl = QtWidgets.QHBoxLayout()
            row_hl.setSpacing(8)

            av = QtWidgets.QLabel(initials)
            av.setFixedSize(32, 32)
            av.setAlignment(Qt.AlignmentFlag.AlignCenter)
            av.setStyleSheet(f"""
                QLabel {{
                    background-color: {av_col};
                    border-radius: 16px;
                    color: white;
                    font-size: 11px;
                    font-weight: bold;
                }}
            """)

            info_vl = QtWidgets.QVBoxLayout()
            info_vl.setSpacing(1)
            name_lbl = QtWidgets.QLabel(name)
            name_lbl.setStyleSheet(f"""
                color: {_TEXT_DARK};
                font-size: 12px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial, sans-serif;
            """)
            role_lbl = QtWidgets.QLabel(role)
            role_lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 10px;")
            info_vl.addWidget(name_lbl)
            info_vl.addWidget(role_lbl)

            logs_lbl = QtWidgets.QLabel(f"{logs} logs")
            logs_lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")

            row_hl.addWidget(av)
            row_hl.addLayout(info_vl)
            row_hl.addStretch()
            row_hl.addWidget(logs_lbl)
            tu_vl.addLayout(row_hl)

        right_vl.addWidget(top_card)

        # ── Recent Critical Actions card ──────────────────────────────────────
        crit_card = self._card_frame()
        ca_vl = QtWidgets.QVBoxLayout(crit_card)
        ca_vl.setContentsMargins(14, 14, 14, 14)
        ca_vl.setSpacing(10)

        ca_hdr_hl = QtWidgets.QHBoxLayout()
        ca_title = QtWidgets.QLabel("Recent Critical Actions")
        ca_title.setStyleSheet(f"""
            color: {_TEXT_DARK};
            font-size: 13px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        ca_view = QtWidgets.QLabel("View All")
        ca_view.setStyleSheet(f"color: {_ACCENT}; font-size: 11px;")
        ca_view.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        ca_hdr_hl.addWidget(ca_title)
        ca_hdr_hl.addStretch()
        ca_hdr_hl.addWidget(ca_view)
        ca_vl.addLayout(ca_hdr_hl)

        for action_text, time_text in CRITICAL_ACTIONS:
            row_hl = QtWidgets.QHBoxLayout()
            row_hl.setSpacing(8)

            dot = QtWidgets.QLabel("●")
            dot.setFixedWidth(14)
            dot.setStyleSheet("color: #ef4444; font-size: 10px;")

            act_lbl = QtWidgets.QLabel(action_text)
            act_lbl.setStyleSheet(f"color: {_TEXT_MID}; font-size: 11px;")

            time_lbl = QtWidgets.QLabel(time_text)
            time_lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 10px;")
            time_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)

            row_hl.addWidget(dot)
            row_hl.addWidget(act_lbl)
            row_hl.addStretch()
            row_hl.addWidget(time_lbl)
            ca_vl.addLayout(row_hl)

        right_vl.addWidget(crit_card)
        right_vl.addStretch()

        right_scroll.setWidget(right_inner)

        right_panel_vl = QtWidgets.QVBoxLayout(right_panel)
        right_panel_vl.setContentsMargins(0, 0, 0, 0)
        right_panel_vl.addWidget(right_scroll)

        outer_hl.addWidget(right_panel)

    # ──────────────────────────────────────────────────────────────────────────
    # TABLE POPULATION
    # ──────────────────────────────────────────────────────────────────────────
    def _populate_table(self, logs: list = None):
        data = logs if logs is not None else self._logs
        self.table.setRowCount(0)

        for row_idx, log in enumerate(data):
            log_id, ts, user_name, role, action, table_aff, rec_id, ip, details = log
            self.table.insertRow(row_idx)
            self.table.setRowHeight(row_idx, 56)

            # Col 0 — checkbox
            chk = QtWidgets.QCheckBox()
            chk_w = QtWidgets.QWidget()
            chk_hl = QtWidgets.QHBoxLayout(chk_w)
            chk_hl.addWidget(chk)
            chk_hl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            chk_hl.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row_idx, 0, chk_w)

            # Col 1 — Log ID
            self._set_item(row_idx, 1, log_id)

            # Col 2 — Timestamp
            self._set_item(row_idx, 2, ts)

            # Col 3 — User  (name + role stacked)
            user_w = QtWidgets.QWidget()
            user_vl = QtWidgets.QVBoxLayout(user_w)
            user_vl.setContentsMargins(6, 4, 6, 4)
            user_vl.setSpacing(1)
            n_lbl = QtWidgets.QLabel(user_name)
            n_lbl.setStyleSheet(f"""
                color: {_TEXT_DARK};
                font-size: 12px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial, sans-serif;
            """)
            r_lbl = QtWidgets.QLabel(role)
            r_lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 10px;")
            user_vl.addWidget(n_lbl)
            user_vl.addWidget(r_lbl)
            self.table.setCellWidget(row_idx, 3, user_w)

            # Col 4 — Action badge
            fg, bg = ACTION_COLOURS.get(action, (_TEXT_MID, "#f3f4f6"))
            badge = _Badge(action, fg, bg)
            badge_w = self._centre_widget(badge)
            self.table.setCellWidget(row_idx, 4, badge_w)

            # Col 5 — Table Affected
            self._set_item(row_idx, 5, table_aff)

            # Col 6 — Record ID
            self._set_item(row_idx, 6, rec_id)

            # Col 7 — IP Address
            self._set_item(row_idx, 7, ip)

            # Col 8 — Details + more button
            det_w = QtWidgets.QWidget()
            det_hl = QtWidgets.QHBoxLayout(det_w)
            det_hl.setContentsMargins(6, 0, 6, 0)
            det_hl.setSpacing(6)

            det_lbl = QtWidgets.QLabel(details)
            det_lbl.setStyleSheet(f"color: {_TEXT_MID}; font-size: 11px;")
            det_lbl.setWordWrap(True)

            more_btn = QtWidgets.QPushButton("⋮")
            more_btn.setFixedSize(24, 24)
            more_btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
            more_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    color: {_TEXT_GREY};
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #f3f4f6;
                    border-radius: 4px;
                }}
            """)
            more_btn.clicked.connect(
                lambda _, r=row_idx, b=more_btn: self._on_row_more(r, b))

            det_hl.addWidget(det_lbl, stretch=1)
            det_hl.addWidget(more_btn)
            self.table.setCellWidget(row_idx, 8, det_w)

    def _set_item(self, row: int, col: int, text: str):
        item = QtWidgets.QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, col, item)

    @staticmethod
    def _centre_widget(widget: QtWidgets.QWidget) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        hl = QtWidgets.QHBoxLayout(w)
        hl.addWidget(widget)
        hl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        hl.setContentsMargins(8, 0, 0, 0)
        return w

    # ──────────────────────────────────────────────────────────────────────────
    # FILTER HELPERS
    # ──────────────────────────────────────────────────────────────────────────
    def _combo_with_label(self, label: str, items: list) -> QtWidgets.QVBoxLayout:
        vl = QtWidgets.QVBoxLayout()
        vl.setSpacing(2)
        lbl = QtWidgets.QLabel(label)
        lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 10px; font-weight: 600;")
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        combo.setFixedHeight(32)
        combo.setMinimumWidth(110)
        combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {_BORDER};
                border-radius: 5px;
                padding: 0px 8px;
                font-size: 11px;
                color: {_TEXT_MID};
                background-color: {_WHITE};
            }}
            QComboBox:focus {{ border: 1.5px solid {_ACCENT}; }}
            QComboBox::drop-down {{ border: none; width: 18px; }}
        """)
        combo.currentIndexChanged.connect(self._on_filter)
        # Store reference so we can read value later
        combo.setObjectName(f"combo_{label.replace(' ','_')}")
        vl.addWidget(lbl)
        vl.addWidget(combo)
        # Keep a reference on self so _on_filter can read it
        attr = f"_{label.lower().replace(' ','_')}_combo"
        setattr(self, attr, combo)
        return vl

    def _date_widget(self, label: str, default: str) -> QtWidgets.QVBoxLayout:
        vl = QtWidgets.QVBoxLayout()
        vl.setSpacing(2)
        lbl = QtWidgets.QLabel(label)
        lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 10px; font-weight: 600;")
        de = QtWidgets.QDateEdit()
        de.setDisplayFormat("dd/MM/yyyy")
        de.setCalendarPopup(True)
        de.setFixedHeight(32)
        de.setMinimumWidth(105)
        d, m, y = default.split("/")
        de.setDate(QtCore.QDate(int(y), int(m), int(d)))
        de.setStyleSheet(f"""
            QDateEdit {{
                border: 1px solid {_BORDER};
                border-radius: 5px;
                padding: 0px 8px;
                font-size: 11px;
                color: {_TEXT_MID};
                background-color: {_WHITE};
            }}
            QDateEdit:focus {{ border: 1.5px solid {_ACCENT}; }}
            QDateEdit::drop-down {{ border: none; width: 18px; }}
        """)
        de.dateChanged.connect(self._on_filter)
        vl.addWidget(lbl)
        vl.addWidget(de)
        attr = f"_{label.lower().replace(' ','_')}_date"
        setattr(self, attr, de)
        return vl

    # ──────────────────────────────────────────────────────────────────────────
    # SLOTS
    # ──────────────────────────────────────────────────────────────────────────
    def _on_filter(self):
        text        = self.search_edit.text().lower()
        action_f    = self._action_type_combo.currentText()
        user_f      = self._user_combo.currentText()
        table_f     = self._table_affected_combo.currentText()

        results = []
        for log in self._logs:
            log_id, ts, user_name, role, action, table_aff, rec_id, ip, details = log

            if action_f  != "All Actions"  and action    != action_f:  continue
            if user_f    != "All Users"    and user_name != user_f:    continue
            if table_f   != "All Tables"   and table_aff != table_f:   continue
            if text and not any(text in v.lower() for v in
                                (log_id, user_name, action, table_aff, details)):
                continue
            results.append(log)

        self._populate_table(results)
        count = len(results)
        self.showing_lbl.setText(
            f"Showing 1 to {min(10, count)} of {count:,} logs"
        )

    def _on_reset(self):
        self.search_edit.clear()
        self._action_type_combo.setCurrentIndex(0)
        self._user_combo.setCurrentIndex(0)
        self._table_affected_combo.setCurrentIndex(0)
        self._date_from_date.setDate(QtCore.QDate(2025, 6, 1))
        self._date_to_date.setDate(QtCore.QDate(2025, 7, 1))
        self._populate_table()
        self.showing_lbl.setText("Showing 1 to 10 of 12,458 logs")

    def _on_export(self):
        QtWidgets.QMessageBox.information(
            self, "Export",
            "Export functionality will be connected to the database in the next sprint."
        )

    def _on_actions(self):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet(self._menu_style())
        menu.addAction("📥  Export CSV")
        menu.addAction("📋  Export PDF")
        menu.addSeparator()
        menu.addAction("🗑  Clear Selected Logs")
        menu.addAction("🔒  Archive Logs")
        pos = self.actions_btn.mapToGlobal(
            QtCore.QPoint(0, self.actions_btn.height()))
        menu.exec(pos)

    def _on_row_more(self, row: int, btn: QtWidgets.QPushButton):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet(self._menu_style())
        menu.addAction("👁  View Full Details")
        menu.addAction("📋  Copy Log Entry")
        menu.addSeparator()
        menu.addAction("🚩  Flag as Critical")
        menu.addAction("🗑  Delete Entry")
        pos = btn.mapToGlobal(QtCore.QPoint(0, btn.height()))
        menu.exec(pos)

    # ──────────────────────────────────────────────────────────────────────────
    # STYLE HELPERS
    # ──────────────────────────────────────────────────────────────────────────
    @staticmethod
    def _card_frame() -> QtWidgets.QFrame:
        f = QtWidgets.QFrame()
        f.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        f.setStyleSheet(f"""
            QFrame {{
                background-color: {_WHITE};
                border: 1px solid {_BORDER};
                border-radius: 10px;
            }}
        """)
        return f

    @staticmethod
    def _outline_btn(text: str) -> QtWidgets.QPushButton:
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(36)
        btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {_WHITE};
                color: {_TEXT_MID};
                border: 1px solid {_BORDER};
                border-radius: 6px;
                padding: 0px 16px;
                font-size: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QPushButton:hover {{ background-color: #f9fafb; }}
        """)
        return btn

    @staticmethod
    def _small_btn(text: str) -> QtWidgets.QPushButton:
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(30)
        btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {_WHITE};
                color: {_TEXT_MID};
                border: 1px solid {_BORDER};
                border-radius: 5px;
                padding: 0px 12px;
                font-size: 11px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QPushButton:hover {{ background-color: #f9fafb; }}
        """)
        return btn

    @staticmethod
    def _input_style() -> str:
        return f"""
            QLineEdit {{
                border: 1px solid {_BORDER};
                border-radius: 6px;
                padding: 0px 14px;
                font-size: 12px;
                color: {_TEXT_MID};
                background-color: {_WHITE};
            }}
            QLineEdit:focus {{ border: 1.5px solid {_ACCENT}; }}
        """

    @staticmethod
    def _menu_style() -> str:
        return f"""
            QMenu {{
                background-color: {_WHITE};
                border: 1px solid {_BORDER};
                border-radius: 6px;
                padding: 4px 0;
                font-size: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QMenu::item {{ color: {_TEXT_MID}; padding: 8px 20px; }}
            QMenu::item:selected {{ background-color: #eff6ff; color: {_NAVY}; }}
            QMenu::separator {{ height: 1px; background: {_BORDER}; margin: 4px 0; }}
        """