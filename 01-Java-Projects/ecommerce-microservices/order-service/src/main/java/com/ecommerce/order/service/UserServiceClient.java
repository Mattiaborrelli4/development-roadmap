package com.ecommerce.order.service;

import com.ecommerce.order.dto.OrderDTO;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class UserServiceClient {

    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    @Value("${user.service.url}")
    private String userServiceUrl;

    public UserServiceClient(WebClient.Builder webClientBuilder, ObjectMapper objectMapper) {
        this.webClient = webClientBuilder.build();
        this.objectMapper = objectMapper;
    }

    public boolean validateUser(Long userId) {
        try {
            Boolean isValid = webClient.get()
                    .uri(userServiceUrl + "/api/users/validate/" + userId)
                    .retrieve()
                    .bodyToMono(Boolean.class)
                    .block();
            return isValid != null && isValid;
        } catch (Exception e) {
            return false;
        }
    }

    public String getUsername(Long userId) {
        try {
            JsonNode response = webClient.get()
                    .uri(userServiceUrl + "/api/users/" + userId)
                    .retrieve()
                    .bodyToMono(JsonNode.class)
                    .block();
            return response != null ? response.get("username").asText() : null;
        } catch (Exception e) {
            return null;
        }
    }
}
