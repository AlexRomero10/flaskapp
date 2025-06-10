pipeline {
    environment {
        IMAGEN = "aleromero10/flask-app"   // Sin :latest aquí
        USUARIO = 'aleromero10'
    }
    agent none
    stages {
        stage("test the project") {
            agent {
                docker {
                    image "python:3"
                    args '-u root:root'
                }
            }
            stages {
                stage('Clone') {
                    steps {
                        git branch:'main',url:'https://github.com/AlexRomero10/flaskapp.git'
                    }
                }
                stage('Install') {
                    steps {
                        sh 'pip install -r app/requirements.txt'
                    }
                }
                stage('Test') {
                    steps {
                        sh 'cd app && pytest test_app.py'
                    }
                }
            }
        }
        stage('Creación de la imagen') {
            agent any
            stages {
                stage('Build') {
                    steps {
                        script {
                            newApp = docker.build("$IMAGEN:$BUILD_NUMBER")
                        }
                    }
                }
                stage('Deploy') {
                    steps {
                        script {
                            docker.withRegistry('', USER_DOCKERHUB) {
                                newApp.push()               // Push con tag $BUILD_NUMBER
                                newApp.push("latest")       // Push con tag latest
                            }
                        }
                    }
                }
                stage('Clean Up') {
                    steps {
                        sh "docker rmi $IMAGEN:$BUILD_NUMBER"
                        sh "docker rmi $IMAGEN:latest"    // Limpia también latest para no acumular
                    }
                }
            }
        }
        stage('Despliegue') {
            agent any
            stages {
                stage('Despliegue flaskapp') {
                    steps {
                        sshagent(credentials: ['SSH_KEY']) {
                            sh '''
                                ssh -o StrictHostKeyChecking=no alejandro@art.alejandroromero.cat "
                                cd flaskapp && \
                                git pull && \
                                docker-compose down -v && \
                                docker pull aleromero10/flask-app:latest && \
                                docker-compose up -d"
                            '''
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            mail to: 'aletromp00@gmail.com',
                 subject: "Estado del pipeline: ${currentBuild.fullDisplayName}",
                 body: "El despliegue ${env.BUILD_URL} ha tenido como resultado: ${currentBuild.result}"
        }
    }
}
