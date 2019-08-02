import logging
import webbrowser

from web_client import create_app

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
if __name__ == '__main__':
    app = create_app()
    import eventlet
    import eventlet.wsgi
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    #app.run(host="127.0.0.1", port=5000, debug=False)
    # 生产环境可以注释
    webbrowser.open("http://127.0.0.1:5000/login")
