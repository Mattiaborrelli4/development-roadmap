package com.example.auth.service;

import com.example.auth.dto.*;
import com.example.auth.exception.ResourceNotFoundException;
import com.example.auth.model.RefreshToken;
import com.example.auth.model.User;
import com.example.auth.repository.UserRepository;
import com.example.auth.security.JwtService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class AuthenticationService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final RefreshTokenService refreshTokenService;
    private final AuthenticationManager authenticationManager;
    private final EmailService emailService;

    @Transactional
    public AuthenticationResponse register(RegisterRequest request) {
        // Verifica se username o email esistono già
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new RuntimeException("Nome utente già in uso");
        }

        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email già in uso");
        }

        // Crea verification token
        String verificationToken = UUID.randomUUID().toString();

        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .phoneNumber(request.getPhoneNumber())
                .role("USER")
                .enabled(true) // Per semplificare, attiviamo l'utente subito
                .emailVerified(false)
                .verificationToken(verificationToken)
                .build();

        user = userRepository.save(user);

        // Invia email di verifica (mock)
        emailService.sendVerificationEmail(user.getEmail(), verificationToken);

        // Genera token JWT
        Map<String, Object> extraClaims = new HashMap<>();
        extraClaims.put("role", user.getRole());

        String accessToken = jwtService.generateToken(extraClaims, user);
        RefreshToken refreshToken = refreshTokenService.createRefreshToken(user);

        return AuthenticationResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken.getToken())
                .username(user.getUsername())
                .email(user.getEmail())
                .message("Registrazione completata. Controlla la tua email per verificare l'account.")
                .build();
    }

    public AuthenticationResponse login(LoginRequest request) {
        // Determina se l'input è username o email
        String username = request.getUsernameOrEmail();
        User user;

        if (username.contains("@")) {
            user = userRepository.findByEmail(username)
                    .orElseThrow(() -> new UsernameNotFoundException("Credenziali non valide"));
            username = user.getUsername();
        } else {
            user = userRepository.findByUsername(username)
                    .orElseThrow(() -> new UsernameNotFoundException("Credenziali non valide"));
        }

        // Autentica l'utente
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(username, request.getPassword())
        );

        // Genera token JWT
        Map<String, Object> extraClaims = new HashMap<>();
        extraClaims.put("role", user.getRole());

        String accessToken = jwtService.generateToken(extraClaims, user);
        RefreshToken refreshToken = refreshTokenService.createRefreshToken(user);

        return AuthenticationResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken.getToken())
                .username(user.getUsername())
                .email(user.getEmail())
                .message("Login effettuato con successo")
                .build();
    }

    public AuthenticationResponse refreshToken(RefreshTokenRequest request) {
        RefreshToken refreshToken = refreshTokenService.findByToken(request.getRefreshToken());
        refreshToken = refreshTokenService.verifyExpiration(refreshToken);

        User user = refreshToken.getUser();

        // Genera nuovo access token
        Map<String, Object> extraClaims = new HashMap<>();
        extraClaims.put("role", user.getRole());

        String accessToken = jwtService.generateToken(extraClaims, user);

        return AuthenticationResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken.getToken())
                .username(user.getUsername())
                .email(user.getEmail())
                .message("Token refreshato con successo")
                .build();
    }

    @Transactional
    public void logout(String refreshToken) {
        refreshTokenService.deleteByToken(refreshToken);
    }

    public UserResponse getCurrentUser(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("Utente non trovato"));

        return mapToUserResponse(user);
    }

    @Transactional
    public UserResponse updateUser(String username, UpdateUserRequest request) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("Utente non trovato"));

        // Verifica se la nuova email è già in uso
        if (request.getEmail() != null && !request.getEmail().equals(user.getEmail())) {
            if (userRepository.existsByEmail(request.getEmail())) {
                throw new RuntimeException("Email già in uso");
            }
            user.setEmail(request.getEmail());
            user.setEmailVerified(false);
        }

        if (request.getFirstName() != null) {
            user.setFirstName(request.getFirstName());
        }

        if (request.getLastName() != null) {
            user.setLastName(request.getLastName());
        }

        if (request.getPhoneNumber() != null) {
            user.setPhoneNumber(request.getPhoneNumber());
        }

        user = userRepository.save(user);

        return mapToUserResponse(user);
    }

    private UserResponse mapToUserResponse(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .phoneNumber(user.getPhoneNumber())
                .role(user.getRole())
                .enabled(user.getEnabled())
                .emailVerified(user.getEmailVerified())
                .createdAt(user.getCreatedAt())
                .updatedAt(user.getUpdatedAt())
                .build();
    }
}
