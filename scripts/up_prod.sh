#!/bin/bash
sudo docker-compose -f production.yml up --build -d --scale goweb=5