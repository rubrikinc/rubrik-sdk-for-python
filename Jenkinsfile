pipeline {
    agent any
    stages {
        stage('Generate Docs') {
            steps {
                sh 'chmod -R 755 .'
                sh 'python3 ./create_docs.py'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}

