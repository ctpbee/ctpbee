import logging

from web_client import create_app

# os.system("killall -9 gunicorn")
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = create_app()
if __name__ == '__main__':
    ## production
    # current_dir_path = os.path.abspath(os.path.dirname(__file__))
    # os.system(f"cd {current_dir_path} && gunicorn -b 127.0.0.1:5000 --worker-class  eventlet -w 1 run:app")

    ## development  --> 你应该在此模式下卸载eventlet包
    app.run(debug=True)
    # 生产环境可以注释
    # webbrowser.open("http://127.0.0.1:5000/login")
