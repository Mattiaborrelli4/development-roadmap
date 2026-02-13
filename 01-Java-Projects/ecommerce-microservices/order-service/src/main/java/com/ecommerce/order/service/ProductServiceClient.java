package com.ecommerce.order.service;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

@Service
public class ProductServiceClient {

    private final WebClient webClient;

    @Value("${product.service.url}")
    private String productServiceUrl;

    public ProductServiceClient(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.build();
    }

    public boolean checkAvailability(Long productId, Integer quantity) {
        try {
            Boolean available = webClient.get()
                    .uri(productServiceUrl + "/api/products/" + productId + "/availability?quantity=" + quantity)
                    .retrieve()
                    .bodyToMono(Boolean.class)
                    .block();
            return available != null && available;
        } catch (Exception e) {
            return false;
        }
    }

    public String getProductName(Long productId) {
        try {
            JsonNode response = webClient.get()
                    .uri(productServiceUrl + "/api/products/" + productId)
                    .retrieve()
                    .bodyToMono(JsonNode.class)
                    .block();
            return response != null ? response.get("name").asText() : null;
        } catch (Exception e) {
            return null;
        }
    }

    public java.math.BigDecimal getProductPrice(Long productId) {
        try {
            JsonNode response = webClient.get()
                    .uri(productServiceUrl + "/api/products/" + productId)
                    .retrieve()
                    .bodyToMono(JsonNode.class)
                    .block();
            return response != null ? response.get("price").decimalValue() : null;
        } catch (Exception e) {
            return null;
        }
    }

    public boolean reserveStock(Long productId, Integer quantity) {
        try {
            Map<String, Integer> request = new HashMap<>();
            request.put("quantity", quantity);

            webClient.post()
                    .uri(productServiceUrl + "/api/products/" + productId + "/reserve")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(Void.class)
                    .block();
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean releaseStock(Long productId, Integer quantity) {
        try {
            Map<String, Integer> request = new HashMap<>();
            request.put("quantity", quantity);

            webClient.patch()
                    .uri(productServiceUrl + "/api/products/" + productId + "/stock")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(Void.class)
                    .block();
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
