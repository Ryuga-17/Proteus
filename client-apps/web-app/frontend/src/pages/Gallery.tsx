import Layout from "@/components/layout/Layout";

// Import generated images
import heroFashion from "@/assets/purpledress.png";
import greenDress from "@/assets/orangeMan.png";
import orangeSweater from "@/assets/gallery-orange-sweater.jpg";
import jewelry from "@/assets/brownMan.png";
import productSweater from "@/assets/product-white-sweater.jpg";
import categoryMen from "@/assets/category-men.jpg";
import categoryWomen from "@/assets/category-women.jpg";
import categoryKids from "@/assets/category-kids.jpg";

const galleryImages = [
  { src: heroFashion, span: "col-span-2 row-span-2", mobileSpan: "col-span-2" },
  { src: greenDress, span: "", mobileSpan: "" },
  { src: orangeSweater, span: "", mobileSpan: "" },
  { src: categoryWomen, span: "row-span-2", mobileSpan: "" },
  { src: categoryMen, span: "", mobileSpan: "" },
  { src: jewelry, span: "", mobileSpan: "" },
  { src: productSweater, span: "col-span-2", mobileSpan: "col-span-2" },
  { src: categoryKids, span: "", mobileSpan: "" },
];

const Gallery = () => {
  return (
    <Layout>
      <div className="container mx-auto px-4 sm:px-6 py-6 sm:py-8">
        <div className="text-center mb-8 sm:mb-12">
          <h1 className="font-serif text-3xl sm:text-4xl lg:text-5xl text-primary mb-3 sm:mb-4">
            Style Gallery
          </h1>
          <p className="text-sm sm:text-base text-muted-foreground max-w-lg mx-auto px-4">
            Explore our curated collection of fashion inspiration and lifestyle imagery
          </p>
        </div>

        {/* Mobile: 2 columns, Desktop: 4 columns */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 sm:gap-4 auto-rows-[120px] sm:auto-rows-[150px] md:auto-rows-[200px]">
          {galleryImages.map((img, i) => (
            <div
              key={i}
              className={`overflow-hidden rounded-lg sm:rounded-xl hover-lift opacity-0 animate-fade-in cursor-pointer ${img.span}`}
              style={{ animationDelay: `${i * 0.1}s`, animationFillMode: "forwards" }}
            >
              <img
                src={img.src}
                alt={`Gallery ${i + 1}`}
                className="w-full h-full object-cover image-hover"
              />
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
};

export default Gallery;
