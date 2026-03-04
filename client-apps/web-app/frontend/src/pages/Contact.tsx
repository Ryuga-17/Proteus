import Layout from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { MapPin, Phone, Mail, Clock } from "lucide-react";

const Contact = () => {
  return (
    <Layout>
      <div className="container mx-auto px-4 sm:px-6 py-6 sm:py-8">
        <div className="text-center mb-8 sm:mb-12">
          <h1 className="font-serif text-3xl sm:text-4xl lg:text-5xl text-primary mb-3 sm:mb-4">
            Get in Touch
          </h1>
          <p className="text-sm sm:text-base text-muted-foreground max-w-lg mx-auto px-4">
            We'd love to hear from you. Reach out with questions, feedback, or just to say hello.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 lg:gap-12 max-w-5xl mx-auto">
          {/* Contact Form */}
          <div className="glass-card rounded-xl sm:rounded-2xl p-5 sm:p-8 opacity-0 animate-slide-up" style={{ animationDelay: "0.1s", animationFillMode: "forwards" }}>
            <h2 className="font-serif text-xl sm:text-2xl text-foreground mb-4 sm:mb-6">Send us a message</h2>
            <form className="space-y-4 sm:space-y-6">
              <div className="grid sm:grid-cols-2 gap-3 sm:gap-4">
                <div className="space-y-1.5 sm:space-y-2">
                  <label className="text-xs sm:text-sm font-medium text-foreground">First Name</label>
                  <Input placeholder="John" className="bg-background/50 text-sm" />
                </div>
                <div className="space-y-1.5 sm:space-y-2">
                  <label className="text-xs sm:text-sm font-medium text-foreground">Last Name</label>
                  <Input placeholder="Doe" className="bg-background/50 text-sm" />
                </div>
              </div>
              <div className="space-y-1.5 sm:space-y-2">
                <label className="text-xs sm:text-sm font-medium text-foreground">Email</label>
                <Input type="email" placeholder="john@example.com" className="bg-background/50 text-sm" />
              </div>
              <div className="space-y-1.5 sm:space-y-2">
                <label className="text-xs sm:text-sm font-medium text-foreground">Message</label>
                <Textarea placeholder="Tell us how we can help..." rows={4} className="bg-background/50 text-sm sm:rows-5" />
              </div>
              <Button variant="action" size="lg" className="w-full text-sm sm:text-base">
                Send Message
              </Button>
            </form>
          </div>

          {/* Contact Info */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-3 sm:gap-4 lg:gap-6">
            <div className="glass-card rounded-xl sm:rounded-2xl p-4 sm:p-6 opacity-0 animate-slide-in-right" style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}>
              <div className="flex items-start gap-3 sm:gap-4">
                <div className="p-2 sm:p-3 rounded-lg bg-primary/10 shrink-0">
                  <MapPin className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium text-foreground mb-0.5 sm:mb-1 text-sm sm:text-base">Visit Our Store</h3>
                  <p className="text-muted-foreground text-xs sm:text-sm">
                    123 Fashion Street, Design District<br />
                    Mumbai, Maharashtra 400001
                  </p>
                </div>
              </div>
            </div>

            <div className="glass-card rounded-xl sm:rounded-2xl p-4 sm:p-6 opacity-0 animate-slide-in-right" style={{ animationDelay: "0.3s", animationFillMode: "forwards" }}>
              <div className="flex items-start gap-3 sm:gap-4">
                <div className="p-2 sm:p-3 rounded-lg bg-primary/10 shrink-0">
                  <Phone className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium text-foreground mb-0.5 sm:mb-1 text-sm sm:text-base">Call Us</h3>
                  <p className="text-muted-foreground text-xs sm:text-sm">
                    +91 98765 43210<br />
                    +91 11 2345 6789
                  </p>
                </div>
              </div>
            </div>

            <div className="glass-card rounded-xl sm:rounded-2xl p-4 sm:p-6 opacity-0 animate-slide-in-right" style={{ animationDelay: "0.4s", animationFillMode: "forwards" }}>
              <div className="flex items-start gap-3 sm:gap-4">
                <div className="p-2 sm:p-3 rounded-lg bg-primary/10 shrink-0">
                  <Mail className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium text-foreground mb-0.5 sm:mb-1 text-sm sm:text-base">Email Us</h3>
                  <p className="text-muted-foreground text-xs sm:text-sm">
                    hello@proteus.com<br />
                    support@proteus.com
                  </p>
                </div>
              </div>
            </div>

            <div className="glass-card rounded-xl sm:rounded-2xl p-4 sm:p-6 opacity-0 animate-slide-in-right" style={{ animationDelay: "0.5s", animationFillMode: "forwards" }}>
              <div className="flex items-start gap-3 sm:gap-4">
                <div className="p-2 sm:p-3 rounded-lg bg-primary/10 shrink-0">
                  <Clock className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium text-foreground mb-0.5 sm:mb-1 text-sm sm:text-base">Store Hours</h3>
                  <p className="text-muted-foreground text-xs sm:text-sm">
                    Mon - Sat: 10:00 AM - 9:00 PM<br />
                    Sunday: 11:00 AM - 7:00 PM
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Contact;
