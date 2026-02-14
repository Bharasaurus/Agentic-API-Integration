package com.generated.client;

import com.generated.dto.UserResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.List;

/**
 * One client class per external service.
 * Uses the injected WebClient bean to call the remote user service.
 */
@Component
public class UserClient {

    private final WebClient webClient;

    public UserClient(WebClient userServiceWebClient) {
        this.webClient = userServiceWebClient;
    }

    /**
     * Calls the external `/users` endpoint and returns a list of {@link UserResponse}.
     *
     * @return List of users
     */
    public List<UserResponse> fetchAllUsers() {
        // The external API is expected to return a JSON array that can be mapped to List<UserResponse>
        return webClient.get()
                .uri("/users")
                .retrieve()
                .bodyToMono(new ParameterizedTypeReference<List<UserResponse>>() {})
                .block(); // Blocking for simplicity in a service layer; can be made reactive if needed
    }
}