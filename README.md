# store-manager-v2
Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.

> ## How to set up the project

### Features

- python 3.7
- [poetry](https://python-poetry.org/docs/) as dependency manager

---

### PROJECT SETUP

- clone the repository

```bash
git clone https://github.com/Hesbon5600/store-manager-v2.git
```

- cd into the directory

```bash
cd store-manager-v2
```

### create the development database

```bash
createdb store_manager
```

### create environment variables

  On Unix or MacOS, run:

```bash
cp .env.example .env
```

You can edit whatever values you like in there.

Note: There is no space next to '='

### On terminal

```bash
source .env
```

---

> > ### VIRTUAL ENVIRONMENT

---

**To Create:**

```bash
make env
```

---

**Installing dependencies:**

```bash
make install
```

**Running the application:**

```bash
make run
```


# Testing with postman
If you ran the application you can test the various api end points using postman. The appi endpoints are

|Endpoint|functionality|contraints(requirements)|
|-------|-------------|----------|
|post /api/v2/auth/signup|create a user|user information|
|post /api/v2/auth/login | login |requires authentication |
|get /api/v2/products| get all the products| pass a token |
|`get /api/v2/products/<productID>`|return a single product| product id, pass token|
|post /api/v2/products | create a new product entry| product data, pass token|
|post /api/v2/sales | create a new sale| product id, pass token|
|get /api/v2/sales | get all sales entries| pass token|
|`get/api/v2/sales/<saleID>`|get a single sale entry| sale id, pass token|
|`delete /api/v2/products/<productID>` | delete a product| product id, pass token|
|`put /api/v2/products/<productID>` | update a products|product id, product data, pass token|


# Acknowledgement
I would like to acknowledge Andela for facilitating this project
