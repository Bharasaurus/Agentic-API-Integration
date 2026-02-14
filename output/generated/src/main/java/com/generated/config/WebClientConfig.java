package com.generated.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

/**
 * Centralised WebClient configuration.
 * Base URL is externalised in application properties.
 */
@Configuration
public class WebClientConfig {

    @Value("${external.user-service.base-url}")
    private String userServiceBaseUrl;

    @Bean
    public WebClient userServiceWebClient() {
        return WebClient.builder()
                .baseUrl(userServiceBaseUrl)
                .build();
    }
}