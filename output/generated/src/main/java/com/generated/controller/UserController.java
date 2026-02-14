package com.generated.controller;

import com.generated.dto.UserResponse;
import com.generated.service.UserService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST controller exposing the `/users` endpoint.
 * Returns a list of users retrieved from the external service.
 */
@RestController
@RequestMapping("/users")
@Validated
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    /**
     * GET /users
     *
     * @return HTTP 200 with the list of users, or HTTP 500 on failure.
     */
    @GetMapping
    public ResponseEntity<List<UserResponse>> getUsers(@Valid @RequestBody(required = false) Object dummy) {
        // No request body is expected; the dummy parameter is only to keep the @Valid annotation path.
        try {
            List<UserResponse> users = userService.getAllUsers();
            return ResponseEntity.ok(users);
        } catch (RuntimeException ex) {
            // Production‑ready error handling – could be replaced by @ControllerAdvice
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(null);
        }
    }
}