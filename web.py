from flask import Flask, request, render_template, redirect, url_for, session
import subprocess
import os
# 按需修改python文件与静态资源路径
app = Flask(__name__, template_folder=r'C:\Users\Administrator\Desktop\palwebconsole')

# 修改秘钥
app.secret_key = 'xiugaimiyao'

# 修改用户名和密码
USERNAME = 'admin'
PASSWORD = 'password'

# PalServer 的绝对路径按需修改
PALSERVER_PATH = r'E:\SteamLibrary\steamapps\common\PalServer\Pal\Binaries\Win64\PalServer-Win64-Test-Cmd.exe'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return '登录失败！'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/start-server')
def start_server():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        subprocess.Popen([PALSERVER_PATH])
        return 'PalServer 已启动！'
    except Exception as e:
        return str(e)

@app.route('/stop-server')
def stop_server():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        subprocess.call(['taskkill', '/F', '/IM', 'PalServer-Win64-Test-Cmd.exe'])
        return 'PalServer 已关闭！'
    except Exception as e:
        return str(e)

@app.route('/check-server-status')
def check_server_status():
    try:
        # 运行命令并获取输出
        process = subprocess.run('tasklist | find /i "PalServer.exe"', shell=True, check=True)
        if process.returncode == 0:
            return {'status': 'running'}
        else:
            return {'status': 'not running'}
    except subprocess.CalledProcessError:
        # 如果 find 命令没有找到进程，会抛出异常
        return {'status': 'not running'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10196, debug=True)
