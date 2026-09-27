pipeline {
    agent any

    tools {
        allure 'allure'
    }

    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox', 'edge'],
            description: 'Browser to run tests'
        )
        choice(
            name: 'ENV',
            choices: ['qa', 'staging', 'prod'],
            description: 'Environment to test against'
        )
        string(
            name: 'RETRY_COUNT',
            defaultValue: '2',
            description: 'Number of test retries'
        )
        string(
            name: 'MARKERS',
            defaultValue: '',
            description: 'Pytest markers (e.g. smoke, regression, login)'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run browser in headless mode'
        )
        string(
            name: 'PARALLEL_WORKERS',
            defaultValue: '1',
            description: 'Number of parallel workers (pytest-xdist)'
        )
    }

    environment {
        PYTHONPATH = "${WORKSPACE}"
        ENV = "${params.ENV}"
        BROWSER = "${params.BROWSER}"
        HEADLESS = "${params.HEADLESS}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    echo "===== Setting up Python environment ====="
                    python3 --version
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    echo "===== Setup Complete ====="
                '''
            }
        }

        stage('Run Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    script {
                        def markerFlag = params.MARKERS ? "-m '${params.MARKERS}'" : ""
                        def parallelFlag = params.PARALLEL_WORKERS.toInteger() > 1 ?
                            "-n ${params.PARALLEL_WORKERS}" : ""

                        sh """
                            . venv/bin/activate
                            echo "===== Running Tests ====="
                            echo "Browser: ${params.BROWSER}"
                            echo "Environment: ${params.ENV}"
                            echo "Headless: ${params.HEADLESS}"
                            echo "Markers: ${params.MARKERS ?: 'all'}"
                            echo "Workers: ${params.PARALLEL_WORKERS}"

                            pytest \\
                                --browser=${params.BROWSER} \\
                                --env=${params.ENV} \\
                                --reruns ${params.RETRY_COUNT} \\
                                --reruns-delay 2 \\
                                --alluredir=allure-results \\
                                --clean-alluredir \\
                                ${markerFlag} \\
                                ${parallelFlag} \\
                                -v

                            echo "===== Test Execution Complete ====="
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**', fingerprint: true
            archiveArtifacts artifacts: 'reports/screenshots/**', allowEmptyArchive: true
            archiveArtifacts artifacts: 'logs/**', allowEmptyArchive: true

            allure(
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            )
        }

        success {
            echo "✅ Build Successful — ${params.BROWSER} / ${params.ENV}"
        }

        failure {
            echo "❌ Build Failed — ${params.BROWSER} / ${params.ENV}"
        }

        cleanup {
            cleanWs()
        }
    }
}
