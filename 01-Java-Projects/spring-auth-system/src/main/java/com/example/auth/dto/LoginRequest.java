package com.example.auth.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LoginRequest {

    @NotBlank(message = "Il nome utente o email è obbligatorio")
    private String usernameOrEmail;

    @NotBlank(message = "La password è obbligatoria")
    private String password;
}
