# 🚲 BikeShareApp

**[BikeShareApp](https://zeli8888.ddns.net/BikeShareApp/)** is a responsive web application designed to help you get the shared bikes information in dublin. You can get real-time updates on bike station availability and current weather conditions based on your location, see visualized availability prediction, history trends and heat map for each bike station, and plan your routes easily using this app with minimal external API calls. 🎉

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [🎈 Demos](#-demos)
- [🚀 Getting Started](#-getting-started)
  - [🔧 Installation](#-installation)
  - [⚙️ Configuration](#️-configuration)
- [💻 Usage](#-usage)
- [🐛 Common Bugs](#-common-bugs)
- [📂 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [📧 Contact](#-contact)

---

## ✨ Features
- **Feature 1**: Interactive Google Map Interface. 🗺️
- **Feature 2**: Real-time Bikes Information. 🚲
- **Feature 3**: Real-time Weather Information Based on Your Location. ☀️
- **Feature 4**: Visualized History Availability Trends for Each Bike Station. 📊
- **Feature 5**: Visualized 24-Hour Availability Prediction for Each Bike Station. 📈
- **Feature 6**: Visualized Availability Heat Map for Each Bike Station. 📌
- **Feature 7**: Route Suggestions With Google Map Interface. 🛞
- **Feature 8**: Every Fetched Bikes and Weather Data Stored in Database, Minimal External API Calls. 📦
- **Feature 9**: Automatically Update and Remove Old Database Data with Customizable Time Interval and Asynchronous Service. 🔃
- **Feature 10**: Responsive Website suitable for different size of mobile phones, tablets and desktop computers. 📱
---

## 🎈 Demos
![demo1](demo/project-bikeshareapp-1.png) 
![demo2](demo/project-bikeshareapp-2.png) 
![demo3](demo/project-bikeshareapp-3.png) 
---

## 🚀 Getting Started

### 🔧 Installation
To get started with **BikeShareApp**, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/zeli8888/BikeShareApp.git
   ```

2. Navigate to the project directory:
   ```bash
   cd BikeShareApp
   ```

3. Install the dependencies (make sure using a python virtual environment with python=3.11):
   ```bash
   python -m pip install -r requirements.txt
   ```
   For EC2 linux server:
   ```bash
   python -m pip install -r ec2_requirements.txt
   ```

### ⚙️ Configuration
- This application use Jcdecaux, OpenWeather, GoogleMap and MySQL database to offer and store data.
- To configure the project, set the following environment variables first:

    ```env
    JCKEY=your_Jcdecaux_key_here
    OPEN_WEATHER_KEY=your_OpenWeather_key_here
    GOOGLE_MAP_KEY=your_GoogleMap_key_here
    GOOGLE_MAP_ID=your_GoogleMap_Id_here

    LOCAL_DB_BIKES_URL=your_Local_DataBase_Url_here
    REMOTE_DB_BIKES_URL=your_Remote_DataBase_Url_here
    EC2_DB_BIKES_URL=your_EC2_DataBase_Url_here
    ```

- Explanation

    - **JCKEY**: Get your Jcdecaux API key from [here](https://developer.jcdecaux.com/#/home).
    - **OPEN_WEATHER_KEY**: Get your OpenWeather API key from [here](https://openweathermap.org/api).
    - **GOOGLE_MAP_KEY and GOOGLE_MAP_ID**: Get your Google Map API key from [here](https://developers.google.com/maps/gmp-get-started).

    - **DB_BIKES_URL**: You only need to set the url for your way of database connection, example format:
    `mysql+pymysql://{username}:{password}@127.0.0.1:{port}/{database_name}`
    - **LOCAL_DB_BIKES_URL**: For local database connection.
    - **REMOTE_DB_BIKES_URL**: For local RDS database connection using SSH tunnel through EC2 using AWS service.
    - **EC2_DB_BIKES_URL**: For EC2 with RDS database connection using AWS service.

- Optional: Customize settings in [config.py](web/src/config.py) to suit your preferences
---

## 💻 Usage
Here’s how to use **BikeShareApp**:

1. Run the project:
   ```bash
   python -m web.bike_share_application --database {your_database_connection}
   ```
    - your_database_connection is LOCAL, REMOTE, EC2 based on your DB_BIKES_URL configuration, default is LOCAL
    - For REMOTE and EC2 database connection, make sure the RDS and EC2 instance is running and SSH tunnel is established.

2. Initial Data Load: Run the following command to populate the database with availability trends data (only required once, after the first project run):
   ```bash
   python database_oneday_data/load_data.py --database {your_database_connection}
   ```

3. Access the application at `http://127.0.0.1:5000`. For EC2 instance, access at `{EC2_Public_IP}:5000`.

Or, you can run the project using Docker:
1. Configure Docker Env:
    ```env
    DB_PASSWORD=your_database_password
    BIKESHAREAPP_MYSQL_VOLUME=your_mysql_container_volume
    EC2_DB_BIKES_URL=your_database_url
    ```

2. Run MySQL container:

    ```bash
    docker compose -p bikeshareapp -f mysql.yaml up -d --force-recreate
    ```

3. Build Docker Image:
    ```bash
    docker build -t bikeshareapp:${version_you_like} .
    docker tag bikeshareapp:${version_you_like} zeli8888/bikeshareapp:${version_you_like}
    ```

4. Run BikeShareApp container:
    ```bash
    export version=${version_you_like} && docker compose -p bikeshareapp -f bikeshareapp.yaml up -d --force-recreate
    ```

5. (Optional) replace zeli8888 in [Jenkinsfile](Jenkinsfile) and [storage-management-api.yaml](bikeshareapp.yaml) to your docker account for deploy
---

## 🐛 Common Bugs

- Package Installation mysqlclient Failed:
    - check https://pypi.org/project/mysqlclient/ to install dependencies for mysqlclient package first.

- Primary Key Not Added in Database:
    - make sure you run the project first before loading data to database.
    - running the project will create tables with primary key in database if tables don't exist.
    - loading data first will result in tables creation without primary key.
    - you can delete the tables and run the project again to fix the problem.
    - or use docker container to avoid this.

- EC2 Security Setting:
    - make sure your EC2 instance allow the incoming traffic from your local machine (custom ip address).

- Google Map Key Restrictions:
    - make sure your google map key allow the url of this application: `http://127.0.0.1:5000` or `{EC2_Public_IP}:5000` running on EC2.

- Domain Not Secure in Browser With EC2:
    - if this application doesn't run on https, the browser will recognize it as not secure and forbid its location access by default when it runs on EC2.
    - you can bypass this by adding `{EC2_Public_IP}:5000` to the exception list of your browser.
        - For edge, access `edge://flags/#unsafely-treat-insecure-origin-as-secure`
        - For chrome, access `chrome://flags/#unsafely-treat-insecure-origin-as-secure`

---

## 📂 Project Structure
- backlog: files related to product backlog and sprint backlog including burn down chart
- report: files related to the report and introduction video
- database_oneday_data: scraper files related to database including history daily trend data
- machine_learning: files related to train machine learning models for availability prediction in each station.
- web: follow a typical Model-View-Controller (MVC) pattern.
    - [bike_share_application.py](web/bike_share_application.py): The main application file.
    - src: Source code directory.
        - [config.py](web/src/config.py): Configuration file.
        - model: Directory for data model classes, represents the data structure in database.
            - [alerts.py](web/src/model/alerts.py): Model for alerts.
            - [availability.py](web/src/model/availability.py): Model for bike availability.
            - [current.py](web/src/model/current.py): Model for current weather.
            - [daily.py](web/src/model/daily.py): Model for daily weather.
            - [db.py](web/src/model/db.py): SQLAlchemy database instance
            - [hourly.py](web/src/model/hourly.py): Model for hourly weather.
            - [station.py](web/src/model/station.py): Model for bike stations.
        - repository: Directory for data repository classes, used to manipulate data models.
            - [alerts_repository.py](web/src/repository/alerts_repository.py): Repository for alerts.
            - [availability_repository.py](web/src/repository/availability_repository.py): Repository for bike availability.
            - [current_repository.py](web/src/repository/current_repository.py): Repository for current weather.
            - [daily_repository.py](web/src/repository/daily_repository.py): Repository for daily weather.
            - [hourly_repository.py](web/src/repository/hourly_repository.py): Repository for hourly weather.
            - [station_repository.py](web/src/repository/station_repository.py): Repository for bike stations.
        - service: Directory for service classes, used to perform complex operations for business logic.
            - [bikes_service.py](web/src/service/bikes_service.py): Service for bike-related logic.
            - [prediction_service.py](web/src/service/prediction_service.py): Service for prediction-related logic.
            - [weather_service.py](web/src/service/weather_service.py): Service for weather-related logic.
        - controller: Directory for controller, used to handle incoming requests.
            - [bikes_controller.py](web/src/controller/bikes_controller.py): Controller for bike-related logic.
            - [prediction_controller.py](web/src/controller/prediction_controller.py): Controller for prediction-related logic.
            - [weather_controller.py](web/src/controller/weather_controller.py): Controller for weather-related logic.
    - static: Static assets directory.
        - css: Directory for CSS files.
            - [index.css](web/static/css/index.css): Styles for the index page.
            - [map.css](web/static/css/map.css): Styles for map-related pages.
            - [sidebar.css](web/static/css/sidebar.css): Styles for the sidebar.
            - [bike-trend.css](web/static/css/bike-trend.css): Styles for bike trend-related pages.
            - [prediction.css](web/static/css/prediction.css): Styles for prediction-related pages.
            - [route.css](web/static/css/route.css): Styles for route-related pages.
            - [stations.css](web/static/css/stations.css): Styles for station-related pages.
            - [weather.css](web/static/css/weather.css): Styles for weather-related pages.
        - js: Directory for JavaScript files.
            - [index.js](web/static/js/index.js): JavaScript code for the index page.
            - [map.js](web/static/js/map.js): JavaScript code for map-related pages.
            - [sidebar.js](web/static/js/sidebar.js): JavaScript code for the sidebar.
            - [bikeTrend.js](web/static/js/bikeTrend.js): JavaScript code for bike trend-related pages.
            - [prediction.js](web/static/js/prediction.js): JavaScript code for prediction-related pages.
            - [route.js](web/static/js/route.js): JavaScript code for route-related pages.
            - [stations.js](web/static/js/stations.js): JavaScript code for station-related pages.
            - [userLocation.js](web/static/js/userLocation.js): JavaScript code for user location-related functionality.
            - [weather.js](web/static/js/weather.js): JavaScript code for weather-related pages.
        - resources: Directory for static resources.
            - [beste-e-bike-app-von-powunity-1536x864.webp](web/static/resources/beste-e-bike-app-von-powunity-1536x864.webp): A static image file used as a background image.
    - templates: HTML template directory.
        - [index.html](web/templates/index.html): The main index page template.
        
---

## 🤝 Contributing
We welcome contributions! 🎉 If you'd like to contribute, please follow these steps:

1. Fork the repository.

2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Commit your changes:
   ```bash
   git commit -m "Add your awesome feature"
   ```

4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a pull request. 🚀

---

## 📝 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details. 🐜

---

## 📧 Contact
If you have any questions or feedback, feel free to reach out:

- **Email**: zeli8888@outlook.com 📩 Sabrina.ragulova@ucdconnect.ie 📩 anju@ucdconnect.ie 📩
- **GitHub Issues**: [Open an Issue](https://github.com/zeli8888/BikeShareApp/issues) 🐛

---

Made with ❤️ by [Ze Li](https://github.com/zeli8888). Happy coding! 🎉
