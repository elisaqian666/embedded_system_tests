pipeline {
    agent none

    options {
        timestamps()
        disableConcurrentBuilds(abortPrevious: true)
        buildDiscarder(logRotator(daysToKeepStr: '60', numToKeepStr: '300'))
    }

    parameters {
        string(name: 'PYTHON_EXE', defaultValue: 'C:\\Python312\\python.exe', description: 'Windows Python executable path')
        booleanParam(name: 'PUBLISH_TO_ARTIFACTORY', defaultValue: false, description: 'Enable after configuring Artifactory CA credentials')
    }

    environment {
        ARTIFACTORY_URL = 'https://jfrog.local/artifactory/test-results-local/system-tests'
    }

    stages {
        stage('System tests') {
            options { timeout(time: 1, unit: 'HOURS') }
            agent { node { label 'windows' } }
            steps {
                bat "\"${params.PYTHON_EXE}\" -m venv .venv"
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install -e "%WORKSPACE%\\embedded_framework[dev]"'
                bat '.venv\\Scripts\\python.exe -m pytest -v system_tests\\test_examples\\test_host_pc.py --junitxml=system_tests_results.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, keepProperties: true, testResults: 'system_tests_results.xml'
                    bat '''@echo off
                        powershell -NoProfile -Command "if (Test-Path 'test_logs') { Compress-Archive -Path test_logs -DestinationPath system_tests_logs.zip -Force }"
                    '''
                    writeFile file: 'system_tests_report.json', text: groovy.json.JsonOutput.prettyPrint(groovy.json.JsonOutput.toJson([
                        job: env.JOB_NAME,
                        build: env.BUILD_NUMBER,
                        commit: env.GIT_COMMIT,
                        junit: 'junit.xml',
                        logs: 'system_tests_logs.zip'
                    ]))
                    archiveArtifacts allowEmptyArchive: true, artifacts: 'system_tests_results.xml,system_tests_report.json,system_tests_logs.zip'
                    script {
                        if (params.PUBLISH_TO_ARTIFACTORY) {
                            withCredentials([
                                usernamePassword(credentialsId: 'jfrog-credentials', passwordVariable: 'ARTIFACTORY_PASSWORD', usernameVariable: 'ARTIFACTORY_USERNAME'),
                                file(credentialsId: 'artifactory-ca-certificate', variable: 'ARTIFACTORY_CA_CERT')
                            ]) {
                                bat '''@echo off
                                    set "REPORT_PATH=%ARTIFACTORY_URL%/%BUILD_TAG%"
                                    if exist system_tests_results.xml curl --fail --silent --show-error --cacert "%ARTIFACTORY_CA_CERT%" -u "%ARTIFACTORY_USERNAME%:%ARTIFACTORY_PASSWORD%" -T system_tests_results.xml "%REPORT_PATH%/junit.xml"
                                    if exist system_tests_report.json curl --fail --silent --show-error --cacert "%ARTIFACTORY_CA_CERT%" -u "%ARTIFACTORY_USERNAME%:%ARTIFACTORY_PASSWORD%" -T system_tests_report.json "%REPORT_PATH%/report.json"
                                    if exist system_tests_logs.zip curl --fail --silent --show-error --cacert "%ARTIFACTORY_CA_CERT%" -u "%ARTIFACTORY_USERNAME%:%ARTIFACTORY_PASSWORD%" -T system_tests_logs.zip "%REPORT_PATH%/test_logs.zip"
                                '''
                            }
                        }
                    }
                }
            }
        }
    }
}
