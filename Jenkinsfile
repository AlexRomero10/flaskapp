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
                        checkout([$class: 'GitSCM', 
                            branches: [[name: 'main']], 
                            userRemoteConfigs: [[
                                url: 'git@github.com:AlexRomero10/flask-app.git', 
                                credentialsId: 'SSH_USER'
                            ]]
                        ])
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
        stage("Construccion") {
            agent any
            stages {
                stage('CloneAnfitrion') {
                    steps {
                        checkout([$class: 'GitSCM', 
                            branches: [[name: 'main']], 
                            userRemoteConfigs: [[
                                url: 'git@github.com:AlexRomero10/flask-app.git', 
                                credentialsId: 'SSH_USER'
                            ]]
                        ])
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
                stage ('Deploy') {
                    steps {
                        sshagent(['SSH_USER']) {
                            sh '''
                            ssh -o StrictHostKeyChecking=no alejandro@art.alejandroromero.cat << EOF
                            cd flask-app || git clone git@github.com:AlexRomero10/flask-app.git && cd flask-app
                            git pull
                            export NOMBRE="Alejandro"
                            docker-compose up -d --build
                            EOF
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
            subject: "Status of pipeline: ${currentBuild.fullDisplayName}",
            body: "${env.BUILD_URL} has result ${currentBuild.result}" 
        }
    }
}
