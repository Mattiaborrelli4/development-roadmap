package com.ecommerce.order;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class OrderServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
        System.out.println("===========================================");
        System.out.println("Order Service avviato sulla porta 8083");
        System.out.println("H2 Console: http://localhost:8083/h2-console");
        System.out.println("===========================================");
    }
}
