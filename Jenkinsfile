def runTestWithTestRunner(Map config) {
    if (!(config.commit ==~ /[0-9a-fA-F]{40}/)) {
        error('COMMIT must be a 40-character Git SHA')
    }
    build(
        job: env.TEST_RUNNER_JOB,
        wait: true,
        propagate: false,
        parameters: [
            string(name: 'REPO_URL', value: config.repo),
            string(name: 'COMMIT', value: config.commit),
            string(name: 'FRAMEWORK_BRANCH', value: config.frameworkBranch),
            string(name: 'TEST_SCRIPT', value: config.testScript),
            string(name: 'TIMEOUT', value: config.timeout ?: '60'),
            string(name: 'Priority', value: config.priority ?: '2'),
            string(name: 'FTP_LOCATION', value: config.ftpLocation ?: 'latest'),
            string(name: 'PASSRATE', value: config.passrate ?: '100'),
            string(name: 'FIRMWARE_VERSION', value: config.fwVersion ?: ''),
            string(name: 'TESTS_SETTINGS', value: config.testsSettings ?: ''),
            booleanParam(name: 'SEND_REPORT_TO_STATUI', value: false),
        ]
    )
}

def collectTestResults(Map testBuild) {
    copyArtifacts(
        projectName: env.TEST_RUNNER_JOB,
        selector: [$class: 'SpecificBuildSelector', buildNumber: testBuild.number.toString()],
        filter: 'test-results/junit.xml',
        target: 'test-results',
        flatten: true
    )
    junit allowEmptyResults: true, keepProperties: true, testResults: 'test-results/junit.xml'
    archiveArtifacts allowEmptyArchive: true, artifacts: 'test-results/junit.xml'
    switch (testBuild.result) {
        case 'SUCCESS':
            return
        case 'UNSTABLE':
            unstable("${env.TEST_RUNNER_JOB} #${testBuild.number} is UNSTABLE")
            return
        case 'ABORTED':
            error("${env.TEST_RUNNER_JOB} #${testBuild.number} was ABORTED")
        default:
            error("${env.TEST_RUNNER_JOB} #${testBuild.number} finished with ${testBuild.result}")
    }
}

pipeline {
    agent none

    options {
        timestamps()
        skipDefaultCheckout(true)
        disableConcurrentBuilds(abortPrevious: true)
        buildDiscarder(logRotator(daysToKeepStr: '60', numToKeepStr: '300'))
    }

    parameters {
        string(name: 'Priority', defaultValue: '2', description: 'test_runner priority')
    }

    environment {
        TEST_RUNNER_JOB = '/test_runner'
    }

    stages {
        stage('Trigger test runner') {
            agent { node { label 'windows' } }
            steps {
                checkout scm
                script {
                    env.TEST_REPO = bat(returnStdout: true, script: '''@echo off
                        git config --get remote.origin.url
                    ''').trim()
                    env.TEST_COMMIT = bat(returnStdout: true, script: '''@echo off
                        git rev-parse HEAD
                    ''').trim()
                    def testBuild = runTestWithTestRunner([
                        repo: env.TEST_REPO,
                        commit: env.TEST_COMMIT,
                        frameworkBranch: 'master',
                        testScript: 'test_examples/test_host_pc.py',
                        priority: params.Priority
                    ])
                    env.TEST_RUNNER_BUILD = testBuild.number.toString()
                    env.TEST_RUNNER_RESULT = testBuild.result ?: 'FAILURE'
                    echo "${env.TEST_RUNNER_JOB} #${env.TEST_RUNNER_BUILD}: ${env.TEST_RUNNER_RESULT}"
                }
            }
        }
        stage('Collect test results') {
            agent { node { label 'windows' } }
            steps {
                script {
                    echo "Collect test results, then copy to artifactory repo..."
                    collectTestResults(number: env.TEST_RUNNER_BUILD, result: env.TEST_RUNNER_RESULT)
                }
            }
        }
    }
}
