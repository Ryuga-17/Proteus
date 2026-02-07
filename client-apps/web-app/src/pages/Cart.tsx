import { useState, useMemo, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { Minus, Plus, Trash2, Sparkles, Shirt, Check, Loader2 } from "lucide-react";
import { useCart } from "@/contexts/CartContext";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { processPurchase } from "@/services/recommendationApi";

const Cart = () => {
  const { items, updateQuantity, removeFromCart, clearCart } = useCart();
  const [selectedItems, setSelectedItems] = useState<Set<string>>(
    new Set(items.map((item) => `${item.id}-${item.size}`))
  );
  const [isProcessing, setIsProcessing] = useState(false);

  // Update selectedItems when items change (select all new items by default)
  useEffect(() => {
    setSelectedItems((prev) => {
      const newSet = new Set(prev);
      items.forEach((item) => {
        const key = `${item.id}-${item.size}`;
        if (!newSet.has(key)) {
          newSet.add(key);
        }
      });
      // Remove keys for items that no longer exist
      Array.from(newSet).forEach((key) => {
        const exists = items.some((item) => `${item.id}-${item.size}` === key);
        if (!exists) {
          newSet.delete(key);
        }
      });
      return newSet;
    });
  }, [items]);

  const toggleItemSelection = (itemId: number, size: string) => {
    const key = `${itemId}-${size}`;
    setSelectedItems((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(key)) {
        newSet.delete(key);
      } else {
        newSet.add(key);
      }
      return newSet;
    });
  };

  const isItemSelected = (itemId: number, size: string) => {
    return selectedItems.has(`${itemId}-${size}`);
  };

  // Get selected items only
  const selectedItemsList = useMemo(() => {
    return items.filter((item) => isItemSelected(item.id, item.size));
  }, [items, selectedItems]);

  // Calculate order totals based on selected items only
  const totals = useMemo(() => {
    const subtotal = selectedItemsList.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const gst = subtotal * 0.18; // 18% GST
    const grandTotal = subtotal + gst;
    return { subtotal, shipping: 0, gst, grandTotal };
  }, [selectedItemsList]);

  // Calculate Drip Score based on selected items only
  const dripScoreData = useMemo(() => {
    const itemCount = selectedItemsList.length;
    let score = 0;
    let recommendation = "";
    let mood = "";

    // Base score from number of items
    if (itemCount >= 4) {
      score = 75 + Math.floor(Math.random() * 20); // 75-95 for complete outfits
      recommendation = "Looking good! Add neutral sneakers to balance the look.";
      mood = "Cozy Core";
    } else if (itemCount === 3) {
      score = 60 + Math.floor(Math.random() * 15); // 60-75
      recommendation = "Great start! Consider adding accessories to elevate your style.";
      mood = "Casual Chic";
    } else if (itemCount === 2) {
      score = 45 + Math.floor(Math.random() * 15); // 45-60
      recommendation = "Nice picks! Add a few more items to complete your look.";
      mood = "Minimalist";
    } else if (itemCount === 1) {
      score = 30 + Math.floor(Math.random() * 15); // 30-45
      recommendation = "Start building your outfit! Mix and match with more pieces.";
      mood = "Getting Started";
    } else {
      score = 0;
      recommendation = "Your cart is empty. Start shopping to build your perfect look!";
      mood = "";
    }

    // Clamp score between 0-100
    score = Math.min(100, Math.max(0, score));

    return { score, recommendation, mood };
  }, [selectedItemsList]);

  const handleQuantityChange = (id: number, size: string, newQuantity: number) => {
    if (newQuantity < 1) {
      removeFromCart(id, size);
      toast.success("Item removed from cart");
    } else {
      updateQuantity(id, size, newQuantity);
    }
  };

  // Extract brand name from product name (simple extraction, can be enhanced)
  const getBrandName = (item: typeof items[0]) => {
    // You can enhance this with actual brand data
    const brands: { [key: string]: string } = {
      "Knitted woolen jumper": "Forever 21",
      "Wide legged jeans": "Van Huesen",
      "Sling Purse": "Reebok",
      "White Sneakers": "Reebok",
    };
    return brands[item.name] || "Proteus";
  };

  // Handle purchase/checkout
  const handlePurchase = async () => {
    if (selectedItemsList.length === 0) {
      toast.error("Please select items to purchase");
      return;
    }

    setIsProcessing(true);
    
    try {
      // Convert cart items to purchase items
      const purchaseItems = selectedItemsList.map(item => ({
        product_id: item.id.toString(),
        sku: `PROD${item.id}`, // Generate SKU from product ID
        quantity: item.quantity,
        size: item.size || undefined
      }));

      const result = await processPurchase(
        purchaseItems,
        "default_user",
        "store_main_street"
      );

      if (result.success) {
        toast.success(`Purchase successful! Order ID: ${result.order_id}`);
        
        // Remove purchased items from cart
        selectedItemsList.forEach(item => {
          removeFromCart(item.id, item.size);
        });
        
        // Clear selection
        setSelectedItems(new Set());
        
        // Show success message with order ID
        setTimeout(() => {
          toast.info(`Your order ${result.order_id} has been placed. Stock has been updated.`);
        }, 1000);
      } else {
        toast.error(result.message || "Purchase failed");
        if (result.errors && result.errors.length > 0) {
          result.errors.forEach(error => {
            toast.error(error);
          });
        }
      }
    } catch (error: any) {
      console.error("Purchase error:", error);
      toast.info("Checkout needs the backend. Your cart is saved locally—add a backend to complete orders.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 sm:px-6 py-6 sm:py-8 pb-24 lg:pb-6">
        <h1 className="font-serif text-3xl sm:text-4xl text-[#B55A00] mb-6 sm:mb-8">
          Your Cart
        </h1>

        <div className="grid lg:grid-cols-3 gap-6 sm:gap-8">
          {/* Cart Items - Left Column (2/3 on desktop) */}
          <div className="lg:col-span-2 space-y-4">
            {items.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 sm:p-12 text-center">
                <p className="text-lg text-muted-foreground mb-4">Your cart is empty</p>
                <Button
                  onClick={() => window.location.href = "/products"}
                  className="bg-[#F6B45A] text-white hover:bg-[#e3a44f]"
                >
                  Start Shopping
                </Button>
              </div>
            ) : (
              items.map((item, index) => {
                const isSelected = isItemSelected(item.id, item.size);
                return (
                  <div
                    key={`${item.id}-${item.size}`}
                    className={cn(
                      "rounded-2xl p-4 sm:p-6 shadow-sm border-2 hover:shadow-md transition-all",
                      isSelected
                        ? "bg-white border-[#B55A00]"
                        : "bg-gray-50 border-amber-100 opacity-60"
                    )}
                  >
                    <div className="flex gap-4 sm:gap-6">
                      {/* Selection Checkbox */}
                      <button
                        onClick={() => toggleItemSelection(item.id, item.size)}
                        className="flex-shrink-0 mt-2"
                      >
                        <div
                          className={cn(
                            "w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all",
                            isSelected
                              ? "bg-[#B55A00] border-[#B55A00]"
                              : "border-gray-300 hover:border-[#B55A00]"
                          )}
                        >
                          {isSelected && <Check className="h-4 w-4 text-white" />}
                        </div>
                      </button>

                      {/* Product Image */}
                      <div className="w-24 h-24 sm:w-32 sm:h-32 flex-shrink-0 rounded-xl overflow-hidden bg-gray-100">
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          // Fallback image if image fails to load
                          e.currentTarget.src = "https://via.placeholder.com/300x400?text=Product";
                        }}
                      />
                    </div>

                    {/* Product Details */}
                    <div className="flex-1 flex flex-col justify-between min-w-0">
                      <div>
                        <p className="text-sm sm:text-base font-semibold text-[#B55A00] mb-1">
                          {getBrandName(item)}
                        </p>
                        <h3 className="text-base sm:text-lg font-medium text-foreground mb-2 truncate">
                          {item.name}
                        </h3>
                        <p className="text-lg sm:text-xl font-semibold text-foreground">
                          ₹{item.price.toLocaleString()}
                        </p>
                        {item.size && (
                          <p className="text-sm text-muted-foreground mt-1">
                            Size: {item.size}
                          </p>
                        )}
                      </div>

                      {/* Quantity Controls */}
                      <div className="flex items-center justify-between mt-4">
                        <div className="flex items-center gap-1">
                          <button
                            onClick={() => handleQuantityChange(item.id, item.size, item.quantity - 1)}
                            className="w-8 h-8 border border-amber-300 bg-white flex items-center justify-center text-[#B55A00] hover:bg-amber-50 transition-colors"
                          >
                            <Minus className="h-4 w-4" />
                          </button>
                          <span className="text-base sm:text-lg font-semibold text-foreground w-10 text-center bg-amber-50 border-y border-amber-300 py-1.5">
                            {item.quantity}
                          </span>
                          <button
                            onClick={() => handleQuantityChange(item.id, item.size, item.quantity + 1)}
                            className="w-8 h-8 border border-amber-300 bg-white flex items-center justify-center text-[#B55A00] hover:bg-amber-50 transition-colors"
                          >
                            <Plus className="h-4 w-4" />
                          </button>
                        </div>

                        <button
                          onClick={() => {
                            removeFromCart(item.id, item.size);
                            toast.success("Item removed from cart");
                          }}
                          className="text-muted-foreground hover:text-red-600 transition-colors p-2"
                        >
                          <Trash2 className="h-5 w-5" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                );
              })
            )}
          </div>

          {/* Right Column (1/3 on desktop) */}
          <div className="lg:col-span-1 space-y-6">
            {/* Drip Score Widget */}
            {items.length > 0 && (
              <div className="bg-white rounded-2xl p-6 shadow-lg border border-amber-100">
                <div className="relative mb-4">
                  <div className="w-full h-14 bg-gradient-to-r from-emerald-300 via-teal-300 to-cyan-300 rounded-full border-2 border-gray-800 flex items-center justify-between px-4 relative overflow-visible">
                    {/* Left section with sparkle and text */}
                    <div className="flex items-center gap-2 z-10">
                      <Sparkles className="h-6 w-6 text-blue-900 -ml-2" />
                      <span className="text-base font-bold text-gray-900">Drip Score</span>
                    </div>
                    
                    {/* Middle section with mannequin icon */}
                    <div className="absolute left-1/2 transform -translate-x-1/2 z-10">
                      <Shirt className="h-6 w-6 text-gray-900" />
                    </div>
                    
                    {/* Right section with score */}
                    <div className="z-10">
                      <span className="text-2xl font-bold text-gray-900">{dripScoreData.score}</span>
                    </div>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mb-3">
                  {dripScoreData.recommendation}
                </p>
                {dripScoreData.mood && (
                  <span className="inline-block px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm font-medium">
                    Mood: {dripScoreData.mood}
                  </span>
                )}
              </div>
            )}

            {/* Address Section */}
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-amber-100">
              <h2 className="text-xl font-bold text-[#B55A00] mb-4">Delivery Address</h2>
              <div className="space-y-2 text-sm sm:text-base text-foreground">
                <p className="font-medium">John Doe</p>
                <p className="text-muted-foreground">123 Main Street</p>
                <p className="text-muted-foreground">Apartment 4B</p>
                <p className="text-muted-foreground">Mumbai, Maharashtra 400001</p>
                <p className="text-muted-foreground mt-3">Phone: +91 98765 43210</p>
              </div>
            </div>

            {/* Order Summary */}
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-amber-100 sticky top-24 mb-4">
              <h2 className="text-xl font-bold text-[#B55A00] mb-4">Order Summary</h2>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center pb-3 border-b border-gray-200">
                  <span className="text-base text-foreground">Subtotal:</span>
                  <span className="text-base font-semibold text-foreground">₹{totals.subtotal.toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center pb-3 border-b border-gray-200">
                  <span className="text-base text-foreground">Shipping:</span>
                  <span className="text-base font-semibold text-foreground">FREE</span>
                </div>
                <div className="flex justify-between items-center pb-3 border-b border-gray-200">
                  <span className="text-base text-foreground">GST:</span>
                  <span className="text-base font-semibold text-foreground">₹{totals.gst.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center pt-2">
                  <span className="text-lg font-bold text-foreground">Grand Total:</span>
                  <span className="text-lg font-bold text-foreground">
                    ₹{totals.grandTotal.toFixed(2)}
                  </span>
                </div>
              </div>
            </div>

            {/* Sticky Buttons at Bottom - Right Side Only */}
            <div className="fixed bottom-0 left-0 right-0 z-50 bg-transparent lg:bg-transparent">
              <div className="container mx-auto px-4 sm:px-6 py-2 lg:px-6 lg:py-0">
                <div className="grid lg:grid-cols-3 gap-6 sm:gap-8">
                  {/* Spacer for left 2 columns on large screens */}
                  <div className="hidden lg:block lg:col-span-2"></div>
                  
                  {/* Buttons in right column */}
                  <div className="lg:col-span-1">
                    <div className="flex gap-3">
                      <Button
                        className="flex-1 h-16 bg-[#FFF7E4] border border-[#B55A00] text-[#B55A00] hover:bg-[#FFF7E4]/90 font-semibold rounded-tl-lg rounded-tr-lg disabled:opacity-50"
                        disabled={selectedItemsList.length === 0 || isProcessing}
                        onClick={handlePurchase}
                      >
                        {isProcessing ? (
                          <span className="flex items-center gap-2">
                            <Loader2 className="h-5 w-5 animate-spin" />
                            Processing...
                          </span>
                        ) : (
                          "Proceed to pay"
                        )}
                      </Button>
                      <Button
                        className="flex-1 h-16 bg-[#FFF7E4] border border-[#B55A00] text-[#B55A00] hover:bg-[#FFF7E4]/90 font-semibold rounded-tl-lg rounded-tr-lg"
                        onClick={() => {
                          toast.info("Coupon feature coming soon!");
                        }}
                      >
                        Apply coupon
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Cart;

