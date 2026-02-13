package com.ecommerce.order.dto;

import java.util.List;

public class CreateOrderRequest {
    private Long userId;
    private String shippingAddress;
    private List<OrderItemRequest> items;

    public CreateOrderRequest() {
    }

    public CreateOrderRequest(Long userId, String shippingAddress, List<OrderItemRequest> items) {
        this.userId = userId;
        this.shippingAddress = shippingAddress;
        this.items = items;
    }

    // Getters and Setters
    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getShippingAddress() {
        return shippingAddress;
    }

    public void setShippingAddress(String shippingAddress) {
        this.shippingAddress = shippingAddress;
    }

    public List<OrderItemRequest> getItems() {
        return items;
    }

    public void setItems(List<OrderItemRequest> items) {
        this.items = items;
    }
}
