# Stage 1: Build
FROM maven:3.9.6-eclipse-temurin-21 AS build

WORKDIR /app

# Copia o código fonte e o arquivo pom.xml
COPY pom.xml .
COPY src ./src

# Compila e empacota o aplicativo
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:21-jdk-alpine

WORKDIR /app

# Copia o JAR gerado do estágio de build
COPY --from=build /app/target/*.jar app.jar

# Exponha a porta padrão do Spring Boot
EXPOSE 8080

# Comando de execução
ENTRYPOINT ["java", "-jar", "app.jar"]
