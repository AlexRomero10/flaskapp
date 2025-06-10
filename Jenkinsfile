pipeline {
    agent none

    environment {
        IMAGE_NAME = "flask-app"
        VPS_USER = "alejandro"
        VPS_HOST = "217.160.22.156"
        PROJECT_PATH = "/home/alejandro/app"
        REPO_URL = "https://github.com/AlexRomero10/flaskapp"
    }

    stages {
        stage('Clone Repository') {
            agent any
            steps {
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Install Dependencies') {
            agent {
                docker {
                    image 'python:3.9-alpine'
                    args '-u root:root'
                }
            }
            steps {
                sh '''
                    pip install --upgrade pip
                    ls -la app
                    pip install -r app/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            agent {
                docker {
                    image 'python:3.9-alpine'
                    args '-u root:root'
                }
            }
            steps {
                sh '''
                    pip install --upgrade pip
                    ls -la app
                    pip install -r app/requirements.txt
                    pytest app/test_app.py
                '''
            }
        }

        stage('Build and Push Docker Image') {
            agent any
            steps {
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: 'USER_DOCKERHUB', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                            sh '''
                                echo "Logging in to Docker Hub..."
                                echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USER" --password-stdin

                                echo "Building Docker image..."
                                docker build -t $IMAGE_NAME .

                                echo "Tagging Docker image..."
                                docker tag $IMAGE_NAME $DOCKER_HUB_USER/$IMAGE_NAME:latest

                                echo "Pushing Docker image..."
                                docker push $DOCKER_HUB_USER/$IMAGE_NAME:latest

                                echo "Removing local Docker image..."
                                docker rmi $IMAGE_NAME $DOCKER_HUB_USER/$IMAGE_NAME:latest
                            '''
                        }
                    } catch (Exception e) {
                        echo "Error en la etapa de Docker: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }

        stage('Deploy to VPS') {
            agent any
            steps {
                script {
                    try {
                        withCredentials([sshUserPrivateKey(credentialsId: 'vps-ssh-credentials', keyFileVariable: 'SSH_KEY')]) {
                            sh '''
                                echo "Conectando al VPS..."
                                ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << EOF
                                    echo "Desplegando en el VPS..."
                                    cd $PROJECT_PATH
                                    docker-compose down
                                    docker pull $DOCKER_HUB_USER/$IMAGE_NAME:latest
                                    docker-compose up -d --build
                                    echo "Despliegue finalizado correctamente."
EOF
                            '''
                        }
                    } catch (Exception e) {
                        echo "Error en la etapa de despliegue: ${e.getMessage()}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }
    }

    post {
        always {
            mail to: 'aletromp00@gmail.com',
                 subject: "Pipeline Finalizado",
                 body: "El pipeline de Jenkins ha finalizado. La imagen generada es: $IMAGE_NAME. Revisa los logs para más detalles."
        }
    }
}
