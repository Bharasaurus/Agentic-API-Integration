package com.generated.service;

import com.generated.client.UserClient;
import com.generated.dto.UserResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;

/**
 * Service layer that orchestrates the call to the external user service.
 * Contains business‑level error handling and logging.
 */
@Service
public class UserService {

    private static final Logger log = LoggerFactory.getLogger(UserService.class);
    private final UserClient userClient;

    public UserService(UserClient userClient) {
        this.userClient = userClient;
    }

    /**
     * Retrieves all users from the external system.
     *
     * @return immutable list of {@link UserResponse}
     */
    public List<UserResponse> getAllUsers() {
        try {
            List<UserResponse> users = userClient.fetchAllUsers();
            return users != null ? Collections.unmodifiableList(users) : Collections.emptyList();
        } catch (Exception ex) {
            // Centralised logging – in a real project you might translate this to a custom exception
            log.error("Failed to fetch users from external service", ex);
            throw new RuntimeException("Unable to retrieve users at this time", ex);
        }
    }
}