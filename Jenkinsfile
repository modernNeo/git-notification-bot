pipeline {
	agent any

	stages {

		stage('Validate Formatting') {
			steps {
				echo 'Checking code style and formatting...'
				sh '''
				    chmod +x ./scripts/validate_formatting.sh
				    export DEVELOPMENT_MODE=True
				    ./scripts/validate_formatting.sh
				'''
			}
		}

		stage('Deploy to Production') {
			when {
				branch 'master'
			}
			steps {
                script {
                    withCredentials([
                        string(credentialsId: 'GIT_NOTIFICATION_BOT_POSTGRES_DB', variable: 'POSTGRES_DB'),
                        string(credentialsId: 'GIT_NOTIFICATION_BOT_POSTGRES_USER', variable: 'POSTGRES_USER'),
                        string(credentialsId: 'GIT_NOTIFICATION_BOT_POSTGRES_PASSWORD', variable: 'POSTGRES_PASSWORD'),
                        string(credentialsId: 'GIT_NOTIFICATION_BOT_DATABASE_URL', variable: 'DATABASE_URL'),
                        string(credentialsId: 'GIT_NOTIFICATION_BOT_DJANGO_ALLOWED_HOSTS', variable: 'DJANGO_ALLOWED_HOSTS'),
                        string(credentialsId: 'GIT_NOTIFICATION_BOT_SLACK_CLIENT_ID', variable: 'SLACK_CLIENT_ID'),
                        string(credentialsId: 'GIT_NOTIFICATION_BOT_SLACK_CLIENT_SECRET', variable: 'SLACK_CLIENT_SECRET')]) {
                            sh '''
                            export POSTGRES_DB="${POSTGRES_DB}"
                            export POSTGRES_USER="${POSTGRES_USER}"
                            export POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"

                            export DATABASE_URL="${DATABASE_URL}"
                            export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS}"
                            export SLACK_CLIENT_ID="${SLACK_CLIENT_ID}"
                            export SLACK_CLIENT_SECRET="${SLACK_CLIENT_SECRET}"

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