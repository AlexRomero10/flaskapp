pipeline {
    environment {
        IMAGEN = "aleromero10/flask-app" 
        LOGIN = 'USER_DOCKERHUB'
    }
    agent none
    stages {
        stage("Desarrollo") {
            agent {
                docker { 
                    image "python:3" 
                    args '-u root:root'
                }
            }
            stages {
                stage('Clone') {
                    steps {
                        git branch:'main', url:'https://github.com/AlexRomero10/flaskapp.git'
                    }
                }
                stage('Install') {
                    steps {
                        sh 'pip install -r app/requirements.txt'
                    }
                }
                stage('Test') {
                    steps {
                        sh 'pytest app/test_app.py'
                    }
                }
            }
        }
        stage("Construcción") {
            agent any
            stages {
                stage('CloneAnfitrion') {
                    steps {
                        git branch:'master', url:'https://github.com/AlexRomero10/flaskapp.git'
                    }
                }
                stage('BuildImage') {
                    steps {
                        script {
                            newApp = docker.build "$IMAGEN:latest" 
                        }
                    }
                }
                stage('UploadImage') {
                    steps {
                        script {
                            docker.withRegistry('', LOGIN) {
                                newApp.push()
                            }
                        }
                    }
                }
                stage('RemoveImage') {
                    steps {
                        sh "docker rmi $IMAGEN:latest" 
                    }
                }
                stage ('Despliegue') {
                    agent any
                    stages {
                        stage ('Despliegue en el VPS'){
                            steps {
                                sshagent(credentials : ['SSH_USER']) {
                                    sh '''ssh -o StrictHostKeyChecking=no alejandro@art.alejandroromero.cat " 
                                    cd flaskapp &&
                                    git pull &&
                                    docker-compose down &&
                                    docker pull aleromero10/flask-app:latest &&
                                    docker-compose up -d &&
                                    docker image prune -f
                                    "'''
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            mail to: 'aletromp00@gmail.com',
            subject: "Status of pipeline: ${currentBuild.fullDisplayName}",
            body: "${env.BUILD_URL} has result ${currentBuild.result}" 
        }
    }
}
