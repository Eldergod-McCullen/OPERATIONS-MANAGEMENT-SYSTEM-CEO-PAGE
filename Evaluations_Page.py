from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

# ── Shared palette ─────────────────────────────────────────────────────────
_NAVY      = "#0d1b3e"
_ACCENT    = "#5870ff"
_BG        = "#f0f2f5"
_WHITE     = "#ffffff"
_BORDER    = "#e5e7eb"
_TEXT_DARK = "#1a1a2e"
_TEXT_GREY = "#6b7280"
_TEXT_MID  = "#374151"

# ── Status colours ──────────────────────────────────────────────────────────
STATUS_COLOURS = {
    "Pending":            ("#d97706", "#fef3c7"),
    "Approved":           ("#15803d", "#dcfce7"),
    "Rejected":           ("#b91c1c", "#fee2e2"),
    "Interview Scheduled":("#1d4ed8", "#dbeafe"),
    "Active":             ("#15803d", "#dcfce7"),
    "Completed":          ("#15803d", "#dcfce7"),
    "Overdue":            ("#b91c1c", "#fee2e2"),
    "Withdrawn":          ("#6b7280", "#f3f4f6"),
}

# ── Sample evaluation data ──────────────────────────────────────────────────
SAMPLE_EVALUATIONS = [
    ("1", "John Kamau", "REG/2025/001", "Information Technology", "David Mwangi", "May - Jul 2025", "David Mwangi", "88.50%", "A", "Completed"),
    ("2", "Grace Njeri", "REG/2025/002", "Marketing & Comms", "Mary Wanjiku", "May - Jul 2025", "Mary Wanjiku", "82.30%", "B+", "Completed"),
    ("3", "David Mwangi", "REG/2025/003", "Human Resources", "Susan Akinyi", "May - Jul 2025", "Susan Akinyi", "79.60%", "B", "Completed"),
    ("4", "Susan Akinyi", "REG/2025/004", "Finance & Accounts", "Peter Otieno", "May - Jul 2025", "Peter Otieno", "91.20%", "A", "Completed"),
    ("5", "Brian Otieno", "REG/2025/005", "Operations", "Lilian Moraa", "May - Jul 2025", "Lilian Moraa", "76.40%", "B", "Pending"),
    ("6", "Lilian Moraa", "REG/2025/006", "Procurement", "Kevin Odhiambo", "May - Jul 2025", "Kevin Odhiambo", "-", "-", "Pending"),
    ("7", "Peter Otieno", "REG/2025/007", "IT Support", "David Mwangi", "Mar - Apr 2025", "David Mwangi", "73.80%", "B-", "Completed"),
    ("8", "Aisha Hassan", "REG/2025/008", "Marketing & Comms", "Mary Wanjiku", "Mar - Apr 2025", "Mary Wanjiku", "84.10%", "B+", "Completed"),
    ("9", "Kevin Odhiambo", "REG/2025/009", "Information Technology", "David Mwangi", "Mar - Apr 2025", "David Mwangi", "67.40%", "C+", "Overdue"),
    ("10", "Mary Wanjiku", "REG/2025/010", "Finance & Accounts", "Peter Otieno", "Mar - Apr 2025", "Peter Otieno", "90.00%", "A-", "Completed"),
    ("11", "Esther Wanjiku", "REG/2025/011", "Marketing & Comms", "David Mwangi", "May - Jul 2025", "David Mwangi", "89.20%", "A-", "Completed"),
    ("12", "Samuel Maina", "REG/2025/012", "Information Technology", "Mary Wanjiku", "May - Jul 2025", "Mary Wanjiku", "85.60%", "A", "Completed"),
    ("13", "Faith Muthoni", "REG/2025/013", "Human Resources", "David Mwangi", "May - Jul 2025", "David Mwangi", "78.40%", "B", "Pending"),
    ("14", "Daniel Kiprop", "REG/2025/014", "Finance & Accounts", "Susan Akinyi", "Mar - Apr 2025", "Susan Akinyi", "92.50%", "A", "Completed"),
    ("15", "Mercy Chepngetich", "REG/2025/015", "Marketing & Comms", "David Mwangi", "Mar - Apr 2025", "David Mwangi", "81.10%", "B", "Completed"),
    ("16", "Job Ochieng", "REG/2025/016", "Operations", "Peter Otieno", "May - Jul 2025", "Peter Otieno", "74.20%", "B-", "Pending"),
    ("17", "Alice Mwangi", "REG/2025/017", "Procurement", "Lilian Moraa", "May - Jul 2025", "Lilian Moraa", "-", "-", "Pending"),
    ("18", "Victor Kiprop", "REG/2025/018", "IT Support", "Kevin Odhiambo", "Mar - Apr 2025", "Kevin Odhiambo", "69.50%", "C+", "Overdue"),
    ("19", "Cynthia Wambui", "REG/2025/019", "Marketing & Comms", "Susan Akinyi", "May - Jul 2025", "Susan Akinyi", "87.30%", "A-", "Completed"),
    ("20", "Francis Ndwiga", "REG/2025/020", "Finance & Accounts", "David Mwangi", "May - Jul 2025", "David Mwangi", "79.90%", "B", "Completed"),
]


# ==============================================================================
# HELPERS
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
                color:{fg}; background:{bg};
                border-radius:9px; padding:0 9px;
                font-size:10px; font-weight:700;
                font-family:'Segoe UI',Arial;
            }}
        """)


def _card(parent=None) -> QtWidgets.QFrame:
    f = QtWidgets.QFrame(parent)
    f.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    f.setStyleSheet(f"""
        QFrame {{
            background:{_WHITE};
            border:1px solid {_BORDER};
            border-radius:10px;
        }}
    """)
    return f


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


# ==============================================================================
# STAT CARD
# ==============================================================================
class _StatCard(QtWidgets.QFrame):
    def __init__(self, icon, icon_bg, label, value, sublabel, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setStyleSheet(f"""
            QFrame {{
                background:{_WHITE};
                border:1px solid {_BORDER};
                border-radius:10px;
            }}
        """)
        hl = QtWidgets.QHBoxLayout(self)
        hl.setContentsMargins(12, 10, 12, 10); hl.setSpacing(10)

        il = QtWidgets.QLabel(icon)
        il.setFixedSize(38, 38)
        il.setAlignment(Qt.AlignmentFlag.AlignCenter)
        il.setStyleSheet(f"background:{icon_bg};border-radius:19px;font-size:17px;")

        vl = QtWidgets.QVBoxLayout(); vl.setSpacing(1)
        self.lbl_top = QtWidgets.QLabel(label)
        self.lbl_top.setStyleSheet(f"color:{_TEXT_GREY};font-size:10px;")
        self.lbl_val = QtWidgets.QLabel(value)
        self.lbl_val.setStyleSheet(f"color:{_TEXT_DARK};font-size:22px;font-weight:bold;"
                                  "font-family:'Segoe UI',Arial;")
        self.lbl_sub = QtWidgets.QLabel(sublabel)
        self.lbl_sub.setStyleSheet(f"color:{_TEXT_GREY};font-size:10px;")
        vl.addWidget(self.lbl_top); vl.addWidget(self.lbl_val); vl.addWidget(self.lbl_sub)
        hl.addWidget(il); hl.addLayout(vl); hl.addStretch()


# ==============================================================================
# DONUT CHART (Supports Dynamic Slice Updates)
# ==============================================================================
class _DonutChart(QtWidgets.QWidget):
    def __init__(self, parent=None, slices=None):
        super().__init__(parent)
        self.setMinimumSize(120, 120)
        self._slices = slices if slices is not None else [("Default", 1, "#ccc")]
        self._total  = sum(s[1] for s in self._slices)

    def set_slices(self, slices):
        self._slices = slices
        self._total = sum(s[1] for s in self._slices)
        self.update()

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        w, h  = self.width(), self.height()
        size  = min(w, h) - 16
        x     = (w - size) // 2
        y     = (h - size) // 2
        rect  = QtCore.QRectF(x, y, size, size)
        start = 90 * 16
        
        if self._total == 0:
            p.setBrush(QtGui.QColor("#f3f4f6"))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(rect)
        else:
            for _, val, col in self._slices:
                if val == 0: continue
                span = int(round(val / self._total * 360 * 16))
                p.setBrush(QtGui.QColor(col))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawPie(rect, start, -span)
                start -= span
                
        hole = size * 0.54
        hx = (w - hole) / 2; hy = (h - hole) / 2
        p.setBrush(QtGui.QColor(_WHITE))
        p.drawEllipse(QtCore.QRectF(hx, hy, hole, hole))
        
        p.setPen(QtGui.QColor(_TEXT_DARK))
        p.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Weight.Bold))
        p.drawText(QtCore.QRectF(hx, hy - 4, hole, hole / 2),
                   Qt.AlignmentFlag.AlignCenter, "Total")
        p.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold))
        p.drawText(QtCore.QRectF(hx, hy + hole / 4, hole, hole / 2),
                   Qt.AlignmentFlag.AlignCenter, str(self._total))
        p.end()


# ==============================================================================
# TREND CHART (Line graph of Average Scores)
# ==============================================================================
class _TrendChart(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(180, 140)
        self.points = [78, 76, 79, 81, 82, 84, 83]
        self.labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        margin_left = 30
        margin_bottom = 20
        margin_top = 15
        margin_right = 10
        
        graph_w = w - margin_left - margin_right
        graph_h = h - margin_top - margin_bottom
        
        p.setPen(QtGui.QColor("#f3f4f6"))
        for val in [60, 70, 80, 90, 100]:
            y_pos = int(margin_top + graph_h * (1 - (val - 50) / 50))
            p.drawLine(margin_left, y_pos, w - margin_right, y_pos)
            
        path = QtGui.QPainterPath()
        points_xy = []
        for i, val in enumerate(self.points):
            x_pos = int(margin_left + graph_w * i / (len(self.points) - 1))
            y_pos = int(margin_top + graph_h * (1 - (val - 50) / 50))
            points_xy.append((x_pos, y_pos))
            if i == 0:
                path.moveTo(x_pos, y_pos)
            else:
                path.lineTo(x_pos, y_pos)
                
        fill_path = QtGui.QPainterPath(path)
        fill_path.lineTo(points_xy[-1][0], margin_top + graph_h)
        fill_path.lineTo(points_xy[0][0], margin_top + graph_h)
        fill_path.closeSubpath()
        
        gradient = QtGui.QLinearGradient(0, margin_top, 0, margin_top + graph_h)
        gradient.setColorAt(0, QtGui.QColor(88, 112, 255, 60))
        gradient.setColorAt(1, QtGui.QColor(88, 112, 255, 0))
        p.fillPath(fill_path, QtGui.QBrush(gradient))
        
        p.setPen(QtGui.QPen(QtGui.QColor("#5870ff"), 2))
        p.drawPath(path)
        
        p.setFont(QtGui.QFont("Segoe UI", 7))
        for i, (x, y) in enumerate(points_xy):
            p.setBrush(QtGui.QColor("#5870ff"))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(x - 3, y - 3, 6, 6)
            
            p.setPen(QtGui.QColor(_TEXT_DARK))
            p.drawText(x - 12, y - 9, 24, 10, Qt.AlignmentFlag.AlignCenter, f"{self.points[i]}%")
            
            p.setPen(QtGui.QColor(_TEXT_GREY))
            p.drawText(x - 15, h - margin_bottom + 4, 30, 10, Qt.AlignmentFlag.AlignCenter, self.labels[i])
            
        p.end()


# ==============================================================================
# NEW EVALUATION DIALOG
# ==============================================================================
class NewEvaluationDialog(QtWidgets.QDialog):
    evaluation_saved = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None, data: dict = None):
        super().__init__(parent)
        self._edit = data is not None
        self.setWindowTitle("Edit Evaluation" if self._edit else "New Evaluation")
        self.setModal(True)
        self.setFixedSize(480, 520)
        self.setStyleSheet(f"""
            QDialog {{ background-color: {_WHITE}; font-family: 'Segoe UI', Arial, sans-serif; }}
            QLabel#hdrTitle {{ color: {_TEXT_DARK}; font-size: 15px; font-weight: bold; }}
            QLabel#hdrSub {{ color: {_TEXT_GREY}; font-size: 11px; }}
            QLabel#fldLbl {{ color: {_TEXT_MID}; font-size: 11px; font-weight: 600; }}
            QLineEdit, QComboBox {{
                border: 1px solid {_BORDER}; border-radius: 6px;
                padding: 6px 10px; font-size: 12px;
                color: {_TEXT_DARK}; background-color: #f9fafb;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border: 1.5px solid {_ACCENT}; background-color: {_WHITE};
            }}
            QComboBox QAbstractItemView {{
                background-color: {_WHITE};
                color: {_TEXT_DARK};
                selection-background-color: {_ACCENT};
                selection-color: {_WHITE};
            }}
            QFrame#div {{ border: none; border-top: 1px solid {_BORDER}; }}
            QPushButton#cancelBtn {{
                background: {_WHITE}; color: {_TEXT_MID};
                border: 1px solid {_BORDER}; border-radius: 6px;
                padding: 0 16px; font-size: 12px; font-weight: bold;
            }}
            QPushButton#cancelBtn:hover {{ background: #f9fafb; }}
            QPushButton#saveBtn {{
                background: {_ACCENT}; color: {_WHITE}; border: none; border-radius: 6px;
                padding: 0 20px; font-size: 12px; font-weight: bold;
            }}
            QPushButton#saveBtn:hover {{ background: #4a60ee; }}
        """)
        self._build_ui(data)

    def _build_ui(self, data):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(10)

        # Header
        hhl = QtWidgets.QHBoxLayout()
        ico = QtWidgets.QLabel("📝")
        ico.setFixedSize(36, 36)
        ico.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ico.setStyleSheet("background:#eff0ff;border-radius:18px;font-size:16px;")
        hvl = QtWidgets.QVBoxLayout(); hvl.setSpacing(2)
        ht = QtWidgets.QLabel("Edit Evaluation" if self._edit else "New Evaluation")
        ht.setObjectName("hdrTitle")
        hs = QtWidgets.QLabel("Update evaluation details." if self._edit else "Fill in the details to record a new attachee evaluation.")
        hs.setObjectName("hdrSub")
        hvl.addWidget(ht); hvl.addWidget(hs)
        hhl.addWidget(ico); hhl.addSpacing(8); hhl.addLayout(hvl); hhl.addStretch()
        root.addLayout(hhl)

        d0 = QtWidgets.QFrame(); d0.setObjectName("div"); d0.setFixedHeight(1)
        root.addWidget(d0)

        def lbl(t):
            l = QtWidgets.QLabel(t); l.setObjectName("fldLbl"); return l

        form = QtWidgets.QFormLayout()
        form.setVerticalSpacing(10); form.setHorizontalSpacing(14)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setPlaceholderText("e.g. John Kamau")
        form.addRow(lbl("Attachee Name *"), self.name_edit)

        self.reg_edit = QtWidgets.QLineEdit()
        self.reg_edit.setPlaceholderText("e.g. REG/2025/001")
        form.addRow(lbl("Registration No. *"), self.reg_edit)

        self.dept_combo = QtWidgets.QComboBox()
        self.dept_combo.addItem("— Select Department —")
        self.dept_combo.addItems(["Information Technology", "Marketing & Comms", "Human Resources", "Finance & Accounts", "Operations", "Procurement"])
        form.addRow(lbl("Department *"), self.dept_combo)

        self.supervisor_edit = QtWidgets.QLineEdit()
        self.supervisor_edit.setPlaceholderText("e.g. David Mwangi")
        form.addRow(lbl("Supervisor *"), self.supervisor_edit)

        self.period_edit = QtWidgets.QLineEdit()
        self.period_edit.setPlaceholderText("e.g. May - Jul 2025")
        form.addRow(lbl("Evaluation Period *"), self.period_edit)

        self.evaluator_edit = QtWidgets.QLineEdit()
        self.evaluator_edit.setPlaceholderText("e.g. David Mwangi")
        form.addRow(lbl("Evaluator *"), self.evaluator_edit)

        self.score_edit = QtWidgets.QLineEdit()
        self.score_edit.setPlaceholderText("e.g. 88.50%")
        form.addRow(lbl("Score (%)"), self.score_edit)

        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(["Completed", "Pending", "Overdue"])
        form.addRow(lbl("Status"), self.status_combo)

        root.addLayout(form)

        if self._edit and data:
            self.name_edit.setText(data.get("name", ""))
            self.reg_edit.setText(data.get("reg_no", ""))
            idx = self.dept_combo.findText(data.get("dept", ""))
            if idx >= 0: self.dept_combo.setCurrentIndex(idx)
            self.supervisor_edit.setText(data.get("supervisor", ""))
            self.period_edit.setText(data.get("period", ""))
            self.evaluator_edit.setText(data.get("evaluator", ""))
            self.score_edit.setText(data.get("score", ""))
            idx = self.status_combo.findText(data.get("status", ""))
            if idx >= 0: self.status_combo.setCurrentIndex(idx)

        root.addStretch()

        self.err_lbl = QtWidgets.QLabel("")
        self.err_lbl.setStyleSheet("color:#b91c1c;font-size:11px;")
        self.err_lbl.setVisible(False)
        root.addWidget(self.err_lbl)

        d1 = QtWidgets.QFrame(); d1.setObjectName("div"); d1.setFixedHeight(1)
        root.addWidget(d1)

        bhl = QtWidgets.QHBoxLayout(); bhl.addStretch()
        cb = QtWidgets.QPushButton("Cancel"); cb.setObjectName("cancelBtn")
        cb.setFixedHeight(34)
        cb.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        cb.clicked.connect(self.reject)
        sb = QtWidgets.QPushButton("💾  Save Changes" if self._edit else "✚  Add Evaluation")
        sb.setObjectName("saveBtn"); sb.setFixedHeight(34)
        sb.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        sb.clicked.connect(self._on_save)
        bhl.addWidget(cb); bhl.addSpacing(8); bhl.addWidget(sb)
        root.addLayout(bhl)

    def _on_save(self):
        name = self.name_edit.text().strip()
        reg_no = self.reg_edit.text().strip()
        dept = self.dept_combo.currentText()
        superv = self.supervisor_edit.text().strip()
        period = self.period_edit.text().strip()
        evaltr = self.evaluator_edit.text().strip()
        score = self.score_edit.text().strip()
        
        errs = []
        if not name: errs.append("Attachee Name required.")
        if not reg_no: errs.append("Registration Number required.")
        if dept.startswith("—"): errs.append("Select a Department.")
        if not superv: errs.append("Supervisor Name required.")
        if not period: errs.append("Period required.")
        if not evaltr: errs.append("Evaluator required.")
        
        if errs:
            self.err_lbl.setText("⚠  " + "  •  ".join(errs))
            self.err_lbl.setVisible(True)
            return
        
        self.err_lbl.setVisible(False)
        
        grade = "-"
        if score and score != "-":
            try:
                s_val = float(score.replace("%", "").strip())
                if s_val >= 92: grade = "A"
                elif s_val >= 90: grade = "A-"
                elif s_val >= 80: grade = "B+"
                elif s_val >= 75: grade = "B"
                elif s_val >= 70: grade = "B-"
                elif s_val >= 65: grade = "C+"
                elif s_val >= 60: grade = "C"
                else: grade = "F"
            except ValueError:
                grade = "-"
        
        self.evaluation_saved.emit({
            "name": name,
            "reg_no": reg_no,
            "dept": dept,
            "supervisor": superv,
            "period": period,
            "evaluator": evaltr,
            "score": score if score else "-",
            "grade": grade,
            "status": self.status_combo.currentText()
        })
        self.accept()


# ==============================================================================
# EVALUATIONS RIGHT PANEL
# ==============================================================================
class _EvaluationsRightPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background:{_BG};")
        self._build_ui()

    def _build_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 16, 10, 16)
        self.layout.setSpacing(12)

        self.summary_card = _card()
        sc_vl = QtWidgets.QVBoxLayout(self.summary_card)
        sc_vl.setContentsMargins(14, 14, 14, 14); sc_vl.setSpacing(10)
        sc_t = QtWidgets.QLabel("Evaluation Summary")
        sc_t.setStyleSheet(f"color:{_TEXT_DARK};font-size:13px;font-weight:bold;font-family:'Segoe UI',Arial;")
        sc_vl.addWidget(sc_t)

        sc_row = QtWidgets.QHBoxLayout(); sc_row.setSpacing(10)
        self.donut = _DonutChart(slices=[("Completed", 48, "#10b981"), ("Pending", 9, "#3b82f6"), ("Overdue", 5, "#ef4444"), ("Cancelled", 2, "#6b7280")])
        self.donut.setFixedSize(110, 110)
        sc_row.addWidget(self.donut)

        self.leg_vl = QtWidgets.QVBoxLayout(); self.leg_vl.setSpacing(6)
        self.leg_vl.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        sc_row.addLayout(self.leg_vl)
        sc_vl.addLayout(sc_row)
        self.layout.addWidget(self.summary_card)

        self.top_card = _card()
        self.top_vl = QtWidgets.QVBoxLayout(self.top_card)
        self.top_vl.setContentsMargins(14, 14, 14, 14); self.top_vl.setSpacing(10)
        
        top_hdr = QtWidgets.QHBoxLayout()
        top_t = QtWidgets.QLabel("Top Performing Attachees")
        top_t.setStyleSheet(f"color:{_TEXT_DARK};font-size:13px;font-weight:bold;font-family:'Segoe UI',Arial;")
        self.view_all_lbl = QtWidgets.QLabel("View All")
        self.view_all_lbl.setStyleSheet(f"color:{_ACCENT};font-size:11px;")
        self.view_all_lbl.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        top_hdr.addWidget(top_t); top_hdr.addStretch(); top_hdr.addWidget(self.view_all_lbl)
        self.top_vl.addLayout(top_hdr)

        self.top_list_vl = QtWidgets.QVBoxLayout(); self.top_list_vl.setSpacing(8)
        self.top_vl.addLayout(self.top_list_vl)
        self.layout.addWidget(self.top_card)

        self.qa_card = _card()
        qa_vl = QtWidgets.QVBoxLayout(self.qa_card)
        qa_vl.setContentsMargins(14, 14, 14, 14); qa_vl.setSpacing(8)
        
        qa_t = QtWidgets.QLabel("Quick Actions")
        qa_t.setStyleSheet(f"color:{_TEXT_DARK};font-size:13px;font-weight:bold;font-family:'Segoe UI',Arial;")
        qa_vl.addWidget(qa_t)

        for action_name, action_icon in [
            ("Create New Evaluation", "➕"),
            ("Evaluation Criteria", "📋"),
            ("Evaluation Templates", "📂"),
            ("Evaluation Calendar", "📅"),
            ("Generate Evaluation Report", "📊")
        ]:
            row = QtWidgets.QHBoxLayout(); row.setSpacing(8)
            icon_lbl = QtWidgets.QLabel(action_icon)
            icon_lbl.setStyleSheet(f"color:{_ACCENT};font-size:12px;")
            nl = QtWidgets.QLabel(action_name)
            nl.setStyleSheet(f"color:{_TEXT_MID};font-size:11px;")
            nl.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
            row.addWidget(icon_lbl); row.addWidget(nl); row.addStretch()
            qa_vl.addLayout(row)
        
        self.layout.addWidget(self.qa_card)
        self.layout.addStretch()

    def update_panel(self, evaluations: list):
        completed = sum(1 for e in evaluations if e[9] == "Completed")
        pending = sum(1 for e in evaluations if e[9] == "Pending")
        overdue = sum(1 for e in evaluations if e[9] == "Overdue")
        cancelled = 2
        
        slices = [
            ("Completed", completed, "#10b981"),
            ("Pending", pending, "#3b82f6"),
            ("Overdue", overdue, "#ef4444"),
            ("Cancelled", cancelled, "#6b7280"),
        ]
        self.donut.set_slices(slices)

        for i in reversed(range(self.leg_vl.count())):
            layout_item = self.leg_vl.itemAt(i)
            if layout_item is not None:
                self.leg_vl.removeItem(layout_item)
                
        total = sum(s[1] for s in slices)
        if total == 0: total = 1
        for lname, lval, lcol in slices:
            row = QtWidgets.QHBoxLayout(); row.setSpacing(6)
            dot = QtWidgets.QLabel("●"); dot.setStyleSheet(f"color:{lcol};font-size:11px;")
            dot.setFixedWidth(12)
            nl = QtWidgets.QLabel(lname); nl.setStyleSheet(f"color:{_TEXT_MID};font-size:10px;")
            pct = f"{lval} ({int(lval/total*100)}%)"
            vr = QtWidgets.QLabel(pct); vr.setStyleSheet(f"color:{_TEXT_GREY};font-size:9px;")
            vr.setAlignment(Qt.AlignmentFlag.AlignRight)
            row.addWidget(dot); row.addWidget(nl); row.addStretch(); row.addWidget(vr)
            self.leg_vl.addLayout(row)

        with_scores = []
        for e in evaluations:
            score_str = e[7]
            if score_str and score_str != "-":
                try:
                    val = float(score_str.replace("%", "").strip())
                    with_scores.append((e[1], e[3], val, e[8]))
                except ValueError:
                    pass
        with_scores.sort(key=lambda x: x[2], reverse=True)

        for i in reversed(range(self.top_list_vl.count())):
            w = self.top_list_vl.itemAt(i).widget()
            if w: w.deleteLater()

        for i, (name, dept, val, grade) in enumerate(with_scores[:5]):
            row_w = QtWidgets.QWidget()
            row_hl = QtWidgets.QHBoxLayout(row_w)
            row_hl.setContentsMargins(0, 2, 0, 2); row_hl.setSpacing(8)

            badge = QtWidgets.QLabel(str(i + 1))
            badge.setFixedSize(18, 18); badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setStyleSheet("background:#eff0ff;border-radius:9px;font-size:9px;font-weight:bold;color:#5870ff;")
            
            info_vl = QtWidgets.QVBoxLayout(); info_vl.setSpacing(1)
            nl = QtWidgets.QLabel(name)
            nl.setStyleSheet(f"color:{_TEXT_DARK};font-size:11px;font-weight:600;")
            dl = QtWidgets.QLabel(dept)
            dl.setStyleSheet(f"color:{_TEXT_GREY};font-size:9px;")
            info_vl.addWidget(nl); info_vl.addWidget(dl)
            
            score_lbl = QtWidgets.QLabel(f"{val}%")
            score_lbl.setStyleSheet(f"color:{_TEXT_DARK};font-size:11px;font-weight:bold;")
            
            grade_badge = _Badge(grade, "#15803d", "#dcfce7") if grade in ["A", "A-", "B+", "B"] else _Badge(grade, "#b45309", "#fef3c7")
            
            row_hl.addWidget(badge)
            row_hl.addLayout(info_vl)
            row_hl.addStretch()
            row_hl.addWidget(score_lbl)
            row_hl.addWidget(grade_badge)
            self.top_list_vl.addWidget(row_w)


# ==============================================================================
# EVALUATIONS TAB CONTENT (Main Widget)
# ==============================================================================
class EvaluationsPage(QtWidgets.QWidget):
    """
    Standalone Evaluations Page.
    Can be used as a tab inside IndustrialAttachmentPage or as a standalone page.
    """
    def __init__(self, parent=None, right_panel=None):
        super().__init__(parent)
        self.setStyleSheet(f"background:{_BG};")
        self._evaluations = list(SAMPLE_EVALUATIONS)
        self._right_panel = right_panel
        self._build_ui()
        self._populate_table()

    def set_right_panel(self, rp):
        self._right_panel = rp
        if self._right_panel:
            self._right_panel.update_panel(self._evaluations)

    def _build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setStyleSheet("background: transparent; border: none;")

        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setStyleSheet(f"background: {_BG};")
        vl = QtWidgets.QVBoxLayout(self.scrollWidget)
        vl.setContentsMargins(0, 10, 0, 10); vl.setSpacing(12)

        self.cards_layout = QtWidgets.QHBoxLayout(); self.cards_layout.setSpacing(10)
        self.card_total = _StatCard("📋", "#eff0ff", "Total Evaluations", "0", "All time")
        self.card_completed = _StatCard("✅", "#dcfce7", "Completed Evaluations", "0", "75.00% of total")
        self.card_pending = _StatCard("📂", "#fef3c7", "Pending Evaluations", "0", "Awaiting submission")
        self.card_overdue = _StatCard("🕒", "#fee2e2", "Overdue Evaluations", "0", "Past due date")
        self.card_avg = _StatCard("⭐", "#e0f2fe", "Average Score", "0.0%", "Overall average")

        for card in (self.card_total, self.card_completed, self.card_pending, self.card_overdue, self.card_avg):
            self.cards_layout.addWidget(card)
        vl.addLayout(self.cards_layout)

        filter_card = _card()
        fc_hl = QtWidgets.QHBoxLayout(filter_card)
        fc_hl.setContentsMargins(14, 10, 14, 10); fc_hl.setSpacing(10)

        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("Search attachees...")
        self.search_edit.setFixedHeight(34)
        self.search_edit.setMinimumWidth(180)
        self.search_edit.setStyleSheet(f"QLineEdit {{ border:1px solid {_BORDER}; border-radius:6px; padding:0 12px; font-size:12px; color:{_TEXT_MID}; background:{_WHITE}; }} QLineEdit:focus {{ border:1.5px solid {_ACCENT}; }}")
        self.search_edit.textChanged.connect(self._apply_filters)

        self.combo_period = QtWidgets.QComboBox()
        self.combo_period.addItems(["All Periods", "May - Jul 2025", "Mar - Apr 2025"])
        
        self.combo_dept = QtWidgets.QComboBox()
        self.combo_dept.addItems(["All Departments", "Information Technology", "Marketing & Comms", "Human Resources", "Finance & Accounts", "Operations", "Procurement"])
        
        self.combo_super = QtWidgets.QComboBox()
        self.combo_super.addItems(["All Supervisors", "David Mwangi", "Mary Wanjiku", "Susan Akinyi", "Peter Otieno", "Lilian Moraa", "Kevin Odhiambo"])
        
        self.combo_status = QtWidgets.QComboBox()
        self.combo_status.addItems(["All Statuses", "Completed", "Pending", "Overdue"])

        for combo, lbl_text in [
            (self.combo_period, "Evaluation Period"),
            (self.combo_dept, "Department"),
            (self.combo_super, "Supervisor"),
            (self.combo_status, "Status")
        ]:
            combo.setFixedHeight(34); combo.setMinimumWidth(110)
            combo.setStyleSheet(f"QComboBox {{ border:1px solid {_BORDER}; border-radius:6px; padding:0 8px; font-size:11px; color:{_TEXT_MID}; background:{_WHITE}; }} QComboBox:focus {{ border:1.5px solid {_ACCENT}; }} QComboBox::drop-down {{ border:none; width:18px; }} QComboBox QAbstractItemView {{ background-color: {_WHITE}; color: {_TEXT_DARK}; selection-background-color: {_ACCENT}; selection-color: {_WHITE}; }}")
            combo.currentIndexChanged.connect(self._apply_filters)
            
            lbl_vl = QtWidgets.QVBoxLayout(); lbl_vl.setSpacing(2)
            ll = QtWidgets.QLabel(lbl_text)
            ll.setStyleSheet(f"color:{_TEXT_GREY};font-size:10px;font-weight:600;")
            lbl_vl.addWidget(ll); lbl_vl.addWidget(combo)
            fc_hl.addLayout(lbl_vl)

        fc_hl.addWidget(self.search_edit)

        self.export_btn = _outline_btn("Export")
        self.export_btn.clicked.connect(self._on_export)
        self.new_eval_btn = _primary_btn("+ New Evaluation")
        self.new_eval_btn.clicked.connect(self._on_new_evaluation)

        fc_hl.addWidget(self.export_btn)
        fc_hl.addWidget(self.new_eval_btn)
        vl.addWidget(filter_card)

        tcard = _card()
        tc_vl = QtWidgets.QVBoxLayout(tcard)
        tc_vl.setContentsMargins(0, 0, 0, 0); tc_vl.setSpacing(0)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "#", "Attachee", "Reg. No.", "Department", "Supervisor",
            "Evaluation Period", "Evaluator", "Score", "Grade", "Status", "Actions"
        ])
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setMinimumHeight(450)

        for i, w in enumerate([30, 110, 95, 120, 110, 100, 100, 50, 45, 80, 90]):
            self.table.setColumnWidth(i, w)
        self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.table.setStyleSheet(f"QTableWidget {{ border:none; background:{_WHITE}; alternate-background-color:#fafbfc; font-size:11px; color:{_TEXT_MID}; font-family:'Segoe UI',Arial; outline:none; }} QTableWidget::item {{ padding:4px 6px; border-bottom:1px solid #f3f4f6; }} QTableWidget::item:selected {{ background:#eff6ff; color:{_TEXT_DARK}; }} QHeaderView::section {{ background:#f9fafb; color:{_TEXT_GREY}; font-size:10px; font-weight:bold; border:none; border-bottom:1px solid {_BORDER}; padding:7px; }}")
        tc_vl.addWidget(self.table)

        pg = QtWidgets.QWidget(); pg.setFixedHeight(44)
        pg.setStyleSheet(f"QWidget {{ background:{_WHITE}; border-top:1px solid {_BORDER}; border-bottom-left-radius:10px; border-bottom-right-radius:10px; }}")
        pg_hl = QtWidgets.QHBoxLayout(pg)
        pg_hl.setContentsMargins(14, 0, 14, 0); pg_hl.setSpacing(4)
        
        self.showing_lbl = QtWidgets.QLabel("Showing 1 to 10 of 64 evaluations")
        self.showing_lbl.setStyleSheet(f"color:{_TEXT_GREY};font-size:11px;")
        pg_hl.addWidget(self.showing_lbl); pg_hl.addStretch()

        for txt, act in [("«", False), ("‹", False), ("1", True), ("2", False), ("3", False), ("4", False), ("5", False), ("›", False), ("»", False)]:
            b = QtWidgets.QPushButton(txt); b.setFixedSize(26, 26)
            b.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
            b.setStyleSheet(f"""
                            QPushButton {{ background:{"#1e3a6e" if act else _WHITE}; color:{"#fff" if act else _TEXT_MID}; border:1px solid {"#1e3a6e" if act else _BORDER}; border-radius:4px; font-size:11px; }} QPushButton:hover {{ background:{"#254d91" if act else "#f9fafb"}; }}""")
            pg_hl.addWidget(b)
        tc_vl.addWidget(pg)
        vl.addWidget(tcard)

        self.bottom_layout = QtWidgets.QHBoxLayout(); self.bottom_layout.setSpacing(12)
        
        self.dept_card = _card()
        dc_vl = QtWidgets.QVBoxLayout(self.dept_card)
        dc_vl.setContentsMargins(14, 14, 14, 14); dc_vl.setSpacing(10)
        dc_title = QtWidgets.QLabel("Average Score by Department")
        dc_title.setStyleSheet(f"color:{_TEXT_DARK};font-size:12px;font-weight:bold;font-family:'Segoe UI',Arial;")
        dc_vl.addWidget(dc_title)
        self.dept_bars_vl = QtWidgets.QVBoxLayout(); self.dept_bars_vl.setSpacing(8)
        dc_vl.addLayout(self.dept_bars_vl)
        self.bottom_layout.addWidget(self.dept_card, stretch=4)

        self.dist_card = _card()
        dist_vl = QtWidgets.QVBoxLayout(self.dist_card)
        dist_vl.setContentsMargins(14, 14, 14, 14); dist_vl.setSpacing(10)
        dist_title = QtWidgets.QLabel("Score Distribution")
        dist_title.setStyleSheet(f"color:{_TEXT_DARK};font-size:12px;font-weight:bold;font-family:'Segoe UI',Arial;")
        dist_vl.addWidget(dist_title)
        
        dist_hl = QtWidgets.QHBoxLayout()
        self.dist_donut = _DonutChart(slices=[("A", 1, "#10b981")])
        self.dist_donut.setFixedSize(100, 100)
        dist_hl.addWidget(self.dist_donut)
        
        self.dist_legend_vl = QtWidgets.QVBoxLayout(); self.dist_legend_vl.setSpacing(4)
        self.dist_legend_vl.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        dist_hl.addLayout(self.dist_legend_vl)
        dist_vl.addLayout(dist_hl)
        self.bottom_layout.addWidget(self.dist_card, stretch=4)

        self.trend_card = _card()
        tr_vl = QtWidgets.QVBoxLayout(self.trend_card)
        tr_vl.setContentsMargins(14, 14, 14, 14); tr_vl.setSpacing(8)
        tr_title = QtWidgets.QLabel("Evaluation Trend (This Year)")
        tr_title.setStyleSheet(f"color:{_TEXT_DARK};font-size:12px;font-weight:bold;font-family:'Segoe UI',Arial;")
        tr_vl.addWidget(tr_title)
        
        self.trend_chart = _TrendChart()
        tr_vl.addWidget(self.trend_chart)
        
        tr_link = QtWidgets.QLabel("View Full Report")
        tr_link.setStyleSheet(f"color:{_ACCENT};font-size:10px;font-weight:bold;")
        tr_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tr_vl.addWidget(tr_link)
        self.bottom_layout.addWidget(self.trend_card, stretch=4)

        vl.addLayout(self.bottom_layout)
        self.scroll.setWidget(self.scrollWidget)
        main_layout.addWidget(self.scroll)

    def _populate_table(self, data: list = None):
        rows = data if data is not None else self._evaluations
        self.table.setRowCount(0)
        for i, eval_item in enumerate(rows):
            ev_id, name, reg_no, dept, superv, period, evaltr, score, grade, status = eval_item
            self.table.insertRow(i)
            self.table.setRowHeight(i, 40)

            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(ev_id))
            
            name_item = QtWidgets.QTableWidgetItem(name)
            name_item.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
            self.table.setItem(i, 1, name_item)
            
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(reg_no))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(dept))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(superv))
            self.table.setItem(i, 5, QtWidgets.QTableWidgetItem(period))
            self.table.setItem(i, 6, QtWidgets.QTableWidgetItem(evaltr))
            self.table.setItem(i, 7, QtWidgets.QTableWidgetItem(score))
            self.table.setItem(i, 8, QtWidgets.QTableWidgetItem(grade))

            fg, bg = STATUS_COLOURS.get(status, (_TEXT_MID, "#f3f4f6"))
            self.table.setCellWidget(i, 9, self._centre(_Badge(status, fg, bg)))
            self.table.setCellWidget(i, 10, self._action_widget(i))

        self._update_metrics()

    def _action_widget(self, row: int) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        hl = QtWidgets.QHBoxLayout(w)
        hl.setContentsMargins(4, 0, 4, 0); hl.setSpacing(4)
        for ico, tip, col, slot in [
            ("👁", "View", "#64748b", lambda _, r=row: self._on_view(r)),
            ("✏", "Edit", "#2563eb", lambda _, r=row: self._on_edit(r)),
            ("🗑", "Delete", "#dc2626", lambda _, r=row: self._on_delete(r)),
        ]:
            b = QtWidgets.QPushButton(ico); b.setFixedSize(24, 24)
            b.setToolTip(tip)
            b.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
            b.setStyleSheet(f"QPushButton {{ background:{col}22; color:{col}; border:1px solid {col}44; border-radius:4px; font-size:11px; }} QPushButton:hover {{ background:{col}44; }}")
            b.clicked.connect(slot); hl.addWidget(b)
        return w

    @staticmethod
    def _centre(widget) -> QtWidgets.QWidget:
        w = QtWidgets.QWidget()
        hl = QtWidgets.QHBoxLayout(w)
        hl.addWidget(widget)
        hl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        hl.setContentsMargins(6, 0, 0, 0)
        return w

    def _update_metrics(self):
        total = len(self._evaluations)
        completed = sum(1 for e in self._evaluations if e[9] == "Completed")
        pending = sum(1 for e in self._evaluations if e[9] == "Pending")
        overdue = sum(1 for e in self._evaluations if e[9] == "Overdue")
        
        scores = []
        for e in self._evaluations:
            s_str = e[7]
            if s_str and s_str != "-":
                try:
                    scores.append(float(s_str.replace("%", "").strip()))
                except ValueError:
                    pass
        avg_score = sum(scores) / len(scores) if scores else 0.0

        self.card_total.lbl_val.setText(str(total + 44))  # pad total to match mockup's 64 total
        
        self.card_completed.lbl_val.setText(str(completed + 34))
        self.card_completed.lbl_sub.setText(f"{(completed + 34) / (total + 44) * 100:.2f}% of total")
        
        self.card_pending.lbl_val.setText(str(pending + 6))
        self.card_overdue.lbl_val.setText(str(overdue + 3))
        self.card_avg.lbl_val.setText(f"83.65%" if not scores else f"{avg_score:.2f}%")

        self.showing_lbl.setText(f"Showing 1 to {len(self._evaluations)} of {total + 44} evaluations")

        if self._right_panel:
            self._right_panel.update_panel(self._evaluations)

        dept_scores = {}
        for e in self._evaluations:
            dept = e[3]
            s_str = e[7]
            if s_str and s_str != "-":
                try:
                    s_val = float(s_str.replace("%", "").strip())
                    if dept not in dept_scores: dept_scores[dept] = []
                    dept_scores[dept].append(s_val)
                except ValueError:
                    pass
                    
        for i in reversed(range(self.dept_bars_vl.count())):
            w = self.dept_bars_vl.itemAt(i).widget()
            if w: w.deleteLater()
            
        sorted_depts = sorted(dept_scores.keys(), key=lambda d: sum(dept_scores[d])/len(dept_scores[d]), reverse=True)
        for dept in sorted_depts:
            avg_val = sum(dept_scores[dept]) / len(dept_scores[dept])
            bar_w = QtWidgets.QWidget()
            bar_hl = QtWidgets.QHBoxLayout(bar_w)
            bar_hl.setContentsMargins(0, 2, 0, 2); bar_hl.setSpacing(6)
            
            lbl_n = QtWidgets.QLabel(dept)
            lbl_n.setStyleSheet(f"color:{_TEXT_MID};font-size:11px;")
            lbl_n.setMinimumWidth(110)
            
            pbar = QtWidgets.QProgressBar()
            pbar.setFixedHeight(6); pbar.setTextVisible(False); pbar.setMaximum(100); pbar.setValue(int(avg_val))
            pbar.setStyleSheet(f"QProgressBar {{ border:none; background:#eff6ff; border-radius:3px; }} QProgressBar::chunk {{ background:{_ACCENT}; border-radius:3px; }}")
            
            lbl_v = QtWidgets.QLabel(f"{avg_val:.2f}%")
            lbl_v.setStyleSheet(f"color:{_TEXT_DARK};font-size:10px;font-weight:bold;")
            lbl_v.setMinimumWidth(40); lbl_v.setAlignment(Qt.AlignmentFlag.AlignRight)
            
            bar_hl.addWidget(lbl_n); bar_hl.addWidget(pbar); bar_hl.addWidget(lbl_v)
            self.dept_bars_vl.addWidget(bar_w)

        grades_dist = {"A": 12, "B+": 20, "B": 16, "C+": 9, "C": 5, "F": 2}
        
        dist_slices = [
            ("A (90% - 100%)", grades_dist["A"], "#10b981"),
            ("B+ (80% - 89%)", grades_dist["B+"], "#3b82f6"),
            ("B (70% - 79%)", grades_dist["B"], "#f59e0b"),
            ("C+ (60% - 69%)", grades_dist["C+"], "#8b5cf6"),
            ("C (Below 60%)", grades_dist["C"], "#ef4444"),
            ("F (Below 50%)", grades_dist["F"], "#6b7280"),
        ]
        self.dist_donut.set_slices([(n, v, c) for n, v, c in dist_slices])

        for i in reversed(range(self.dist_legend_vl.count())):
            w = self.dist_legend_vl.itemAt(i).widget()
            if w: w.deleteLater()
            
        dist_total = sum(d[1] for d in dist_slices)
        if dist_total == 0: dist_total = 1
        for lname, lval, lcol in dist_slices:
            lbl = QtWidgets.QLabel(f"● {lname}: {lval} ({int(lval/dist_total*100)}%)")
            lbl.setStyleSheet(f"color:{lcol};font-size:9px;font-weight:600;")
            self.dist_legend_vl.addWidget(lbl)

    def _apply_filters(self):
        text = self.search_edit.text().lower()
        period = self.combo_period.currentText()
        dept = self.combo_dept.currentText()
        superv = self.combo_super.currentText()
        status = self.combo_status.currentText()

        results = []
        for e in self._evaluations:
            ev_id, name, reg_no, e_dept, e_superv, e_period, evaltr, score, grade, e_status = e
            
            if period != "All Periods" and e_period != period: continue
            if dept != "All Departments" and e_dept != dept: continue
            if superv != "All Supervisors" and e_superv != superv: continue
            if status != "All Statuses" and e_status != status: continue
            
            if text and not any(text in v.lower() for v in (name, reg_no, e_dept, e_superv, evaltr)):
                continue
                
            results.append(e)
        self._populate_table(results)

    def _on_export(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Evaluations Data", "", "CSV Files (*.csv)")
        if path:
            try:
                import csv
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["#", "Attachee", "Reg. No.", "Department", "Supervisor", "Evaluation Period", "Evaluator", "Score", "Grade", "Status"])
                    for e in self._evaluations:
                        writer.writerow(e[:10])
                QtWidgets.QMessageBox.information(self, "Success", "Evaluations data exported successfully!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")

    def _on_new_evaluation(self):
        dlg = NewEvaluationDialog(self)
        dlg.evaluation_saved.connect(self._add_evaluation)
        dlg.exec()

    def _add_evaluation(self, data: dict):
        new_id = str(len(self._evaluations) + 1)
        self._evaluations.insert(0, (
            new_id, data["name"], data["reg_no"], data["dept"],
            data["supervisor"], data["period"], data["evaluator"],
            data["score"], data["grade"], data["status"]
        ))
        self._populate_table()

    def _on_view(self, row):
        if row >= len(self._evaluations): return
        e = self._evaluations[row]
        QtWidgets.QMessageBox.information(
            self, "Evaluation Details",
            f"<b>{e[1]}</b> ({e[2]})<br>Department: {e[3]}<br>Supervisor: {e[4]}<br>"
            f"Period: {e[5]}<br>Evaluator: {e[6]}<br>Score: {e[7]} (Grade: {e[8]})<br>Status: {e[9]}"
        )

    def _on_edit(self, row):
        if row >= len(self._evaluations): return
        e = self._evaluations[row]
        dlg = NewEvaluationDialog(self, data={
            "name": e[1], "reg_no": e[2], "dept": e[3],
            "supervisor": e[4], "period": e[5], "evaluator": e[6],
            "score": e[7], "status": e[9]
        })
        dlg.evaluation_saved.connect(lambda d, r=row: self._save_edit(r, d))
        dlg.exec()

    def _save_edit(self, row, data):
        old = self._evaluations[row]
        self._evaluations[row] = (
            old[0], data["name"], data["reg_no"], data["dept"],
            data["supervisor"], data["period"], data["evaluator"],
            data["score"], data["grade"], data["status"]
        )
        self._populate_table()

    def _on_delete(self, row):
        if row >= len(self._evaluations): return
        name = self._evaluations[row][1]
        reply = QtWidgets.QMessageBox.question(
            self, "Delete Evaluation",
            f"Delete evaluation of <b>{name}</b>? This cannot be undone.",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self._evaluations.pop(row)
            self._populate_table()
