// Dati di esempio per i prodotti
export const products = [
  {
    id: 1,
    name: "Smartphone Pro Max",
    category: "Elettronica",
    price: 899.99,
    originalPrice: 1099.99,
    image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1598327105666-5b89351aff70?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600&h=600&fit=crop"
    ],
    description: "Smartphone di ultima generazione con display AMOLED da 6.7 pollici, processore octa-core, 8GB di RAM e 256GB di storage. Fotocamera principale da 108MP con stabilizzazione ottica.",
    features: ["Display 6.7\" AMOLED", "256GB Storage", "8GB RAM", "Fotocamera 108MP", "5G"],
    rating: 4.8,
    reviews: 234,
    stock: 15,
    featured: true
  },
  {
    id: 2,
    name: "Laptop UltraBook",
    category: "Elettronica",
    price: 1299.99,
    originalPrice: 1499.99,
    image: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&h=600&fit=crop"
    ],
    description: "Laptop ultraleggero con display retina da 15.6\", processore Intel Core i7 di undicesima generazione, 16GB di RAM e SSD da 512GB. Perfetto per il lavoro e il gaming leggero.",
    features: ["Intel Core i7", "16GB RAM", "512GB SSD", "Display 15.6\"", "Windows 11"],
    rating: 4.9,
    reviews: 187,
    stock: 8,
    featured: true
  },
  {
    id: 3,
    name: "Cuffie Wireless Premium",
    category: "Elettronica",
    price: 299.99,
    originalPrice: 349.99,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&h=600&fit=crop"
    ],
    description: "Cuffie wireless con cancellazione del rumore attiva, 30 ore di autonomia e supporto per audio ad alta risoluzione. Design premium e comfort elevato.",
    features: ["ANC Active", "30h Autonomia", "Hi-Res Audio", "Bluetooth 5.2", "Foldable"],
    rating: 4.7,
    reviews: 312,
    stock: 25,
    featured: false
  },
  {
    id: 4,
    name: "Smartwatch Fitness",
    category: "Elettronica",
    price: 199.99,
    originalPrice: 249.99,
    image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&h=600&fit=crop"
    ],
    description: "Smartwatch con monitoraggio completo della salute, GPS integrato, resistenza all'acqua 5ATM e oltre 100 modalità sport.",
    features: ["GPS Integrato", "5ATM Water Resistant", "Health Monitor", "100+ Sport Modes", "7 Day Battery"],
    rating: 4.6,
    reviews: 156,
    stock: 30,
    featured: false
  },
  {
    id: 5,
    name: "Fotocamera Mirrorless 4K",
    category: "Elettronica",
    price: 1599.99,
    originalPrice: 1799.99,
    image: "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1606985523755-5112af8d76f4?w=600&h=600&fit=crop"
    ],
    description: "Fotocamera mirrorless professionale con sensore APS-C, registrazione video 4K a 60fps e stabilizzazione dell'immagine a 5 assi.",
    features: ["4K 60fps", "APS-C Sensor", "5-Axis Stabilization", "WiFi", "Touchscreen"],
    rating: 4.9,
    reviews: 89,
    stock: 5,
    featured: true
  },
  {
    id: 6,
    name: "T-Shirt Premium Cotton",
    category: "Abbigliamento",
    price: 39.99,
    originalPrice: 49.99,
    image: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600&h=600&fit=crop"
    ],
    description: "T-shirt in cotone premium 100%, taglio moderno e comfort elevato. Disponibile in più colori.",
    features: ["100% Cotton", "Modern Fit", "Breathable", "Machine Washable", "Multiple Colors"],
    rating: 4.5,
    reviews: 445,
    stock: 100,
    featured: false
  },
  {
    id: 7,
    name: "Jeans Slim Fit",
    category: "Abbigliamento",
    price: 79.99,
    originalPrice: 99.99,
    image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=600&h=600&fit=crop"
    ],
    description: "Jeans slim fit in denim di alta qualità. Comfort elevato grazie alla tecnologia stretch-flex.",
    features: ["Stretch-Flex", "Slim Fit", "Premium Denim", "5 Pockets", "Multiple Washes"],
    rating: 4.6,
    reviews: 267,
    stock: 75,
    featured: false
  },
  {
    id: 8,
    name: "Giacca Invernale",
    category: "Abbigliamento",
    price: 149.99,
    originalPrice: 199.99,
    image: "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1544923246-77307dd628b0?w=600&h=600&fit=crop"
    ],
    description: "Giacca invernale con imbottitura termica, cappuccio rimovibile e resistenza all'acqua.",
    features: ["Thermal Insulation", "Water Resistant", "Removable Hood", "Multiple Pockets", "Windproof"],
    rating: 4.7,
    reviews: 123,
    stock: 40,
    featured: true
  },
  {
    id: 9,
    name: "Scarpe Sportive",
    category: "Abbigliamento",
    price: 119.99,
    originalPrice: 149.99,
    image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=600&h=600&fit=crop"
    ],
    description: "Scarpe sportive con suola in memory foam, tessuto traspirante e design ergonomico.",
    features: ["Memory Foam", "Breathable Mesh", "Ergonomic Design", "Non-slip Sole", "Lightweight"],
    rating: 4.8,
    reviews: 389,
    stock: 60,
    featured: false
  },
  {
    id: 10,
    name: "Zaino Laptop",
    category: "Accessori",
    price: 69.99,
    originalPrice: 89.99,
    image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&h=600&fit=crop"
    ],
    description: "Zaino ergonomico con scomparto per laptop fino a 17\", tasche multiple e resistenza all'acqua.",
    features: ["17\" Laptop Compartment", "Water Resistant", "USB Charging Port", "Anti-theft", "Ergonomic"],
    rating: 4.6,
    reviews: 234,
    stock: 50,
    featured: false
  },
  {
    id: 11,
    name: "Sedia Gaming Ergonomica",
    category: "Casa",
    price: 299.99,
    originalPrice: 399.99,
    image: "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1600490670103-42b8c99e962e?w=600&h=600&fit=crop"
    ],
    description: "Sedia gaming ergonomica con supporto lombare, poggiatesta regolabile e braccioli 4D.",
    features: ["4D Armrests", "Lumbar Support", "180° Recline", "Premium PU Leather", "Weight 150kg"],
    rating: 4.8,
    reviews: 178,
    stock: 20,
    featured: true
  },
  {
    id: 12,
    name: "Lampada LED Smart",
    category: "Casa",
    price: 49.99,
    originalPrice: 69.99,
    image: "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1565814329452-e1efa11c5b89?w=600&h=600&fit=crop"
    ],
    description: "Lampada LED smart con controllo app, 16 milioni di colori e sincronizzazione musica.",
    features: ["16M Colors", "App Control", "Music Sync", "Voice Control", "Energy Efficient"],
    rating: 4.5,
    reviews: 512,
    stock: 80,
    featured: false
  },
  {
    id: 13,
    name: "Divano Moderno 3 Posti",
    category: "Casa",
    price: 799.99,
    originalPrice: 999.99,
    image: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1540574163026-643ea20ade25?w=600&h=600&fit=crop"
    ],
    description: "Divano moderno 3 posti in tessuto premium, schienali reclinabili e design elegante.",
    features: ["Premium Fabric", "Reclinable Backrests", "Solid Wood Frame", "High Density Foam", "Easy Assembly"],
    rating: 4.9,
    reviews: 67,
    stock: 10,
    featured: true
  },
  {
    id: 14,
    name: "Tavolo da Pranzo",
    category: "Casa",
    price: 449.99,
    originalPrice: 549.99,
    image: "https://images.unsplash.com/photo-1617806118233-18e1de247200?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1617806118233-18e1de247200?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=600&h=600&fit=crop"
    ],
    description: "Tavolo da pranzo in legno massello, design moderno e capacità per 6 persone.",
    features: ["Solid Wood", "Seats 6", "Modern Design", "Easy Assembly", "Scratch Resistant"],
    rating: 4.7,
    reviews: 93,
    stock: 15,
    featured: false
  },
  {
    id: 15,
    name: "Orologio da Parete",
    category: "Casa",
    price: 59.99,
    originalPrice: 79.99,
    image: "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=600&h=600&fit=crop"
    ],
    description: "Orologio da parete di design moderno, movimento al quarzo silenzioso.",
    features: ["Silent Movement", "Modern Design", "Easy to Read", "Battery Operated", "Lightweight"],
    rating: 4.4,
    reviews: 278,
    stock: 45,
    featured: false
  },
  {
    id: 16,
    name: "Borsa Donna Pelle",
    category: "Accessori",
    price: 129.99,
    originalPrice: 169.99,
    image: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=600&h=600&fit=crop"
    ],
    description: "Borsa in vera pelle, chiusura con cerniera e multiple tasche interne.",
    features: ["Genuine Leather", "Zip Closure", "Multiple Pockets", "Adjustable Strap", "Dust Bag Included"],
    rating: 4.7,
    reviews: 189,
    stock: 35,
    featured: false
  },
  {
    id: 17,
    name: "Occhiali da Sole",
    category: "Accessori",
    price: 89.99,
    originalPrice: 119.99,
    image: "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&h=600&fit=crop"
    ],
    description: "Occhiali da sole con lenti polarizzate UV400 e montatura in titanio.",
    features: ["UV400 Protection", "Polarized", "Titanium Frame", "Lightweight", "Case Included"],
    rating: 4.6,
    reviews: 298,
    stock: 65,
    featured: false
  },
  {
    id: 18,
    name: "Tablet Pro 12.9",
    category: "Elettronica",
    price: 1099.99,
    originalPrice: 1299.99,
    image: "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop",
    images: [
      "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&h=600&fit=crop",
      "https://images.unsplash.com/photo-1561154464-82e9adf3277a?w=600&h=600&fit=crop"
    ],
    description: "Tablet professionale con display Retina da 12.9\", supporto Apple Pencil e keyboard.",
    features: ["12.9\" Retina Display", "256GB Storage", "Face ID", "Apple Pencil Support", "All-day Battery"],
    rating: 4.9,
    reviews: 145,
    stock: 12,
    featured: true
  }
];

export const categories = [
  "Tutti",
  "Elettronica",
  "Abbigliamento",
  "Casa",
  "Accessori"
];

export const featuredProducts = products.filter(p => p.featured);
