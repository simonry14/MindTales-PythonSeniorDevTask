# MindTales-PythonSeniorDevTask
My Submission for the MindTales Senior Dev Task. Employee Restaurant Poling Backend and API

## API Features

1. Authentication 
2. Creating restaurant
3. Uploading menu for restaurant every day - Only one menu is uploaded per day per restaurant
4. Creating an employee
5. Getting current day menu
6. Voting for restaurant menu (for APP Version 1.0 each user only votes for one menu. For version 1.1 each user gets to vote for 3 menus awarding 3,2,1 points respectively)
7. Getting results for the current day. The winner is restaurant menu with the most number of votes


### Dependencies Used

1. Django==4.0.6
2. djangorestframework==3.13.1
3. drf_yasg==1.21.0
4. psycopg2-binary==2.9.1


## API Endpoints

The table below shows the various end points for the API. All endpoints require a token for authentication. The API call should have the token in Authorization header.

    `{'Authorization': 'Toekn': <token>}`

Call for the vote API also requires an Accept-Version entry in the header to specify what app version the employee is using. For version 1.0 to vote for menu with id 1, the follwoing json is sent in the body {"menu_id" : 1} and for version 1.1 to vote for menus with ids 1 (3 points), 6(2 points), 8(1 point) the following json is sent {"menu_ids":[1,6,8]}


| EndPoint                                        |                       Functionality |
| ------------------------------------------------|-----------------------------------: |
| POST /register                                  |                Register a user      |
| POST /login                                     |                     User login      |
| POST /create_employee                           |         Creates a new employee      |
| POST /create_restaurant                         |         Creates a new Restaurant    |
| POST /create_menu                               |            Cretes a new menu        |
| GET /employees                                  |           List all employees        |
| GET /restaurants                                |            List all restaurants     |
| GET /menus                                      |            List all menus           |
| GET /today-menus                                |   List all menus of current day     |
| POST /vote                                      |                   Vote for menu     |
| GET /results                                    |         Show results of the day     |

## Running API
Run the docker-compose up command from the top level directory of the project.