pipeline {
    agent docker-leader
    stages {
        stage ('SCM Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/iamgajanantaur/ditiss-hackathon-sept.git'
            }
        }

        stage ('testing where am i') {
            steps {
		sh 'hostname'
            }
        }

        
    }
}
