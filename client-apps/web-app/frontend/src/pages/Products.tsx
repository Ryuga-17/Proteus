import { useState, useEffect } from "react";
import { useSearchParams, Link } from "react-router-dom";
import Layout from "@/components/layout/Layout";
import CategoryCard from "@/components/products/CategoryCard";
import BrandLogo from "@/components/products/BrandLogo";
import { Button } from "@/components/ui/button";
import { ShoppingBag, Heart } from "lucide-react";
import { getProducts } from "@/services/recommendationApi";
import { allProducts } from "@/data/products";
import { useCart } from "@/contexts/CartContext";
import { toast } from "sonner";

// Import generated images
import categoryWomen from "@/assets/chick.png";
import categoryMen from "@/assets/guy.png";
import categoryKids from "@/assets/kiddos.png";
import categoryAccessories from "@/assets/jewel.png";
import categoryDecor from "@/assets/home.png";

const categories = [
  { 
    title: "Shop Women", 
    image: categoryWomen,
    href: "/shop/women"
  },
  { 
    title: "Shop Men", 
    image: categoryMen,
    href: "/shop/men"
  },
  { 
    title: "Shop Kids", 
    image: categoryKids,
    href: "/shop/kids"
  },
  { 
    title: "Shop Accessories", 
    image: categoryAccessories,
    href: "/shop/accessories"
  },
  { 
    title: "Shop Decor", 
    image: categoryDecor,
    href: "/shop/decor"
  },
];

const brands = [
  "Allen Solly",
  "American Eagle",
  "Fred Perry",
  "Tommy Hilfiger",
  "Zara",
  "H&M",
];

const Products = () => {
  const [searchParams] = useSearchParams();
  const searchQuery = searchParams.get("search");
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const { addToCart } = useCart();

  useEffect(() => {
    if (searchQuery) {
      setLoading(true);
      getProducts(undefined, searchQuery)
        .then((data) => {
          setProducts(data.products || []);
          setLoading(false);
        })
        .catch(() => {
          // No backend: fall back to local product search
          const q = searchQuery.toLowerCase();
          const local = allProducts.filter(
            (p) => p.name.toLowerCase().includes(q) || p.category.toLowerCase().includes(q)
          );
          setProducts(local.map((p) => ({ id: p.id, product_id: `PROD${p.id}`, name: p.name, title: p.name, price: p.price, images: p.images, sizes: p.sizes })));
          setLoading(false);
          if (local.length === 0) toast.info("No products match your search.");
        });
    } else {
      setProducts([]);
    }
  }, [searchQuery]);

  const handleAddToCart = (product: any) => {
    addToCart({
      id: parseInt(product.id || product.product_id?.replace("PROD", "") || "1"),
      name: product.name || product.title || "Product",
      price: product.price || 0,
      size: product.sizes?.[0] || "M",
      quantity: 1,
      image: product.images?.[0] || "https://via.placeholder.com/300x400?text=Product"
    });
    toast.success("Added to cart!");
  };

  if (searchQuery) {
    return (
      <Layout>
        <div className="container mx-auto px-4 sm:px-6 py-6 sm:py-8">
          <h1 className="font-serif text-3xl sm:text-4xl text-[#B55A00] mb-6">
            Search Results: "{searchQuery}"
          </h1>
          
          {loading ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">Loading products...</p>
            </div>
          ) : products.length > 0 ? (
            <div className="grid grid-cols-2 gap-4 sm:gap-6">
              {products.map((product, index) => {
                const originalPrice = product.originalPrice || (product.price * 1.35);
                const currentPrice = product.price || 0;
                const discount = Math.round(((originalPrice - currentPrice) / originalPrice) * 100);
                const priceInRupees = Math.round(currentPrice * 83);
                const originalPriceInRupees = Math.round(originalPrice * 83);
                
                return (
                  <div
                    key={product.id || product.product_id || index}
                    className="group relative overflow-hidden rounded-xl hover:shadow-lg transition-all bg-white"
                  >
                    <Link to={`/products/${product.id || product.product_id?.replace("PROD", "") || index + 1}`}>
                      <div className="relative aspect-[3/4] overflow-hidden rounded-xl mb-3 bg-gray-100">
                        <img
                          src={product.images?.[0] || "https://via.placeholder.com/300x400?text=Product"}
                          alt={product.name || product.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                          onError={(e) => {
                            e.currentTarget.src = "https://via.placeholder.com/300x400?text=Product";
                          }}
                        />
                        {discount > 0 && (
                          <div className="absolute top-2 left-2 bg-[#B55A00] text-white px-2 py-1 rounded text-xs font-semibold">
                            {discount}% OFF
                          </div>
                        )}
                      </div>
                      <div className="px-1">
                        <h3 className="font-sans text-sm sm:text-base text-foreground font-medium mb-2 line-clamp-2 min-h-[2.5rem]">
                          {product.name || product.title}
                        </h3>
                        <div className="flex items-center gap-2 mb-3">
                          <span className="text-base sm:text-lg font-bold text-[#B55A00]">
                            ₹{priceInRupees.toLocaleString()}
                          </span>
                          {originalPrice > currentPrice && (
                            <span className="text-sm text-muted-foreground line-through">
                              ₹{originalPriceInRupees.toLocaleString()}
                            </span>
                          )}
                        </div>
                      </div>
                    </Link>
                    <div className="px-1 pb-2">
                      <Button
                        onClick={() => handleAddToCart(product)}
                        className="w-full bg-[#FEB464] hover:bg-[#FEB464]/90 text-white"
                        size="sm"
                      >
                        <ShoppingBag className="h-4 w-4 mr-2" />
                        Add to Cart
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground">No products found for "{searchQuery}"</p>
              <Button
                onClick={() => window.location.href = "/products"}
                className="mt-4"
                variant="outline"
              >
                Browse All Categories
              </Button>
            </div>
          )}
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container mx-auto px-4 sm:px-6 py-6 sm:py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
          <div className="space-y-3 sm:space-y-4">
            <CategoryCard
              {...categories[0]}
              className="h-28 sm:h-36 md:h-50 opacity-0 animate-slide-up"
              style={{ animationDelay: "0s", animationFillMode: "forwards" }}
            />
            <CategoryCard
              {...categories[1]}
              className="h-28 sm:h-36 md:h-50 opacity-0 animate-slide-up"
              style={{ animationDelay: "0.1s", animationFillMode: "forwards" }}
            />
            <CategoryCard
              {...categories[3]}
              className="h-28 sm:h-36 md:h-50 opacity-0 animate-slide-up"
              style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}
            />
          </div>
          <div className="space-y-3 sm:space-y-4 lg:mt-28">
            <CategoryCard
              {...categories[2]}
              className="h-28 sm:h-36 md:h-50 opacity-0 animate-slide-up"
              style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
            />
            <CategoryCard
              {...categories[4]}
              className="h-28 sm:h-36 md:h-50 opacity-0 animate-slide-up"
              style={{ animationDelay: "0.25s", animationFillMode: "forwards" }}
            />
          </div>
        </div>
        <section className="mt-10 sm:mt-16 text-center">
          <Button
            variant="category"
            size="default"
            className="mb-6 sm:mb-8 text-sm sm:text-base"
          >
            Our brands
          </Button>
          <div className="relative overflow-hidden">
            <div className="flex gap-4 sm:gap-8 animate-scroll">
              {[...brands, ...brands, ...brands].map((brand, i) => (
                <BrandLogo key={`${brand}-${i}`} name={brand} className="flex-shrink-0" />
              ))}
            </div>
          </div>
        </section>
      </div>

      <style>{`
        @keyframes scroll {
          0% {
            transform: translateX(0);
          }
          100% {
            transform: translateX(-33.333%);
          }
        }
        .animate-scroll {
          animation: scroll 20s linear infinite;
        }
        .animate-scroll:hover {
          animation-play-state: paused;
        }
      `}</style>
    </Layout>
  );
};

export default Products;
