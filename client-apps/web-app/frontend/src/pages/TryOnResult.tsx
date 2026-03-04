import { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Share2, Download, ShoppingBag, Check, Loader2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { useCart } from "@/contexts/CartContext";
import { useTryOn } from "@/contexts/TryOnContext";
import tryOnPic from "@/assets/TryOnPic.png";
import MixMatchGallery from "@/components/product/MixMatchGallery";

const TryOnResult = () => {
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { tryOnResult } = useTryOn();
  const [selectedColor, setSelectedColor] = useState<string>("cream");
  const [isAddingToCart, setIsAddingToCart] = useState(false);
  const [justAdded, setJustAdded] = useState(false);

  // Redirect if no try-on result
  useEffect(() => {
    if (!tryOnResult) {
      toast.error("No try-on result found. Please try again.");
      navigate("/products");
    }
  }, [tryOnResult, navigate]);

  if (!tryOnResult) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-8 flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-[#B55A00]" />
            <p className="text-muted-foreground">Loading try-on result...</p>
          </div>
        </div>
      </Layout>
    );
  }

  const colors = [
    { name: "Light Blue", value: "light-blue", hex: "#87CEEB", selected: selectedColor === "light-blue" },
    { name: "Pink", value: "pink", hex: "#FFB6C1", selected: selectedColor === "pink" },
    { name: "Cream", value: "cream", hex: "#FFF8DC", selected: selectedColor === "cream" },
  ];

  const product = {
    id: 1,
    name: tryOnResult.productName || "Knitted woolen jumper",
    price: 1599,
  };

  const handleAddToCart = () => {
    setIsAddingToCart(true);

    setTimeout(() => {
      addToCart({
        id: product.id,
        name: product.name,
        price: product.price,
        size: "M", // Default size
        quantity: 1,
        image: tryOnPic,
      });

      setIsAddingToCart(false);
      setJustAdded(true);

      toast.success(`${product.name} has been added to your bag!`, {
        description: `Color: ${colors.find(c => c.value === selectedColor)?.name} • ₹${product.price.toLocaleString()}`,
      });

      setTimeout(() => setJustAdded(false), 2000);
    }, 600);
  };

  const handleBuyNow = () => {
    handleAddToCart();
    setTimeout(() => {
      navigate("/products");
    }, 800);
  };

  const handleViewProduct = (productId: number) => {
    navigate(`/products/${productId}`);
  };

  const handleSuggestionAddToCart = (productId: number) => {
    toast.success("Added to cart!", {
      description: "Suggested item has been added to your shopping bag",
    });
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 sm:px-6 py-6 sm:py-8">
        {/* Header */}
        <div className="mb-6 sm:mb-8">
          <Button
            variant="ghost"
            onClick={() => navigate(-1)}
            className="gap-2 text-[#B55A00] hover:text-[#A04A00] hover:bg-amber-50 mb-4"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </Button>
          <h1 className="font-serif text-3xl sm:text-4xl lg:text-5xl text-[#B55A00] mb-2">
            Your Virtual Try-On
          </h1>
          <p className="text-sm sm:text-base text-muted-foreground">
            See how the outfit looks on you!
          </p>
        </div>

        {/* Main Content */}
        <div className="flex flex-col lg:flex-row gap-6 sm:gap-8 items-center lg:items-start">
          {/* Image Section */}
          <div className="w-full lg:w-2/3 flex justify-center">
            <div className="relative w-full max-w-2xl">
              <div className="relative rounded-2xl sm:rounded-3xl overflow-hidden shadow-2xl bg-white p-4 sm:p-6">
                <img
                  src={tryOnResult.resultImage}
                  alt="Virtual try-on result"
                  className="w-full h-auto rounded-xl sm:rounded-2xl object-contain"
                  onError={(e) => {
                    // Fallback to default image if API result fails to load
                    e.currentTarget.src = tryOnPic;
                  }}
                />
              </div>
            </div>
          </div>

          {/* Action Section */}
          <div className="w-full lg:w-1/3 space-y-4 sm:space-y-6">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 sm:p-8 shadow-lg border border-amber-100">
              <h2 className="text-xl sm:text-2xl font-bold text-[#B55A00] mb-4">
                Love the Look?
              </h2>
              <p className="text-sm sm:text-base text-muted-foreground mb-6">
                Share your virtual try-on or download the image to save for later.
              </p>

              <div className="space-y-3">
                <Button
                  className="w-full gap-2 bg-[#F6B45A] text-white hover:bg-[#e3a44f] h-12 text-base"
                  onClick={() => {
                    if (navigator.share) {
                      navigator.share({
                        title: "My Virtual Try-On",
                        text: "Check out my virtual try-on!",
                        url: window.location.href,
                      });
                    }
                  }}
                >
                  <Share2 className="h-5 w-5" />
                  Share
                </Button>
                <Button
                  variant="outline"
                  className="w-full gap-2 border-2 border-[#B55A00] text-[#B55A00] hover:bg-amber-50 h-12 text-base"
                  onClick={async () => {
                    try {
                      // Convert blob URL to downloadable format
                      const response = await fetch(tryOnResult.resultImage);
                      const blob = await response.blob();
                      const url = window.URL.createObjectURL(blob);
                      const link = document.createElement("a");
                      link.href = url;
                      link.download = "virtual-try-on.png";
                      document.body.appendChild(link);
                      link.click();
                      document.body.removeChild(link);
                      window.URL.revokeObjectURL(url);
                      toast.success("Image downloaded successfully!");
                    } catch (error) {
                      toast.error("Failed to download image");
                    }
                  }}
                >
                  <Download className="h-5 w-5" />
                  Download
                </Button>
              </div>
            </div>

            {/* Color Selection */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 sm:p-8 shadow-lg border border-amber-100">
              <h3 className="text-lg sm:text-xl font-bold text-[#B55A00] mb-4">
                Try these amazing colors!
              </h3>
              <div className="flex gap-4">
                {colors.map((color) => (
                  <button
                    key={color.value}
                    onClick={() => setSelectedColor(color.value)}
                    className={cn(
                      "w-12 h-12 sm:w-14 sm:h-14 rounded-full border-2 transition-all hover:scale-110",
                      color.selected
                        ? "border-[#B55A00] ring-2 ring-[#B55A00] ring-offset-2"
                        : "border-gray-300 hover:border-amber-400"
                    )}
                    style={{ backgroundColor: color.hex }}
                    title={color.name}
                  />
                ))}
              </div>
            </div>

            {/* Buy Now / Add to Bag Buttons */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 sm:p-8 shadow-lg border border-amber-100">
              <div className="space-y-3">
                <Button
                  variant={justAdded ? "default" : "ghost"}
                  className={cn(
                    "w-full h-12 sm:h-14 rounded-xl bg-white text-foreground ring-1 ring-black/5 shadow-md hover:shadow-lg hover:bg-white transition-all text-base",
                    justAdded && "bg-emerald-50 text-foreground hover:bg-emerald-50/90"
                  )}
                  onClick={handleAddToCart}
                  disabled={isAddingToCart}
                >
                  {isAddingToCart ? (
                    <>
                      <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                      Adding...
                    </>
                  ) : justAdded ? (
                    <>
                      <Check className="h-5 w-5 mr-2" />
                      Added!
                    </>
                  ) : (
                    <>
                      <ShoppingBag className="h-5 w-5 mr-2" />
                      Add to Bag!
                    </>
                  )}
                </Button>
                <Button
                  className="w-full h-12 sm:h-14 gap-2 bg-[#F6B45A] text-white hover:bg-[#e3a44f] text-base rounded-xl"
                  onClick={handleBuyNow}
                  disabled={isAddingToCart}
                >
                  Buy Now
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Mix & Match Section */}
        <div className="mt-8 sm:mt-12">
          <MixMatchGallery
            currentProductName={product.name}
            onViewProduct={handleViewProduct}
            onAddToCart={handleSuggestionAddToCart}
          />
        </div>

        {/* Tips Section - Moved to Bottom */}
        <div className="mt-8 sm:mt-12">
          <div className="bg-[#FFF7ED] rounded-2xl p-6 sm:p-8 border border-amber-200">
            <h3 className="text-lg sm:text-xl font-semibold text-[#B55A00] mb-4">
              Tips for Best Results
            </h3>
            <ul className="space-y-3 text-sm sm:text-base text-muted-foreground">
              <li className="flex items-start gap-2">
                <span className="text-amber-600 mt-1">•</span>
                <span>Ensure good lighting for accurate color representation</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-amber-600 mt-1">•</span>
                <span>Stand straight with arms at your sides</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-amber-600 mt-1">•</span>
                <span>Try different angles to see how the fit looks</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default TryOnResult;

