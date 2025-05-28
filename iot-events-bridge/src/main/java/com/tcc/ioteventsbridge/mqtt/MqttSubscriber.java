package com.tcc.ioteventsbridge.mqtt;

import com.tcc.ioteventsbridge.kafka.KafkaPublisher;
import com.hivemq.client.mqtt.mqtt3.Mqtt3AsyncClient;
import com.hivemq.client.mqtt.mqtt3.Mqtt3Client;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class MqttSubscriber {

    private static final Logger logger = LoggerFactory.getLogger(MqttSubscriber.class);

    @Value("${mqtt.broker}")
    private String broker;

    @Value("${mqtt.topic}")
    private String topic;

    @Value("${mqtt.client-id}")
    private String clientId;

    private final KafkaPublisher kafkaPublisher;

    public MqttSubscriber(KafkaPublisher kafkaPublisher) {
        this.kafkaPublisher = kafkaPublisher;
    }

    @PostConstruct
    public void subscribe() {
        logger.info("MQTT subscribe initialize!");
        Mqtt3AsyncClient client = Mqtt3Client.builder()
                .identifier(clientId)
                .serverHost(broker.split(":")[1].replace("//", ""))
                .serverPort(Integer.parseInt(broker.split(":")[2]))
                .buildAsync();

        try {
            client.connect().thenAccept(connAck -> {
                logger.info("MQTT Connected!");
                client.subscribeWith()
                        .topicFilter(topic)
                        .callback(publish -> {
                            String payload = new String(publish.getPayloadAsBytes());
                            logger.info("MQTT Received: " + payload);
                            kafkaPublisher.publish(payload);
                        })
                        .send();
            });
        } catch (Exception e) {
            logger.error("MQTT connect error {}", e.getMessage());
        }

    }
}
