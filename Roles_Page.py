from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPainter, QBrush, QColor, QFont

# ── Shared colour palette (matches Users_Page.py and CEO_Page.py) ───────────────
_NAVY       = "#0d1b3e"
_BLUE_ACT   = "#1e3a6e"
_ACCENT     = "#5870ff"
_BG         = "#f0f2f5"
_WHITE      = "#ffffff"
_BORDER     = "#e5e7eb"
_TEXT_DARK  = "#1a1a2e"
_TEXT_GREY  = "#6b7280"
_TEXT_MID   = "#374151"

# ── Role status badge colours ─────────────────────────────────────────────────
STATUS_COLOURS: dict[str, tuple[str, str]] = {
    "Active":   ("#15803d", "#dcfce7"),
    "Inactive": ("#b91c1c", "#fee2e2"),
}

# ── Master Permissions Map ───────────────────────────────────────────────────
ROLE_PERMISSIONS = {
    "SYS_ADMIN": [
        "access_control_full", "system_read", "system_write", "system_edit_config",
        "users_add", "users_edit", "users_delete", "roles_add", "roles_edit", 
        "roles_delete", "roles_map_permissions", "audit_logs_view", "audit_logs_export"
    ],
    "CEO": [
        "dashboard_read", "executive_approve", "reports_read", "reports_export",
        "users_view", "departments_view", "audit_logs_view"
    ],
    "GM": [
        "management_oversight", "tasks_approve", "tasks_modify", "reports_view",
        "reports_export", "users_read", "users_write", "departments_view"
    ],
    "COO": [
        "operations_read", "operations_write", "tasks_manage", "reports_view",
        "departments_view", "users_view"
    ],
    "OPS_MGR": [
        "operations_read", "operations_write", "tasks_manage", "departments_view"
    ],
    "IT_MGR": [
        "system_read", "system_write", "users_edit", "audit_logs_view"
    ],
    "MKT_OFF": [
        "marketing_view", "marketing_edit", "campaigns_manage"
    ],
    "DEPT_HEAD": [
        "departments_view", "departments_edit", "tasks_create", "tasks_assign",
        "tasks_track", "meetings_schedule", "meetings_close"
    ],
    "FIN_OFF": [
        "finance_view", "finance_edit", "reports_view"
    ],
    "SUPPORT": [
        "users_view", "tasks_view", "announcements_view"
    ]
}

# ── Helper to map role code to classification category ────────────────────────
def get_category(code: str) -> str:
    code = code.upper()
    if "SYS" in code or "ADMIN" in code:
        return "System Admin"
    elif code in ["CEO", "COO", "EXEC"]:
        return "Executive"
    elif "MGR" in code or "HEAD" in code or "DIR" in code or code == "GM":
        return "Management"
    elif "OFF" in code or "FIN" in code or "MKT" in code or "HR" in code:
        return "Departmental"
    else:
        return "Support"

# ── Initial roles list ────────────────────────────────────────────────────────
SAMPLE_ROLES = [
    ("1", "System Administrator", "SYS_ADMIN", "Full system access and control", "1", "Active", "12 Jan 2024 08:30 AM", "System Admin", "10 Jul 2026 10:15 AM"),
    ("2", "Chief Executive Officer", "CEO", "Executive access to all modules", "1", "Active", "12 Jan 2024 08:45 AM", "System Admin", "10 Jul 2026 09:20 AM"),
    ("3", "General Manager", "GM", "Manage all operations and departments", "2", "Active", "12 Jan 2024 09:15 AM", "System Admin", "10 May 2025 02:40 PM"),
    ("4", "Administrator / COO", "COO", "Administrative and operational control", "3", "Active", "13 Jan 2024 10:00 AM", "System Admin", "14 Feb 2025 11:30 AM"),
    ("5", "Operations Manager", "OPS_MGR", "Manage operations and daily activities", "8", "Active", "15 Jan 2024 11:10 AM", "System Admin", "29 Jun 2025 04:12 PM"),
    ("6", "IT Manager", "IT_MGR", "Manage IT systems and infrastructure", "5", "Active", "16 Jan 2024 02:30 PM", "System Admin", "30 Jun 2025 09:47 AM"),
    ("7", "Marketing Officer", "MKT_OFF", "Manage marketing and communications", "4", "Active", "18 Jan 2024 09:15 AM", "System Admin", "30 Jun 2025 03:21 PM"),
    ("8", "Department Head", "DEPT_HEAD", "Manage department activities", "18", "Active", "20 Jan 2024 10:45 AM", "System Admin", "01 Jul 2025 08:05 AM"),
    ("9", "Finance Officer", "FIN_OFF", "Manage financial operations", "3", "Active", "22 Jan 2024 11:30 AM", "System Admin", "01 Jul 2025 08:32 AM"),
    ("10", "Support Staff", "SUPPORT", "Basic system access for support tasks", "103", "Inactive", "25 Jan 2024 09:00 AM", "System Admin", "05 Mar 2026 03:50 PM"),
]

# ==============================================================================
# CUSTOM FILTER PROXY MODEL (Allows combined Search AND Status Filtering)
# ==============================================================================
class RolesFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_text = ""
        self.status_filter = ""

    def setSearchText(self, text: str):
        self.search_text = text.lower().strip()
        self.invalidateFilter()  # Triggers dynamic filtering update

    def setStatusFilter(self, status: str):
        self.status_filter = status.lower().strip()
        self.invalidateFilter()  # Triggers dynamic filtering update

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        
        # 1. Filter by Status
        if self.status_filter:
            status_idx = model.index(source_row, 5, source_parent)
            status_val = str(model.data(status_idx) or "").lower().strip()
            if status_val != self.status_filter:
                return False
                
        # 2. Filter by Search Text (checks Name, Code, Description)
        if self.search_text:
            name_idx = model.index(source_row, 1, source_parent)
            code_idx = model.index(source_row, 2, source_parent)
            desc_idx = model.index(source_row, 3, source_parent)
            
            name_val = str(model.data(name_idx) or "").lower()
            code_val = str(model.data(code_idx) or "").lower()
            desc_val = str(model.data(desc_idx) or "").lower()
            
            if (self.search_text not in name_val and 
                self.search_text not in code_val and 
                self.search_text not in desc_val):
                return False
                
        return True

# ==============================================================================
# BADGE  helper widget
# ==============================================================================
class _Badge(QtWidgets.QLabel):
    """A pill-shaped coloured label for statuses."""
    def __init__(self, text: str, fg: str, bg: str, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(22)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.setStyleSheet(f"""
            QLabel {{
                color: {fg};
                background-color: {bg};
                border-radius: 10px;
                padding: 0px 10px;
                font-size: 11px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)

# ==============================================================================
# STAT CARD
# ==============================================================================
class _StatCard(QtWidgets.QFrame):
    def __init__(self, icon: str, label: str, value: str, sublabel: str,
                 icon_bg: str = "#eff6ff", icon_fg: str = "#3b82f6", parent=None):
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
        hl.setContentsMargins(18, 14, 18, 14)
        hl.setSpacing(14)

        icon_lbl = QtWidgets.QLabel(icon)
        icon_lbl.setFixedSize(42, 42)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"""
            QLabel {{
                background-color: {icon_bg};
                border-radius: 21px;
                font-size: 18px;
            }}
        """)

        vl = QtWidgets.QVBoxLayout()
        vl.setSpacing(2)

        lbl_top = QtWidgets.QLabel(label)
        lbl_top.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px; font-weight: bold;")

        self.lbl_val = QtWidgets.QLabel(value)
        self.lbl_val.setStyleSheet(f"""
            color: {_TEXT_DARK};
            font-size: 26px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        self.lbl_sub = QtWidgets.QLabel(sublabel)
        self.lbl_sub.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")

        vl.addWidget(lbl_top)
        vl.addWidget(self.lbl_val)
        vl.addWidget(self.lbl_sub)

        hl.addWidget(icon_lbl)
        hl.addLayout(vl)
        hl.addStretch()

    def set_value(self, val_str: str):
        self.lbl_val.setText(val_str)

    def set_sublabel(self, sub_str: str):
        self.lbl_sub.setText(sub_str)

# ==============================================================================
# DONUT CHART  (using QPainter)
# ==============================================================================
class _DonutChart(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(180, 180)
        self.data = []

    def set_data(self, data: list[tuple[str, int, str]]):
        self.data = data
        self.update()  # Repaint chart

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        size = min(rect.width(), rect.height()) - 20
        square = QtCore.QRect((rect.width() - size) // 2, (rect.height() - size) // 2, size, size)

        total = sum(val for _, val, _ in self.data)
        if total == 0:
            painter.setBrush(QBrush(QColor("#eff6ff")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(square)
            
            center_size = int(size * 0.65)
            center_square = QtCore.QRect((rect.width() - center_size) // 2, (rect.height() - center_size) // 2, center_size, center_size)
            painter.setBrush(QBrush(QColor(_WHITE)))
            painter.drawEllipse(center_square)
            
            painter.setPen(QColor(_TEXT_GREY))
            font = painter.font()
            font.setPointSize(10)
            font.setBold(False)
            painter.setFont(font)
            painter.drawText(center_square, Qt.AlignmentFlag.AlignCenter, "No Roles")
            return

        start_angle = 90 * 16  # 12 o'clock
        for label, val, color in self.data:
            if val == 0:
                continue
            span = int((val / total) * 360 * 16)
            painter.setBrush(QBrush(QColor(color)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(square, start_angle, -span)
            start_angle -= span

        # Center hole
        center_size = int(size * 0.65)
        center_square = QtCore.QRect(
            (rect.width() - center_size) // 2,
            (rect.height() - center_size) // 2,
            center_size,
            center_size
        )
        painter.setBrush(QBrush(QColor(_WHITE)))
        painter.drawEllipse(center_square)

        # Labels in center
        painter.setPen(QColor(_TEXT_DARK))
        font = painter.font()
        font.setPointSize(16)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(center_square, Qt.AlignmentFlag.AlignCenter, f"\n{total}")

        font.setPointSize(9)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(center_square, Qt.AlignmentFlag.AlignCenter, "Total Roles\n\n")

# ==============================================================================
# PROGRESS BAR  for top role usage
# ==============================================================================
class _UsageBar(QtWidgets.QWidget):
    def __init__(self, role_name: str, current_users: int, max_users: int, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(10)

        self.name_lbl = QtWidgets.QLabel(role_name)
        self.name_lbl.setMinimumWidth(120)
        self.name_lbl.setStyleSheet(f"color: {_TEXT_MID}; font-size: 12px; font-weight: 500;")

        self.pbar = QtWidgets.QProgressBar()
        self.pbar.setMaximum(max_users)
        self.pbar.setValue(current_users)
        self.pbar.setTextVisible(False)
        self.pbar.setFixedHeight(8)
        self.pbar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: #eff6ff;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {_ACCENT};
                border-radius: 4px;
            }}
        """)

        self.val_lbl = QtWidgets.QLabel(f"{current_users} users")
        self.val_lbl.setMinimumWidth(60)
        self.val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.val_lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")

        layout.addWidget(self.name_lbl)
        layout.addWidget(self.pbar)
        layout.addWidget(self.val_lbl)

# ==============================================================================
# ADD / EDIT ROLE DIALOG
# ==============================================================================
class AddRoleDialog(QtWidgets.QDialog):
    role_saved = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None, role_data: dict = None):
        super().__init__(parent)
        self._edit_mode = role_data is not None
        self.setWindowTitle("Edit Role" if self._edit_mode else "Add New Role")
        self.setModal(True)
        self.setFixedSize(480, 420)
        self.setStyleSheet(f"""
            QDialog {{ background-color: {_WHITE}; font-family: 'Segoe UI', Arial, sans-serif; }}
            QLabel {{ color: {_TEXT_MID}; font-size: 12px; font-weight: 600; }}
            QLineEdit, QTextEdit, QComboBox {{
                border: 1px solid {_BORDER};
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                color: {_TEXT_DARK}; /* Explicit text color */
                background-color: #f9fafb;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 1.5px solid {_ACCENT};
                background-color: {_WHITE};
                color: {_TEXT_DARK};
            }}
            /* Explicitly style list items in QComboBox dropdown to prevent white-on-white text */
            QComboBox QAbstractItemView {{
                background-color: #ffffff;
                color: {_TEXT_DARK};
                selection-background-color: #eff6ff;
                selection-color: {_BLUE_ACT};
                border: 1px solid {_BORDER};
            }}
            QPushButton {{
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
                padding: 8px 18px;
            }}
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Title
        title_lbl = QtWidgets.QLabel("Edit Role Details" if self._edit_mode else "Create New Role")
        title_lbl.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {_TEXT_DARK};")
        layout.addWidget(title_lbl)

        # Form Fields
        layout.addWidget(QtWidgets.QLabel("Role Name"))
        self.name_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.name_edit)

        layout.addWidget(QtWidgets.QLabel("Role Code (e.g. DEPT_HEAD)"))
        self.code_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.code_edit)

        layout.addWidget(QtWidgets.QLabel("Description"))
        self.desc_edit = QtWidgets.QTextEdit()
        self.desc_edit.setMaximumHeight(80)
        layout.addWidget(self.desc_edit)

        layout.addWidget(QtWidgets.QLabel("Status"))
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(["Active", "Inactive"])
        layout.addWidget(self.status_combo)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()

        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; color: {_TEXT_MID};")
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QtWidgets.QPushButton("Save Role")
        self.save_btn.setStyleSheet(f"background-color: {_ACCENT}; color: {_WHITE}; border: none;")
        self.save_btn.clicked.connect(self._on_save)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

        # Fill if editing
        if self._edit_mode:
            self.name_edit.setText(role_data.get("name", ""))
            self.code_edit.setText(role_data.get("code", ""))
            self.desc_edit.setPlainText(role_data.get("desc", ""))
            self.status_combo.setCurrentText(role_data.get("status", "Active"))

    def _on_save(self):
        if not self.name_edit.text().strip() or not self.code_edit.text().strip():
            self._show_info("Validation Error", "Name and Code fields are required.")
            return

        data = {
            "name": self.name_edit.text().strip(),
            "code": self.code_edit.text().strip().upper(),
            "desc": self.desc_edit.toPlainText().strip(),
            "status": self.status_combo.currentText()
        }
        self.role_saved.emit(data)
        self.accept()

    def _show_info(self, title: str, text: str):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg_box.setStyleSheet(f"""
            QMessageBox {{ background-color: #ffffff; }}
            QLabel {{ color: {_TEXT_DARK}; font-size: 13px; font-family: 'Segoe UI', Arial, sans-serif; }}
            QPushButton {{
                background-color: {_ACCENT};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                min-width: 60px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {_BLUE_ACT}; }}
        """)
        msg_box.exec()

# ==============================================================================
# ROLES PAGE MAIN CONTAINER
# ==============================================================================
class RolesPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Roles_Page")
        self.setStyleSheet(f"background-color: {_BG}; font-family: 'Segoe UI', Arial, sans-serif;")

        self._roles: list[tuple] = list(SAMPLE_ROLES)
        
        # ── Scroll Area setup ─────────────────────────────────────────────────
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_content.setStyleSheet(f"background-color: {_BG};")
        
        # Setup static layouts
        self._build_ui(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
        
        # ── Setup persistent data models ──────────────────────────────────────
        headers = ["#", "Role Name", "Role Code", "Description", "Users", "Status", "Actions"]
        self.model = QStandardItemModel(0, len(headers), self)
        for col_idx, header in enumerate(headers):
            self.model.setHorizontalHeaderItem(col_idx, QStandardItem(header))

        self.proxy_model = RolesFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        
        self.table_view.setModel(self.proxy_model)
        
        # Apply standard width definitions once
        self.table_view.setColumnWidth(0, 40)
        self.table_view.setColumnWidth(1, 160)
        self.table_view.setColumnWidth(2, 100)
        self.table_view.setColumnWidth(3, 240)
        self.table_view.setColumnWidth(4, 60)
        self.table_view.setColumnWidth(5, 80)
        self.table_view.setColumnWidth(6, 110)

        # Bind event triggers
        self.table_view.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self.table_view.horizontalHeader().sectionClicked.connect(self._update_badges_and_actions)
        
        self._populate_table()

        # Select General Manager (index 2 in the roles list) by default on startup
        if self.proxy_model.rowCount() > 2:
            self.table_view.selectRow(2)
        elif self.proxy_model.rowCount() > 0:
            self.table_view.selectRow(0)

    def _build_ui(self, container_widget):
        root = QtWidgets.QVBoxLayout(container_widget)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        # ── Page Header Row ───────────────────────────────────────────────────
        hdr_hl = QtWidgets.QHBoxLayout()
        hdr_hl.setSpacing(14)

        icon_lbl = QtWidgets.QLabel("🔑")
        icon_lbl.setFixedSize(44, 44)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"background-color: #eff0ff; border-radius: 22px; font-size: 20px;")

        title_vl = QtWidgets.QVBoxLayout()
        title_vl.setSpacing(2)
        pg_title = QtWidgets.QLabel("Roles Management")
        pg_title.setStyleSheet(f"color: {_TEXT_DARK}; font-size: 20px; font-weight: bold;")
        pg_sub = QtWidgets.QLabel("Create, manage and assign permissions to system roles.")
        pg_sub.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 12px;")
        title_vl.addWidget(pg_title)
        title_vl.addWidget(pg_sub)

        hdr_hl.addWidget(icon_lbl)
        hdr_hl.addLayout(title_vl)
        hdr_hl.addStretch()

        # Breadcrumbs
        bread_lbl = QtWidgets.QLabel("Dashboard  >  Roles")
        bread_lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 12px; font-weight: 500;")
        hdr_hl.addWidget(bread_lbl)

        root.addLayout(hdr_hl)

        # ── Stat Cards Row ────────────────────────────────────────────────────
        cards_hl = QtWidgets.QHBoxLayout()
        cards_hl.setSpacing(14)

        self.card_total       = _StatCard("🛡️", "Total Roles", "0", "All roles in system", "#eff0ff", "#3b82f6")
        self.card_active      = _StatCard("✅", "Active Roles", "0", "Currently active", "#e6f9f0", "#10b981")
        self.card_inactive    = _StatCard("⏸️", "Inactive Roles", "0", "Currently inactive", "#fffbeb", "#f59e0b")
        self.card_users       = _StatCard("👥", "Users Assigned", "0", "Across all roles", "#faf5ff", "#8b5cf6")
        self.card_permissions = _StatCard("🔑", "Permissions", "0", "Total permissions", "#f0fdfa", "#0d9488")

        for card in (self.card_total, self.card_active, self.card_inactive, self.card_users, self.card_permissions):
            cards_hl.addWidget(card)

        root.addLayout(cards_hl)

        # ── Mid Split Pane: Roles List Table & Role Details card ──────────────
        mid_hl = QtWidgets.QHBoxLayout()
        mid_hl.setSpacing(16)

        # Left panel: Roles List
        self.list_panel = QtWidgets.QFrame()
        self.list_panel.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; border-radius: 10px;")
        list_vl = QtWidgets.QVBoxLayout(self.list_panel)
        list_vl.setContentsMargins(18, 16, 18, 16)
        list_vl.setSpacing(12)

        # Table Header Row: Search + filter + export + add
        tbl_hdr_hl = QtWidgets.QHBoxLayout()
        tbl_hdr_hl.setSpacing(10)

        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("🔍  Search roles...")
        self.search_edit.setFixedHeight(36)
        self.search_edit.setMinimumWidth(240)
        self.search_edit.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {_BORDER};
                border-radius: 6px;
                padding: 0px 12px;
                font-size: 12px;
                color: {_TEXT_MID};
                background-color: {_WHITE};
            }}
            QLineEdit:focus {{ border: 1.5px solid {_ACCENT}; }}
        """)
        self.search_edit.textChanged.connect(self._on_search)

        self.filter_btn = QtWidgets.QPushButton("Filter  ▾")
        self.filter_btn.setFixedHeight(36)
        self.filter_btn.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; border-radius: 6px; padding: 0 14px; font-size: 12px; font-weight: 600; color: {_TEXT_MID};")
        self.filter_btn.clicked.connect(self._on_filter_clicked)

        self.export_btn = QtWidgets.QPushButton("Export")
        self.export_btn.setFixedHeight(36)
        self.export_btn.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; border-radius: 6px; padding: 0 14px; font-size: 12px; font-weight: 600; color: {_TEXT_MID};")
        self.export_btn.clicked.connect(self._on_export_clicked)

        self.add_btn = QtWidgets.QPushButton("＋ Add Role")
        self.add_btn.setFixedHeight(36)
        self.add_btn.setStyleSheet(f"background-color: {_ACCENT}; border: none; border-radius: 6px; padding: 0 16px; font-size: 12px; font-weight: 600; color: {_WHITE};")
        self.add_btn.clicked.connect(self._on_add_role)

        tbl_hdr_hl.addWidget(self.search_edit)
        tbl_hdr_hl.addWidget(self.filter_btn)
        tbl_hdr_hl.addWidget(self.export_btn)
        tbl_hdr_hl.addStretch()
        tbl_hdr_hl.addWidget(self.add_btn)
        list_vl.addLayout(tbl_hdr_hl)

        # Table view with Locked Minimum Height to prevent layout shifting
        self.table_view = QtWidgets.QTableView()
        self.table_view.setShowGrid(False)
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setHighlightSections(False)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setMinimumHeight(420)  # Visual locked geometry
        self.table_view.setStyleSheet(f"""
            QTableView {{
                background-color: {_WHITE};
                alternate-background-color: #f9fafb;
                color: {_TEXT_MID}; /* Explicit dark text color overrides global parent styles */
                border: none;
                gridline-color: transparent;
                selection-background-color: #eff6ff;
                selection-color: {_TEXT_DARK};
            }}
            QHeaderView::section {{
                background-color: #f9fafb;
                color: {_TEXT_GREY};
                padding: 10px;
                border: none;
                border-bottom: 1.5px solid {_BORDER};
                font-weight: bold;
                font-size: 11px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        """)

        list_vl.addWidget(self.table_view)

        # Footer Row (Pagination)
        pag_hl = QtWidgets.QHBoxLayout()
        self.pag_lbl = QtWidgets.QLabel("Showing 1 to 10 of 10 roles")
        self.pag_lbl.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        pag_hl.addWidget(self.pag_lbl)
        pag_hl.addStretch()

        self.prev_btn = QtWidgets.QPushButton("<")
        self.prev_btn.setFixedSize(28, 28)
        self.prev_btn.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; border-radius: 4px; font-weight: bold;")
        self.page1_btn = QtWidgets.QPushButton("1")
        self.page1_btn.setFixedSize(28, 28)
        self.page1_btn.setStyleSheet(f"background-color: {_ACCENT}; color: {_WHITE}; border: none; border-radius: 4px; font-weight: bold;")
        self.next_btn = QtWidgets.QPushButton(">")
        self.next_btn.setFixedSize(28, 28)
        self.next_btn.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; border-radius: 4px; font-weight: bold;")

        pag_hl.addWidget(self.prev_btn)
        pag_hl.addWidget(self.page1_btn)
        pag_hl.addWidget(self.next_btn)
        list_vl.addLayout(pag_hl)

        mid_hl.addWidget(self.list_panel, stretch=7)

        # Right panel: Role Details
        self.details_panel = QtWidgets.QFrame()
        self.details_panel.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; border-radius: 10px;")
        det_vl = QtWidgets.QVBoxLayout(self.details_panel)
        det_vl.setContentsMargins(18, 16, 18, 16)
        det_vl.setSpacing(14)

        # Details Header
        det_lbl = QtWidgets.QLabel("Role Details")
        det_lbl.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {_TEXT_DARK};")
        det_vl.addWidget(det_lbl)

        # Large Badge Indicator
        self.det_icon_frame = QtWidgets.QFrame()
        self.det_icon_frame.setFixedSize(80, 80)
        self.det_icon_frame.setStyleSheet(f"background-color: #eff6ff; border-radius: 40px;")
        det_icon_layout = QtWidgets.QHBoxLayout(self.det_icon_frame)
        self.det_shield_lbl = QtWidgets.QLabel("🛡️")
        self.det_shield_lbl.setStyleSheet("font-size: 32px;")
        self.det_shield_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        det_icon_layout.addWidget(self.det_shield_lbl)

        det_center_hl = QtWidgets.QHBoxLayout()
        det_center_hl.addStretch()
        det_center_hl.addWidget(self.det_icon_frame)
        det_center_hl.addStretch()
        det_vl.addLayout(det_center_hl)

        # Name and Status Label
        self.det_name_lbl = QtWidgets.QLabel("Select a Role")
        self.det_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.det_name_lbl.setStyleSheet(f"color: {_TEXT_DARK}; font-size: 16px; font-weight: bold;")
        det_vl.addWidget(self.det_name_lbl)

        self.det_badge_layout = QtWidgets.QHBoxLayout()
        self.det_badge_layout.addStretch()
        self.det_status_badge = _Badge("Active", "#15803d", "#dcfce7")
        self.det_badge_layout.addWidget(self.det_status_badge)
        self.det_badge_layout.addStretch()
        det_vl.addLayout(self.det_badge_layout)

        det_vl.addSpacing(10)

        # Grid metadata fields
        self.fields_grid = QtWidgets.QGridLayout()
        self.fields_grid.setSpacing(12)

        self.lbl_code_title = QtWidgets.QLabel("Role Code")
        self.lbl_code_title.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        self.lbl_code_val = QtWidgets.QLabel("—")
        self.lbl_code_val.setStyleSheet(f"color: {_TEXT_DARK}; font-size: 12px; font-weight: 500;")

        self.lbl_desc_title = QtWidgets.QLabel("Description")
        self.lbl_desc_title.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        self.lbl_desc_val = QtWidgets.QLabel("—")
        self.lbl_desc_val.setWordWrap(True)
        self.lbl_desc_val.setStyleSheet(f"color: {_TEXT_DARK}; font-size: 12px; font-weight: 500;")

        self.lbl_users_title = QtWidgets.QLabel("Users Assigned")
        self.lbl_users_title.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        self.lbl_users_val = QtWidgets.QLabel("—")
        self.lbl_users_val.setStyleSheet(f"color: {_TEXT_DARK}; font-size: 12px; font-weight: 500;")

        self.lbl_created_title = QtWidgets.QLabel("Created On")
        self.lbl_created_title.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        self.lbl_created_val = QtWidgets.QLabel("—")
        self.lbl_created_val.setStyleSheet(f"color: {_TEXT_DARK}; font-size: 12px; font-weight: 500;")

        self.lbl_by_title = QtWidgets.QLabel("Created By")
        self.lbl_by_title.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        self.lbl_by_val = QtWidgets.QLabel("—")
        self.lbl_by_val.setStyleSheet(f"color: {_TEXT_DARK}; font-size: 12px; font-weight: 500;")

        self.lbl_updated_title = QtWidgets.QLabel("Last Updated")
        self.lbl_updated_title.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        self.lbl_updated_val = QtWidgets.QLabel("—")
        self.lbl_updated_val.setStyleSheet(f"color: {_TEXT_DARK}; font-size: 12px; font-weight: 500;")

        self.fields_grid.addWidget(self.lbl_code_title,    0, 0)
        self.fields_grid.addWidget(self.lbl_code_val,      0, 1)
        self.fields_grid.addWidget(self.lbl_desc_title,    1, 0)
        self.fields_grid.addWidget(self.lbl_desc_val,      1, 1)
        self.fields_grid.addWidget(self.lbl_users_title,   2, 0)
        self.fields_grid.addWidget(self.lbl_users_val,     2, 1)
        self.fields_grid.addWidget(self.lbl_created_title,  3, 0)
        self.fields_grid.addWidget(self.lbl_created_val,    3, 1)
        self.fields_grid.addWidget(self.lbl_by_title,       4, 0)
        self.fields_grid.addWidget(self.lbl_by_val,         4, 1)
        self.fields_grid.addWidget(self.lbl_updated_title,  5, 0)
        self.fields_grid.addWidget(self.lbl_updated_val,    5, 1)

        det_vl.addLayout(self.fields_grid)
        det_vl.addStretch()

        self.perm_btn = QtWidgets.QPushButton("View Role Permissions")
        self.perm_btn.setFixedHeight(36)
        self.perm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.perm_btn.setStyleSheet(f"background-color: {_BLUE_ACT}; color: {_WHITE}; border: none; border-radius: 6px; font-size: 12px; font-weight: 600;")
        self.perm_btn.clicked.connect(self._on_view_permissions_clicked)
        det_vl.addWidget(self.perm_btn)

        mid_hl.addWidget(self.details_panel, stretch=3)
        root.addLayout(mid_hl)

        # ── Bottom Analytics Cards Row ────────────────────────────────────────
        bot_hl = QtWidgets.QHBoxLayout()
        bot_hl.setSpacing(16)

        # Bottom Card 1: Roles Summary (Donut Chart)
        self.bot_card1 = QtWidgets.QFrame()
        self.bot_card1.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; border-radius: 10px;")
        bc1_vl = QtWidgets.QVBoxLayout(self.bot_card1)
        bc1_vl.setContentsMargins(18, 16, 18, 16)
        bc1_vl.setSpacing(8)

        bc1_title = QtWidgets.QLabel("Roles Summary")
        bc1_title.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {_TEXT_DARK};")
        bc1_sub = QtWidgets.QLabel("Overview of role distribution and usage.")
        bc1_sub.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        bc1_vl.addWidget(bc1_title)
        bc1_vl.addWidget(bc1_sub)

        # Donut chart
        chart_hl = QtWidgets.QHBoxLayout()
        self.donut_chart = _DonutChart()
        chart_hl.addWidget(self.donut_chart)
        
        # Donut Chart Legend layout
        self.legend_vl = QtWidgets.QVBoxLayout()
        self.legend_vl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.legend_vl.setSpacing(4)
        chart_hl.addLayout(self.legend_vl)

        bc1_vl.addLayout(chart_hl)
        bot_hl.addWidget(self.bot_card1, stretch=4)

        # Bottom Card 2: Recently Added Roles
        self.bot_card2 = QtWidgets.QFrame()
        self.bot_card2.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; border-radius: 10px;")
        bc2_vl = QtWidgets.QVBoxLayout(self.bot_card2)
        bc2_vl.setContentsMargins(18, 16, 18, 16)
        bc2_vl.setSpacing(8)

        bc2_title = QtWidgets.QLabel("Recently Added Roles")
        bc2_title.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {_TEXT_DARK};")
        bc2_sub = QtWidgets.QLabel("Latest roles added to the system.")
        bc2_sub.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        bc2_vl.addWidget(bc2_title)
        bc2_vl.addWidget(bc2_sub)
        bc2_vl.addSpacing(4)

        # Container for dynamic recent roles with Locked Height
        self.recent_container = QtWidgets.QWidget()
        self.recent_container.setMinimumHeight(140)
        self.recent_layout = QtWidgets.QVBoxLayout(self.recent_container)
        self.recent_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_layout.setSpacing(8)
        bc2_vl.addWidget(self.recent_container)

        bot_hl.addWidget(self.bot_card2, stretch=3)

        # Bottom Card 3: Role Usage (Top 5)
        self.bot_card3 = QtWidgets.QFrame()
        self.bot_card3.setStyleSheet(f"background-color: {_WHITE}; border: 1px solid {_BORDER}; border-radius: 10px;")
        bc3_vl = QtWidgets.QVBoxLayout(self.bot_card3)
        bc3_vl.setContentsMargins(18, 16, 18, 16)
        bc3_vl.setSpacing(8)

        bc3_title = QtWidgets.QLabel("Role Usage (Top 5)")
        bc3_title.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {_TEXT_DARK};")
        bc3_sub = QtWidgets.QLabel("Most assigned roles in the system.")
        bc3_sub.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
        bc3_vl.addWidget(bc3_title)
        bc3_vl.addWidget(bc3_sub)
        bc3_vl.addSpacing(4)

        # Container for dynamic usage progress bars with Locked Height
        self.usage_container = QtWidgets.QWidget()
        self.usage_container.setMinimumHeight(180)
        self.usage_layout = QtWidgets.QVBoxLayout(self.usage_container)
        self.usage_layout.setContentsMargins(0, 0, 0, 0)
        self.usage_layout.setSpacing(8)
        bc3_vl.addWidget(self.usage_container)

        bot_hl.addWidget(self.bot_card3, stretch=3)
        root.addLayout(bot_hl)

    # ──────────────────────────────────────────────────────────────────────────
    # SMOOTH TABLE ROW DATA RE-POPULATION (Retains Scroll and View State)
    # ──────────────────────────────────────────────────────────────────────────
    def _populate_table(self):
        # 1. Temporarily disconnect selection changed handler to prevent unwanted fires
        try:
            self.table_view.selectionModel().selectionChanged.disconnect(self._on_selection_changed)
        except Exception:
            pass

        # 2. Clear old items smoothly without resetting model pointer
        self.model.removeRows(0, self.model.rowCount())

        # 3. Populate rows in existing model
        for row_idx, row_data in enumerate(self._roles):
            self.model.insertRow(row_idx)
            for col, val in enumerate(row_data[:6]):
                item = QStandardItem(val)
                item.setForeground(QtGui.QBrush(QtGui.QColor(_TEXT_MID)))
                self.model.setItem(row_idx, col, item)
            self.model.setItem(row_idx, 6, QStandardItem(""))

        # 4. Reconnect selection changed trigger
        self.table_view.selectionModel().selectionChanged.connect(self._on_selection_changed)

        # 5. Refresh custom badges, action layouts, and metrics panel
        self._update_badges_and_actions()
        self._update_statistics()

    def _update_badges_and_actions(self):
        for row in range(self.proxy_model.rowCount()):
            status_idx = self.proxy_model.index(row, 5)
            action_idx = self.proxy_model.index(row, 6)

            status_text = self.proxy_model.data(status_idx)
            fg, bg = STATUS_COLOURS.get(status_text, ("#374151", "#f3f4f6"))

            # Set badge in status column
            badge = _Badge(status_text, fg, bg)
            self.table_view.setIndexWidget(status_idx, badge)

            # Set custom actions wrapper widget
            actions_widget = QtWidgets.QWidget()
            actions_hl = QtWidgets.QHBoxLayout(actions_widget)
            actions_hl.setContentsMargins(4, 0, 4, 0)
            actions_hl.setSpacing(4)

            # View Btn
            view_btn = QtWidgets.QPushButton("👁")
            view_btn.setFixedSize(24, 24)
            view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            view_btn.setStyleSheet(f"background-color: #eff6ff; color: {_ACCENT}; border: 1px solid {_BORDER}; border-radius: 4px; font-weight: bold; font-size: 12px;")
            view_btn.clicked.connect(lambda checked=False, r=row: self._on_view_action(r))

            # Edit Btn
            edit_btn = QtWidgets.QPushButton("✏️")
            edit_btn.setFixedSize(24, 24)
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.setStyleSheet(f"background-color: #fef3c7; color: #d97706; border: 1px solid {_BORDER}; border-radius: 4px; font-weight: bold; font-size: 11px;")
            edit_btn.clicked.connect(lambda checked=False, r=row: self._on_edit_action(r))

            # Delete Btn
            del_btn = QtWidgets.QPushButton("🗑️")
            del_btn.setFixedSize(24, 24)
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.setStyleSheet(f"background-color: #fee2e2; color: #ef4444; border: 1px solid {_BORDER}; border-radius: 4px; font-weight: bold; font-size: 11px;")
            del_btn.clicked.connect(lambda checked=False, r=row: self._on_delete_action(r))

            actions_hl.addWidget(view_btn)
            actions_hl.addWidget(edit_btn)
            actions_hl.addWidget(del_btn)
            self.table_view.setIndexWidget(action_idx, actions_widget)

    # ──────────────────────────────────────────────────────────────────────────
    # DYNAMIC CALCULATIONS & METRICS UPDATES
    # ──────────────────────────────────────────────────────────────────────────
    def _update_statistics(self):
        if not hasattr(self, "_roles"):
            return

        total_roles = len(self._roles)
        active_roles = sum(1 for r in self._roles if r[5] == "Active")
        inactive_roles = sum(1 for r in self._roles if r[5] == "Inactive")
        users_assigned = sum(int(r[4]) for r in self._roles)

        # Dynamic Permissions calculation based on current roles
        total_permissions = sum(len(ROLE_PERMISSIONS.get(r[2], ["perm_read", "perm_view", "perm_edit"])) for r in self._roles)

        # Update stats cards
        self.card_total.set_value(str(total_roles))
        self.card_active.set_value(str(active_roles))
        self.card_inactive.set_value(str(inactive_roles))
        self.card_users.set_value(str(users_assigned))
        self.card_permissions.set_value(str(total_permissions))

        # Update donut chart data
        categories = {
            "System Admin": 0,
            "Executive": 0,
            "Management": 0,
            "Departmental": 0,
            "Support": 0
        }
        for r in self._roles:
            cat = get_category(r[2])
            categories[cat] = categories.get(cat, 0) + 1

        donut_data = [
            ("System Admin", categories["System Admin"], "#3b4fd8"),
            ("Executive", categories["Executive"], "#10b981"),
            ("Management", categories["Management"], "#f59e0b"),
            ("Departmental", categories["Departmental"], "#8b5cf6"),
            ("Support", categories["Support"], "#ef4444")
        ]
        self.donut_chart.set_data(donut_data)

        # Rebuild donut legend
        for i in reversed(range(self.legend_vl.count())):
            w = self.legend_vl.itemAt(i).widget()
            if w is not None:
                w.deleteLater()
        for name, count, color in donut_data:
            lbl = QtWidgets.QLabel(f"● {name} ({count})")
            lbl.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")
            self.legend_vl.addWidget(lbl)

        # Rebuild Top 5 usages
        for i in reversed(range(self.usage_layout.count())):
            w = self.usage_layout.itemAt(i).widget()
            if w is not None:
                w.deleteLater()

        sorted_by_users = sorted(self._roles, key=lambda x: int(x[4]), reverse=True)
        max_users = max(int(x[4]) for x in self._roles) if self._roles else 100
        if max_users == 0:
            max_users = 100

        for r in sorted_by_users[:5]:
            self.usage_layout.addWidget(_UsageBar(r[1], int(r[4]), max_users))

        # Rebuild recently added roles (last 3 items)
        for i in reversed(range(self.recent_layout.count())):
            w = self.recent_layout.itemAt(i).widget()
            if w is not None:
                w.deleteLater()

        category_colors = {
            "System Admin": ("#e0f2fe", "#0284c7"),
            "Executive": ("#dcfce7", "#15803d"),
            "Management": ("#f3e8ff", "#7e22ce"),
            "Departmental": ("#fef3c7", "#d97706"),
            "Support": ("#fee2e2", "#ef4444")
        }

        recent_list = self._roles[-3:]
        recent_list.reverse()

        for r in recent_list:
            name = r[1]
            created_on = r[6]
            cat = get_category(r[2])
            bg, fg = category_colors.get(cat, ("#f3f4f6", "#374151"))

            item = QtWidgets.QWidget()
            item_hl = QtWidgets.QHBoxLayout(item)
            item_hl.setContentsMargins(0, 4, 0, 4)
            item_hl.setSpacing(10)

            badge = QtWidgets.QLabel(name[0])
            badge.setFixedSize(28, 28)
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setStyleSheet(f"background-color: {bg}; color: {fg}; border-radius: 14px; font-weight: bold; font-size: 12px;")

            item_text_vl = QtWidgets.QVBoxLayout()
            item_text_vl.setSpacing(1)
            item_title = QtWidgets.QLabel(name)
            item_title.setStyleSheet(f"color: {_TEXT_DARK}; font-size: 12px; font-weight: 600;")
            item_desc = QtWidgets.QLabel(f"Added on {created_on}")
            item_desc.setStyleSheet(f"color: {_TEXT_GREY}; font-size: 11px;")
            item_text_vl.addWidget(item_title)
            item_text_vl.addWidget(item_desc)

            item_hl.addWidget(badge)
            item_hl.addLayout(item_text_vl)
            item_hl.addStretch()
            self.recent_layout.addWidget(item)

        # Update pagination display text
        self.pag_lbl.setText(f"Showing 1 to {self.proxy_model.rowCount()} of {self.proxy_model.rowCount()} roles")

    # ──────────────────────────────────────────────────────────────────────────
    # SYSTEM DIALOG STYLING HELPERS (Ensures visibility & consistent colors)
    # ──────────────────────────────────────────────────────────────────────────
    def _show_info(self, title: str, text: str):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: #ffffff;
            }}
            QLabel {{
                color: {_TEXT_DARK};
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QPushButton {{
                background-color: {_ACCENT};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                min-width: 60px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {_BLUE_ACT};
            }}
        """)
        msg_box.exec()

    def _show_question(self, title: str, text: str) -> bool:
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: #ffffff;
            }}
            QLabel {{
                color: {_TEXT_DARK};
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QPushButton {{
                background-color: {_ACCENT};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                min-width: 60px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {_BLUE_ACT};
            }}
        """)
        reply = msg_box.exec()
        return reply == QtWidgets.QMessageBox.StandardButton.Yes

    # ──────────────────────────────────────────────────────────────────────────
    # INTERACTIONS AND BINDINGS
    # ──────────────────────────────────────────────────────────────────────────
    def _on_selection_changed(self, selected, deselected):
        indexes = self.table_view.selectionModel().selectedRows()
        if not indexes:
            return
        
        row_idx = indexes[0].row()
        self._update_details_panel(row_idx)

    def _update_details_panel(self, row_idx: int):
        source_idx = self.proxy_model.mapToSource(self.proxy_model.index(row_idx, 0))
        if not source_idx.isValid():
            return
        
        source_row = source_idx.row()
        role = self._roles[source_row]

        self.det_name_lbl.setText(role[1])
        
        status = role[5]
        fg, bg = STATUS_COLOURS.get(status, ("#374151", "#f3f4f6"))
        self.det_status_badge.setText(status)
        self.det_status_badge.setStyleSheet(f"""
            QLabel {{
                color: {fg};
                background-color: {bg};
                border-radius: 10px;
                padding: 0px 10px;
                font-size: 11px;
                font-weight: 600;
            }}
        """)

        self.lbl_code_val.setText(role[2])
        self.lbl_desc_val.setText(role[3])
        self.lbl_users_val.setText(role[4])
        self.lbl_created_val.setText(role[6])
        self.lbl_by_val.setText(role[7])
        self.lbl_updated_val.setText(role[8])

    def _on_search(self, text: str):
        self.proxy_model.setSearchText(text)
        self._update_badges_and_actions()
        if self.proxy_model.rowCount() > 0:
            self.table_view.selectRow(0)

    def _on_add_role(self):
        dialog = AddRoleDialog(self)
        dialog.role_saved.connect(self._add_role_to_list)
        dialog.exec()

    def _add_role_to_list(self, data: dict):
        new_id = str(len(self._roles) + 1)
        new_role = (
            new_id,
            data["name"],
            data["code"],
            data["desc"],
            "0",  # default to 0 users
            data["status"],
            QtCore.QDateTime.currentDateTime().toString("dd MMM yyyy hh:mm AP"),
            "System Admin",
            QtCore.QDateTime.currentDateTime().toString("dd MMM yyyy hh:mm AP")
        )
        self._roles.append(new_role)
        
        # Insert row directly to source model
        row_idx = self.model.rowCount()
        self.model.insertRow(row_idx)
        for col, val in enumerate(new_role[:6]):
            item = QStandardItem(val)
            item.setForeground(QtGui.QBrush(QtGui.QColor(_TEXT_MID)))
            self.model.setItem(row_idx, col, item)
        self.model.setItem(row_idx, 6, QStandardItem(""))
        
        self._update_badges_and_actions()
        self._update_statistics()
        
        # Select newly added row
        last_row = self.proxy_model.rowCount() - 1
        self.table_view.selectRow(last_row)
        self._show_info("Success", f"Role '{data['name']}' added successfully!")

    def _on_view_action(self, row_idx: int):
        source_row = self.proxy_model.mapToSource(self.proxy_model.index(row_idx, 0)).row()
        role = self._roles[source_row]
        msg = f"Role Details:\n\nName: {role[1]}\nCode: {role[2]}\nDescription: {role[3]}\nUsers Assigned: {role[4]}\nStatus: {role[5]}\nCreated: {role[6]} by {role[7]}"
        self._show_info("Role Info", msg)

    def _on_edit_action(self, row_idx: int):
        source_row = self.proxy_model.mapToSource(self.proxy_model.index(row_idx, 0)).row()
        role = self._roles[source_row]
        role_dict = {
            "name": role[1],
            "code": role[2],
            "desc": role[3],
            "status": role[5]
        }
        dialog = AddRoleDialog(self, role_dict)
        dialog.role_saved.connect(lambda data: self._save_edited_role(source_row, data))
        dialog.exec()

    def _save_edited_role(self, source_row: int, data: dict):
        orig = self._roles[source_row]
        updated = (
            orig[0],
            data["name"],
            data["code"],
            data["desc"],
            orig[4],  # users count remains
            data["status"],
            orig[6],  # created date remains
            orig[7],  # created by remains
            QtCore.QDateTime.currentDateTime().toString("dd MMM yyyy hh:mm AP")
        )
        self._roles[source_row] = updated
        
        # Update source model row directly
        for col, val in enumerate(updated[:6]):
            item = self.model.item(source_row, col)
            if item:
                item.setText(val)
            else:
                item = QStandardItem(val)
                item.setForeground(QtGui.QBrush(QtGui.QColor(_TEXT_MID)))
                self.model.setItem(source_row, col, item)
                
        self._update_badges_and_actions()
        self._update_statistics()
        
        # Maintain selection
        proxy_idx = self.proxy_model.mapFromSource(self.model.index(source_row, 0))
        if proxy_idx.isValid():
            self.table_view.selectRow(proxy_idx.row())
        self._show_info("Success", "Role details updated successfully!")

    def _on_delete_action(self, row_idx: int):
        source_idx = self.proxy_model.mapToSource(self.proxy_model.index(row_idx, 0))
        if not source_idx.isValid():
            return
        source_row = source_idx.row()
        role = self._roles[source_row]
        
        confirmed = self._show_question(
            "Delete Role",
            f"Are you sure you want to delete the role '{role[1]}'? This action cannot be undone."
        )
        if confirmed:
            # Clear selection to avoid index changed trigger during removal
            self.table_view.clearSelection()
            
            self._roles.pop(source_row)
            self.model.removeRow(source_row)
            
            self._update_badges_and_actions()
            self._update_statistics()
            
            # Select first row if exists
            if self.proxy_model.rowCount() > 0:
                self.table_view.selectRow(0)
                
            self._show_info("Success", "Role deleted successfully!")

    def _on_filter_clicked(self):
        # Present status filter options as context menu
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #ffffff; border: 1px solid #e0e4ec; border-radius: 6px; padding: 4px; }
            QMenu::item { padding: 6px 20px; color: #374151; font-size: 12px; }
            QMenu::item:selected { background-color: #eff6ff; color: #1e3a6e; }
        """)
        
        act_active = menu.addAction("Show Active Only")
        act_inactive = menu.addAction("Show Inactive Only")
        act_all = menu.addAction("Show All Roles")
        
        act_active.triggered.connect(lambda: self._apply_status_filter("Active"))
        act_inactive.triggered.connect(lambda: self._apply_status_filter("Inactive"))
        act_all.triggered.connect(lambda: self._apply_status_filter(""))
        
        menu.exec(self.filter_btn.mapToGlobal(QtCore.QPoint(0, self.filter_btn.height())))

    def _apply_status_filter(self, status: str):
        self.proxy_model.setStatusFilter(status)
        self._update_badges_and_actions()
        if self.proxy_model.rowCount() > 0:
            self.table_view.selectRow(0)

    def _on_export_clicked(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Roles Data", "", "CSV Files (*.csv)"
        )
        if path:
            try:
                import csv
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Role Name", "Role Code", "Description", "Users Count", "Status", "Created On", "Created By", "Last Updated"])
                    for role in self._roles:
                        writer.writerow(role)
                self._show_info("Success", "Roles data exported successfully!")
            except Exception as e:
                msg_box = QtWidgets.QMessageBox(self)
                msg_box.setWindowTitle("Error")
                msg_box.setText(f"Failed to export data: {str(e)}")
                msg_box.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                msg_box.setStyleSheet(f"""
                    QMessageBox {{ background-color: #ffffff; }}
                    QLabel {{ color: {_TEXT_DARK}; font-size: 13px; }}
                    QPushButton {{ background-color: #ef4444; color: #ffffff; border: none; border-radius: 6px; padding: 6px 16px; min-width: 60px; font-weight: bold; }}
                """)
                msg_box.exec()

    def _on_view_permissions_clicked(self):
        indexes = self.table_view.selectionModel().selectedRows()
        if not indexes:
            return
        row_idx = indexes[0].row()
        source_row = self.proxy_model.mapToSource(self.proxy_model.index(row_idx, 0)).row()
        role = self._roles[source_row]
        
        # Mock permissions depending on the role code
        code = role[2]
        perms = []
        if "ADMIN" in code:
            perms = [
                "Access Control: Full permissions (SYS_ADMIN)",
                "System: Read, Write, Edit Configs",
                "Users: Add, Edit, Delete User Accounts",
                "Roles: Add, Edit, Delete Roles & Map Permissions",
                "Audit Logs: View & Export log reports"
            ]
        elif code == "CEO":
            perms = [
                "Dashboard: Read-only visual overview",
                "Executive: Approve organizational decisions",
                "Reports: Read-only access & Export reports",
                "Users: View accounts & assignments"
            ]
        elif code == "GM":
            perms = [
                "Management: Direct operational oversight",
                "Decisions: Approve & modify task lists",
                "Reports: View and export stats graphs",
                "Users: Read & Write user settings"
            ]
        elif "MGR" in code or "HEAD" in code:
            perms = [
                "Department: View and edit departmental profiles",
                "Tasks: Create, assign and track member tickets",
                "Meetings: Schedule and close meeting updates"
            ]
        else:
            perms = [
                "Users: View profile info only",
                "Tasks: View self-assigned workflows",
                "Announcements: View notices"
            ]
            
        perms_str = "\n".join(f"● {p}" for p in perms)
        self._show_info(
            "Role Permissions List", 
            f"Active permissions listed for the role '{role[1]}':\n\n{perms_str}\n\n(Note: Logic to dynamically assign permissions is not yet initialized.)"
        )
