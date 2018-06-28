pipeline {
    agent any 
    environment {
        NAME = "blue-green"
        TAG = "v0"
        LOCAL_REGISTRY = "192.168.100.166:5000"
        NAMESPACE = "default"
        NUM = "4"
        COUNT = "3"
    }
    stages {
        stage('Build') {
            steps {
                timeout(time: 3, unit: 'MINUTES') {   
                    retry(5) {
                        sh "docker build -t ${env.LOCAL_REGISTRY}/${env.NAME}:${env.TAG} ."
                    }
                }
                sh "docker push ${env.LOCAL_REGISTRY}/${env.NAME}:${env.TAG}"
            }
        }
        stage('Deploy - Staging') {
            steps {
                sh "sed -i s/\"{{.namespace}}\"/\"${env.NAMESPACE}\"/g ./manifest/controller.yaml"
                sh "sed -i s/\"{{.name}}\"/\"${env.NAME}\"/g ./manifest/controller.yaml"
                sh "sed -i s/\"{{.count}}\"/\"${env.count}\"/g ./manifest/controller.yaml"
                sh "sed -i s/\"{{.local.registry}}\"/\"${env.LOCAL_REGISTRY}\"/g ./manifest/controller.yaml"
                sh "sed -i s/\"{{.tag}}\"/\"${env.TAG}\"/g ./manifest/controller.yaml"
                sh "sed -i s/\"{{.num}}\"/\"${env.NUM}\"/g ./manifest/controller.yaml"
                sh "sed -i s/\"{{.num}}\"/\"${env.NUM}\"/g ./manifest/pvc.yaml"
                sh "sed -i s/\"{{.namespace}}\"/\"${env.NAMESPACE}\"/g ./manifest/pvc.yaml"
                sh "sed -i s/\"{{.name}}\"/\"${env.NAME}\"/g ./manifest/pvc.yaml"
                sh "sed -i s/\"{{.namespace}}\"/\"${env.NAMESPACE}\"/g ./manifest/service.yaml"
                sh "sed -i s/\"{{.name}}\"/\"${env.NAME}\"/g ./manifest/service.yaml"
                sh "if kubectl -n ${env.NAMESPACE} get pod | grep ${env.NAME}; then kubectl delete -f ./manifest/controller.yaml; fi"
            }
        }
        stage('Deploy - Production') {
            steps {
                sh 'kubectl create -f ./manifest/service.yaml'
                sh 'kubectl create -f ./manifest/pvc.yaml'
                sh 'kubectl create -f ./manifest/controller.yaml'
            }
        }
    }
    post {
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}
