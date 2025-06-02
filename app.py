from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)


# 读取 participants.txt 并返回一个列表
def load_participants(file_path='participants.txt'):
    participants = []
    try:
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                name = line.strip()
                if name:
                    participants.append(name)
    except FileNotFoundError:
        # 如果文件不存在，就返回空列表
        return []
    return participants


@app.route('/', methods=['GET'])
def index():
    """
    首页：展示所有参与者，以及抽奖数量输入框。
    """
    participants = load_participants()
    return render_template('index.html', participants=participants)


@app.route('/draw', methods=['POST'])
def draw():
    """
    抽奖路由：从 participants 列表中随机抽取指定数量的参与者，跳转到结果页面。
    """
    participants = load_participants()
    if not participants:
        # 如果没有参与者，重定向回首页
        return redirect(url_for('index'))

    # 从表单获取要抽取的人数
    try:
        count = int(request.form.get('count', '1'))
    except ValueError:
        count = 1

    # 边界检查，最少抽1人，最多抽 participants 列表长度
    count = max(1, min(count, len(participants)))

    # 用 random.sample 不重复地抽取
    winners = random.sample(participants, count)

    return render_template('result.html', winners=winners, count=count)


if __name__ == '__main__':
    # debug 模式下启动，便于开发调试
    app.run(host='0.0.0.0', port=5000, debug=True)
