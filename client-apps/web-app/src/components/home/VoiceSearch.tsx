import { useState, useEffect } from "react";
import { Mic, MicOff, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { getVoiceRecommendations, type RecommendationResponse } from "@/services/recommendationApi";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

const VoiceSearch = () => {
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    setIsSupported(
      "webkitSpeechRecognition" in window || "SpeechRecognition" in window
    );
  }, []);

  const startListening = () => {
    if (!isSupported) {
      console.warn("Speech recognition not supported in this browser");
      return;
    }

    const SpeechRecognition =
      (window as any).webkitSpeechRecognition ||
      (window as any).SpeechRecognition;

    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      setIsListening(true);
      console.log("🎤 [VOICE SEARCH] Listening started");
      console.log("🎤 [VOICE SEARCH] Waiting for user input...");
    };

    recognition.onresult = async (event: any) => {
      const transcriptText = event.results[0][0].transcript;
      const confidence = event.results[0][0].confidence || "N/A";
      
      console.log("🎤 [VOICE SEARCH] ========================================");
      console.log("🎤 [VOICE SEARCH] Voice input received");
      console.log("🎤 [VOICE SEARCH] Transcript:", transcriptText);
      console.log("🎤 [VOICE SEARCH] Confidence:", confidence);
      console.log("🎤 [VOICE SEARCH] ========================================");
      
      setTranscript(transcriptText);
      
      setIsProcessing(true);
      console.log("🔄 [VOICE SEARCH] Processing voice query...");
      console.log("🔄 [VOICE SEARCH] Sending to backend API...");
      
      const startTime = Date.now();
      
      try {
        const result: RecommendationResponse = await getVoiceRecommendations(
          transcriptText,
          "default_user"
        );
        
        const processingTime = Date.now() - startTime;
        
        console.log("✅ [VOICE SEARCH] ========================================");
        console.log("✅ [VOICE SEARCH] Backend response received");
        console.log("✅ [VOICE SEARCH] Processing time:", `${processingTime}ms`);
        console.log("✅ [VOICE SEARCH] Success:", result.success);
        console.log("✅ [VOICE SEARCH] Recommendations found:", result.recommendations.length);
        
        if (result.recommendations.length > 0) {
          console.log("✅ [VOICE SEARCH] Top recommendations:");
          result.recommendations.slice(0, 3).forEach((rec, idx) => {
            console.log(`   ${idx + 1}. ${rec.title} - Score: ${rec.score?.toFixed(2) || 'N/A'}`);
          });
        }
        
        console.log("✅ [VOICE SEARCH] ========================================");
        
        if (result.success && result.recommendations.length > 0) {
          toast.success(`Found ${result.recommendations.length} recommendations!`);
          console.log("🚀 [VOICE SEARCH] Navigating to products page...");
          navigate(`/products?search=${encodeURIComponent(transcriptText)}`);
        } else {
          console.log("⚠️  [VOICE SEARCH] No recommendations found");
          toast.info("No recommendations found. Try a different query.");
        }
      } catch (error) {
        const processingTime = Date.now() - startTime;
        console.error("❌ [VOICE SEARCH] ========================================");
        console.error("❌ [VOICE SEARCH] Error processing voice query");
        console.error("❌ [VOICE SEARCH] Processing time:", `${processingTime}ms`);
        console.error("❌ [VOICE SEARCH] Error:", error);
        console.error("❌ [VOICE SEARCH] ========================================");
        toast.info("Voice recommendations need the backend. Try browsing by category or use search.");
        navigate(`/products?search=${encodeURIComponent(transcriptText)}`);
      } finally {
        setIsProcessing(false);
        console.log("🏁 [VOICE SEARCH] Processing complete");
      }
    };

    recognition.onerror = (event: any) => {
      console.error("❌ [VOICE SEARCH] ========================================");
      console.error("❌ [VOICE SEARCH] Speech recognition error");
      console.error("❌ [VOICE SEARCH] Error type:", event.error);
      console.error("❌ [VOICE SEARCH] ========================================");
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  const stopListening = () => {
    setIsListening(false);
  };

  return (
    <div className="w-full max-w-md mb-4 sm:mb-6">
      <div
        className={cn(
          "relative flex items-center gap-2 px-3 py-2 sm:py-2.5 rounded-full",
          "bg-[#FDEDDF] border border-[#FEB464]/30",
          "transition-all duration-300",
          isListening && "ring-2 ring-[#FEB464] ring-opacity-50"
        )}
      >
        <button
          onClick={isListening ? stopListening : startListening}
          disabled={!isSupported}
          className={cn(
            "flex-shrink-0 w-8 h-8 sm:w-9 sm:h-9 rounded-full",
            "bg-[#FEB464] hover:bg-[#FEB464]/90",
            "flex items-center justify-center",
            "transition-all duration-300",
            "shadow-sm hover:shadow-md",
            "disabled:opacity-50 disabled:cursor-not-allowed",
            isListening && "animate-pulse"
          )}
          aria-label={isListening ? "Stop listening" : "Start voice search"}
        >
          {isListening ? (
            <MicOff className="h-4 w-4 sm:h-5 sm:w-5 text-white" />
          ) : (
            <Mic className="h-4 w-4 sm:h-5 sm:w-5 text-white" />
          )}
        </button>

        <span className="flex-1 text-sm sm:text-base font-sans font-medium text-[#8B4513]">
          {isProcessing ? (
            <span className="flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              Processing...
            </span>
          ) : transcript ? (
            transcript
          ) : (
            "Voice Search"
          )}
        </span>
      </div>
    </div>
  );
};

export default VoiceSearch;

