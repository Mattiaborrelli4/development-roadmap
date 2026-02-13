package com.ecommerce.product.dto;

public class UpdateStockRequest {
    private Integer quantity;

    public UpdateStockRequest() {
    }

    public UpdateStockRequest(Integer quantity) {
        this.quantity = quantity;
    }

    // Getters and Setters
    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }
}
