package com.tcc.healthalertmanager.listener;


import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.tcc.healthalertmanager.metrics.AnomalyMetrics;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class HealthAlertListener {

    private static final Logger logger = LoggerFactory.getLogger(HealthAlertListener.class);

    private final AnomalyMetrics anomalyMetrics;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public HealthAlertListener(AnomalyMetrics anomalyMetrics) {
        this.anomalyMetrics = anomalyMetrics;
    }

    @KafkaListener(topics = "iot-events-alert", groupId = "health-alert-manager")
    public void listen(String message) {
        try {

            logger.info("Received alert message {}", message);

            JsonNode jsonNode = objectMapper.readTree(message);
            JsonNode anomalies = jsonNode.get("anomalies");

            if (anomalies != null && anomalies.isArray()) {
                logger.info("Received anomalies size {}", anomalies.size());
                for (JsonNode anomaly : anomalies) {
                    anomalyMetrics.incrementAnomaly(anomaly.asText());
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

