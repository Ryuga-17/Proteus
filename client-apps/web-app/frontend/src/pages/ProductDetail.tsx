import { useParams, useNavigate, Link } from "react-router-dom";
import Layout from "@/components/layout/Layout";
import ProductGallery from "@/components/product/ProductGallery";
import ProductDetails from "@/components/product/ProductDetails";
import { getProductById, getProductsByCategory } from "@/data/products";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

const ProductDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const productId = parseInt(id || "1", 10);
  const product = getProductById(productId);

  const productImages = product?.images || [];

  // Fallback if product not found
  if (!product) {
    return (
      <Layout>
        <div className="container mx-auto px-4 sm:px-6 py-12 text-center">
          <h1 className="font-serif text-3xl text-foreground mb-4">Product Not Found</h1>
          <p className="text-muted-foreground mb-6">The product you're looking for doesn't exist.</p>
          <Button onClick={() => navigate(-1)} variant="outline" className="gap-2">
            <ArrowLeft className="h-4 w-4" />
            Go Back
          </Button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container mx-auto px-4 sm:px-6 py-6 sm:py-8">
        <div className="mb-4 sm:mb-6 opacity-0 animate-fade-in" style={{ animationFillMode: "forwards" }}>
          <button 
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors text-sm"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to collection
          </button>
        </div>

        <div className="grid lg:grid-cols-2 gap-6 sm:gap-8 lg:gap-12">
          <div className="opacity-0 animate-fade-in" style={{ animationDelay: "0.1s", animationFillMode: "forwards" }}>
            <ProductGallery images={productImages} />
          </div>

          <div className="opacity-0 animate-slide-in-right" style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}>
            <ProductDetails 
              product={product} 
              productImage={productImages[0]}
            />
          </div>
        </div>

        <div className="mt-12 sm:mt-16 opacity-0 animate-fade-in" style={{ animationDelay: "0.3s", animationFillMode: "forwards" }}>
          <h2 className="font-serif text-2xl sm:text-3xl text-foreground mb-6 sm:mb-8">
            Similar Items
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
            {getProductsByCategory(product.category)
              .filter((p) => p.id !== product.id)
              .slice(0, 4)
              .map((similarProduct, index) => (
                <Link
                  key={similarProduct.id}
                  to={`/products/${similarProduct.id}`}
                  className="group opacity-0 animate-slide-up"
                  style={{ animationDelay: `${index * 0.1}s`, animationFillMode: "forwards" }}
                >
                  <div className="bg-card rounded-xl sm:rounded-2xl overflow-hidden hover-lift border border-border/50">
                    <div className="relative aspect-[3/4] overflow-hidden">
                      <img
                        src={similarProduct.images[0]}
                        alt={similarProduct.name}
                        className="w-full h-full object-cover image-hover"
                      />
                      <div className="absolute top-2 left-2 sm:top-3 sm:left-3 bg-soft-green text-foreground text-xs font-medium px-2 py-1 rounded-full">
                        {similarProduct.discount}% OFF
                      </div>
                    </div>
                    <div className="p-3 sm:p-4">
                      <h3 className="font-medium text-foreground text-sm sm:text-base mb-1 line-clamp-2 group-hover:text-primary transition-colors">
                        {similarProduct.name}
                      </h3>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-base sm:text-lg font-semibold text-foreground">
                          ₹{similarProduct.price.toLocaleString()}
                        </span>
                        <span className="text-xs sm:text-sm text-muted-foreground line-through">
                          ₹{similarProduct.originalPrice.toLocaleString()}
                        </span>
                      </div>
                      <div className="flex items-center gap-1">
                        <span className="text-xs text-muted-foreground">
                          ⭐ {similarProduct.rating}
                        </span>
                        <span className="text-xs text-muted-foreground">
                          ({similarProduct.reviews})
                        </span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ProductDetail;
