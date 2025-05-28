package com.tcc.eventsprocessor.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.tcc.eventsprocessor.model.HealthEvent;
import com.tcc.eventsprocessor.model.SensorData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ThreadLocalRandom;

@Component
public class HealthEventProcessor {

    private static final Logger logger = LoggerFactory.getLogger(HealthEventProcessor.class);

    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Value("${kafka.topic.ok}")
    private String okTopic;

    @Value("${kafka.topic.alert}")
    private String alertTopic;

    public HealthEventProcessor(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    @KafkaListener(topics = "iot-raw-events", groupId = "events-processor-group")
    public void listen(String message, Acknowledgment ack) {
        logger.info("Processing message {}", message);
        try {
            HealthEvent event = objectMapper.readValue(message, HealthEvent.class);
            boolean isHealthy = classify(event);

            if (isHealthy) {
                kafkaTemplate.send(okTopic, message);
                logger.info("Processed event and sent to okTopic!");
            } else {
                List<String> anomalies = detectAnomalies(event);
                Map<String, Object> enrichedPayload = objectMapper.convertValue(event, Map.class);
                enrichedPayload.put("anomalies", anomalies);

                String enrichedMessage = objectMapper.writeValueAsString(enrichedPayload);
                kafkaTemplate.send(alertTopic, enrichedMessage);
                logger.info("Processed event and sent to alertTopic!");
            }

            // ✅ Latência randômica: 1ms a 20ms
            int delay = ThreadLocalRandom.current().nextInt(1, 20);
            Thread.sleep(delay);

            ack.acknowledge();

        } catch (Exception e) {
            logger.error("Sent failed message to DLQ: iot-raw-events-dlq {}", e.getMessage());
            kafkaTemplate.send("iot-raw-events-dlq", message);
        }
    }

    private List<String> detectAnomalies(HealthEvent event) {
        List<String> anomalies = new ArrayList<>();

        SensorData sensorData = event.getSensorData();

        int hr = sensorData.getHeartRate();
        double temp = sensorData.getTemperature();
        String[] bp = sensorData.getBloodPressure().split("/");

        int systolic = Integer.parseInt(bp[0]);
        int diastolic = Integer.parseInt(bp[1]);

        if (temp > 38.0) anomalies.add("TEMP");
        if (hr > 120) anomalies.add("HR");
        if (systolic < 90 || systolic > 140 || diastolic < 60 || diastolic > 90) anomalies.add("BP");

        return anomalies;
    }

    private boolean classify(HealthEvent event) {
        SensorData sensorData = event.getSensorData();

        int hr = sensorData.getHeartRate();
        double temp = sensorData.getTemperature();
        String[] bp = sensorData.getBloodPressure().split("/");

        int systolic = Integer.parseInt(bp[0]);
        int diastolic = Integer.parseInt(bp[1]);

        boolean normalTemp = temp <= 38.0;
        boolean normalHR = hr <= 120;
        boolean normalBP = (systolic >= 90 && systolic <= 140) && (diastolic >= 60 && diastolic <= 90);

        return normalTemp && normalHR && normalBP;
    }
}

