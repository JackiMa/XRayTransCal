from flask import Flask, render_template, request, jsonify, url_for
from XRayTransmissionCalculator.myinclude.mypkgs import *
import numpy as np
import os
import pickle

# 创建 Flask 应用
app = Flask(__name__)


# 全局变量
elements = None

def get_elements():
    global elements
    pickle_file = './elements.pickle'

    # 如果pickle文件存在，直接从文件加载elements
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as f:
            elements = pickle.load(f)
    else:
        XrayMassCoef_csv_lists = r"./XRayTransmissionCalculator/Data/XrayMassCoef_csv_lists/"
        elements = ELEMENTS()
        for element in os.listdir(XrayMassCoef_csv_lists):
            symbol, name, Z, A, _ = [par.strip() for par in element.split('_')]
            elements.add(ELEMENT(symbol, name, Z, A, pd.read_csv(XrayMassCoef_csv_lists+"/"+element)))
        print(elements.print_all_elements())

        # 保存elements到pickle文件
        with open(pickle_file, 'wb') as f:
            pickle.dump(elements, f)

    return elements


# 定义路由和处理函数
@app.route('/', methods=['GET', 'POST'])
def index():
    # 初始化 elements
    elements = get_elements()

    # 处理 POST 请求
    if request.method == 'POST':
        if not request.is_json:
            print("request is not json")
            return render_template('index.html', img_path_1=None, img_path_2=None)
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        print(data)  # 打印数据以进行调试
        # # 获取表单数据
        chemical = data['chemical'] if data['chemical'] else 'H2O'
        density = float(data['density']) if data['density'] else 1
        thickness = float(data['thickness']) if data['thickness'] else 1
        Emin = float(data['Emin']) if data['Emin'] else 0.1
        Emax = float(data['Emax']) if data['Emax'] else 1
        precision = int(data['precision']) if data['precision'] else 3000

        # chemical = request.form.get('chemical') or 'H2O'
        # density = float(request.form.get('density') or 1)
        # thickness = float(request.form.get('thickness') or 1)
        # Emin = float(request.form.get('Emin') or 0.1)
        # Emax = float(request.form.get('Emax') or 1)
        # precision = int(request.form.get('precision') or 1000)


        # 校验 Emin 和 Emax
        if not 0.001 <= Emin <= 20 or not 0.01 <= Emax <= 20:
            return jsonify(error="Emin and Emax must be between 0.01 and 20"), 400
        
        # 确保precision的值不会太离谱
        precision = 1 if precision < 1 else precision
        precision = 100000 if precision > 100000 else precision

        # 生成 energy_lists
        energy_lists = np.linspace(Emin, Emax, precision)

        # 生成图片路径
        img_path_1 = './static/images/transmission.png'
        img_path_2 = './static/images/μ_ρ.png'
        data_path = './static/data/data.csv'

        # 调用 draw_transmission 函数
        elements.draw_transmission(chemical, energy_lists, density, thickness, img_path_1, img_path_2, data_path)

        # 返回图片路径
        img_url_1 = url_for('static', filename='images/images/transmission.png')
        img_url_2 = url_for('static', filename='images/images/μ_ρ.png')
        return jsonify(img_url_1=img_url_1, img_url_2=img_url_2)
        # return render_template('index.html', img_path_1=img_path_1, img_path_2=img_path_2)

    # 处理 GET 请求
    return render_template('index.html', img_path_1=None, img_path_2=None)

# 运行 Flask 应用
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)