pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    stage('Setup workspace'){
      steps{
        sh 'pip install -r requirements.txt'
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
        sh 'coverage report test.py > reports/coverage.txt'
      }
    }
    stage('Package') {
      steps {
        sh 'python3 setup.py build'
      }
    }
    stage('Verify') {
      steps {
        sh 'bandit -r -lll -s B605 ./ -o "reports/bandit.txt"'
      }
    }
    stage('Deploy') {
      steps {
        sh 'tar -cvzf build.tar.gz build/'
      }
    }
    stage('Benchmarking'){
      steps {
        sh 'curl -o benchmark.sh -s https://gist.githubusercontent.com/losete/e730dff4edd5b4e5910cac15057265cb/raw/benchmark.sh'
        sh 'bash benchmark.sh'
      }
    }
  }
  post {
    always{
      sh 'tar -cvzf reports.tar.gz reports/'
      emailext (attachmentsPattern: 'reports.tar.gz',
        body: 'Workflow result on ${currentBuild.currentResult}, check attached artifacts for further information',
        subject: "Jenkins Build ${currentBuild.currentResult} on Job ${env.JOB_NAME}",
        from: 'notificaciones.torusnewies@gmail.com',
        replyTo: '',
        to: 'losetazo@gmail.com'
      )
    }
    success {
      archiveArtifacts 'reports.tar.gz'
      archiveArtifacts artifacts: 'build.tar.gz'
      script{
        if (env.BRANCH_NAME.startsWith('PR')){
          withCredentials([usernamePassword(credentialsId: 'CarlosCredGH', passwordVariable: 'pass', usernameVariable: 'user')]) {
            sh "git remote update"
            sh "git fetch --all"
            sh "git pull --all"
            sh "git checkout dev"
            sh "git merge origin/master"
            sh "git merge ${BRANCH_NAME}"
            sh "git push https://$user:$pass@github.com/losete/twitter-scraper/"
          }
        }
      }
    }
    cleanup{
      cleanWs()
    }
  }
}