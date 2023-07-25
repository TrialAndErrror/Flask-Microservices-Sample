# pAIrFlaskProject

This project is an example of a Flask Microservices app. 
It has a handler app which receives commands, as well as individual flask apps for tracking 
Temperature and Humidity Data, Feeding logs, and Nutramigen formula calculations.

I started this project as an experiment to learn about working with large language models for writing code, but kept working
on it by myself because the platform was very useful for me at the time. I'm still working on some of the core features
in the codebase and cleaning up the code for production deployments, but it stands as an example of a hand-built
microservices architecture with a simple and configurable messaging service to orchestrate communication between the
individual services and the external user.

Building a complex microservices system by hand is **not** recommended for production use. There are many talented and
hard-working individuals making great libraries and frameworks that help make this process easy and relatively painless.
I wanted to do everything myself so that I could learn about the foundation of microservices architecture and discover
the piece of the puzzle that is largely locked away behind abstractions. I plan on building more services like this 
in the future using the established tooling, but the process of working on this project taught me so much about why 
we need messaging queues and what strengths a microservices architecture can bring, as well as how complex the problems
can become when dealing with a naturally asynchronous messaging-based communcation instead of direct calls in Python.


# Usage

To get started quickly, do these steps:

* Rename `env.example` to `.env` and provide the values you would like to use (or leave the defaults)
* `docker compose up` to start all backend flask services
* `yarn && yarn dev` to start the development react frontend

Great, now i've got a bunch of console output and there's a whole heap of servers running. What do I do now?
Well, keep reading to learn about the services that are there and how to interact with them.
Each section has a "Sample Request" section that has working python code that demonstrates how to interact with the
specific service; feel free to throw that in the REPL or a Jupyter Notebook and see what you get back. You can also use
Postman or your favorite request management tools.

# Services

In your browser, you will be able to access the services below:
* Handler
* Feeding Calculator
* Journal
* Temperature

## Handler
This service is the entrypoint for external messages. By sending a message to this service, it will be processed by the
command handler and dispatched to the proper endpoint for further processing. 

Depending on the service that you are addressing, the message format will change.
The message format is as follows:
```python
incoming_json = {
    'command': ('calc' or 'journal'),
    'data': {"insert": "data_here"}
}
```

### Sample Request:
We just need to specify a service and pass along some data, like so:
```python
import requests

data = {"hello": "world"}

request_data = {
    "command": "do_something",
    "data": data
}

handler_port = 55001

response = requests.post(f"http://127.0.0.1:{handler_port}", json=request_data)

print(response.status_code)
print(response.json())
```

So we got a 200 status code, but the JSON is saying there's an error. This is because we successfully sent the message to
the Handler service, but it ran into an error; the "do_something" command is not enabled. Let's look at some of the services
we can call using this message in the sections below.

_Note: If you get an error saying "requests not found", try installing the `dev-requirements.txt` to your virtual environment using `pip install -r dev-requirements.txt`_

## Feeding Calculator
This service helps you to calculate the ratio of powder to water when measuring baby formula. As a first time dad, 
preparing formula at 3 a.m. was a significant challenge. I built this calculator service to make it easy to just read clear
instructions on how to make the formula so that I can properly prepare the formula and get back to bed.

The message format is as follows:
```python
data = {
    'calories': "float",
    'volume': "float",
}
```
`calories` is the target kCal/mL ratio of the prepared formula. With this formula, the starting target kCal/mL ratio was
20, but we increased to 22 over time which increased the complexity of the calculation.

`volume` is the total volume of prepared formula that you want to make. Generally, a scoop of powder will displace ~7 mL
of water, so it can have a significant impact on the volume of prepared formula when making larger batches. Because we tell
the service what the target volume of the formula is, it can tell us how much water to mix with how many scoops in order to
make the formula accurately.

### Sample Request:

The standard label instructions of the formula say that you should mix 1 scoop of powder with 60 mL of water to make 67mL
of prepared formula at 20 kCal/mL. Let's see if the calculator agrees:
```python
import requests

data = {
    "calories": "20",
    "volume": "67",
}

request_data = {
    "command": "feeding_calc",
    "data": data
}

handler_port = 55001

response = requests.post(f"http://127.0.0.1:{handler_port}", json=request_data)

print(response.status_code)
print(response.json())
```

You should see that the calculator confirms the package directions. This should also
be reflected on the service page at `http://127.0.0.1:55003` (or whatever your custom Feeding
Calc port is set to)

## Temperature
This service helps you to monitor your baby's room while they sleep. Our baby had nights where she would start to get
a bit chilly, so we wanted to keep a closer eye on the room temperature to make sure she's comfortable.

This service was created as an endpoint for my custom temperature sensor that I deployed in the room. It was built from 
an Adafruit ESP32-S2 Feather and a temperature sensor, and was configured using CircuitPython to measure temperature every
minute and send the data to the server on the local network.

The message format is as follows:
```python
data = {
    'temperature': "float",
    'humidity': "str"
}
```
`temperature` is a float that returns the current temperature in the room, in Fahrenheit as a float. 

`humidity` is a string that returns the current local humidity in the room as a string, formatted as a two-digit integer.

### Sample Request:

As long as you set up whatever temperature monitor you want to send data from to post json data to the temperature 
endpoint, it will be able to receive the data and display accordingly.
```python
import requests

data = {
    "temperature": 78.6,
    "humidity": "63",
}

request_data = {
    "command": "temperature",
    "data": data
}

handler_port = 55001

response = requests.post(f"http://127.0.0.1:{handler_port}", json=request_data)

print(response.status_code)
print(response.json())
```

You should get a message confirming that you logged a temperature of 78.6 degrees and 63% humidity. This should also
be reflected on the service page at `http://127.0.0.1:55004`

## Journal
Journal is a service for tracking food and water intake of the baby over time. The current functionality is to just log 
the records and display for reference, but it can quickly be expanded to process data over time and extract insights.
The next step for this service is to implement a mobile endpoint or voice assistant integration to capture logs of
food and water without the use of hands, to facilitate record keeping during a messy mealtime.

The message format is as follows:
```python
data = {
    'entry_type': "str",
    'amount': "float",
    'name': "str",
}
```

`entry_type` is a string that represents what type of entry: food or water. The endpoint expects the command to be either 
exactly one of the options: `'food'` or `'drink'`

`amount` is the amount of food or water, and is stored as a float for numeric records. This can be something like `1` for
"1 bottle of water" or `4` for "4 oz of water" or `3` for "3 baby carrots", or anything that works with your system of recordkeeping.

`name` is the name of the food or beverage, along with the unit of measurement, that you want to store. So for "1 bottle
of water", you would enter `"bottle of water`; for "3 baby carrots", you would enter `baby carrots`

### Sample Request:
```python
import requests

data = {
    "entry_type": "food",
    "amount": "3",
    "name": "baby carrots"
}

request_data = {
    "command": "journal",
    "data": data
}

handler_port = 55001

response = requests.post(f"http://127.0.0.1:{handler_port}", json=request_data)

print(response.status_code)
print(response.json())
```

You should get a response confirming your submission, and it should show up on `http://127.0.0.1:55002`

# Frontend
As a more recent addition, there is a React-based frontend application that can interface with the microservices backend
to gather temperature data from the Temperature service. It runs separately outside the container to maintain separation 
of concerns, but is currently in development and there are active branches with improvements and renovations to the 
frontend, including adding support for logging feeding calculations.

# Running as a service
You can also use `docker.feeding_flask_service` with your system's service manager (such as `systemctl`). 
This will enable restarts on failure and generally continuous uptime, managed by the system service manager.

If you run this service on a home server, you can connect directly to the services through other computers or mobile devices
to enable fast access to the services. The page design is intentionally kept simple so that formatting is easy to see
and read no matter your screen size.

## In Progress

* Incorporate react build process into frontend flask service to ensure continuity in deployment
* Move from custom messaging service to a more robust task queue, such as Celery
* Secure and deploy using production settings over https with built-in service implementation
