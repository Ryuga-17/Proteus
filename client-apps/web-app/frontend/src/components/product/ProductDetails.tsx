import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Star, ShoppingBag, Zap, Sparkles, Check, Loader2, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import VirtualTryOnModal from "./VirtualTryOnModal";
import StoreLocatorModal from "./StoreLocatorModal";
import { toast } from "sonner";
import { useCart } from "@/contexts/CartContext";

interface ProductDetailsProps {
  product: {
    id?: number;
    name: string;
    price: number;
    originalPrice: number;
    discount: number;
    rating: number;
    reviews: string;
    stock: number;
    sizes: string[];
  };
  productImage?: string;
  mixMatchImage?: string;
}

const ProductDetails = ({ product, productImage, mixMatchImage }: ProductDetailsProps) => {
  const [selectedSize, setSelectedSize] = useState<string | null>("S");
  const [selectedColor, setSelectedColor] = useState<string>("cream");
  const [showTryOnModal, setShowTryOnModal] = useState(false);
  const [showStoreModal, setShowStoreModal] = useState(false);
  const [isAddingToCart, setIsAddingToCart] = useState(false);
  const [justAdded, setJustAdded] = useState(false);
  const [isFlashing, setIsFlashing] = useState(false);
  const { addToCart } = useCart();

  // Available colors
  const colors = [
    { name: "Light Blue", value: "light-blue", hex: "#87CEEB" },
    { name: "Pink", value: "pink", hex: "#FFB6C1" },
    { name: "Cream", value: "cream", hex: "#FFF8DC" },
  ];

  // Recommended size (could be calculated based on user data)
  const recommendedSize = "S";

  const handleSizeSelect = (size: string) => {
    setSelectedSize(size);
    // Flash if non-recommended size is selected
    if (size !== recommendedSize) {
      setIsFlashing(true);
      setTimeout(() => setIsFlashing(false), 600);
    }
  };

  const handleAddToCart = () => {
    // Check if size is selected
    if (!selectedSize) {
      toast.error("Please select a size", {
        description: "Choose your preferred size before adding to bag",
      });
      return;
    }

    // Show loading state
    setIsAddingToCart(true);

    // Simulate adding to cart (would be API call in production)
    setTimeout(() => {
      addToCart({
        id: product.id || 1,
        name: product.name,
        price: product.price,
        size: selectedSize,
        quantity: 1,
        image: productImage || "",
      });

      setIsAddingToCart(false);
      setJustAdded(true);

      toast.success(`${product.name} has been added to your bag!`, {
        description: `Size: ${selectedSize} • ₹${product.price.toLocaleString()}`,
      });

      // Reset the "just added" state after 2 seconds
      setTimeout(() => setJustAdded(false), 2000);
    }, 600);
  };


  return (
    <div className="space-y-4 sm:space-y-6 pb-32 sm:pb-36">
      {/* Try It On Badge - Clickable */}
      <div className="flex justify-end">
        <button
          onClick={() => setShowTryOnModal(true)}
          className="animate-float focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded-full"
        >
          <div className="bg-gradient-to-r from-[#3D94E0] via-[#41A4B4] to-[#44B38A]  px-7 sm:px-7 py-4 sm:py-4 rounded-full shadow-lg flex items-center gap-2 hover:shadow-xl transition-shadow cursor-pointer">
            <Sparkles className="h-7 w-7 sm:h-7 sm:w-7 text-white" />
            <span className="text-xl sm:text-xl font-medium text-white">Try it on</span>
          </div>
        </button>
      </div>

      {/* Product Name */}
      <h1 className="font-serif text-2xl sm:text-3xl lg:text-4xl text-foreground">
        Forever 21
      </h1>
      <h1 className="font-jockey text-2xl sm:text-2xl lg:text-xl text-[#C27A2E]">
        {product.name}
      </h1>

      {/* Price Section */}
      <div className="flex flex-wrap items-center gap-2 sm:gap-4">
        <span className="text-2xl sm:text-3xl font-semibold text-foreground">
          ₹{product.price.toLocaleString()}
        </span>
        <span className="text-base sm:text-lg text-muted-foreground line-through">
          ₹{product.originalPrice.toLocaleString()}
        </span>
        <span className="px-2 sm:px-3 py-0.5 sm:py-1 bg-soft-green/20 text-emerald-500 text-xs sm:text-sm font-medium rounded-full">
          {product.discount}% off
        </span>
      </div>

     {/* Stock & Reviews */}
<div className="flex flex-wrap items-center gap-4 sm:gap-6">
  <div className="flex items-center gap-2">
    <span className="text-2xl sm:text-3xl font-bold text-foreground">
      {product.rating}
    </span>
    <div className="flex flex-col gap-1">
      <div className="flex items-center">
        {[...Array(5)].map((_, i) => (
          <Star
            key={i}
            className={cn(
              "h-3 w-3 sm:h-4 sm:w-4",
              i < Math.floor(product.rating)
                ? "fill-yellow-300 text-yellow-300"
                : "fill-gray-300 text-gray-300"
            )}
          />
        ))}
      </div>
      <span className="text-xs text-muted-foreground">
        ({product.reviews.toLocaleString()} REVIEWS)
      </span>
    </div>
  </div>
</div>

{/* Size Selection */}
<div className="space-y-4 sm:space-y-5">
  <div className="text-sm sm:text-base font-medium text-foreground mb-4">Select Size</div>
  <div className="flex flex-wrap gap-3 sm:gap-4">
    {product.sizes.map((size) => (
      <button
        key={size}
        className={cn(
          "w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center text-sm sm:text-base font-medium transition-all",
          selectedSize === size
            ? "bg-[#EBFFD0] ring-2 ring-emerald-700"
            : "bg-[#EBFFD0] hover:bg-emerald-100"
        )}
        onClick={() => handleSizeSelect(size)}
      >
        {size}
      </button>
    ))}
  </div>
  
  {/* Recommended Size Button */}
  {recommendedSize && (
    <div style={{ marginTop: '24px' }}>
      <button
        onClick={() => setSelectedSize(recommendedSize)}
        className={cn(
          "px-5 py-3 rounded-full font-medium text-base transition-all shadow-md hover:shadow-lg",
          "bg-gradient-to-r from-[#3D94E0] via-[#41A4B4] to-[#44B38A] text-white",
          "hover:opacity-90 flex items-center gap-2",
          isFlashing && selectedSize !== recommendedSize && "animate-flash"
        )}
      >
        <Sparkles className="h-4 w-4" />
        Recommended Size {recommendedSize}
      </button>
    </div>
  )}
</div>

{/* Color Selection */}
<div className="space-y-3">
  <div className="flex items-center justify-between">
    <label className="text-sm sm:text-base font-medium text-foreground">Color</label>
    <ChevronRight className="h-4 w-4 text-muted-foreground" />
  </div>
  <div className="flex gap-3">
    {colors.map((color) => (
      <button
        key={color.value}
        onClick={() => setSelectedColor(color.value)}
        className={cn(
          "w-10 h-10 sm:w-12 sm:h-12 rounded-full border-2 transition-all hover:scale-110",
          selectedColor === color.value
            ? "border-[#B55A00] ring-2 ring-[#B55A00] ring-offset-2"
            : "border-gray-300 hover:border-amber-400"
        )}
        style={{ backgroundColor: color.hex }}
        title={color.name}
        aria-label={`Select ${color.name} color`}
      />
    ))}
  </div>
</div>
      {/* In-Store Try On - Clickable Store Locator */}
      <button
        onClick={() => setShowStoreModal(true)}
        className="w-full cursor-pointer "
      >
       
        <div className="text-left flex-1">
          <span className="w-full glass-card  bg-gradient-to-r from-[#FEBA73] to-[#F9D7AF] text-[#B55A00] py-4 rounded-full font-semibold flex items-center justify-center gap-3 hover:from-orange-400 hover:to-amber-400 transition shadow-md"> <ShoppingBag className="w-5 h-5" />
IN-STORE TRY ON</span>
          <p className="mt-4 text-[20px] sm:text-xs text-muted-foreground text-[#B55A00]">Find stores near you • Click to view locations</p>
        </div>
      </button>

      {/* Action Buttons */}
      {/* Fixed CTA Bar */}
<div className="fixed bottom-0 left-0 right-0 z-50 pb-[env(safe-area-inset-bottom)]">
  <div className="mx-2 sm:mx-4 mb-4 rounded-tl-[30px] rounded-tr-[30px] bg-[#FDB971] ring-1 ring-black/5">
    <div className="max-w-4xl mx-auto p-4 sm:p-5">
      <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 pt-0">
        <Button
          variant={justAdded ? "default" : "ghost"}
          size="lg"
          className={cn(
            // white pill like screenshot
            " flex-1 h-10 sm:h-12 lg:h-14 w-28 sm:w-32 lg:w-36rounded-xl bg-white text-foreground ring-1 ring-black/5 shadow-md hover:shadow-lg hover:bg-white transition-all text-xs sm:text-sm lg:text-base",
                    "text-sm sm:text-base",
            justAdded && "bg-soft-green text-foreground hover:bg-soft-green/90"
          )}
          onClick={handleAddToCart}
          disabled={isAddingToCart}
        >
          {isAddingToCart ? (
            <>
              <Loader2 className="h-4 w-4 sm:h-5 sm:w-5 mr-2 animate-spin" />
              Adding...
            </>
          ) : justAdded ? (
            <>
              <Check className="h-4 w-4 sm:h-5 sm:w-5 mr-2" />
              Added!
            </>
          ) : (
            <>
              <ShoppingBag className="h-4 w-4 sm:h-5 sm:w-5 mr-2" />
              Add to Bag!
            </>
          )}
        </Button>

        <Button
          variant="ghost"
          size="lg"
          className="
    flex-1 
    h-10 sm:h-12 lg:h-14
    w-28 sm:w-32 lg:w-36
    rounded-xl 
    bg-white text-foreground 
    ring-1 ring-black/5 
    shadow-md hover:shadow-lg hover:bg-white 
    transition-all 
    text-xs sm:text-sm lg:text-base
  "
        >
          <Zap className="h-5 w-5 sm:h-6 sm:w-5 mr-2" />
          Buy Now
        </Button>
      </div>
    </div>
  </div>
</div>


      {/* Virtual Try-On Modal */}
      <VirtualTryOnModal
        open={showTryOnModal}
        onOpenChange={setShowTryOnModal}
        productImage={productImage || ""}
        productName={product.name}
      />

      {/* Store Locator Modal */}
      <StoreLocatorModal
        open={showStoreModal}
        onOpenChange={setShowStoreModal}
      />
    </div>
  );
};

export default ProductDetails;
