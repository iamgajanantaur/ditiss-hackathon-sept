pipeline {
    agent any
    stages {
        stage ('SCM Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/iamgajanantaur/ditiss-hackathon-sept.git'
            }
        }
        
	stage ('login to the docker leader') {
            steps {
                sh 'ssh shuhari@192.168.80.10'
            }
        }

        stage ('testing where am i') {
            steps {
		sh 'hostname'
            }
        }

        
    }
}
