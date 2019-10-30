pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    stage('Setup workspace'){
      steps{
        sh 'pip install -r requirements.txt'
        sh 'pip install flake8 pytest bandit'
        sh 'mkdir -p reports/'
      }
    }
    stage('validate') {
      steps {
        sh 'flake8 --builtins="process_paragraph" > reports/flake8.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'pytest -rA test.py > reports/tests.txt'
      }
    }
    stage('Package') {
      steps {
        sh 'ls -la'
      }
    }
    stage('Verify') {
      steps {
        sh 'bandit -r -lll -s B605 ./ -o "reports/bandit.txt"'
      }
    }
    stage('Deploy') {
      steps {
        sh 'python3 setup.py build'
      }
    }
  }
  }