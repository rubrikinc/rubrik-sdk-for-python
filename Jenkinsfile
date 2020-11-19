pipeline {
    agent any
    environment {
    GIT_CREDS = credentials('github-user')
    }
    stages {
        stage('Generate Docs') {
            steps {
                sh 'chmod -R 755 .'
                sh 'sudo pip3.8 install jinja2 requests'
                sh '/usr/local/bin/python3.8 ./create_docs.py'
            }
        }
        stage('Commit Docs') {
                        steps {
                            sh '''
                                git config --global user.name ${GIT_AUTHOR_NAME}
                                git add -A ./docs/
                                if [ `git diff --cached --exit-code` ]
                                then
                                    PUSH=true
                                else
                                    PUSH=false
                                fi
                                echo $PUSH > .PUSH
                            '''
                        }

                stages {
                    stage('Git - Perform Commit') {
                        steps {
                            sh '''
                                PUSH=`cat .PUSH`
                                if [ "$PUSH" = true ]
                                then
                                    git commit -a -m "Documentation Update for Commit ${GIT_COMMIT}"
                                else
                                    echo "No code change required, skipping commit"
                                fi
                            '''
                        }
                    }
                    stage('Git - Perform Push') {
                        steps {
                            sh '''
                                PUSH=`cat .PUSH`
                                if [ "$PUSH" = true ]
                                then
                                    echo 'Code changed, pushing...'
                                    git push https://${GIT_CREDS_USR}:${GIT_CREDS_PSW}@github.com/trinity-team/rubrik-sdk-for-python.git HEAD:${BRANCH_NAME}
                                else
                                    echo 'No code change required, skipping push'
                                fi
                            '''
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
