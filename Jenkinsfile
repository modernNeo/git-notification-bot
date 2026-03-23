pipeline {
	agent any

	stages {

		stage('Validate Formatting') {
			steps {
				echo 'Checking code style and formatting...'
				sh 'chmod +x ./scripts/validate_formatting.sh'
				sh './scripts/validate_formatting.sh'
			}
		}

		stage('Deploy to Production') {
			when {
				branch 'master'
			}
			steps {
                script {
                    withCredentials([string(credentialsId: 'GIT_NOTIFICATION_BOT_POSTGRES_PASSWORD', variable: 'POSTGRES_PASSWORD'),
                                    string(credentialsId: 'GIT_NOTIFICATION_BOT_DATABASE_URL', variable: 'DATABASE_URL')]) {
                            sh '''
                            export POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"
                            export DATABASE_URL="${DATABASE_URL}"

                            echo 'Deploying to production...'
                            # Ensure the script is executable and then run it
                            chmod +x ./.ci/deploy_to_prod.sh


                            ./.ci/deploy_to_prod.sh
                            '''
                    }
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