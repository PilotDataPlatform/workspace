pipeline {
    agent { label 'small' }
    environment {
      imagename_dev = "ghcr.io/pilotdataplatform/workspace"
      imagename_staging = "ghcr.io/pilotdataplatform/workspace"
      commit = sh(returnStdout: true, script: 'git describe --always').trim()
      registryCredential = 'pilot-ghcr'
      dockerImage = ''
    }

    stages {

    stage('Git clone for dev') {
        when {branch "develop"}
        steps{
          script {
          git branch: "develop",
              url: 'https://github.com/PilotDataPlatform/workspace',
              credentialsId: 'lzhao'
            }
        }
    }

    stage('DEV unit test') {
      when {branch "develop"}
      steps{
         withCredentials([
            string(credentialsId:'VAULT_TOKEN', variable: 'VAULT_TOKEN'),
            string(credentialsId:'VAULT_URL', variable: 'VAULT_URL'),
            file(credentialsId:'VAULT_CRT', variable: 'VAULT_CRT')
          ]) {
            sh """
            export CONFIG_CENTER_ENABLED='true'
            export VAULT_TOKEN=${VAULT_TOKEN}
            export VAULT_URL=${VAULT_URL}
            export VAULT_CRT=${VAULT_CRT}
            export GREEN_ZONE_LABEL="Greenroom"
            pip install --user poetry==1.1.12
            ${HOME}/.local/bin/poetry config virtualenvs.in-project true
            ${HOME}/.local/bin/poetry install --no-root --no-interaction
            ${HOME}/.local/bin/poetry run pytest --verbose -c tests/pytest.ini
            """
          }
      }
    }

    stage('DEV Build and push image') {
      when {branch "develop"}
      steps{
        script {
            docker.withRegistry('https://ghcr.io', registryCredential) {
                customImage = docker.build("$imagename_dev:$commit-CAC", "--add-host git.indocresearch.org:10.4.3.151 --target web-image .")
                customImage.push()
            }
        }
      }
    }
    stage('DEV Remove image') {
      when {branch "develop"}
      steps{
        sh "docker rmi $imagename_dev:$commit-CAC"
      }
    }

    stage('DEV Deploy') {
      when {branch "develop"}
      steps{
        build(job: "/VRE-IaC/UpdateAppVersion", parameters: [
          [$class: 'StringParameterValue', name: 'TF_TARGET_ENV', value: 'dev' ],
          [$class: 'StringParameterValue', name: 'TARGET_RELEASE', value: 'workspace' ],
          [$class: 'StringParameterValue', name: 'NEW_APP_VERSION', value: "$commit-CAC" ]
      ])
      }
    }

    stage('Git clone staging') {
        when {branch "main"}
        steps{
          script {
          git branch: "main",
              url: 'https://github.com/PilotDataPlatform/workspace',
              credentialsId: 'lzhao'
            }
        }
    }

    stage('STAGING Building and push image') {
      when {branch "main"}
      steps{
        script {
          docker.withRegistry('https://ghcr.io', registryCredential) {
              customImage = docker.build("$imagename_staging:$commit", "--add-host git.indocresearch.org:10.4.3.151 '--target web-image .")
              customImage.push()
          }
        }
      }
    }

    stage('STAGING Remove image') {
      when {branch "main"}
      steps{
        sh "docker rmi $imagename_staging:$commit"
      }
    }

    stage('STAGING Deploy') {
      when {branch "main"}
      steps{
      build(job: "/VRE-IaC/Staging-UpdateAppVersion", parameters: [
        [$class: 'StringParameterValue', name: 'TF_TARGET_ENV', value: 'staging' ],
        [$class: 'StringParameterValue', name: 'TARGET_RELEASE', value: 'workspace' ],
        [$class: 'StringParameterValue', name: 'NEW_APP_VERSION', value: "$commit" ]
      ])
      }
    }
  }
  post {
    failure {
        slackSend color: '#FF0000', message: "Build Failed! - ${env.JOB_NAME} $commit  (<${env.BUILD_URL}|Open>)", channel: 'jenkins-dev-staging-monitor'
    }
  }

}
