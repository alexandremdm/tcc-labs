package com.tcc.ioteventsbridge.kafka;

import com.tcc.ioteventsbridge.mqtt.MqttSubscriber;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class KafkaPublisher {

    private static final Logger logger = LoggerFactory.getLogger(KafkaPublisher.class);

    @Value("${kafka.topic}")
    private String topic;

    private final KafkaTemplate<String, String> kafkaTemplate;

    public KafkaPublisher(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void publish(String message) {
        kafkaTemplate.send(topic, message);
        logger.info("Published to Kafka: " + message);
    }
}

