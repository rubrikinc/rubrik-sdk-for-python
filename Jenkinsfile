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
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-user', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh """
                        echo 'Set Author'
                        git config --global user.name ${GIT_AUTHOR_NAME}
                        echo 'Test for adding files'
                        git add -A ./docs/ || echo 'No new files to add to commit'
                        echo 'Test for commit'
                        git commit -a -m "Documentation Update for Commit ${GIT_COMMIT}" || PUSH=1
                        echo 'If commit then push'
                        if [ $PUSH ]
                        then
                            echo 'Push back up to github'
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/trinity-team/rubrik-sdk-for-python.git HEAD:${BRANCH_NAME}
                            echo 'Reset push flag'
                            export PUSH=0
                        fi
                    """
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
