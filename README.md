# cdn-prototype
#### This prototype is to demostrate the Kong API Gateway act as a reverse proxy to handle CDN functionality for a web application without implementing caching.

In this prototype im using Docker containers for **kong gateway, python server and html page** to test its functionality. Im using DB-less configuration all the request are passing through **KONG API GATEWAY**
from uploading to retrival and serving of file to public is all passing through **KONG API GATEWAY** to **python server** for handling appropriate action.

# [DEMO](http://143.198.146.23)

## REQUIREMENTS
* DOCKER
* Ubuntu 22.04.3 LTS

## INSTALLATION
Just follow the instruction below for successfull implementation of CDN PROTOTYPE for both localhost and server.
1. Installing Docker
    ```shell
     $ curl -fsSL https://get.docker.com -o get-docker.sh
     $ sudo sh ./get-docker.sh
    ```
    make sure docker is by run the following command.
    ```shell
     $ docker -v
    ```
2. Setting up the prototype
    clone git respository by running the following command.
    ```shell
     $ git clone https://github.com/goharsb/cdn-prototype
    ```
    **(OPTIONAL)** if you want to run this prototype on server you need to provide ip of your server in file **Dockerfile.python** located at **cdn-prototype/python/Dockerfile.python**. For example if your server ip is **143.198.146.23** then change the following line.
        
    > CMD ["python", "server.py", "0.0.0.0:8080", "--kong_url", "127.0.0.1"]
    
    into   
    
    > CMD ["python", "server.py", "0.0.0.0:8080", "--kong_url", "143.198.146.23"]
    
3. Running the prototype

   we need to create network for kong gateway
    ```shell
     $ docker network create kong-net
    ```
    after creating network run change you current directory to the **cdn-prototype** as **docker-compose.yml** located there.
    ```shell
     $ cd cdn-prototype
    ```

    **(OPTIONAL)** if you want to use **KONG MANAGER** then uncomment the following line in **docker-compose.yml** and change localhost to your server IP if you are running on server then your MANAGER will be accessable at **http://YOUR_IP:8002**
    > #KONG_ADMIN_GUI_URL: http://localhost:8002
    
    then compose the container by running following command .
    ```shell
    $ docker compose up --build
    ```
    for deattached mode
    ```shell
    $ docker compose up --build -d
    ```  	
    after all the containers are up you can access **KONG ADMIN** at port **http://YOUR_IP:8001** and **PYTHON SERVER** at **http://YOUR_IP:8080**.

## INSTRUCTIONS
For testing you can use two types of methods
1. CURL
    * Uploading of files for server make sure to use SERVER IP.
      
      > curl -F "file=@/path/to/your/file.png" http://127.0.0.1:8000/cdn

    * Retrieve file for server make sure to use SERVER IP.
      
      > curl -X POST -d "filename=your_file_name.ext" http://127.0.0.1:8000/check
      
2. HTML FORM
    * I built it for testing purpose after all the containers are up and running you can access following for testing

      > http://127.0.0.1 or http://YOUR_IP

3. HOW TO STOP ALL CONTAINERS
     * First press CTRL+C if you are not in deatached mode
      ```shell
       $ docker stop $(docker ps -aq)
       $ docker rm $(docker ps -aq)
      ```


