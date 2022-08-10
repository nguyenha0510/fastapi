VERSION-TAG=latest
PROJECT-NAME=tip-ws-report
REPO_URL=https://gitlab.viettelcyber.com/threat-intelligence/ti-platform/tip-ws-report
DOMAIN_IP=10.255.244.100
PROXY=http://10.30.118.20:8080
BRANCH_NAME=develop
# SCA
RID=tip-ws-report
# SonarQube
SONAR_URL=https://sonarqube.viettelcyber.com
SONAR_KEY=tip-ws-report
# Checkmarx
CX_PRJ=TI
IGNORE_FOLDERS=ansible-cd,tests,docs,.scannerwork,vendor
IGNORE_FILES=sca,*.ini,*.txt,*.yml,*.yaml,Jenkinsfile,*.md,*.conf


jenkins-sca-check:
	curl -L -X GET 'https://sca.viettelcyber.com/download/sca' --output sca
	chmod +x sca
	docker run --rm --add-host sca.viettelcyber.com:$(DOMAIN_IP) --env https_proxy=$(PROXY) --env http_proxy=$(PROXY) --env no_proxy=sca.viettelcyber.com -v $(WORKSPACE):/opt/project -w /opt/project golang /bin/bash -c "./sca analyze branch_commit --rid=$(RID) --bn=$(BRANCH_NAME) --token=$(SCA_TOKEN)"
	docker run --rm --add-host seatable.viettelcyber.com:$(DOMAIN_IP) --add-host sca.viettelcyber.com:$(DOMAIN_IP) hub.viettelcybersecurity.com/library/sca_seatable_extension:latest /app/sca_seatable -sca_tk=$(SCA_TOKEN) -rid=$(RID) -bn=$(BRANCH_NAME) -app=$(PROJECT-NAME) -branch=$(BRANCH_NAME) -tk=$(SEATABLE_TOKEN)

jenkins-sonar-check:
	docker run --rm --add-host=sonarqube.viettelcyber.com:$(DOMAIN_IP) -v $(WORKSPACE):/usr/src sonarsource/sonar-scanner-cli -Dsonar.projectKey=$(SONAR_KEY) -Dsonar.sources=. -Dsonar.host.url=$(SONAR_URL) -Dsonar.login=$(SONAR_TOKEN) -Dsonar.branch.name=$(BRANCH_NAME) -Dsonar.scm.forceReloadAll=true

jenkins-checkmarx-check:
	docker run --rm --add-host checkmarx.viettelcyber.com:$(DOMAIN_IP) --add-host gitlab.viettelcyber.com:$(DOMAIN_IP) -v $(WORKSPACE):/opt/$(PROJECT-NAME) -v $(WORKSPACE)/seatable_json:/opt/json -v $(WORKSPACE)/scanComment.groovy:/opt/scanComment.groovy --env-file=.cx_env --env CHECKMARX_PASSWORD=$(CHECKMARX_PASSWORD) --env CHECKMARX_USERNAME=$(CHECKMARX_USERNAME) --env GITLAB_TOKEN=$(GITLAB_TOKEN) checkmarx/cx-flow java -jar /app/cx-flow.jar --scan --app=$(PROJECT-NAME) --cx-project=$(CX_PRJ) --spring.profiles.active=sast --f=/opt/$(PROJECT-NAME) --branch=$(BRANCH_NAME) --repo-url=$(REPO_URL) --cx-flow.comment-script=/opt/scanComment.groovy --exclude-folders=$(IGNORE_FOLDERS) --exclude-files=$(IGNORE_FILES) --cx-flow.bug-tracker=Json --cx-flow.bug-tracker-impl=Json --json.file-name-format=data.json --json.data-folder=/opt/json

jenkins-push-checkmarx-report:
	docker run --rm -v $(WORKSPACE)/seatable_json/data.json:/app/config/data.json --add-host seatable.viettelcyber.com:$(DOMAIN_IP) hub.viettelcybersecurity.com/library/checkmarx_seatable_report:latest /app/checkmarx_extension -app=$(PROJECT-NAME) -branch=$(BRANCH_NAME) -tk=$(SEATABLE_TOKEN)

dev-install:
	pip install -r requirements.txt -r test_requirements.txt

dev-alltests:
	pytest --cov=. --cov-report term-missing tests --disable-warnings

dev-init-db:
	python init_db.py

dev-run:
	python -m app

docker-build:
	docker build -t $(PROJECT_NAME):$(VERSION_TAG) .

docker-test:
	docker run --rm $(PROJECT_NAME):$(VERSION_TAG) pytest --cov-config=tox.ini --cov=. --cov-report term-missing tests/unit_tests --disable-warnings