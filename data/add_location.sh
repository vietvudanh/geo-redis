#!/bin/bash
curl --data "lat=1&lon=100&name=Hanoi" http://localhost:5000/add
curl --data "lat=85&lon=20&name=Tokyo" http://localhost:5000/add
curl --data "lat=70&lon=30&name=San Francisco" http://localhost:5000/add
curl --data "lat=60&lon=40&name=Paris" http://localhost:5000/add
curl --data "lat=50&lon=50&name=Osaka" http://localhost:5000/add
curl --data "lat=55&lon=50&name=Saigon" http://localhost:5000/add
curl --data "lat=45&lon=60&name=London" http://localhost:5000/add
curl --data "lat=30&lon=70&name=Berlin" http://localhost:5000/add
curl --data "lat=20&lon=80&name=Los Angeles" http://localhost:5000/add
curl --data "lat=10&lon=90&name=New York" http://localhost:5000/add