// products.js - Database dei prodotti
export const products = [
  {
    id: 1,
    name: "Laptop Pro 15",
    price: 1299.99,
    image: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop",
    category: "Elettronica",
    description: "Laptop professionale con processore di ultima generazione"
  },
  {
    id: 2,
    name: "Smartphone X",
    price: 799.99,
    image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop",
    category: "Elettronica",
    description: "Smartphone premium con fotocamera avanzata"
  },
  {
    id: 3,
    name: "Cuffie Wireless",
    price: 199.99,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop",
    category: "Audio",
    description: "Cuffie bluetooth con cancellazione del rumore"
  },
  {
    id: 4,
    name: "Smart Watch",
    price: 349.99,
    image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop",
    category: "Wearable",
    description: "Orologio intelligente con monitoraggio salute"
  },
  {
    id: 5,
    name: "Tablet Pro",
    price: 599.99,
    image: "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop",
    category: "Elettronica",
    description: "Tablet versatile per lavoro e intrattenimento"
  },
  {
    id: 6,
    name: "Fotocamera DSLR",
    price: 899.99,
    image: "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400&h=300&fit=crop",
    category: "Fotografia",
    description: "Fotocamera professionale per fotografi amatoriali"
  },
  {
    id: 7,
    name: "Mouse Gaming",
    price: 79.99,
    image: "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop",
    category: "Accessori",
    description: "Mouse gaming ad alte prestazioni"
  },
  {
    id: 8,
    name: "Tastiera Meccanica",
    price: 129.99,
    image: "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop",
    category: "Accessori",
    description: "Tastiera meccanica RGB retroilluminata"
  }
];

// Funzione per ottenere un prodotto per ID
export const getProductById = (id) => {
  return products.find(product => product.id === parseInt(id));
};

// Funzione per filtrare prodotti per categoria
export const getProductsByCategory = (category) => {
  return products.filter(product => product.category === category);
};

// Categorie uniche
export const getCategories = () => {
  return [...new Set(products.map(product => product.category))];
};
