pipeline {
    agent any

    tools {
        // Name should match the Allure Commandline tool configured in Jenkins
        allure 'allure'
    }
    parameters {
            string(
                name: 'RETRY_COUNT',
                defaultValue: '2',
                description: 'Number of test retries'
            )
        }

    stages {

        stage('Checkout') {
            steps {
                echo 'Installing requirements...'
                checkout scm
            }
        }

        stage('Run Selenium Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        echo "===== Running Python Selenium Tests ====="

                        python3 --version

                        # Create virtual environment
                        python3 -m venv venv

                        # Activate virtual environment
                        . venv/bin/activate

                        # Upgrade pip
                        pip install --upgrade pip

                        # Install dependencies
                        pip install -r requirements.txt

                        export PYTHONPATH=$PWD

                        # Run tests and generate Allure results
                        pytest -v --reruns ${RETRY_COUNT} --reruns-delay 2 --alluredir=allure-results --clean-alluredir
                        echo "===== Test Execution Completed ====="
                    '''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**', fingerprint: true

            allure(
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            )
        }

        success {
            echo 'Build Successful'
        }

        failure {
            echo 'Build Failed'
        }
    }
}