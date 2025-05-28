package com.tcc.healthalertmanager.metrics;

import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.stereotype.Component;

@Component
public class AnomalyMetrics {

    private final MeterRegistry meterRegistry;

    public AnomalyMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
    }

    public void incrementAnomaly(String type) {
        meterRegistry.counter("health_alerts_total", "type", type).increment();
    }
}

