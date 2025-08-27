pipeline{

  agent any
  environment {
    version = '1.0'
    DB_PASSWORD = credentials('DB_PASSWORD')
    BIKESHAREAPP_MYSQL_VOLUME = credentials('BIKESHAREAPP_MYSQL_VOLUME')
    OPEN_WEATHER_KEY = credentials('OPEN_WEATHER_KEY')
    GOOGLE_MAP_KEY = credentials('GOOGLE_MAP_KEY')
    GOOGLE_MAP_ID = credentials('GOOGLE_MAP_ID')
    JCKEY = credentials('JCKEY')
    EC2_DB_BIKES_URL = credentials('EC2_DB_BIKES_URL')
  }

  stages{

    stage('Start Database'){
      steps{
        sh script: 'docker stop bikeshareapp-mysql', returnStatus: true
        sh script: 'docker rm bikeshareapp-mysql', returnStatus: true
        sh 'docker compose -p bikeshareapp -f mysql.yaml up -d --force-recreate'
      }
    }

    stage('Wait for Database to Start'){
      steps{
        sh '''#!/bin/sh
            max_attempts=60
            attempt=1
            until (docker inspect bikeshareapp-mysql --format '{{.State.Running}}' | grep -q true &&
                   docker exec bikeshareapp-mysql mysqladmin ping -h localhost --silent) || [ $attempt -gt $max_attempts ];
            do
                echo "Attempt $attempt/$max_attempts - Database not ready yet"
                sleep 1
                attempt=$((attempt+1))
            done
            if [ $attempt -gt $max_attempts ]; then
                echo "Database did not start within $max_attempts seconds!"
                exit 1
            fi'''
      }
    }

    stage('Build Docker Image'){
      steps{
        sh "docker build -t bikeshareapp:${version} ."
        sh "docker tag bikeshareapp:${version} zeli8888/bikeshareapp:${version}"
        sh "docker push zeli8888/bikeshareapp:${version}"
        sh "docker image prune -f"
      }
    }

    stage('Run Docker Container'){
      steps{
        sh script: 'docker stop bikeshareapp', returnStatus: true
        sh script: 'docker rm bikeshareapp || true', returnStatus: true
        sh "export version=${version} && docker compose -p bikeshareapp -f bikeshareapp.yaml up -d --force-recreate"
      }
    }
  }
}