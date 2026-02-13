package com.ecommerce.product;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ProductServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(ProductServiceApplication.class, args);
        System.out.println("===========================================");
        System.out.println("Product Service avviato sulla porta 8082");
        System.out.println("H2 Console: http://localhost:8082/h2-console");
        System.out.println("===========================================");
    }
}
