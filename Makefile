.PHONY: setup test lint build test-web test-java test-python test-cpp test-pipelines build-cpp docker-up auto-up partner-api vehicle-signals auto-dashboard auto-test launch-readiness-report ingest-sample release-report clean

test: test-web test-java test-python test-cpp test-pipelines

setup:
	cd apps/web-dashboard && npm install
	cd services/ml-python && python -m pip install -r requirements-dev.txt
	cd pipelines && python -m pip install -r requirements-dev.txt

lint:
	python -m compileall services/ml-python pipelines tests

build:
	cd apps/web-dashboard && npm run build
	cd services/api-java && mvn package
	cd services/partner-integration-java && mvn package
	cmake -S services/matcher-cpp -B services/matcher-cpp/build
	cmake --build services/matcher-cpp/build

test-web:
	cd apps/web-dashboard && npm install && npm test -- --run

test-java:
	cd services/api-java && mvn test
	cd services/partner-integration-java && mvn test

test-python:
	cd services/ml-python && python -m pip install -r requirements-dev.txt && python -m pytest

test-cpp:
	cmake -S services/matcher-cpp -B services/matcher-cpp/build
	cmake --build services/matcher-cpp/build
	cd services/matcher-cpp/build && ctest --output-on-failure

test-pipelines:
	cd pipelines && python -m pip install -r requirements-dev.txt && python -m pytest

build-cpp:
	cmake -S services/matcher-cpp -B services/matcher-cpp/build
	cmake --build services/matcher-cpp/build

docker-up:
	docker compose up --build

auto-up:
	docker compose up --build partner-integration-java vehicle-signals-python auto-headunit-simulator

partner-api:
	cd services/partner-integration-java && mvn spring-boot:run

vehicle-signals:
	cd services/vehicle-signals-python && python -m pip install -e ".[dev]" && uvicorn geospeed_vehicle.app:app --host 0.0.0.0 --port 8010

auto-dashboard:
	cd apps/auto-headunit-simulator && npm install && npm run dev

auto-test:
	cd services/vehicle-signals-python && python -m pip install -e ".[dev]" && python -m pytest
	cd services/partner-integration-java && mvn test
	cd apps/auto-headunit-simulator && npm install && npm test

launch-readiness-report:
	python pipelines/validate/generate_release_report.py --input data/sample/release_candidate.geojson --output data/sample/release_report.md

ingest-sample:
	python pipelines/ingest/ingest_osm_roads.py --input data/sample/roads.geojson --output data/sample/normalized_roads.json
	python pipelines/transform/infer_speed_limits.py --segments data/sample/roads.geojson --speeds data/sample/speed_limits.geojson --signs data/sample/signs.geojson --observed data/sample/observed_speeds.csv --output data/sample/release_candidate.geojson

release-report:
	python pipelines/validate/generate_release_report.py --input data/sample/release_candidate.geojson --output data/sample/release_report.md

clean:
	cmake -E rm -rf services/matcher-cpp/build
