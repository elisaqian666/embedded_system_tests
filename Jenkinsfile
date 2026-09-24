@Library('oxygenlib@master')_

pipeline {
    agent none

    options {
        timestamps()
        disableConcurrentBuilds(abortPrevious: true)
        buildDiscarder(logRotator(daysToKeepStr: '60', numToKeepStr: '300'))
    }

    environment {
        ARTIFACTORY_URL = 'https://jfrog.local/artifactory/test-results-local/system-tests'
    }

    stages {
        stage('System tests') {
            options { timeout(time: 1, unit: 'HOURS') }
            agent { node { label 'windows&&BEL' } }
            steps {
                script {
                    pyVenvWrapper.withUvEnv(venvName: 'embedded_framework_system_tests', tentoBranch: 'latest_release') {
                        bat '''@echo off
                            python -m pip install -e "%WORKSPACE%\\embedded_framework[dev]"
                            python -m pytest -v system_tests --junitxml=system_tests_results.xml
                        '''
                    }
                }
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
                    withCredentials([usernamePassword(credentialsId: 'jfrog-credentials', passwordVariable: 'ARTIFACTORY_PASSWORD', usernameVariable: 'ARTIFACTORY_USERNAME')]) {
                        bat '''@echo off
                            set "REPORT_PATH=%ARTIFACTORY_URL%/%BUILD_TAG%"
                            if exist system_tests_results.xml curl --fail --silent --show-error -u "%ARTIFACTORY_USERNAME%:%ARTIFACTORY_PASSWORD%" -T system_tests_results.xml "%REPORT_PATH%/junit.xml"
                            if exist system_tests_report.json curl --fail --silent --show-error -u "%ARTIFACTORY_USERNAME%:%ARTIFACTORY_PASSWORD%" -T system_tests_report.json "%REPORT_PATH%/report.json"
                            if exist system_tests_logs.zip curl --fail --silent --show-error -u "%ARTIFACTORY_USERNAME%:%ARTIFACTORY_PASSWORD%" -T system_tests_logs.zip "%REPORT_PATH%/test_logs.zip"
                        '''
                    }
                }
            }
        }
    }
}
