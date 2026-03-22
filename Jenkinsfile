pipeline {
	agent any

	stages {

		stage('Validate Formatting') {
			steps {
				echo 'Checking code style and formatting...'
				// Ensure script is executable and run it
				sh 'chmod +x ./scripts/validate_formatting.sh'
				sh './scripts/validate_formatting.sh'
			}
		}

		stage('Deploy to Production') {
			when {
				branch 'master'
			}
			steps {
				withCredentials([string(credentialsId: 'GIT_NOTIFICATION_BOT_POSTGRES_PASSWORD', variable: 'POSTGRES_PASSWORD')]) {
					sh """
					echo 'Deploying to production...'
					// Ensure the script is executable and then run it
					chmod +x ./deploy_to_prod.sh
					echo $POSTGRES_PASSWORD | docker secret create POSTGRES_PASSWORD - || true
					./deploy_to_prod.sh
                    """
				}
			}
		}
	}

	post {
		always {
			script {
				if (fileExists('test_results/test.xml')){
					junit testResults: 'test_results/test.xml'
				}
			}
		}
	}
}