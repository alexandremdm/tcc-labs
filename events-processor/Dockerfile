# Stage 1: Build
FROM maven:3.9.6-eclipse-temurin-21 AS build

WORKDIR /app

# Copia apenas o pom.xml primeiro para baixar as dependências
# Isso permite que o Docker armazene em cache as dependências
# a menos que o pom.xml mude.
COPY pom.xml .

# Baixa as dependências.
# O 'resolve-plugins' garante que os plugins necessários sejam baixados também.
# O '-Dmaven.test.skip=true' evita a execução de testes aqui,
# pois estamos interessados apenas nas dependências.
RUN mvn dependency:go-offline -B -Dmaven.test.skip=true

# Agora copia o código fonte
COPY src ./src

# Compila e empacota o aplicativo
# Não usamos 'clean' aqui para aproveitar as dependências já baixadas.
# Os testes são pulados para agilizar o build do Docker.
RUN mvn package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:21-jdk-alpine

WORKDIR /app

# Copia o JAR gerado do estágio de build
COPY --from=build /app/target/*.jar app.jar

# Exponha a porta padrão do Spring Boot
EXPOSE 8080

# Comando de execução
ENTRYPOINT ["java", "-jar", "app.jar"]
