pipeline {
    agent any

    environment {
        IMAGE_NAME = "ME-CFS-Depression-Detection"
        DOCKER_TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image') {
            steps {
                echo 'Building Docker image...'
                bat "docker build -t $IMAGE_NAME:$DOCKER_TAG ."
            }
        }

        stage('Run container') {
            steps {
                echo 'Running container...'
                bat "docker run -d -p 8501:8501 -p 8000:8000 $IMAGE_NAME:$DOCKER_TAG"
            }
        }

        // Optional: Push to Docker Hub
        /*
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh "echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin"
                    sh "docker tag $IMAGE_NAME:$DOCKER_TAG $DOCKERHUB_USER/$IMAGE_NAME:$DOCKER_TAG"
                    sh "docker push $DOCKERHUB_USER/$IMAGE_NAME:$DOCKER_TAG"
                }
            }
        }
        */
    }

    post {
        success {
            echo 'Pipeline executed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
