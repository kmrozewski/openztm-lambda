pipeline {
    agent any

    stages {
        stage('setup parameters') {
            steps {
                script {
                    properties([
                        parameters([
                            choice(
                                name: 'LAMBDA_FUNCTION',
                                choices: ['openztm-closest-stops', 'openztm-s3-upload'],
                                description: 'Pick up lambda function to deploy')
                        ])
                    ])
                }
            }
        }
        stage('build') {
            steps {
                sh "./build.sh -n ${parameters.LAMBDA_FUNCTION} -f ${parameters.LAMBDA_FUNCTION == 'openztm-closest-stops' ? 'closeststops.py' : 's3upload.py'}"
                sh "docker images -a"
            }
        }
        stage('tag') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID'),
                    string(credentialsId: 'aws-region', variable: 'AWS_REGION')
                    ]) {
                        sh "docker tag ${parameters.LAMBDA_FUNCTION}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${parameters.LAMBDA_FUNCTION}:latest"
                    }
            }
        }
        stage('ready to push') {
            options {
                timeout(time: 15, unit: 'MINUTES')
            }
            steps {
                input(message: 'Deploy to AWS?')
            }
        }
        stage('push') {
            steps {
                withCredentials([
                [$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-keys', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'],
                string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID'),
                string(credentialsId: 'aws-region', variable: 'AWS_REGION')
                ]) {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                    sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${parameters.LAMBDA_FUNCTION}:latest"
                }
            }
        }
        stage('clean up') {
            steps {
                withCredentials([
                string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID'),
                string(credentialsId: 'aws-region', variable: 'AWS_REGION')
                ]) {
                    echo 'Before:'
                    sh 'docker images -a'
                    sh "docker rmi -f ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${parameters.LAMBDA_FUNCTION}"
                    sh "docker rmi -f ${parameters.LAMBDA_FUNCTION}"
                    echo 'After:'
                    sh 'docker images -a'
                }
            }
        }
        stage('ready to prune') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                input(message: 'Prune local docker images?')
            }
        }
        stage('prune local images') {
            steps {
                echo 'Before:'
                sh 'docker images -a'
                sh 'docker image prune --force --all'
                echo 'After:'
                sh 'docker images -a'
            }
        }
    }
}