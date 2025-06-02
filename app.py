from flask import Flask, render_template, request, redirect, url_for, send_file
import random
import qrcode
import os

app = Flask(__name__)

# 内存保存参与者（可改为数据库或写入文件）
participants = set()
ip_records = set()  # 存储已注册 IP
n = 0


# 生成二维码，保存为 static/qrcode.png
def generate_qrcode(link='http://localhost:5000/signup'):
    img = qrcode.make(link)
    path = 'static/qrcode.png'
    os.makedirs('static', exist_ok=True)
    img.save(path)
    return path


def get_client_ip():
    # 支持通过代理（如 Nginx）传递的真实 IP
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip


@app.route('/')
def index():
    return render_template('index.html', participants=list(participants))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global n
    client_ip = get_client_ip()
    if client_ip in ip_records:
        return "你已经领过号啦，每个设备只能参与一次！", 403
    n += 1
    participants.add(f"阿瓦隆{n}号")
    ip_records.add(client_ip)
    return render_template('signup.html', no=n)


@app.route('/draw', methods=['POST'])
def draw():
    count = int(request.form.get('count', 1))
    selected = random.sample(list(participants), min(count, len(participants)))
    return render_template('result.html',
                           count=min(count, len(participants)),
                           winners=selected)


@app.route('/clear', methods=['POST'])
def clear():
    participants.clear()
    ip_records.clear()
    return redirect(url_for('index'))


@app.route('/qrcode')
def show_qrcode():
    link = request.host_url.rstrip('/') + '/signup'
    path = generate_qrcode(link)
    return render_template('qrcode.html', qrcode_path=path)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
