package com.ecommerce.order.service;

import com.ecommerce.order.dto.*;
import com.ecommerce.order.model.Order;
import com.ecommerce.order.model.OrderItem;
import com.ecommerce.order.repository.OrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
public class OrderService {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private UserServiceClient userServiceClient;

    @Autowired
    private ProductServiceClient productServiceClient;

    public List<OrderDTO> getAllOrders() {
        return orderRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    public List<OrderDTO> getOrdersByUserId(Long userId) {
        return orderRepository.findByUserIdOrderByOrderDateDesc(userId).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    public OrderDTO getOrderByOrderNumber(String orderNumber) {
        return orderRepository.findByOrderNumber(orderNumber)
                .map(this::convertToDTO)
                .orElse(null);
    }

    public OrderDTO getOrderById(Long id) {
        return orderRepository.findById(id)
                .map(this::convertToDTO)
                .orElse(null);
    }

    @Transactional
    public OrderDTO createOrder(CreateOrderRequest request) {
        // Validazione utente
        if (!userServiceClient.validateUser(request.getUserId())) {
            throw new RuntimeException("Utente non valido");
        }

        if (request.getItems() == null || request.getItems().isEmpty()) {
            throw new RuntimeException("L'ordine deve contenere almeno un prodotto");
        }

        // Validazione disponibilità prodotti
        for (OrderItemRequest item : request.getItems()) {
            if (!productServiceClient.checkAvailability(item.getProductId(), item.getQuantity())) {
                throw new RuntimeException("Prodotto " + item.getProductId() + " non disponibile o quantità insufficiente");
            }
        }

        // Creazione ordine
        Order order = new Order();
        order.setUserId(request.getUserId());
        order.setOrderNumber(generateOrderNumber());
        order.setShippingAddress(request.getShippingAddress());
        order.setStatus(Order.OrderStatus.PENDING);

        // Creazione order items e calcolo totale
        BigDecimal totalAmount = BigDecimal.ZERO;

        for (OrderItemRequest itemRequest : request.getItems()) {
            OrderItem item = new OrderItem();
            item.setOrder(order);
            item.setProductId(itemRequest.getProductId());
            item.setQuantity(itemRequest.getQuantity());
            item.setProductName(productServiceClient.getProductName(itemRequest.getProductId()));
            item.setUnitPrice(productServiceClient.getProductPrice(itemRequest.getProductId()));
            item.calculateSubtotal();

            order.getItems().add(item);
            totalAmount = totalAmount.add(item.getSubtotal());
        }

        order.setTotalAmount(totalAmount);

        // Salvataggio ordine
        Order savedOrder = orderRepository.save(order);

        // Riserva stock
        for (OrderItemRequest itemRequest : request.getItems()) {
            if (!productServiceClient.reserveStock(itemRequest.getProductId(), itemRequest.getQuantity())) {
                throw new RuntimeException("Errore nella riserva dello stock per il prodotto " + itemRequest.getProductId());
            }
        }

        return convertToDTO(savedOrder);
    }

    @Transactional
    public OrderDTO updateOrderStatus(Long orderId, String newStatus) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new RuntimeException("Ordine non trovato"));

        try {
            Order.OrderStatus status = Order.OrderStatus.valueOf(newStatus.toUpperCase());
            order.setStatus(status);
            Order updatedOrder = orderRepository.save(order);
            return convertToDTO(updatedOrder);
        } catch (IllegalArgumentException e) {
            throw new RuntimeException("Stato non valido: " + newStatus);
        }
    }

    @Transactional
    public void cancelOrder(Long orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new RuntimeException("Ordine non trovato"));

        if (order.getStatus() == Order.OrderStatus.SHIPPED || order.getStatus() == Order.OrderStatus.DELIVERED) {
            throw new RuntimeException("Impossibile cancellare un ordine già spedito o consegnato");
        }

        // Rilascio stock
        for (OrderItem item : order.getItems()) {
            productServiceClient.releaseStock(item.getProductId(), item.getQuantity());
        }

        order.setStatus(Order.OrderStatus.CANCELLED);
        orderRepository.save(order);
    }

    private String generateOrderNumber() {
        return "ORD-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }

    private OrderDTO convertToDTO(Order order) {
        List<OrderItemDTO> itemDTOs = order.getItems().stream()
                .map(item -> new OrderItemDTO(
                        item.getId(),
                        item.getProductId(),
                        item.getProductName(),
                        item.getQuantity(),
                        item.getUnitPrice(),
                        item.getSubtotal()
                ))
                .collect(Collectors.toList());

        return new OrderDTO(
                order.getId(),
                order.getUserId(),
                order.getOrderNumber(),
                order.getTotalAmount(),
                order.getStatus().name(),
                order.getOrderDate(),
                order.getShippingAddress(),
                itemDTOs
        );
    }
}
