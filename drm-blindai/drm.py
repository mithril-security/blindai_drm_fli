from flask import Flask, request
import json


# DRM server, goals: 
#   - listening requests from the Inference Server for comsuption budget
#   - sending each inference for tracing
def drm_server():
    app = Flask(__name__)

    @app.route('/request_consumption', methods=['POST', 'GET'])
    def request_consumption():
        if request.method == 'POST':
            # we can imagine that it looks into a database to see if the number of inferences asked for 
            # is allowed
            number_inferences = request.form['number_inferences']
            print("* [POST: /request_consumption] New number of inferences : " + str(number_inferences))

            with open('inferences.json', 'w') as f: 
                json.dump({"inferences" : str(number_inferences)}, f)
            return {"inferences": number_inferences}
        elif request.method == 'GET':
            json_inferences = {}
            with open('inferences.json', 'r') as f:
                json_inferences = json.load(f)
            print("* [GET: /request_consumption] Number of inferences remaining : " + str(json_inferences["inferences"]))
            return json_inferences
        else:
            return {"error" : "Method not allowed"}
        
    @app.route('/consume_model', methods=['POST'])
    def consume_model():
        if request.method == "POST":
            number_inferences = 0
            with open('inferences.json', 'r+') as f: 
                number_inferences = int(json.load(f)["inferences"])
                f.seek(0)
                if number_inferences > 0:
                    number_inferences -= 1
                    print("* [POST: /consume_model] Model ran by user : " + request.form['user'] + ". Number of inferences remaining : " + str(number_inferences))
                else: 
                    print("* [POST: /consume_model] No inferences left for user : " + request.form['user'] + ". Model not allowed to run.")

                json.dump({"inferences": str(number_inferences)},f)
                return {"inferences": number_inferences}
        else:
            return {"error" : "Method not allowed"}
    return app