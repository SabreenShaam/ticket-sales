### Objective/Business Requirement

Develop key components of a ticket sales system with distinct user tiers and link generation rules.

The system categorizes users into three tiers with varying privileges for ticket purchasing.

The system should consist of two services (“Ticketing Service” and “Rule Service”) communicating with each other through a message broker type of connection.

Ticketing Service should be able to handle http requests from our users (curl, Postman, Insomnia, etc). This service should have Bearer token authorization.

After requesting a link - based on user role and login status - the message should be sent to “Rule Service”, where it will be validated against pre-existing rules according to the role.

The “Rule Service” should be validating the incoming messages and create an accessToken based on which access link for the Ticketing Service will be created.

The link should be obtained by any user through `GET` [example.com/check_ticketing_link](https://) route according to the abilities of the user roles described above.

#### User Groups:
 - Premium Users:
   - Can login and request a link. Link will instantly grant access to page to buy a ticket.
 - Standard Users:
   - Can login and request a link. Link will grant access after 10 minutes.
 - Not Registered Users:
   - Ability to get an access page with ticket sale will be available at 00:00(UTC) the next day. 


#### Rule example: 
```json 
{
  "premium": "instant", 
  "standard": "10 minutes", 
  "default": "start of the next day"
} 
```

#### Link example which is sent to user:
[example.com/buy_ticket/accessToken](https://)


 - #### Ticketing Service:
   - Endpoints:

     - `POST` [example.com/login](https://)
     - `GET` [example.com/request_for_ticketing_link](https://)
     - `GET` [example.com/check_ticketing_link](https://) (returns the link if ready)
     - `GET` [example.com/buy_ticket/accessToken](https://) (validates token and returns a response (simple json with text `Welcome to the ticket page` is enough) or a message with waiting time until ticket page will be available)

   - Communications:
     - Produces message with info which is required for validating user against the rules
     - Consumes message with info which is required for sending user access link
     
 - #### Rule Service:
     - Communications: 
       - Consumes message with info which is required for validating user against the rules 
       - Produces message with info which is required for sending user access link

# Project Setup Guidelines

#### Assumptions

- user should give their role when do register.
- can buy the ticket only once by using generated link.
- each [/request_for_ticketing_link](https://) and [/check_ticketing_link](https://) should be sent with request_id.
- "Ticket Service" token validity period is one hour for registered user.
- user can not interact with "Rule Service" it's only for internal use.
- unregistered/default user will be identified by using specific request_id.
- rule can be store in a file or db as a hard coded value in "RuleService".

### Technologies Used

- python flask framework
- python-kafka streaming with 2 topics
- mysql db
- pytest

#### Covered
- 2 python services and 3 infrastructure(2 mysql services & a kafka service) services.
- python best practices as much possible.
- user registration implemented with minor validation.
- links inactivating feature for default user after 2 hours was implemented.
- pytest added for happy path.

#### To Setup and Start

1) ### Kafka Service
- open the project folder using pycharm/vscode etc.
- open the docker-compose.yaml file resides in "KafkaService" folder and replace KAFKA_ADVERTISED_HOST_NAME: 192.168.1.101 ip with your local machine ip under the environment section and do save changes.
- navigate inside the "KafkaService" directory via terminal.
- type 'docker-compose build' and hit enter.
- if build success, type 'docker-compose up' and hit enter, this will start the kafka server with 2 topics.
- Kafka sever will be started successfully with Zookeper.
2) ### Rule Service
- open app/utility/constants.py file in "RuleService", modify KAFKA_SERVER_URL = '192.168.1.101:9092' with your above used same ip and save changes.
- navigate inside the "RuleService" directory via terminal.
- type 'docker-compose build' and hit enter.
- if build success, type 'docker-compose up' and hit enter.
- this will start the "RuleService" with mysql DB.
3) ### Ticket Service
- open app/utility/constants.py file in "TicketService", modify KAFKA_SERVER_URL = '192.168.1.101:9092' with your above used same ip and save changes.
- navigate inside the "TicketService" directory via terminal.
- type 'docker-compose build' and hit enter.
- if build success, type 'docker-compose up' and hit enter.
- this will start the "RuleService" with mysql DB.

#### Note-1: 
- If you experience the 'mysql connection refused or bind-address or db not exists' issue, down the server using 'docker-compose down' and restart after some time since we are trying to use 2 different mysql instance from the local machine.

#### Note-2: If you want to run without docker
- still you can use this dockerized 'KafkaService' using 'docker-compose up' command before that you need to configure hosts with your local machine's ip in all 3 services same as mentioned above.
- make app directory as a root directory in both 'Ticket' and 'Rule' service.
- create virtual env using python3.9 inside the app directory in each service.
- install all the packages mentioned in the requirements.txt
- create relevant mysql db and configure in 2 python services. (the code is already there you need to uncomment and modify as per your environment)
- you can run each services using 'python app.py' command.
- one service will run on port 5000 and other one with 5001

##### Note-3
- Kafka sever should be up and run before 'Rule' and 'Ticket' service, otherwise it will throw broker not available error.

## Sample Request and Response

1) ### Premium User
#### Registration
Request

`curl --location --request POST 'http://localhost:5000/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"john@gmail.com",
    "username":"john",
    "password":"1q2W3E4r",
    "role": "premium"
}'`

Response
`{
    "message": "Account created successfully"
}`

#### Login
Request

`curl --location --request POST 'http://localhost:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"john",
    "password":"1q2W3E4r"
}'`

Response

`{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ4ODYzOSwianRpIjoiNDBiZTgzNjEtODRiNi00ZjJlLThhMjQtNDBkNTQ5ZTQ2MjQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzAzNDg4NjM5LCJjc3JmIjoiNzA3MDkzMTUtZDZjNS00ODM3LTllNzgtZjgxZDg2YjE4MDFlIiwiZXhwIjoxNzAzNDkyMjM5fQ.5aG8KF53iBOlzMnAAtSJRankZSj_BeoLE6-BIiNmXOQ",
    "message": "Login Success"
}`


#### Request for Ticketing Link
Request

`curl --location --request GET 'http://localhost:5000/request_for_ticketing_link' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ4ODYzOSwianRpIjoiNDBiZTgzNjEtODRiNi00ZjJlLThhMjQtNDBkNTQ5ZTQ2MjQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzAzNDg4NjM5LCJjc3JmIjoiNzA3MDkzMTUtZDZjNS00ODM3LTllNzgtZjgxZDg2YjE4MDFlIiwiZXhwIjoxNzAzNDkyMjM5fQ.5aG8KF53iBOlzMnAAtSJRankZSj_BeoLE6-BIiNmXOQ' \
--data-raw ''`

Response

`{
    "message": "Your request is created successfully",
    "request_id": "412816fb-efe7-4af9-96a1-e159d4e30baf"
}`

####  Check Ticketing Link
Request

`curl --location --request GET 'http://localhost:5000/check_ticketing_link?request_id=412816fb-efe7-4af9-96a1-e159d4e30baf' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ4ODYzOSwianRpIjoiNDBiZTgzNjEtODRiNi00ZjJlLThhMjQtNDBkNTQ5ZTQ2MjQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzAzNDg4NjM5LCJjc3JmIjoiNzA3MDkzMTUtZDZjNS00ODM3LTllNzgtZjgxZDg2YjE4MDFlIiwiZXhwIjoxNzAzNDkyMjM5fQ.5aG8KF53iBOlzMnAAtSJRankZSj_BeoLE6-BIiNmXOQ' \
--data-raw ''`

Response

`{
    "link": "http://localhost:5000/buy_ticket/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ4OTAyMiwianRpIjoiNGFiYmQ4N2QtZGQyMi00NWVjLTg4ZTUtNmJhOTgxZTRiYjMwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNzAzNDg5MDIyLCJjc3JmIjoiMzMwNmM1ODAtYzhiYS00MTc1LWJmMjMtYTY2YTM1M2YzM2I5IiwiZXhwIjoxNzAzNDg5OTIyfQ.yeFY4GIv0NSspWN-O9K7bdGkzv_1lHonmk9BeUUUdag?request_id=412816fb-efe7-4af9-96a1-e159d4e30baf",
    "message": "Link Generated Successfully"
}`

#### Buy Ticket
Request

`curl --location --request GET 'http://localhost:5000/buy_ticket/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ5MDkzMSwianRpIjoiNDNkOTIxMmItM2RjYi00YzRkLWE0NmUtZTBjZWJkZjdjZjcwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNzAzNDkwOTMxLCJjc3JmIjoiNzRjZTRjZTYtMzdkNy00NjQ2LTkwODAtNzMzYzM5Nzg0MDVjIiwiZXhwIjoxNzAzNDk0NTMxfQ.Mpo44-e093xDsJtPdNM5ElOyqatYHY977JegoAL62Vs?request_id=412816fb-efe7-4af9-96a1-e159d4e30baf'`

Response

`{
    "message": "Welcome to the Ticket Page"
}`

***********************************************************************

2) ### Standard User
#### Registration
Request

`curl --location --request POST 'http://localhost:5000/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"cena@gmail.com",
    "username":"cena",
    "password":"1q2W3E4r",
    "role": "standard"
}'`

Response
`{
    "message": "Account created successfully"
}`

#### Login
Request

`curl --location --request POST 'http://localhost:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"cena",
    "password":"1q2W3E4r"
}'`

Response

`{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ4ODYzOSwianRpIjoiNDBiZTgzNjEtODRiNi00ZjJlLThhMjQtNDBkNTQ5ZTQ2MjQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzAzNDg4NjM5LCJjc3JmIjoiNzA3MDkzMTUtZDZjNS00ODM3LTllNzgtZjgxZDg2YjE4MDFlIiwiZXhwIjoxNzAzNDkyMjM5fQ.5aG8KF53iBOlzMnAAtSJRankZSj_BeoLE6-BIiNmXOQ",
    "message": "Login Success"
}`


#### Request for Ticketing Link
Request

`curl --location --request GET 'http://localhost:5000/request_for_ticketing_link' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ4ODc0NSwianRpIjoiMjg4MzlkNTktZjA5Mi00Yzg5LTljNWEtNDcwOGUzNWU4M2Y4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNzAzNDg4NzQ1LCJjc3JmIjoiNzgzYzllMGEtNTczNy00NWUxLThiYjItODExYzMzM2YxNDFiIiwiZXhwIjoxNzAzNDkyMzQ1fQ.OtXZb22VJdUGX-Qc6QSVyzTFBVEbiVWvcaHB-1LJgM0' \
--data-raw ''`

Response

`{
    "message": "Your request is created successfully",
    "request_id": "c2a8e4b1-3cf2-4177-841f-58f21213ec77"
}`

####  Check Ticketing Link (will be available after 10 minutes)
Request

`curl --location --request GET 'http://localhost:5000/check_ticketing_link?request_id=c2a8e4b1-3cf2-4177-841f-58f21213ec77' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ4ODc0NSwianRpIjoiMjg4MzlkNTktZjA5Mi00Yzg5LTljNWEtNDcwOGUzNWU4M2Y4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNzAzNDg4NzQ1LCJjc3JmIjoiNzgzYzllMGEtNTczNy00NWUxLThiYjItODExYzMzM2YxNDFiIiwiZXhwIjoxNzAzNDkyMzQ1fQ.OtXZb22VJdUGX-Qc6QSVyzTFBVEbiVWvcaHB-1LJgM0' \
--data-raw '''`

Response

`{
    "message": "Your link is not ready yet please wait"
}`

#### Buy Ticket (will be accessible after 10 minutes i.e. here we are using above check_ticketing_link response as a request)
Request

`curl --location --request GET 'http://localhost:5000/buy_ticket/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ5MDkzMSwianRpIjoiNDNkOTIxMmItM2RjYi00YzRkLWE0NmUtZTBjZWJkZjdjZjcwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNzAzNDkwOTMxLCJjc3JmIjoiNzRjZTRjZTYtMzdkNy00NjQ2LTkwODAtNzMzYzM5Nzg0MDVjIiwiZXhwIjoxNzAzNDk0NTMxfQ.Mpo44-e093xDsJtPdNM5ElOyqatYHY977JegoAL62Vs?request_id=c2a8e4b1-3cf2-4177-841f-58f21213ec77'`

Response

`{
    "message": "Welcome to the Ticket Page"
}`

***********************************************************************

3) ### Default/Unregistered User
#### Registration
No Registration
#### Login
No Login


#### Request for Ticketing Link
Request

`curl --location --request GET 'http://localhost:5000/request_for_ticketing_link' \
--data-raw ''`

Response

`{
    "message": "Your request is created successfully",
    "request_id": "7a7d8b9c-6b83-4174-afe1-014775912f0c"
}`

####  Check Ticketing Link ( link will be available on next day at 00:00:00 UTC)
Request

`curl --location --request GET 'http://localhost:5000/check_ticketing_link?request_id=7a7d8b9c-6b83-4174-afe1-014775912f0c' \
--data-raw ''`

Response

`{
    "message": "Your link is not ready yet please wait"
}`

#### Buy Ticket (will be accessible on next day at 00:00:00 UTC i.e.  here we are using above check_ticketing_link response as a request)
Request

`curl --location --request GET 'http://localhost:5000/buy_ticket/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzQ5MDkzMSwianRpIjoiNDNkOTIxMmItM2RjYi00YzRkLWE0NmUtZTBjZWJkZjdjZjcwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNzAzNDkwOTMxLCJjc3JmIjoiNzRjZTRjZTYtMzdkNy00NjQ2LTkwODAtNzMzYzM5Nzg0MDVjIiwiZXhwIjoxNzAzNDk0NTMxfQ.Mpo44-e093xDsJtPdNM5ElOyqatYHY977JegoAL62Vs?request_id=7a7d8b9c-6b83-4174-afe1-014775912f0c'`

Response

`{
    "message": "Welcome to the Ticket Page"
}`