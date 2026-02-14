package com.generated.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

/**
 * POJO representing a user returned by the external service.
 */
public class UserResponse {

    @NotNull(message = "User id must not be null")
    private Long id;

    @NotBlank(message = "User name must not be blank")
    private String name;

    @Email(message = "Email should be valid")
    private String email;

    // Default constructor for deserialization
    public UserResponse() {}

    public UserResponse(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    // Getters / Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

	public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}