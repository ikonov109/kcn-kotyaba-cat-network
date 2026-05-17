import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QStatusBar, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl

SERVER = "http://217.198.5.134:4433"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 KCN/1.0"

class KCNBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KCN - Kotyaba Cat Network")
        self.setGeometry(100, 100, 1200, 800)

        # Устанавливаем глобальный User-Agent для WebEngine
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(USER_AGENT)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Панель ввода
        top = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("kcp://мой-кот")
        self.url_input.returnPressed.connect(self.navigate)
        top.addWidget(self.url_input)

        go_btn = QPushButton("🔍 Перейти")
        go_btn.clicked.connect(self.navigate)
        top.addWidget(go_btn)

        search_btn = QPushButton("🔎 KCS Поиск")
        search_btn.clicked.connect(self.kcs_search)
        top.addWidget(search_btn)

        layout.addLayout(top)

        # WebView
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)

        # Статус
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Готов")

        self.webview.setHtml("""
        <html><body style="background:#1e1e2e; color:white; font-family:Arial; text-align:center; padding:50px">
        <h1>🐱 KCN Browser</h1>
        <p>Введи:<br>kcp://мой-кот<br>kcp://register.domains<br>kcp://image.cat.kcn.cat/картинка.jpg<br>http://google.com</p>
        </body></html>
        """)

    def resolve_domain(self, domain):
        try:
            r = requests.get(f"{SERVER}/api/resolve?name={domain}", timeout=5, headers={"User-Agent": USER_AGENT})
            if r.status_code == 200:
                return r.json().get("address")
        except:
            pass
        return None

    def kcs_search(self):
        query = self.url_input.text().strip()
        if not query:
            return

        if query.startswith("kcp://"):
            query = query[6:]

        parts = query.split("/", 1)
        domain = parts[0]
        path = "/" + parts[1] if len(parts) > 1 else ""

        if domain == "register.domains":
            self.webview.setUrl(QUrl("http://217.198.5.134:4433"))
            self.statusbar.showMessage("📝 Регистратор")
            return

        self.statusbar.showMessage(f"🔍 Поиск {domain}...")
        addr = self.resolve_domain(domain)

        if addr:
            if addr.startswith("http://"):
                addr = addr[7:]
            full_url = f"http://{addr}{path}"
            self.webview.setUrl(QUrl(full_url))
            self.statusbar.showMessage(f"✅ {domain}")
        else:
            self.webview.setHtml(f"<h1>❌ Домен {domain} не найден</h1><p>Зарегистрируй на http://217.198.5.134:4433</p>")
            self.statusbar.showMessage(f"❌ {domain} не найден")

    def navigate(self):
        url = self.url_input.text().strip()
        if not url:
            return

        if not url.startswith(("http://", "https://", "kcp://")):
            url = "http://" + url

        if url.startswith("kcp://"):
            self.kcs_search()
        else:
            self.webview.setUrl(QUrl(url))
            self.statusbar.showMessage(f"🌐 Открыт")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = KCNBrowser()
    browser.show()
    sys.exit(app.exec_())