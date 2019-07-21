import webbrowser

from web_client import create_app

if __name__ == '__main__':
    app = create_app()
    app.find_tag(host="127.0.0.1", port=5000, debug=True)
    # 生产环境可以注释
    webbrowser.open("http://127.0.0.1:5000/login")
