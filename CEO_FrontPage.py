from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

from CEO_Page import Ui_MainWindow, SIDEBAR_EXPANDED, SIDEBAR_COLLAPSED

class CEOPage(QMainWindow, Ui_MainWindow):
    """
    Main window for the CEO role.

    Responsibilities:
    ─────────────────
    Wires every sidebar navigation button to its corresponding stacked-widget page.
    Drives the smooth sidebar expand/collapse animation via QPropertyAnimation.
    Manages the Industrial Attachment submenu expand/collapse.
    Keeps track of which button is currently active so the highlight stays correct.
    THIS PAGE BASICALLY CONTAINS THE BACKEND LOGI OF HOW THE ENTIRE FRAME OF THE CEO PAGE WORKS
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Operations Management System (OMS) — CEO")

        # Track sidebar state
        self._sidebar_expanded = True

        # ── Sidebar animation ──────────────────────────────────────────────────
        self._sidebar_anim = QPropertyAnimation(self.Menubar, b"maximumWidth")
        self._sidebar_anim.setDuration(250)
        self._sidebar_anim.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # Also animate minimumWidth so the sidebar actually shrinks
        self._sidebar_anim_min = QPropertyAnimation(self.Menubar, b"minimumWidth")
        self._sidebar_anim_min.setDuration(250)
        self._sidebar_anim_min.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # ── Connect hamburger button ───────────────────────────────────────────
        self.Menu_Button.clicked.connect(self.toggle_sidebar)

        # ── Connect main nav buttons ──────────────────────────────────────────
        self.Dashboard.clicked.connect(self.open_Dashboard_Page)
        self.Users.clicked.connect(self.open_Users_Page)
        self.Departments.clicked.connect(self.open_Departments_Page)
        self.Roles.clicked.connect(self.open_Roles_Page)
        self.Industrial_Attachment.clicked.connect(self.toggle_ia_submenu)
        self.Tasks.clicked.connect(self.open_Tasks_Page)
        self.Meetings.clicked.connect(self.open_Meetings_Page)
        self.Maintenance.clicked.connect(self.open_Maintenance_Page)
        self.Announcements.clicked.connect(self.open_Announcements_Page)
        self.Reports.clicked.connect(self.open_Reports_Page)
        self.Audit_Logs.clicked.connect(self.open_AuditLogs_Page)
        self.Settings.clicked.connect(self.open_Settings_Page)
        self.Log_out.clicked.connect(self.handle_logout)

        # ── Connect Industrial Attachment sub-buttons ──────────────────────────
        self.Applicants.clicked.connect(self.open_Applicants_Page)
        self.Interviews.clicked.connect(self.open_Interviews_Page)
        self.Attachees.clicked.connect(self.open_Attachees_Page)
        self.Attendance.clicked.connect(self.open_Attendance_Page)
        self.Evaluations.clicked.connect(self.open_Evaluations_Page)
        self.Clearances.clicked.connect(self.open_Clearances_Page)
        self.Reports_Attachment.clicked.connect(self.open_AttachmentReports_Page)

        # ── Open Dashboard by default and check its button ────────────────────
        self.Dashboard.setChecked(True)
        self.open_Dashboard_Page()

    # ==========================================================================
    # SIDEBAR TOGGLE
    # ==========================================================================
    def toggle_sidebar(self):
        """Smoothly expand or collapse the sidebar."""
        if self._sidebar_expanded:
            # Collapse
            target = SIDEBAR_COLLAPSED
            # Hide text labels inside logo block so only icon shows
            self.label_2.setVisible(False)
            self.logoSubLabel.setVisible(False)
            self.menuSectionLabel.setVisible(False)
            self.sessionLoginLabel.setVisible(False)
            self.sessionVersionLabel.setVisible(False)
        else:
            # Expand — reveal labels first so they fade in with the animation
            target = SIDEBAR_EXPANDED
            self.label_2.setVisible(True)
            self.logoSubLabel.setVisible(True)
            self.menuSectionLabel.setVisible(True)
            self.sessionLoginLabel.setVisible(True)
            self.sessionVersionLabel.setVisible(True)

        current = self.Menubar.width()

        self._sidebar_anim.setStartValue(current)
        self._sidebar_anim.setEndValue(target)
        self._sidebar_anim.start()

        self._sidebar_anim_min.setStartValue(current)
        self._sidebar_anim_min.setEndValue(target)
        self._sidebar_anim_min.start()

        self._sidebar_expanded = not self._sidebar_expanded

    # ==========================================================================
    # INDUSTRIAL ATTACHMENT  — expand / collapse submenu
    # ==========================================================================
    def toggle_ia_submenu(self):
        """Show or hide the Industrial Attachment sub-navigation items."""
        visible = self.IndustrialAttachment_Submenu.isVisible()
        self.IndustrialAttachment_Submenu.setVisible(not visible)
        # Navigate to the IA container page whenever the menu is opened
        if not visible:
            self.stackedWidget.setCurrentIndex(4)

    # ==========================================================================
    # MAIN PAGE NAVIGATION
    # ==========================================================================

    def _navigate(self, index: int):
        """Switch the outer stacked widget to *index* and close IA submenu if needed."""
        self.stackedWidget.setCurrentIndex(index)
        # Close the IA submenu when navigating away from it
        if index != 4:
            self.IndustrialAttachment_Submenu.setVisible(False)
            self.Industrial_Attachment.setChecked(False)

    def open_Dashboard_Page(self):
        self._navigate(0)

    def open_Users_Page(self):
        self._navigate(1)

    def open_Departments_Page(self):
        self._navigate(2)

    def open_Roles_Page(self):
        self._navigate(3)

    def open_IndustrialAttachment_Page(self):
        self._navigate(4)

    def open_Tasks_Page(self):
        self._navigate(5)

    def open_Meetings_Page(self):
        self._navigate(6)

    def open_Maintenance_Page(self):
        self._navigate(7)

    def open_Announcements_Page(self):
        self._navigate(8)

    def open_Reports_Page(self):
        self._navigate(9)

    def open_AuditLogs_Page(self):
        self._navigate(10)

    def open_Settings_Page(self):
        self._navigate(11)

    # ==========================================================================
    # INDUSTRIAL ATTACHMENT  — sub-page navigation
    # ==========================================================================

    def _ia_navigate(self, index: int):
        """Switch the inner (IA) stacked widget and ensure the IA page is showing."""
        self.stackedWidget.setCurrentIndex(4)
        self.stackedWidget_2.setCurrentIndex(index)

    def open_Applicants_Page(self):
        self._ia_navigate(0)

    def open_Attachees_Page(self):
        self._ia_navigate(1)

    def open_Attendance_Page(self):
        self._ia_navigate(2)

    def open_Evaluations_Page(self):
        self._ia_navigate(3)

    def open_AttachmentReports_Page(self):
        self._ia_navigate(4)

    def open_Interviews_Page(self):
        self._ia_navigate(5)

    def open_Clearances_Page(self):
        self._ia_navigate(6)

    # ==========================================================================
    # CONTEXT MENUS  (skeleton — extend per page as needed)
    # ==========================================================================

    def show_context_menu(self, button: QtWidgets.QPushButton, menu_items: list):
        """
        Display a styled context menu anchored below *button*.

        Args:
            button     : The QPushButton that triggered the menu.
            menu_items : List of (label, callback) tuples.
        """
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid #e0e4ec;
                border-radius: 6px;
                padding: 4px 0px;
                font-size: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QMenu::item {
                color: #374151;
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #eff6ff;
                color: #1e3a6e;
            }
            QMenu::separator {
                height: 1px;
                background-color: #e0e4ec;
                margin: 4px 0px;
            }
        """)

        for label, callback in menu_items:
            if label == "---":
                menu.addSeparator()
            else:
                action = QAction(label, self)
                action.triggered.connect(callback)
                menu.addAction(action)

        # Position below the button
        pos = button.mapToGlobal(QtCore.QPoint(0, button.height()))
        menu.exec(pos)

    # ==========================================================================
    # LOG OUT
    # ==========================================================================

    def handle_logout(self):
        """Prompt for confirmation then close the application."""
        reply = QtWidgets.QMessageBox.question(
            self,
            "Log Out",
            "Are you sure you want to log out?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.close()