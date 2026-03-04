import { useRef } from "react";
import { Button } from "@/components/ui/button";
import { ShoppingBag, ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { Sparkles } from "lucide-react";


interface SuggestedProduct {
  id: number;
  name: string;
  price: number;
  image: string;
  category: string;
}

interface MixMatchGalleryProps {
  currentProductName: string;
  suggestions?: SuggestedProduct[];
  onViewProduct?: (productId: number) => void;
  onAddToCart?: (productId: number) => void;
}

// Default suggestions if none provided
const defaultSuggestions: SuggestedProduct[] = [
  {
    id: 101,
    name: "Distressed Slim Jeans",
    price: 2499,
    image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=300&h=400&fit=crop",
    category: "Jeans",
  },
  {
    id: 102,
    name: "Classic Leather Belt",
    price: 899,
    image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=400&fit=crop",
    category: "Accessories",
  },
  {
    id: 103,
    name: "White Sneakers",
    price: 3499,
    image: "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300&h=400&fit=crop",
    category: "Footwear",
  },
  {
    id: 104,
    name: "Minimal Watch",
    price: 4999,
    image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=300&h=400&fit=crop",
    category: "Accessories",
  },
  {
    id: 105,
    name: "Cropped Trousers",
    price: 1999,
    image: "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=300&h=400&fit=crop",
    category: "Pants",
  },
  {
    id: 106,
    name: "Canvas Tote Bag",
    price: 1299,
    image: "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=400&fit=crop",
    category: "Bags",
  },
];

const MixMatchGallery = ({
  currentProductName,
  suggestions = defaultSuggestions,
  onViewProduct,
  onAddToCart,
}: MixMatchGalleryProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  const scroll = (direction: "left" | "right") => {
    if (scrollRef.current) {
      const scrollAmount = 200;
      scrollRef.current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  return (
    <div className="space-y-3 sm:space-y-4">
      <div className="flex items-center justify-between">
        
      <div className="flex flex-col items-center gap-2">
  <div className="bg-gradient-to-r from-[#3D94E0] via-[#41A4B4] to-[#44B38A] px-20 sm:px-20 py-4 sm:py-4 rounded-full shadow-lg flex items-center gap-2 hover:shadow-xl transition-shadow whitespace-nowrap">
    <Sparkles className="h-7 w-7 sm:h-7 sm:w-7 text-white" />
    <span className="text-xl sm:text-xl font-jockey text-white">Mix & Match</span>
  </div>
  <p className="text-[18px] sm:text-[16px] text-[#B55A00]">
    Try your jumper with these jeans
  </p>
</div>

        <div className="hidden sm:flex gap-1">
          <Button
            variant="outline"
            size="icon"
            className="h-8 w-8"
            onClick={() => scroll("left")}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            className="h-8 w-8"
            onClick={() => scroll("right")}
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Horizontal Scrollable Gallery */}
      <div
        ref={scrollRef}
        className="flex gap-3 overflow-x-auto pb-2 scroll-smooth scrollbar-hide"
        style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
      >
        {suggestions.map((product, index) => (
          <div
            key={product.id}
            className={cn(
              "shrink-0 w-[140px] sm:w-[160px] bg-card border border-border rounded-xl overflow-hidden hover:border-primary/30 transition-all hover:-translate-y-1 group",
              "opacity-0 animate-slide-up"
            )}
            style={{ animationDelay: `${index * 0.1}s`, animationFillMode: "forwards" }}
          >
            {/* Product Image */}
            <div className="relative aspect-square overflow-hidden">
              <img
                src={product.image}
                alt={product.name}
                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
              <div className="absolute top-1.5 left-1.5 bg-background/80 backdrop-blur-sm text-foreground text-[10px] px-2 py-0.5 rounded-full">
                {product.category}
              </div>
            </div>

            {/* Product Info */}
            <div className="p-2.5 sm:p-3">
              <h4 className="text-xs sm:text-sm font-medium text-foreground line-clamp-2 mb-1.5 min-h-[2.5rem]">
                {product.name}
              </h4>
              <p className="font-serif text-sm sm:text-base font-semibold text-primary mb-2">
                ₹{product.price.toLocaleString()}
              </p>
              <div className="flex gap-1.5">
                <Button
                  variant="actionOutline"
                  size="sm"
                  className="flex-1 text-[10px] sm:text-xs h-7 sm:h-8 px-2"
                  onClick={() => onAddToCart?.(product.id)}
                >
                  <ShoppingBag className="h-3 w-3 sm:mr-1" />
                  <span className="hidden sm:inline">Add</span>
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-[10px] sm:text-xs h-7 sm:h-8 px-2 text-primary"
                  onClick={() => onViewProduct?.(product.id)}
                >
                  View
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <p className="text-[10px] sm:text-xs text-muted-foreground italic">
        ✨ Suggestions generated by Recommendation Agent based on style matching
      </p>
    </div>
  );
};

export default MixMatchGallery;
