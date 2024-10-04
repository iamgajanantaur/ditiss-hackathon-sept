pipeline {
    agent { label 'leader' }

    stages {
        
	stage ('SCM Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/iamgajanantaur/ditiss-hackathon-sept.git'
            }
        }

        stage ('Builld') {
            steps {
		sh 'docker build -t iamgajanantaur/myapp:latest .'
            }
        }

        stage ('Push Image to dockerhub') {
            steps {
		sh 'docker push iamgajanantaur/myapp:latest'
            }
        }
        
    }
}
