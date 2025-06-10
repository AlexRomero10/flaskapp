pipeline {
    agent none

    environment {
        IMAGE_NAME = "flask-app"  // Nombre de la imagen de Docker
        VPS_USER = "alejandro"  // Usuario del VPS
        VPS_HOST = "217.160.22.156"  // IP del VPS
        PROJECT_PATH = "/home/alejandro/app"  // Ruta donde está docker-compose en el VPS
        REPO_URL = "https://github.com/AlexRomero10/flaskapp"  // URL del repositorio
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
                    ls -la app  # Verificar que requirements.txt está presente
                    pip install -r app/requirements.txt  # Cambiar la ruta de requirements.txt
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
                    ls -la app  # Verificar que test_app.py está presente
                    pip install -r app/requirements.txt  # Cambiar la ruta de requirements.txt
                    pytest app/test_app.py  # Apuntar al archivo de prueba correcto
                '''
            }
        }

        stage('Build and Push Docker Image') {
            agent any
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                        sh '''
                            docker build -t $IMAGE_NAME .
                            echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USER" --password-stdin
                            docker tag $IMAGE_NAME $DOCKER_HUB_USER/$IMAGE_NAME:latest
                            docker push $DOCKER_HUB_USER/$IMAGE_NAME:latest
                            docker rmi $IMAGE_NAME
                        '''
                    }
                }
            }
        }

        stage('Deploy to VPS') {
            agent any
            steps {
                script {
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
