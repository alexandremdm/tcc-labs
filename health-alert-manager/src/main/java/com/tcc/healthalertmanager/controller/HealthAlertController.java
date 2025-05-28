package com.tcc.healthalertmanager.controller;

import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthAlertController {

    private final MeterRegistry meterRegistry;

    public HealthAlertController(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
    }

    @GetMapping("/metrics/alerts")
    public Object getCustomMetrics() {
        return meterRegistry.get("health_alerts_total").meters();
    }
}

