import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { ShoppingBag, Search, User, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { useCart } from "@/contexts/CartContext";

const navLinks = [
  { name: "HOME", path: "/" },
  { name: "PRODUCTS", path: "/products" },
  { name: "GALLERY", path: "/gallery" },
  { name: "CONTACT", path: "/contact" },
];

const Header = () => {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  const { itemCount } = useCart();

  return (
<header className="fixed top-0 left-1/2 transform -translate-x-1/2 w-full max-w-368 lg:max-w-16xl z-50 bg-[#FFF6E4] backdrop-blur-md border-b border-border/50 rounded-b-2xl shadow-sm">      <div className="container mx-auto px-6 sm:px-6 py-3 sm:py-4">
        {/* Mobile Header */}
        <div className="flex items-center justify-between lg:hidden">
          {/* Mobile Menu Trigger */}
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="text-foreground">
                <Menu className="h-6 w-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-72 bg-background p-6">
              <div className="flex flex-col h-full">
                <div className="mb-8">
                  <Link to="/" onClick={() => setIsOpen(false)}>
                    <h1 className="font-kurale text-3xl text-[#B55A00]">
                      Proteus
                    </h1>
                  </Link>
                </div>
                <nav className="flex-1">
                  <ul className="space-y-4">
                    {navLinks.map((link) => (
                      <li key={link.name}>
                        <Link
                          to={link.path}
                          onClick={() => setIsOpen(false)}
                          className={cn(
                            "block font-sans text-lg tracking-wide transition-colors py-2",
                            location.pathname === link.path
                              ? "text-primary font-medium"
                              : "text-muted-foreground hover:text-foreground"
                          )}
                        >
                          {link.name}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </nav>
              </div>
            </SheetContent>
          </Sheet>

          {/* Mobile Logo */}
          <Link to="/" className="group">
            <h1 className="font-kurale text-2xl tracking-wide text-[#B55A00] transition-colors group-hover:text-primary">
              Proteus
            </h1>
          </Link>

          {/* Mobile Right Icons */}
          <div className="flex items-center gap-1">
            <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground h-9 w-9 relative" asChild>
              <Link to="/cart">
                <ShoppingBag className="h-5 w-5" />
                {itemCount > 0 && (
                  <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-primary text-[10px] font-medium text-primary-foreground flex items-center justify-center">
                    {itemCount > 99 ? "99+" : itemCount}
                  </span>
                )}
              </Link>
            </Button>
          </div>
        </div>

        {/* Desktop Header */}
        <div className="hidden lg:block">
          {/* Logo */}
          <div className="flex justify-center mb-3">
            <Link to="/" className="group">
              <h1 className="font-kurale text-4xl tracking-wide text-[#B55A00] transition-colors group-hover:text-primary">
                Proteus
              </h1>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="flex items-center justify-between">
            <ul className="flex items-center gap-8">
              {navLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.path}
                    className={cn(
                      "font-sans text-sm tracking-widest transition-all duration-300 relative py-1",
                      location.pathname === link.path
                        ? "text-[#b55a00] font-medium"
                        : "text-muted-[#b55a00] hover:text-foreground"
                    )}
                  >
                    {link.name}
                    <span
                      className={cn(
                        "absolute bottom-0 left-0 h-0.5 bg-[#b55a00] transition-all duration-300",
                        location.pathname === link.path ? "w-full" : "w-0 group-hover:w-full"
                      )}
                    />
                  </Link>
                </li>
              ))}
            </ul>

            {/* Right side icons */}
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground">
                <Search className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground">
                <User className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground relative" asChild>
                <Link to="/cart">
                  <ShoppingBag className="h-5 w-5" />
                  {itemCount > 0 && (
                    <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-primary text-[10px] font-medium text-primary-foreground flex items-center justify-center">
                      {itemCount > 99 ? "99+" : itemCount}
                    </span>
                  )}
                </Link>
              </Button>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
