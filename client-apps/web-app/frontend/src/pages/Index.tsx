import Layout from "@/components/layout/Layout";
import HeroSection from "@/components/home/HeroSection";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

// Import generated images
import heroFashion from "@/assets/purpledress.png";
import greenDress from "@/assets/orangeMan.png";
import orangeSweater from "@/assets/necklace.png";
import jewelry from "@/assets/brownMan.png";
import productSweater from "@/assets/girlinred.png";

const galleryImages = [greenDress, orangeSweater, jewelry, productSweater];

const Index = () => {
  return (
    <Layout>
      <HeroSection heroImage={heroFashion} galleryImages={galleryImages} />
      
      {/* Featured Section */}
      <section className="container mx-auto px-6 py-16">
        <div className="flex items-center justify-between mb-8">
          <h2 className="font-serif text-3xl text-foreground">New Arrivals</h2>
          <Button variant="heroText" asChild className="group">
            <Link to="/products" className="flex items-center gap-2">
              View all
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Link>
          </Button>
        </div>
        
        <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6">
          {[
            { name: "Cashmere Sweater", price: "₹2,499", img: productSweater },
            { name: "Emerald Silk Dress", price: "₹3,899", img: greenDress },
            { name: "Orange Knit Sweater", price: "₹1,599", img: orangeSweater },
            { name: "Pearl Jewelry Set", price: "₹4,999", img: jewelry },
          ].map((item, i) => (
            <Link
              key={i}
              to="/products/1"
              className="group block overflow-hidden rounded-xl hover-lift opacity-0 animate-slide-up"
              style={{ animationDelay: `${i * 0.1}s`, animationFillMode: "forwards" }}
            >
              <div className="aspect-[3/4] overflow-hidden rounded-xl mb-3">
                <img
                  src={item.img}
                  alt={item.name}
                  className="w-full h-full object-cover image-hover"
                />
              </div>
              <h3 className="font-sans text-foreground font-medium group-hover:text-primary transition-colors">
                {item.name}
              </h3>
              <p className="text-muted-foreground">{item.price}</p>
            </Link>
          ))}
        </div>
      </section>
    </Layout>
  );
};

export default Index;
