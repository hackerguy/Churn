# -*- coding: utf-8 -*-
"""
	Default Mortgage Predictions
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	An example web application for making predicions using a saved WLM model
	using Flask and the IBM WLM APIs.

	Created by Rich Tarro
	June 2017
"""

import os, urllib3, requests, json
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash, jsonify

app = Flask(__name__)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
))


def predictChurn(ID, Gender, Status, Children, EstIncome, CarOwner, Age, LongDistance, 
	International, Local, Dropped, Paymethod, LocalBilltype, LongDistanceBilltype, 
	Usage, RatePlan):
	
	service_path = 'https://ibm-watson-ml.mybluemix.net'
	username = 'ee688c5a-e7d7-4767-8bc8-651466173e0f'
	password = 'a8b6bec8-bd87-4534-981a-0a02e492c1d4'

	headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
	url = '{}/v2/identity/token'.format(service_path)
	response = requests.get(url, headers=headers)
	mltoken = json.loads(response.text).get('token')
	header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
	scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/3679"
	payload_scoring = ({"record":[ID, Gender, Status, Children, EstIncome, CarOwner, Age,
		 LongDistance, International, Local, Dropped, Paymethod, LocalBilltype, 
		 LongDistanceBilltype, Usage, RatePlan]})
	response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
	
	result = response_scoring.text
	return response_scoring


@app.route('/',  methods=['GET', 'POST'])
def index():
	if request.method == 'POST':

		# ID = 2095
		# Gender = "F"
		# Status = "M"
		# Children = 2.000000
		# EstIncome = 7551.100000
		# CarOwner = "Y"
		# Age = 33.600000
		# LongDistance = 20.530000
		# International = 0.000000
		# Local = 41.890000
		# Dropped = 1.000000	
		# Paymethod = "CC"
		# LocalBilltype = "Budget"
		# LongDistanceBilltype = "Intnl_discount"
		# Usage = LongDistance + International + Local
		# RatePlan = 2.000000


		# user inputs
		ID = 2095
		Gender = request.form.get('Gender')
		Status = request.form.get('Status')
		Children = int(request.form.get('Children'))
		EstIncome = int(request.form.get('EstIncome'))
		CarOwner = request.form.get('CarOwner')
		Age = int(request.form.get('Age'))
		LongDistance = int(request.form.get('LongDistance'))
		International = int(request.form.get('International'))
		Local = int(request.form.get('Local'))
		Dropped = int(request.form.get('Dropped'))	
		Paymethod = request.form.get('Paymethod')
		LocalBilltype = request.form.get('LocalBilltype')
		LongDistanceBilltype = request.form.get('LongDistanceBilltype')
		Usage = LongDistance + International + Local
		RatePlan = int(request.form.get('RatePlan'))
		

		print(ID, Gender, Status, Children, EstIncome, CarOwner, Age, LongDistance, International, 
			Local, Dropped, Paymethod, LocalBilltype, LongDistanceBilltype, Usage, RatePlan)

		
		response_scoring = predictChurn(ID, Gender, Status, Children, EstIncome, CarOwner, Age, 
			LongDistance, International, Local, Dropped, Paymethod, LocalBilltype, 
			LongDistanceBilltype, Usage, RatePlan)


		prediction = response_scoring.json()["result"]["prediction"]
		probability = response_scoring.json()["result"]["probability"]["values"][0]


		print(prediction, probability)

		return jsonify(prediction=prediction, probability=probability)

	else:
		return render_template('input.html')


# if __name__ == '__main__':
#   app.run()
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
