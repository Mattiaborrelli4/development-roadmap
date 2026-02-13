package com.example.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UpdateUserRequest {

    @Size(min = 3, max = 50, message = "Il nome deve essere tra 3 e 50 caratteri")
    private String firstName;

    @Size(min = 3, max = 50, message = "Il cognome deve essere tra 3 e 50 caratteri")
    private String lastName;

    @Size(min = 9, max = 15, message = "Il numero di telefono non è valido")
    private String phoneNumber;

    @Email(message = "Email non valida")
    private String email;
}
