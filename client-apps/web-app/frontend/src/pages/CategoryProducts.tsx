import { useParams, Link } from "react-router-dom";
import Layout from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { Heart, ShoppingBag } from "lucide-react";
import { allProducts, getProductsByCategory } from "@/data/products";

const categoryTitles: Record<string, string> = {
  women: "Women's Collection",
  men: "Men's Collection",
  kids: "Kids' Collection",
  accessories: "Accessories",
  decor: "Home Decor",
};

const CategoryProducts = () => {
  const { category } = useParams<{ category: string }>();
  const products = getProductsByCategory(category || "");
  const categoryTitle = categoryTitles[category || ""] || "Collection";

  return (
    <Layout>
      <div className="container mx-auto px-4 sm:px-6 py-6 sm:py-8">
        {/* Header */}
        <div className="text-center mb-8 sm:mb-12">
          <h1 className="font-serif text-3xl sm:text-4xl md:text-5xl text-primary mb-3">
            {categoryTitle}
          </h1>
          <p className="text-muted-foreground text-sm sm:text-base max-w-md mx-auto">
            Discover our curated selection of premium {category}'s fashion
          </p>
        </div>

        {/* Product Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          {products.map((product, index) => (
            <Link
              key={product.id}
              to={`/products/${product.id}`}
              className="group opacity-0 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s`, animationFillMode: "forwards" }}
            >
              <div className="bg-card rounded-xl sm:rounded-2xl overflow-hidden hover-lift border border-border/50">
                {/* Image Container */}
                <div className="relative aspect-[3/4] overflow-hidden">
                  <img
                    src={product.images[0]}
                    alt={product.name}
                    className="w-full h-full object-cover image-hover"
                  />
                  {/* Discount Badge */}
                  <div className="absolute top-2 left-2 sm:top-3 sm:left-3 bg-soft-green text-foreground text-xs font-medium px-2 py-1 rounded-full">
                    {product.discount}% OFF
                  </div>
                  {/* Wishlist Button */}
                  <button className="absolute top-2 right-2 sm:top-3 sm:right-3 p-1.5 sm:p-2 bg-background/80 backdrop-blur-sm rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
                    <Heart className="h-4 w-4 text-foreground" />
                  </button>
                </div>

                {/* Product Info */}
                <div className="p-3 sm:p-4">
                  <h3 className="font-sans text-sm sm:text-base font-medium text-foreground truncate mb-2">
                    {product.name}
                  </h3>
                  <div className="flex items-center gap-2">
                    <span className="font-serif text-base sm:text-lg font-semibold text-primary">
                      ₹{product.price.toLocaleString()}
                    </span>
                    <span className="text-xs sm:text-sm text-muted-foreground line-through">
                      ₹{product.originalPrice.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Load More */}
        <div className="text-center mt-8 sm:mt-12">
          <Button variant="outline" size="lg" className="gap-2">
            <ShoppingBag className="h-4 w-4" />
            Load More Products
          </Button>
        </div>
      </div>
    </Layout>
  );
};

export default CategoryProducts;
