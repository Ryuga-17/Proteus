import { useState } from "react";
import { cn } from "@/lib/utils";

interface ProductGalleryProps {
  images: string[];
}

const ProductGallery = ({ images }: ProductGalleryProps) => {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <div className="flex flex-col-reverse sm:flex-row gap-3 sm:gap-4">
      {/* Thumbnail Strip - Left side on desktop, bottom on mobile */}
      <div className="flex sm:flex-col gap-2 sm:gap-3 overflow-x-auto sm:overflow-x-visible sm:w-20 pb-1 sm:pb-0 scrollbar-hide">
        {images.map((img, index) => (
          <button
            key={index}
            onClick={() => setActiveIndex(index)}
            className={cn(
              "shrink-0 overflow-hidden rounded-lg transition-all duration-300 border-2",
              activeIndex === index
                ? "border-primary shadow-md scale-105"
                : "border-transparent opacity-70 hover:opacity-100 hover:border-border"
            )}
          >
            <img
              src={img}
              alt={`View ${index + 1}`}
              className="w-16 h-20 sm:w-20 sm:h-24 object-cover rounded-md"
            />
          </button>
        ))}
      </div>

      {/* Main Image */}
      <div className="flex-1 overflow-hidden rounded-xl sm:rounded-2xl bg-card border border-border/50 shadow-sm">
        <img
          src={images[activeIndex]}
          alt="Product main view"
          className="w-full h-72 sm:h-96 lg:h-[520px] object-cover transition-all duration-500"
        />
      </div>
    </div>
  );
};

export default ProductGallery;
