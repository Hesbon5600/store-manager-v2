# store-manager-v2
Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.  
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/694b6ed7daad7fca8e9f)

Heroku link  
https://hesbon-store-manager.herokuapp.com/

Documentation link  
https://documenter.getpostman.com/view/4074074/RzZ1qN7c  


**How should this be manually tested?**
1. Create  a virtual environment with the command  
`$ virtualenv -p python3 venv`  

1. Activate the venv with the command     
`$ source venv/bin/activate`

1. Install git  
1. clone this repo  
`$ git@github.com:Hesbon5600/Store-Manager-V1.git"` 
  
1. cd into the folder Store-Manager-V2  
1. `git checkout bg-fix-bugs-v2-161502130`  
1. export required enviroments  
	`export SECRET_KEY='yoursecretkey`  
	`export DB_NAME="store_manager"`  
	`export DB_HOST="localhost"`  
	`export DB_USER="your-DB-username"`  
	`export APP_SETTINGS="development"`  
	`export FLASK_ENV="development"`  
	`export FLASK_APP=run.py`  
  
1. install requirements      
`$ pip install -r requirements.txt` 
1. create the development database  
	`createdb store_manager`  
1. create the testing database  
`$ createdb test_dtb`
1. now we are ready to run. 
	1. for tests run  
         `$ export APP_SETTINGS="testing"`  
	`$ pytest`   
	1. for the application run  
	`$ flask run`  

If you ran the application you can test the various api end points using postman. The appi endpoints are  

|Endpoint|functionality|contraints(requirements)|
|-------|-------------|----------|
|post /api/v2/auth/signup|create a user|user information|
|post /api/v2/auth/login | login |requires authentication |
|get /api/v2/products| get all the products| pass a token |
|get /api/v2/products/</productID>|return a single product| product id, pass token|
|post /api/v2/products | create a new product entry| product data, pass token|
|post /api/v2/sales | create a new sale| product id, pass token|
|get /api/v2/sales | get all sales entries| pass token|
|get/api/v2/sales/<saleID>|get a single sale entry| sale id, pass token| 
|delete /api/v2/products/<productID> | delete a product| product id, pass token|
|put /api/v2/products/<productID> | update a products|product id, product data, pass token|



