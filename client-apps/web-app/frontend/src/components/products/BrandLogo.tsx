import { cn } from "@/lib/utils";

interface BrandLogoProps {
  name: string;
  className?: string;
  style?: React.CSSProperties;
}

const BrandLogo = ({ name, className, style }: BrandLogoProps) => {
  return (
    <div
      className={cn(
        "flex items-center justify-center px-6 py-4 bg-card/50 rounded-lg border border-border/30 hover:border-primary/30 transition-all duration-300 hover-lift",
        className
      )}
      style={style}
    >
      <span className="font-sans text-sm font-medium text-muted-foreground tracking-wider uppercase">
        {name}
      </span>
    </div>
  );
};

export default BrandLogo;
