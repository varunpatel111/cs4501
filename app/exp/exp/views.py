from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.shortcuts import render
import urllib.request
import urllib.parse
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

def homePage(request):
	print ("About to perform the GET request...")
	req = urllib.request.Request('http://models-api:8000/api/listings')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def get_listing(request):
	listing = request.POST.get('listing')
	s = "http://models-api:8000/api/listings/" + listing + "/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

# Kafka stuff here

	authenticator = request.POST.get('authenticator')
	if authenticator:
		url = "http://models-api:8000/api/getUserId/"
		result = urllib.request.urlopen(url, urllib.parse.urlencode({"authenticator" : authenticator}).encode("utf-8"))
		resp2 = result.read().decode('utf-8')
		user_id = json.loads(resp2)["user_id"]
		listing_id = resp["data"][0]["id"]

		data = {}
		data["user_id"] = user_id
		data["listing_id"] = listing_id
		resp["data2"] = (user_id, listing_id)
		producer = KafkaProducer(bootstrap_servers='kafka:9092')
		producer.send('clickedListings', json.dumps(data).encode('utf-8'))


# Ends here

	return JsonResponse(resp)

def get_user(request, user):
	s = "http://models-api:8000/api/users/" + user + "/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def get_rec(request, rec):
	s = "http://models-api:8000/api/rec/" + rec + "/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)


def newListingForm(request):
	s = "http://models-api:8000/api/listings/createForm/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def createListing(request):
	url = "http://models-api:8000/api/listings/create/"
	result = urllib.request.urlopen(url, urllib.parse.urlencode(request.POST).encode('utf-8'))
	content = result.read().decode('utf-8')
	resp = json.loads(content)
	if(resp["status"] == "SUCCESS"):
		data = request.POST.copy()
		data["id"] = resp["id"]
		producer = KafkaProducer(bootstrap_servers='kafka:9092')
		producer.send('new-listings', json.dumps(data).encode('utf-8'))

	return JsonResponse(resp)

def createUser(request):
	url = "http://models-api:8000/api/users/create/"
	result = urllib.request.urlopen(url, urllib.parse.urlencode(request.POST).encode('utf-8'))
	content = result.read().decode('utf-8')
	return JsonResponse(json.loads(content))

def newUserForm(request):
	s = "http://models-api:8000/api/users/createForm/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def loginForm(request):
	s = "http://models-api:8000/api/authenticate/login/"
	req = urllib.request.Request(s)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp)

def userLogin(request):
	url = "http://models-api:8000/api/login/"
	result = urllib.request.urlopen(url, urllib.parse.urlencode(request.POST).encode('utf-8'))
	content = result.read().decode('utf-8')
	return JsonResponse(json.loads(content))

def getUserId(request):
	url = "http://models-api:8000/api/getUserId/"
	authenticator = request.POST.get('authenticator')
	result = urllib.request.urlopen(url, urllib.parse.urlencode({"authenticator" : authenticator}).encode("utf-8"))
	resp = result.read().decode('utf-8')
	resp = json.loads(resp)
	return JsonResponse(resp)

def logoutUser(request):
	url = "http://models-api:8000/api/logout/"
	result = urllib.request.urlopen(url, urllib.parse.urlencode(request.POST).encode("utf-8"))
	resp = result.read().decode('utf-8')
	resp = json.loads(resp)
	return JsonResponse(resp)

def search(request):
	query = (request.POST["query"])
	es = Elasticsearch(['es'])
	result = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
	return JsonResponse(result)
