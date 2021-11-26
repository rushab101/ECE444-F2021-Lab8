import flask
import requests

model_id = "mrm8488/bert-tiny-finetuned-fake-news-detection"
api_token = "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"




"""Code taken directly from: https://huggingface.co/inference-api"""
def query(payload, model_id, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()



##############################################################################################
#
#   FLASK APP
#
##############################################################################################

# The flask app for serving predictions
application = flask.Flask(__name__)

@application.route('/')
def hello():
    return "Welcome to your own Sentiment Analysis Tool"

@application.route('/news', methods=['GET','Post'])
def news_tester():
    """Do an inference on a single batch of data.
    """
    data = None

    if flask.request.content_type == 'application/json':
        data = flask.request.get_json()
    else:
        return flask.Response(response='This predictor only supports Json data', status=415, mimetype='text/plain')
    
    model = query(data.get('text'),model_id,api_token)[0]
    #print(model)
    real_score = model[0]['score']
    fake_score = model[1]['score']
    result = ""
    if real_score >= fake_score:
        result = str(real_score * 100) + ":" + "0"
    else:
        result = str(fake_score * 100) + ":" + "1"

    return_response = flask.jsonify(result)
    return return_response

if __name__ == '__main__':
    application.run()
