import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { products, categories } from '../data/products';
import ProductList from '../components/ProductList';
import './Products.css';

const Products = () => {
  const [searchParams] = useSearchParams();
  const categoryParam = searchParams.get('category');
  const searchParam = searchParams.get('search');

  const filteredProducts = React.useMemo(() => {
    let filtered = [...products];

    // Filter by category
    if (categoryParam && categoryParam !== 'Tutti') {
      filtered = filtered.filter(p => p.category === categoryParam);
    }

    // Filter by search
    if (searchParam) {
      const searchTerm = searchParam.toLowerCase();
      filtered = filtered.filter(p =>
        p.name.toLowerCase().includes(searchTerm) ||
        p.description.toLowerCase().includes(searchTerm) ||
        p.category.toLowerCase().includes(searchTerm)
      );
    }

    return filtered;
  }, [categoryParam, searchParam]);

  const getPageTitle = () => {
    if (categoryParam) {
      return categoryParam;
    }
    if (searchParam) {
      return `Risultati per "${searchParam}"`;
    }
    return 'Tutti i Prodotti';
  };

  return (
    <div className="products-page">
      <div className="container">
        <div className="page-header">
          <h1>{getPageTitle()}</h1>
          <p>{filteredProducts.length} prodotti trovati</p>
        </div>

        {/* Category Tabs */}
        <div className="category-tabs">
          {categories.map(category => (
            <a
              key={category}
              href={`/products${category === 'Tutti' ? '' : `?category=${encodeURIComponent(category)}`}`}
              className={`category-tab ${(!categoryParam && category === 'Tutti') || categoryParam === category ? 'active' : ''}`}
            >
              {category}
            </a>
          ))}
        </div>

        <ProductList products={filteredProducts} />
      </div>
    </div>
  );
};

export default Products;
