package com.example.auth.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class EmailService {

    private static final Logger log = LoggerFactory.getLogger(EmailService.class);

    @Value("${email.verification.enabled:true}")
    private boolean emailVerificationEnabled;

    @Value("${email.verification.mock-delay:1000}")
    private long mockDelay;

    public void sendVerificationEmail(String to, String verificationToken) {
        if (!emailVerificationEnabled) {
            log.info("Verifica email disabilitata. Token per {}: {}", to, verificationToken);
            return;
        }

        // Simula l'invio dell'email con un delay
        try {
            Thread.sleep(mockDelay);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        String verificationUrl = "http://localhost:8080/api/auth/verify?token=" + verificationToken;

        log.info("===========================================");
        log.info("MOCK EMAIL - Verifica Email");
        log.info("===========================================");
        log.info("A: {}", to);
        log.info("Oggetto: Verifica il tuo account");
        log.info("Messaggio:");
        log.info("Ciao,");
        log.info("");
        log.info("Per verificare il tuo account, clicca sul link seguente:");
        log.info(verificationUrl);
        log.info("");
        log.info("Questo link scadrà tra 24 ore.");
        log.info("===========================================");
    }

    public void sendPasswordResetEmail(String to, String resetToken) {
        if (!emailVerificationEnabled) {
            log.info("Reset password email disabilitata. Token per {}: {}", to, resetToken);
            return;
        }

        // Simula l'invio dell'email con un delay
        try {
            Thread.sleep(mockDelay);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        String resetUrl = "http://localhost:8080/api/auth/reset-password?token=" + resetToken;

        log.info("===========================================");
        log.info("MOCK EMAIL - Reset Password");
        log.info("===========================================");
        log.info("A: {}", to);
        log.info("Oggetto: Reset della password");
        log.info("Messaggio:");
        log.info("Ciao,");
        log.info("");
        log.info("Per resettare la tua password, clicca sul link seguente:");
        log.info(resetUrl);
        log.info("");
        log.info("Questo link scadrà tra 1 ora.");
        log.info("===========================================");
    }
}
