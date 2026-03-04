import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles, Image as ImageIcon } from "lucide-react";
import VoiceSearch from "./VoiceSearch";

interface HeroSectionProps {
  heroImage: string;
  galleryImages: string[]; // can be fewer than 6
}

const HeroSection = ({ heroImage, galleryImages }: HeroSectionProps) => {
  const allImages = [heroImage, ...galleryImages].slice(0, 5);
  
  return (
    <section className="container mx-auto px-4 sm:px-6 py-8 sm:py-12">
      <div className="grid lg:grid-cols-2 gap-8 lg:gap-12 items-start">
        {/* Left - Hero Text */}
        <div className="space-y-6 sm:space-y-8 animate-fade-in order-1 lg:order-1">
          <div className="mt-4 sm:mt-6 lg:mt-28 space-y-3 sm:space-y-4">
            {/* Voice Search Component */}
            <VoiceSearch />
            
            <h2 className="font-kurale text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl leading-tight text-[#b55a00]">
              Shop quality apparel in a tap
            </h2>
            <p className="text-base sm:text-lg text-muted-foreground font-sans max-w-md">
              Drip without having to drain your pockets
            </p>
          </div>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-start gap-3 sm:gap-4">
            <Button
              variant="hero"
              size="lg"
              className="sm:size-xl w-full sm:w-auto bg-[#F6F1D1] rounded-2xl hover:bg-[#ebddb0] transition-colors duration-300"
              asChild
            >
              <Link
                to="/shop/women"
                className="flex items-center justify-center gap-2 group text-[#5a4320] hover:text-[#b55a00]"
              >
                Shop Women
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </Button>

            <Button
              variant="heroText"
              size="lg"
              className="sm:size-xl w-full sm:w-auto bg-[#ebddb0] rounded-2xl hover:bg-[#F6F1D1] transition-colors duration-300"
              asChild
            >
              <Link
                to="/shop/men"
                className="flex items-center justify-center gap-2 group text-[#5a4320] hover:text-[#b55a00]"
              >
                Shop Men
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </Button>
          </div>

          {/* Immersive Experience Box */}
          <div className="rounded-xl sm:rounded-2xl p-4 sm:p-6 max-w-md hover-lift bg-[linear-gradient(90deg,#F0FFDD_40%,#FAE4CD_100%)] shadow-sm transition-transform duration-300">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-lg bg-accent/50 shrink-0">
                <Sparkles className="h-4 w-4 sm:h-5 sm:w-5 text-soft-green" />
              </div>
              <div>
                <h3 className="font-serif text-base sm:text-lg font-medium text-foreground mb-1 sm:mb-2">
                  Immersive Experience
                </h3>
                <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                  Experience fashion like never before, with in-store try-ons and immersive 3D virtual try-ons at your fingertips.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Right - Masonry Style Image Gallery - Hidden on mobile */}
        <div className="hidden lg:grid grid-cols-2 gap-4 order-2 animate-slide-in-right auto-rows-auto">
          {/* Left Column - Taller images */}
          <div className="flex flex-col gap-4">
            {allImages[0] && (
              <div className="overflow-hidden rounded-3xl hover-lift col-span-1">
                <img
                  src={allImages[0]}
                  alt="Fashion 1"
                  className="w-full h-[600px] object-cover image-hover"
                />
              </div>
            )}
            {allImages[3] && (
              <div className="overflow-hidden rounded-3xl hover-lift">
                <img
                  src={allImages[3]}
                  alt="Fashion 4"
                  className="w-full h-[480px] object-cover image-hover"
                />
              </div>
            )}
          </div>

          {/* Right Column - Varied heights */}
          <div className="flex flex-col gap-4 mt-8">
            {allImages[1] && (
              <div className="overflow-hidden rounded-3xl hover-lift">
                <img
                  src={allImages[1]}
                  alt="Fashion 2"
                  className="w-full h-[350px] object-cover image-hover"
                />
              </div>
            )}
            {allImages[2] && (
              <div className="overflow-hidden rounded-3xl hover-lift">
                <img
                  src={allImages[2]}
                  alt="Fashion 3"
                  className="w-full h-[350px] object-cover image-hover"
                />
              </div>
            )}
            {allImages[4] ? (
              <div className="overflow-hidden rounded-3xl hover-lift">
                <img
                  src={allImages[4]}
                  alt="Fashion 5"
                  className="w-full h-[440px] object-cover image-hover"
                />
              </div>
            ) : (
              <div className="flex items-center justify-center rounded-3xl bg-[#F6F1D1] h-[240px] hover-lift border border-border/40">
                <ImageIcon className="h-10 w-10 text-[#b55a00]/70" />
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;