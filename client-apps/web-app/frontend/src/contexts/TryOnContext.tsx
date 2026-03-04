import { createContext, useContext, useState, type ReactNode } from "react";

interface TryOnResult {
  resultImage: string;
  modelImage: string;
  garmentImage: string;
  productName: string;
}

interface TryOnContextType {
  tryOnResult: TryOnResult | null;
  setTryOnResult: (result: TryOnResult | null) => void;
  clearTryOnResult: () => void;
}

const TryOnContext = createContext<TryOnContextType | undefined>(undefined);

export const TryOnProvider = ({ children }: { children: ReactNode }) => {
  const [tryOnResult, setTryOnResult] = useState<TryOnResult | null>(() => {
    // Load from localStorage on mount
    const saved = localStorage.getItem("tryOnResult");
    return saved ? JSON.parse(saved) : null;
  });

  const updateTryOnResult = (result: TryOnResult | null) => {
    setTryOnResult(result);
    if (result) {
      localStorage.setItem("tryOnResult", JSON.stringify(result));
    } else {
      localStorage.removeItem("tryOnResult");
    }
  };

  const clearTryOnResult = () => {
    setTryOnResult(null);
    localStorage.removeItem("tryOnResult");
  };

  return (
    <TryOnContext.Provider
      value={{
        tryOnResult,
        setTryOnResult: updateTryOnResult,
        clearTryOnResult,
      }}
    >
      {children}
    </TryOnContext.Provider>
  );
};

export const useTryOn = () => {
  const context = useContext(TryOnContext);
  if (context === undefined) {
    throw new Error("useTryOn must be used within a TryOnProvider");
  }
  return context;
};

