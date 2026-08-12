"""
AIRA - Phase 1: Floating Orb Widget

A small, borderless, transparent, always-on-top, draggable orb that
sits in a corner of the screen. This is pure UI - no AI, no voice,
no logic beyond drag-to-move. Later phases will hook wake-word /
voice / AI behavior into this same widget.
"""

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QColor, QRadialGradient, QMouseEvent
from PySide6.QtWidgets import QWidget, QApplication


class FloatingOrb(QWidget):
    """A small circular, always-on-top desktop widget."""

    ORB_SIZE = 90          # diameter in pixels
    MARGIN = 24             # gap from screen edge for default position

    def __init__(self):
        super().__init__()

        # --- window behavior flags ---
        # FramelessWindowHint  -> no title bar / borders
        # WindowStaysOnTopHint -> always above normal windows
        # Tool                 -> keeps it out of the taskbar
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        # transparent background so only the circle is visible
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(self.ORB_SIZE, self.ORB_SIZE)

        # for drag-to-move
        self._dragging = False
        self._drag_offset = QPoint()

        self._move_to_default_corner()

    # ------------------------------------------------------------------
    # Positioning
    # ------------------------------------------------------------------
    def _move_to_default_corner(self):
        """Place the orb in the bottom-right corner of the primary screen."""
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.ORB_SIZE - self.MARGIN
        y = screen.bottom() - self.ORB_SIZE - self.MARGIN
        self.move(x, y)

    # ------------------------------------------------------------------
    # Painting - this draws the actual orb look
    # ------------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # soft radial gradient so it looks like a glowing orb, not a flat circle
        gradient = QRadialGradient(rect.center(), self.ORB_SIZE / 2)
        gradient.setColorAt(0.0, QColor(120, 170, 255, 230))   # bright core
        gradient.setColorAt(0.6, QColor(90, 120, 230, 200))    # mid
        gradient.setColorAt(1.0, QColor(60, 80, 180, 60))      # soft fade edge

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect.adjusted(4, 4, -4, -4))

    # ------------------------------------------------------------------
    # Drag to move
    # ------------------------------------------------------------------
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_offset = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._dragging:
            new_pos = event.globalPosition().toPoint() - self._drag_offset
            self.move(new_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = False

    # ------------------------------------------------------------------
    # Quit shortcut for testing (right-click to close, for now)
    # ------------------------------------------------------------------
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # Phase 1 convenience only: double-click closes the orb.
        # This will be replaced by a proper tray-icon quit option later.
        if event.button() == Qt.LeftButton:
            QApplication.quit()