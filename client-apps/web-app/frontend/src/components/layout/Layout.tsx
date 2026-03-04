import type { ReactNode } from "react";
import Header from "./Header";

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen gradient-background">
      <Header />
      <main className="pt-20 sm:pt-28">{children}</main>
    </div>
  );
};

export default Layout;
