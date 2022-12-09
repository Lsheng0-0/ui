import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from MainPane import MainPane

if __name__ == '__main__':
    # PyQt5高清屏幕自适应设置,以及让添加的高清图标显示清晰，不然designer导入的图标在程序加载时会特别模糊
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    ui = MainPane()
    ui.show()
    sys.exit(app.exec_())


