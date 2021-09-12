from flask import Flask, config, json, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from prediction_service import prediction
import os
import yaml
import joblib
import numpy as np

# params_path = "params.yaml"
webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

# def read_params(config_path):
#     with open(config_path) as yaml_file:
#         config = yaml.safe_load(yaml_file)
#     return config

# def predict(data):
#     config = read_params(params_path)
#     model_dir_path = config['webapp_model_dir']
#     model = joblib.load(model_dir_path)
#     prediction = model.predict(data)
#     print(prediction)
#     return prediction[0]

# def api_response(request):
#     try:
#         data = np.array([list(request.json.values())])
#         response = predict(data)
#         response = {"response": response}
#         return response
#     except Exception as e:
#         print(e)
#         error = {"error": "Something went wrong!! Try again"}
#         return error


@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def index():
    return render_template('index.html')


@app.route("/profile", methods=['GET', 'POST'])
@cross_origin()
def report():
    return render_template('report.html')


@app.route("/predict", methods=["POST"])
@cross_origin()
def predict_result():
    if request.method == "POST":
        try:
            if request.form:
                data_req = dict(request.form)
                response = prediction.form_response(data_req)
                return render_template('result.html', result=response)

            elif request.json:
                response = prediction.api_response(request, json)
                return jsonify(response)

        except Exception as e:
            error = {'error':e}
            return render_template('404.html', error=error)
    else:
        return render_template('404.html',
                               error="Something went wrong!! Try again")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
