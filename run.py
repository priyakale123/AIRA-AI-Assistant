"""
AIRA - Entry point (Phase 1)

Run this file to launch the floating orb.
"""

import sys
from PySide6.QtWidgets import QApplication

from app.ui.floating_orb import FloatingOrb


def main():
    app = QApplication(sys.argv)

    # Keep the app running even if the orb window loses focus,
    # since it has no title bar / normal window controls.
    app.setQuitOnLastWindowClosed(True)

    orb = FloatingOrb()
    orb.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()