pipeline {
    agent { label 'leader' }

    stages {
        stage ('SCM Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/iamgajanantaur/ditiss-hackathon-sept.git'
            }
        }

        stage ('Build') {
            steps {
                sh 'docker build -t iamgajanantaur/myflaskapp:latest .'
            }
        }

        stage ('Push docker image to dockerhub') {
            steps {
                sh 'docker push iamgajanantaur/myflaskapp:latest'
            }
        }

        stage ('Remove existing service') {
            steps {
                sh 'docker service rm myflaskappservice'
            }
        }

        stage ('Create a service') {
            steps {
                sh 'docker service create --name myflaskappservice -p 80:4000 --replicas=2 iamgajanantaur/myflaskapp:latest'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }

        success {
            echo 'Deployment successful!'
        }

        failure {
            echo 'Deployment failed!'
        }
    }
}
