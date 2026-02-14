package com.generated.client.service;

import com.generated.client.client.UserClient;
import com.generated.client.dto.UserResponseDto;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClientResponseException;

/**
 * Business service that orchestrates the call to the external user API.
 */
@Service
public class UserService {

    private final UserClient userClient;

    public UserService(UserClient userClient) {
        this.userClient = userClient;
    }

    /**
     * Retrieves a user by its identifier.
     *
     * @param id the user id (must be positive)
     * @return the {@link UserResponseDto}
     * @throws IllegalArgumentException if the external service returns a 4xx status
     * @throws RuntimeException         for any other unexpected error
     */
    public UserResponseDto getUserById(Long id) {
        try {
            // Block here because the controller works with a synchronous API.
            // In a fully reactive stack you would return Mono<UserResponseDto>.
            return userClient.fetchUserById(id).block();
        } catch (WebClientResponseException e) {
            // Translate HTTP errors to domain‑specific exceptions / status codes.
            if (e.getStatusCode() == HttpStatus.NOT_FOUND) {
                throw new IllegalArgumentException("User with id " + id + " not found", e);
            }
            if (e.getStatusCode().is4xxClientError()) {
                throw new IllegalArgumentException("Invalid request to external service: " + e.getMessage(), e);
            }
            // 5xx or other unexpected errors
            throw new RuntimeException("External service error: " + e.getMessage(), e);
        } catch (Exception e) {
            // Catch any non‑WebClient exceptions (e.g., serialization issues)
            throw new RuntimeException("Unexpected error while fetching user", e);
        }
    }
}