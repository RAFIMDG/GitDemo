pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Installing requirements...'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    echo "===== Running Python Selenium Tests ====="

                    export PATH=$PATH:/opt/homebrew/bin/allure

                    # Check Python version
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

                    # Run tests
                    pytest

                    echo "===== Test Execution Completed ====="
                '''
            }
        }
    }

    post {
        success {
            echo 'Build Successful'
        }
        failure {
            echo 'Build Failed'
        }
    }
}
