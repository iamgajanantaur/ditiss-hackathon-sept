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
	
	stage ('Remove existing service')
	{
	    steps {
	        sh 'docker service rm myflaskappservice'

            }
	}

        stage ('Create a service') {
            steps {
		sh 'docker service create --name myflaskappservice -p 80:4000 --replicas=2 iamgajanantaur/myflaskapp:latest'
            }
        }

	post {
        success {
            emailext (
                subject: "SUCCESS: Job '${env.JOB_NAME}' build ${env.BUILD_NUMBER}",
                body: "Good news! The build succeeded.",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        failure {
            emailext (
                subject: "FAILURE: Job '${env.JOB_NAME}' build ${env.BUILD_NUMBER}",
                body: "Oops! The build failed.",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
    }
    }
}
