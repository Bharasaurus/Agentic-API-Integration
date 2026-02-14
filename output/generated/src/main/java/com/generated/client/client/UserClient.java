package com.generated.client.client;

import com.generated.client.dto.UserResponseDto;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

/**
 * Dedicated client for the external *User* service.
 * One client per external service – this keeps the service layer thin
 * and focused on business rules.
 */
@Component
public class UserClient {

    private final WebClient webClient;

    public UserClient(WebClient webClient) {
        this.webClient = webClient;
    }

    /**
     * Calls GET /users/{id} on the external system.
     *
     * @param id the user identifier
     * @return a {@link Mono} emitting the {@link UserResponseDto}
     */
    public Mono<UserResponseDto> fetchUserById(Long id) {
        return webClient.get()
                .uri(uriBuilder -> uriBuilder.path("/users/{id}").build(id))
                .retrieve()
                .bodyToMono(UserResponseDto.class);
    }
}