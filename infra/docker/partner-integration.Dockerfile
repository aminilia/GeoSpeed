FROM maven:3.9.9-eclipse-temurin-21 AS build
WORKDIR /workspace
COPY services/partner-integration-java/ ./
RUN mvn test package -DskipTests=false

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /workspace/target/*.jar app.jar
EXPOSE 8090
ENTRYPOINT ["java", "-jar", "app.jar"]

