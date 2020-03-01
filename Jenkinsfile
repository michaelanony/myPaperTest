APP_NAME = 'paperTest'
NAMESPACE = 'lab'
COMP_NAME = 'test'
IMAGE_TAG = ''
IMAGE_URI = ''
IMAGE_LATEST = ''
WAR = ''
FILENAME = ''


DOCKER_REGISTRY_HOST_NAME = "192.168.11.3:10000"
DOCKER_REGISTRY_ORG = "ci"
DOCKER_REGISTRY_CREDIENTIAL_ID = "harbor"

GIT_REGISTRY = "https://github.com/michaelanony/myPaperTest.git"
COMPILE_AGENT_IMAGE = ""


/** BRANCH = "" is Defined in Parameter  */

COMPILE_SOURCE = false
DEPLOY= true

pipeline {
    agent {
    label 'jenkins-ci'
  }

    options { timestamps () }
    stages {



        stage('Git Checkout') {
            steps {
                dir('source'){
                    git branch: "master", credentialsId: '1afda173-d7ab-4ffb-89cc-36106a82febe', url: "${GIT_REGISTRY}"

                    script {
                        COMMIT_HASH = sh(returnStdout: true, script: 'git rev-parse HEAD').trim().take(7)
                        BRANCH_MOD = BRANCH.replaceAll(/\//,'_')
                        def now = new Date()
                        DATE = now.format("yyMMdd", TimeZone.getTimeZone('UTC'))
                        IMAGE_TAG="${APP_NAME}:${COMP_NAME}.${BRANCH_MOD}.${COMMIT_HASH}.${DATE}.${BUILD_NUMBER}"
                        IMAGE_URI="${DOCKER_REGISTRY_HOST_NAME}/${DOCKER_REGISTRY_ORG}/${IMAGE_TAG}"
                        IMAGE_LATEST="${DOCKER_REGISTRY_HOST_NAME}/${DOCKER_REGISTRY_ORG}/${APP_NAME}"
                        echo "${IMAGE_URI}"
                    }
                }
            }
        }

         stage('Compile') {
            when {
                expression { COMPILE_SOURCE == true }
            }
            steps {
                script {
                    sh "./script/${APP_NAME}-${COMP_NAME}.sh ${WAR}"
                }
            }
        }

        stage('Docker Image Build') {
            steps{
                script{
                    sh 'cd source'
                    sh 'ls -l'
                    docker.withRegistry("http://${DOCKER_REGISTRY_HOST_NAME}", "${DOCKER_REGISTRY_CREDIENTIAL_ID}") {

                        def image = docker.build("${IMAGE_URI}","-f source/Dockerfile --force-rm .")
                        image.push()
                        image.push('latest.${COMP_NAME}')
                        }
                    }
                }
            }

       stage('Deploy dev') {
                when {
                    // Only deploy if it is requested
                    expression { DEPLOY == true }
                }
                steps{
                script{
                        sh "kubectl set image -n ${NAMESPACE} --record deployment ${APP_NAME}-${COMP_NAME} ${APP_NAME}-${COMP_NAME}=${IMAGE_URI}"
                        sh "kubectl rollout status deploy ${APP_NAME}-${COMP_NAME} -n ${NAMESPACE}"

                }
            }
        }




        stage ("Clean") {
            steps {
                dir('source') {
                    deleteDir()
                }

                dir('source_tmp') {
                    deleteDir()
                }
            }
        }
    }

}