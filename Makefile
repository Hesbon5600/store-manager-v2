#!/bin/bash

#@-- help command to show usage of make commands --@#
help:
	@echo "----------------------------------------------------------------------------"
	@echo "-                     Available commands                                   -"
	@echo "----------------------------------------------------------------------------"
	@echo "---> make env                 - To create virtual environment"
	@echo "---> make install             - To install dependencies from poetry.lock"
	@echo "---> make start-kafka	     - To start kafka"
	@echo "---> make run 		   		 - To run the application"
	@echo "---> make help                - To show usage commands"
	@echo "----------------------------------------------------------------------------"



env:
	@ echo '<<<<<<<<<<Creating virtual environment>>>>>>>>>'
	poetry env use python3.7 && poetry shell
	@ echo ''


install:
	@ echo '<<<<<<<<<<installing requirements>>>>>>>>>'
	poetry install
	@ echo ''

run:
	@ echo '<<<<<<<<<<Running the application>>>>>>>>>'
	flask run
	@ echo ''


default: help