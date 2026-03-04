import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { MapPin, Navigation, Clock, Phone, ExternalLink } from "lucide-react";

interface Store {
  id: number;
  name: string;
  address: string;
  distance: number;
  phone: string;
  hours: string;
  lat: number;
  lng: number;
}

interface StoreLocatorModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

// Sample store data
const storesData: Store[] = [
  {
    id: 1,
    name: "Proteus Flagship - MG Road",
    address: "12, MG Road, Bangalore, Karnataka 560001",
    distance: 2.3,
    phone: "+91 80 4567 8901",
    hours: "10:00 AM - 9:00 PM",
    lat: 12.9716,
    lng: 77.5946,
  },
  {
    id: 2,
    name: "Proteus - Indiranagar",
    address: "100 Feet Road, Indiranagar, Bangalore 560038",
    distance: 4.7,
    phone: "+91 80 4567 8902",
    hours: "10:00 AM - 9:00 PM",
    lat: 12.9784,
    lng: 77.6408,
  },
  {
    id: 3,
    name: "Proteus - Phoenix Mall",
    address: "Phoenix MarketCity, Whitefield, Bangalore 560066",
    distance: 8.2,
    phone: "+91 80 4567 8903",
    hours: "11:00 AM - 10:00 PM",
    lat: 12.9973,
    lng: 77.6961,
  },
  {
    id: 4,
    name: "Proteus - Koramangala",
    address: "80 Feet Road, Koramangala, Bangalore 560034",
    distance: 5.1,
    phone: "+91 80 4567 8904",
    hours: "10:00 AM - 9:00 PM",
    lat: 12.9352,
    lng: 77.6245,
  },
  {
    id: 5,
    name: "Proteus - UB City",
    address: "UB City Mall, Vittal Mallya Road, Bangalore 560001",
    distance: 3.5,
    phone: "+91 80 4567 8905",
    hours: "10:00 AM - 10:00 PM",
    lat: 12.9712,
    lng: 77.5964,
  },
];

const StoreLocatorModal = ({ open, onOpenChange }: StoreLocatorModalProps) => {
  const [stores, setStores] = useState<Store[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (open) {
      setIsLoading(true);
      // Simulate getting user location and sorting by distance
      setTimeout(() => {
        const sortedStores = [...storesData].sort((a, b) => a.distance - b.distance);
        setStores(sortedStores);
        setIsLoading(false);
      }, 1000);
    }
  }, [open]);

  const handleGetDirections = (store: Store) => {
    // Open Google Maps with directions
    const mapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${store.lat},${store.lng}&destination_place_id=${encodeURIComponent(store.address)}`;
    window.open(mapsUrl, "_blank");
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px] max-h-[80vh] p-0 overflow-hidden">
        <DialogHeader className="p-4 sm:p-6 pb-0 border-b border-border">
          <DialogTitle className="font-serif text-xl sm:text-2xl flex items-center gap-2">
            <MapPin className="h-5 w-5 text-primary" />
            Find a Store
          </DialogTitle>
          <p className="text-muted-foreground text-sm mt-1">
            Stores sorted by distance from your location
          </p>
        </DialogHeader>

        <div className="overflow-y-auto max-h-[60vh] p-4 sm:p-6 pt-4">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-12">
              <div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin mb-3" />
              <p className="text-sm text-muted-foreground">Finding stores near you...</p>
            </div>
          ) : (
            <div className="space-y-3">
              {stores.map((store, index) => (
                <div
                  key={store.id}
                  className="bg-card border border-border rounded-xl p-4 hover:border-primary/30 transition-colors opacity-0 animate-slide-up"
                  style={{ animationDelay: `${index * 0.1}s`, animationFillMode: "forwards" }}
                >
                  <div className="flex justify-between items-start gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-medium text-foreground text-sm truncate">
                          {store.name}
                        </h3>
                        <span className="shrink-0 bg-soft-green/20 text-soft-green text-xs font-medium px-2 py-0.5 rounded-full">
                          {store.distance} km
                        </span>
                      </div>
                      <p className="text-muted-foreground text-xs mb-2 line-clamp-2">
                        {store.address}
                      </p>
                      <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {store.hours}
                        </span>
                        <span className="flex items-center gap-1">
                          <Phone className="h-3 w-3" />
                          {store.phone}
                        </span>
                      </div>
                    </div>
                    <Button
                      onClick={() => handleGetDirections(store)}
                      variant="action"
                      size="sm"
                      className="shrink-0"
                    >
                      <Navigation className="h-4 w-4 mr-1" />
                      <span className="hidden sm:inline">Directions</span>
                      <ExternalLink className="h-3 w-3 sm:hidden" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

       
      </DialogContent>
    </Dialog>
  );
};

export default StoreLocatorModal;
