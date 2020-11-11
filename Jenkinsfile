pipeline {
    agent any
    stages {
        stage('Generate Docs') {
            steps {
                sh 'chmod 755 createdocs.py; ./create_docs.py'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
