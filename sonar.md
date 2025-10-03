## Create project in sonar-qube

Copy SONAR_TOKEN and PROJECT_KEY and SONAR_HOST_URL

## Create sonar-project.properties

<<<
sonar.projectKey=PROJECT_KEY
sonar.qualitygate.wait=true
>>>

## Add secrets variables in CICD

- SONAR_HOST_URL
- SONAR_TOKEN


## Add stage in Gitlab CI

1. For NodeJS

```yaml
stages:
  - code_check

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
  - node_modules/

sonarqube-check:
  stage: code_check
  image: 
    name: sonarsource/sonar-scanner-cli:latest
    entrypoint: [""]
  variables:
    SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"  # Defines the location of the analysis task cache
    GIT_DEPTH: "0"  # Tells git to fetch all the branches of the project, required by the analysis task
  cache:
    key: "${CI_JOB_NAME}"
    paths:
      - .sonar/cache
  script: 
    - sonar-scanner
  allow_failure: true
  only:
    - dev
  environment:
    name: $CI_COMMIT_REF_NAME
  tags:
    - dev
```

2. For PHP

```yaml
stages:
  - code_check

cache:
  key: ${CI_COMMIT_REF_SLUG}

sonarqube-check: 
  stage: code_check 
  image: 
    name: sonarsource/sonar-scanner-cli:latest 
    entrypoint: [""] 
  variables: 
    SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar" # Defines the location of the analysis task cache 
    GIT_DEPTH: "0" # Tells git to fetch all the branches of the project, required by the analysis task 
  cache: 
    key: "${CI_JOB_NAME}"
    paths: 
      - .sonar/cache 
  script: 
    - sonar-scanner 
  allow_failure: true  # Set false to bypass pipeline without solving all issues 
  only: 
  - dev 
  #tags: 
  #	- dev 
  environment: 
    name: $CI_COMMIT_REF_NAME
  tags:
    - dev
```
