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
		sh 'docker build -t iamgajanantaur/myapp:latest .'
            }
        }

        stage ('Push docker image to dockerhub') {
            steps {
		sh 'docker push iamgajanantaur/myapp:latest'
            }
        }

        stage ('Create a service') {
            steps {
		sh 'docker service ls --filter name=myappservice --format '{{.Name}}' | grep -w myappservice && docker service rm myappservice; docker service create --name myappservice -p 80:80 --replicas=2 iamgajanantaur/myapp:latest'
            }
        }
    }
}
