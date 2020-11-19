pipeline {
    agent any
    stages {
        stage('Generate Docs') {
            steps {
                sh 'chmod -R 755 .'
                sh 'sudo pip3.8 install jinja2 requests'
                sh '/usr/local/bin/python3.8 ./create_docs.py'
            }
        }
        stage('Commit Docs') {
            echo "Commit Docs"
            withCredentials([usernamePassword(credentialsId: 'github-user', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                stages {
                    stage('Git - Set Author') {
                        steps {
                            sh '''
                                git config --global user.name ${GIT_AUTHOR_NAME}
                            '''
                        }
                    }
                    stage('Git - Add new files') {
                        steps {
                            sh '''
                                git config --global user.name ${GIT_AUTHOR_NAME}
                            '''
                        }
                    }
                    stage('Git - Perform Commit') {
                        steps {
                            sh '''
                                NO_PUSH=true
                                git commit -a -m "Documentation Update for Commit ${GIT_COMMIT}" || PUSH=false
                            '''
                        }
                    }
                    stage('Git - Perform Push') {
                        steps {
                            sh '''
                                if [ ${NO_PUSH} = false ]
                                then
                                    echo 'Code changed, pushing...'
                                    git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/trinity-team/rubrik-sdk-for-python.git HEAD:${BRANCH_NAME}
                                    export PUSH=true
                                else
                                    echo 'No code change required, skipping push'
                                fi
                            '''
                        }
                    }
                }
            }
        }
        stage('Function Tests') {
            steps {
                echo 'Run Tests'
                withCredentials([
                    usernamePassword(credentialsId: 'polaris_beta', usernameVariable: 'POLARIS_BETA_USR', passwordVariable: 'POLARIS_BETA_PWD'),
                    usernamePassword(credentialsId: 'polaris_prod', usernameVariable: 'POLARIS_PROD_USR', passwordVariable: 'POLARIS_PROD_PWD')
                ]) {
                    sh 'printenv'
                }
            }
        }
    }
    post {
        always {
            echo 'always'
            // cleanWs()
        }
        success {
            echo 'successful'
        }
        failure {
            echo 'failed'
        }
        unstable {
            echo 'unstable'
        }
        changed {
            echo 'changed'
        }
    }
}
