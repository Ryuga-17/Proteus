import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Dialog,
  DialogClose,
  DialogContent,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { UploadCloud, X, CheckCircle2, RefreshCcw, Check, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import correctPose from "@/assets/correct.png";
import wrongPose from "@/assets/wrong.jpg";
import { performVirtualTryOn } from "@/services/virtualTryOnApi";
import { useTryOn } from "@/contexts/TryOnContext";

interface VirtualTryOnModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  productImage: string;
  productName: string;
}

const VirtualTryOnModal = ({
  open,
  onOpenChange,
  productImage,
  productName,
}: VirtualTryOnModalProps) => {
  const navigate = useNavigate();
  const { setTryOnResult } = useTryOn();
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(37);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const revokePreview = useCallback(
    (url: string | null) => {
      if (url && url.startsWith("blob:")) {
        URL.revokeObjectURL(url);
      }
    },
    []
  );

  const resetUpload = useCallback(() => {
    revokePreview(previewUrl);
    setPreviewUrl(null);
    setUploadProgress(37);
    setIsDragging(false);
    setIsUploading(false);
    setIsProcessing(false);
    setUploadedFile(null);
  }, [previewUrl, revokePreview]);

  useEffect(() => {
    return () => revokePreview(previewUrl);
  }, [previewUrl, revokePreview]);

  useEffect(() => {
    if (!open) {
      resetUpload();
    }
  }, [open, resetUpload]);

  const startProgress = () => {
    setIsUploading(true);
    setUploadProgress(42);
    let current = 42;

    const interval = setInterval(() => {
      current = Math.min(current + 14, 100);
      setUploadProgress(current);

      if (current >= 100) {
        clearInterval(interval);
        setIsUploading(false);
      }
    }, 220);
  };

  const handleFile = (file?: File) => {
    if (!file || !file.type.startsWith("image/")) {
      toast.error("Please upload a valid image file");
      return;
    }
    const nextUrl = URL.createObjectURL(file);

    revokePreview(previewUrl);
    setPreviewUrl(nextUrl);
    setUploadedFile(file);
    startProgress();
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);
    const file = event.dataTransfer.files?.[0];
    handleFile(file);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    handleFile(file);
    event.target.value = "";
  };

  const handleProcessTryOn = async () => {
    if (!uploadedFile || !productImage) {
      toast.error("Please upload your photo first");
      return;
    }

    setIsProcessing(true);
    setUploadProgress(50);

    try {
      toast.info("Processing your virtual try-on... This may take a moment.", {
        duration: 5000,
      });

      const result = await performVirtualTryOn(uploadedFile, productImage);

      if (result.success && result.resultImage) {
        setTryOnResult({
          resultImage: result.resultImage,
          modelImage: previewUrl || "",
          garmentImage: productImage,
          productName: productName,
        });

        toast.success("Virtual try-on completed successfully!");
        onOpenChange(false);
        navigate("/try-on-result");
      } else {
        throw new Error(result.error || "Failed to process try-on");
      }
    } catch (error) {
      console.error("Try-on error:", error);
      toast.error(
        error instanceof Error
          ? error.message
          : "Failed to process virtual try-on. Please try again."
      );
    } finally {
      setIsProcessing(false);
      setUploadProgress(100);
    }
  };

  const displayProgress = previewUrl ? Math.min(uploadProgress, 100) : 37;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        showCloseButton={false}
        className="sm:max-w-5xl border-0 bg-transparent p-0 shadow-none"
      >
        <div className="relative">
          <DialogClose
            onClick={resetUpload}
            className="absolute -right-2 -top-2 z-10 flex h-10 w-10 items-center justify-center rounded-full bg-[#B55A00] text-white transition hover:bg-[#A04A00] shadow-lg"
          >
            <X className="h-5 w-5" />
          </DialogClose>
          
          <div className="relative w-full overflow-hidden rounded-[28px] bg-white shadow-2xl ring-1 ring-black/5">

          <div className="grid gap-0 md:grid-cols-2">
            <div className="bg-[#FFE3B3]/70 p-6 md:p-8">
              <div
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(event) => {
                  event.preventDefault();
                  setIsDragging(true);
                }}
                onDragLeave={(event) => {
                  event.preventDefault();
                  setIsDragging(false);
                }}
                onDrop={handleDrop}
                className={cn(
                  "group relative flex min-h-[480px] flex-col items-center justify-center rounded-[22px] border-2 border-dashed border-amber-300 bg-white/90 px-6 text-center shadow-inner transition",
                  isDragging && "border-amber-500 bg-amber-50"
                )}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleInputChange}
                  className="hidden"
                />

                {previewUrl ? (
                  <div className="flex w-full flex-col items-center gap-8">
                    <div className="relative w-full overflow-hidden rounded-[18px] border border-amber-200 bg-white">
                      <img
                        src={previewUrl}
                        alt="Uploaded preview"
                        className="h-[320px] w-full object-contain"
                      />
                      <div className="absolute left-4 top-4 rounded-full bg-white/90 px-3 py-1 text-xs font-semibold text-amber-700 shadow-sm">
                        Your photo
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Replace or drop another image to update the preview.
                    </p>
                  </div>
                ) : (
                  <div className="flex flex-col items-center gap-4">
                    <div className="flex h-28 w-28 items-center justify-center rounded-full bg-amber-100/80 text-amber-700">
                      <UploadCloud className="h-10 w-10" />
                    </div>
                    <div className="space-y-2">
                      <p className="text-lg font-semibold text-foreground">
                        Upload or Drag and drop your image here
                      </p>
                      <p className="text-sm text-muted-foreground">
                        High quality photos give the best fit preview.
                      </p>
                    </div>
                    <Button
                      type="button"
                      variant="default"
                      onClick={() => fileInputRef.current?.click()}
                      className="bg-[#F6B45A] text-white hover:bg-[#e3a44f]"
                    >
                      Choose a photo
                    </Button>
                  </div>
                )}
              </div>
            </div>

            <div className="flex flex-col p-6 md:p-8">
              <div className="mb-8 space-y-4">
                {(isUploading || isProcessing) && (
                  <div className="flex items-center justify-end gap-4">
                    <div className="h-2 w-48 rounded-full bg-[#F8E5C8]">
                      <div
                        className="h-2 rounded-full bg-[#B55A00] transition-[width]"
                        style={{ width: `${displayProgress}%` }}
                      />
                    </div>
                    <span className="text-sm font-semibold text-[#B55A00] whitespace-nowrap">
                      {isProcessing ? "Processing..." : `${displayProgress}% Uploaded`}
                    </span>
                  </div>
                )}

                <div className="space-y-2">
                  <h2 className="text-2xl font-bold text-[#B55A00] leading-tight">
                    Upload your favorite pics here to see how the fit looks on you!
                  </h2>
                  <p className="text-sm text-muted-foreground">
                    Drop a photo to instantly preview it in your try-on gallery.
                  </p>
                </div>
              </div>

              <div className="flex-1">
                <div className="grid grid-cols-2 gap-6 md:gap-8">
                  {/* Wrong Pose */}
                  <div className="relative overflow-hidden rounded-[18px] border border-amber-100 bg-[#FFF7ED] shadow-sm">
                    <img
                      src={wrongPose}
                      alt="Wrong pose guide"
                      className="h-[280px] w-full object-cover"
                    />
                    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex h-12 w-12 items-center justify-center rounded-full bg-[#B55A00] shadow-lg">
                      <X className="h-6 w-6 text-white" />
                    </div>
                  </div>
                  {/* Correct Pose */}
                  <div className="relative overflow-hidden rounded-[18px] border border-amber-100 bg-[#FFF7ED] shadow-sm">
                    <img
                      src={correctPose}
                      alt="Correct pose guide"
                      className="h-[280px] w-full object-cover"
                    />
                    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex h-12 w-12 items-center justify-center rounded-full bg-[#B55A00] shadow-lg">
                      <CheckCircle2 className="h-6 w-6 text-white" />
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-6">
                <Button
                  type="button"
                  variant="outline"
                  onClick={resetUpload}
                  className="gap-2 border-amber-200 text-[#B55A00] hover:bg-amber-50"
                >
                  <RefreshCcw className="h-4 w-4" />
                  Reset
                </Button>
                <Button
                  type="button"
                  variant="default"
                  disabled={!previewUrl || isUploading || isProcessing}
                  className="gap-2 bg-[#F6B45A] text-white hover:bg-[#e3a44f] disabled:opacity-60"
                  onClick={handleProcessTryOn}
                >
                  {isProcessing ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Check className="h-4 w-4" />
                      Process Try-On
                    </>
                  )}
                </Button>
              </div>
            </div>
          </div>
        </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default VirtualTryOnModal;