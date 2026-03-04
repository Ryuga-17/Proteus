import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

interface CategoryCardProps {
  title: string;
  image: string;
  href: string;
  className?: string;
  style?: React.CSSProperties;
}

const CategoryCard = ({ title, image, href, className, style }: CategoryCardProps) => {
  return (
    <Link
      to={href}
      className={cn(
        "group relative overflow-hidden rounded-xl hover-lift block",
        className
      )}
      style={style}
    >
      <div className="absolute inset-0 bg-gradient-to-t from-foreground/70 via-foreground/20 to-transparent z-10" />
      <img
        src={image}
        alt={title}
        className="w-full h-full object-cover image-hover"
      />
      <div className="absolute bottom-0 left-0 right-0 p-6 z-20">
        <h3 className="font-serif text-xl lg:text-2xl text-white font-medium">
          {title}
        </h3>
        
      </div>
    </Link>
  );
};

export default CategoryCard;
