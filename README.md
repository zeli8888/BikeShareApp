# 🚲 BikeShareApp

**BikeShareApp** is a web application designed to help you get the shared bikes information in dublin. You can get real-time updates on bike station availability and current weather conditions, see visualized availability trends for each bike station, and choose routes to bike station based on your location with ease using this app. 🎉

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [🚀 Getting Started](#-getting-started)
  - [🔧 Installation](#-installation)
  - [⚙️ Configuration](#️-configuration)
- [💻 Usage](#-usage)
- [🐛 Common Bugs](#-common-bugs)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [📧 Contact](#-contact)

---

## ✨ Features
- **Feature 1**: Interactive Google Map Interface. 🗺️
- **Feature 2**: Real-time Bikes Information. 🚲
- **Feature 3**: Real-time Weather Information Based on Your Location. ☀️
- **Feature 4**: Visualized Availability Trends for Each Bike Station. 📈
- **Feature 5**: Route Service to Bike Station With Google Map Based on Your Location. 🗺️

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

3. Install the dependencies (make sure using a python virtual environment):
   ```bash
   python -m pip install -r requirements.txt
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
---

## 💻 Usage
Here’s how to use **BikeShareApp**:

1. Run the project:
   ```bash
   python web/BikeShareApplication.py --database {your_database_connection}
   ```
    - your_database_connection is LOCAL, REMOTE, EC2 based on your DB_BIKES_URL configuration, default is LOCAL
    - For REMOTE and EC2 database connection, make sure the RDS and EC2 instance is running and SSH tunnel is established.

2. Load data for availability trends analysis (one-time job, after run the project for the first time):
   ```bash
   python database/load_data.py --database {your_database_connection}
   ```

3. Access the application at `http://127.0.0.1:5000`. For EC2 instance, access at `{EC2_Public_IP}:5000`.

---

## 🐛 Common Bugs

- Package Installation mysqlclient Failed:
    - check https://pypi.org/project/mysqlclient/ to install dependencies for mysqlclient package first.

- Primary Key Not Added in Database:
    - make sure you run the project first before loading data to database.
    - running the project will create tables with primary key in database if tables don't exist.
    - loading data first will result in tables creation without primary key.
    - you can delete the tables and run the project again to fix the problem.

- EC2 Security Setting:
    - make sure your EC2 instance allow the incoming traffic from your local machine (custom ip address).

- Google Map Key Restrictions:
    - make sure your google map key allow the url of this application: `http://127.0.0.1:5000` or `{EC2_Public_IP}:5000` running on EC2.
    - notice that EC2 uses dynamic public ip address, which means you need to update the url in your google map key when restarting EC2 instance.

- Domain Not Secure in Browser With EC2:
    - since this application doesn't run on https, the browser will recognize it as not secure and forbid its location access by default when it runs on EC2.
    - you can bypass this by adding `{EC2_Public_IP}:5000` to the exception list of your browser.
        - For edge, access `edge://flags/#unsafely-treat-insecure-origin-as-secure`
        - For chrome, access `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
    - notice that EC2 uses dynamic public ip address, which means you need to update the url in your exception list when restarting EC2 instance.


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
