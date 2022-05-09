# blue-dynamic-task

Interview task for blue dynamic

## How to run it

### Launch server + MongoDB

    docker-compose up -d

### Launch client

    cd app

    #create venv

    pip install -r requirements.txt
    python client.py

## Notes about the task and possible improvements

First, the task was really interesting. It allows me to discover the gRPC technology. I try to create a clean code for answering this task. Please don't hesitate to send me some feedback about this code, it really interested me to know your opinion. Also you can find some ideas in the notes below.

- The client code can be improved by implementing a real test (like unit tests). With the tests written, I try to test the main functionalities of the microservice. But it's not tests.
- I just separated the code of the client and server in two distinct files for simplicity but I think it can be separating in two different modules.
- I created docker containers for MongoDB and I didn't provide any identification. I did it also for the easiest implementation but it's not secure and in a real implementation it should be configured correctly.
- I noticed a few typos in the db.proto file. I think I fix it (see the db.proto).
