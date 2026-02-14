package com.generated.client.controller;

import com.generated.client.dto.UserResponseDto;
import com.generated.client.service.UserService;
import jakarta.validation.constraints.Positive;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

/**
 * REST controller exposing the GET /users/{id} endpoint.
 * Validation, exception handling and proper HTTP status mapping are performed here.
 */
@RestController
@RequestMapping("/users")
@Validated   // Enables method‑level validation
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    /**
     * Retrieves a user by id.
     *
     * @param id the user identifier (must be positive)
     * @return {@link ResponseEntity} containing the {@link UserResponseDto}
     */
    @GetMapping("/{id}")
    public ResponseEntity<UserResponseDto> getUser(
            @PathVariable @Positive(message = "User id must be a positive number") Long id) {

        try {
            UserResponseDto user = userService.getUserById(id);
            return ResponseEntity.ok(user);
        } catch (IllegalArgumentException ex) {
            // Bad request or not‑found – map to appropriate status
            String msg = ex.getMessage();
            if (msg != null && msg.contains("not found")) {
                return ResponseEntity.status(404).body(null);
            }
            return ResponseEntity.badRequest().body(null);
        } catch (Exception ex) {
            // Unexpected errors – hide details from the client
            return ResponseEntity.status(500).build();
        }
    }
}