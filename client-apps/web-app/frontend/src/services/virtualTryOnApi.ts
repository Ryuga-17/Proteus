/**
 * Virtual Try-On API Service
 * Uses multiple reliable APIs with proper fallbacks for high-quality virtual try-on
 * Primary: Fal.ai (modern ML platform)
 * Fallback: Hugging Face Inference API (free tier)
 * Final fallback: Enhanced canvas-based composition
 */

export interface TryOnRequest {
  modelImage: string; // Base64 encoded image of the person
  garmentImage: string; // Base64 encoded image of the clothing item
}

export interface TryOnResponse {
  success: boolean;
  resultImage?: string; // URL or base64 of the result
  error?: string;
  taskId?: string;
}

/**
 * Convert file to base64 string
 */
export const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      // Remove data:image/...;base64, prefix if present
      const base64 = result.includes(',') ? result.split(',')[1] : result;
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

/**
 * Upload image to a temporary hosting service and get URL
 * Uses multiple free image hosting services as fallbacks
 */
const uploadImageToTempHost = async (base64Image: string): Promise<string> => {
  try {
    // Convert base64 to blob
    const base64Data = base64Image.includes(',') 
      ? base64Image.split(',')[1] 
      : base64Image;
    
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'image/jpeg' });
    
    // Try imgbb.com first (if API key is available)
    const imgbbKey = import.meta.env.VITE_IMGBB_API_KEY;
    if (imgbbKey && imgbbKey !== 'YOUR_IMGBB_KEY') {
      try {
        const formData = new FormData();
        formData.append('image', blob, 'image.jpg');
        
        const imgbbResponse = await fetch(
          `https://api.imgbb.com/1/upload?key=${imgbbKey}`,
          {
            method: 'POST',
            body: formData
          }
        );
        
        if (imgbbResponse.ok) {
          const imgbbData = await imgbbResponse.json();
          if (imgbbData.data?.url) {
            return imgbbData.data.url;
          }
        }
      } catch (error) {
        console.warn('ImgBB upload failed, trying alternative...', error);
      }
    }
    
    // Fallback: Use imgur (no API key required for anonymous uploads)
    try {
      const formData = new FormData();
      formData.append('image', blob);
      
      const imgurResponse = await fetch('https://api.imgur.com/3/image', {
        method: 'POST',
        headers: {
          'Authorization': 'Client-ID 546c25a59c58ad7' // Public client ID for anonymous uploads
        },
        body: formData
      });
      
      if (imgurResponse.ok) {
        const imgurData = await imgurResponse.json();
        if (imgurData.data?.link) {
          return imgurData.data.link;
        }
      }
    } catch (error) {
      console.warn('Imgur upload failed, using data URL...', error);
    }
    
    // Final fallback: return data URL
    return `data:image/jpeg;base64,${base64Image}`;
  } catch (error) {
    console.error('Error uploading image:', error);
    // Fallback to data URL
    return `data:image/jpeg;base64,${base64Image}`;
  }
};

/**
 * Use Fal.ai API for virtual try-on (modern, reliable ML platform)
 * Uses the IDM-VTON model which is excellent for virtual try-on
 */
export const tryOnWithFal = async (
  modelImage: File,
  garmentImageUrl: string
): Promise<TryOnResponse> => {
  try {
    const falApiKey = import.meta.env.VITE_FAL_API_KEY;
    
    if (!falApiKey || falApiKey === 'YOUR_FAL_API_KEY') {
      throw new Error('Fal.ai API key not configured');
    }

    // Convert model image to base64 and upload
    const modelBase64 = await fileToBase64(modelImage);
    const modelImageUrl = await uploadImageToTempHost(modelBase64);

    // Ensure garment image is also a URL
    let garmentUrl = garmentImageUrl;
    if (garmentImageUrl.startsWith('data:')) {
      const garmentBase64 = garmentImageUrl.split(',')[1] || garmentImageUrl;
      garmentUrl = await uploadImageToTempHost(garmentBase64);
    }

    // Use Fal.ai IDM-VTON model
    const response = await fetch('https://fal.run/fal-ai/idm-vton', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Key ${falApiKey}`
      },
      body: JSON.stringify({
        human: modelImageUrl,
        garment: garmentUrl,
        is_checked: true,
        category: 'upper_body'
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.message || `Fal.ai API error: ${response.status}`);
    }

    const result = await response.json();
    
    // Fal.ai returns the result directly or with a status URL
    if (result.output) {
      const outputUrl = Array.isArray(result.output) ? result.output[0] : result.output;
      return {
        success: true,
        resultImage: outputUrl,
        taskId: result.request_id
      };
    } else if (result.status_url) {
      // Poll for result if async
      let statusResult = result;
      let attempts = 0;
      const maxAttempts = 60;
      
      while ((statusResult.status === 'IN_PROGRESS' || statusResult.status === 'IN_QUEUE') && attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 2000));
        const statusResponse = await fetch(result.status_url, {
          headers: {
            'Authorization': `Key ${falApiKey}`
          }
        });
        
        if (!statusResponse.ok) {
          throw new Error(`Failed to check status: ${statusResponse.status}`);
        }
        
        statusResult = await statusResponse.json();
        attempts++;
      }

      if (statusResult.status === 'COMPLETED' && statusResult.output) {
        const outputUrl = Array.isArray(statusResult.output) ? statusResult.output[0] : statusResult.output;
        return {
          success: true,
          resultImage: outputUrl,
          taskId: statusResult.request_id
        };
      } else if (statusResult.status === 'FAILED') {
        throw new Error(statusResult.error || 'Processing failed');
      } else {
        throw new Error('Processing timed out');
      }
    } else {
      throw new Error('Unexpected response format');
    }
  } catch (error) {
    console.error('Fal.ai API error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to process try-on with Fal.ai'
    };
  }
};

/**
 * Use Hugging Face Inference API for virtual try-on (free tier available)
 * Uses the IDM-VTON model via Hugging Face
 */
export const tryOnWithHuggingFace = async (
  modelImage: File,
  garmentImageUrl: string
): Promise<TryOnResponse> => {
  try {
    const hfApiKey = import.meta.env.VITE_HUGGINGFACE_API_KEY;
    
    // Convert model image to base64
    const modelBase64 = await fileToBase64(modelImage);
    const modelDataUrl = `data:image/jpeg;base64,${modelBase64}`;

    // Ensure garment image is base64
    let garmentDataUrl = garmentImageUrl;
    if (!garmentImageUrl.startsWith('data:')) {
      // If it's a URL, we'll need to fetch it and convert
      try {
        const response = await fetch(garmentImageUrl);
        const blob = await response.blob();
        const reader = new FileReader();
        garmentDataUrl = await new Promise((resolve) => {
          reader.onload = () => resolve(reader.result as string);
          reader.readAsDataURL(blob);
        });
      } catch (error) {
        console.warn('Could not convert garment URL to base64, using as-is');
      }
    }

    // Use Hugging Face Inference API with IDM-VTON model
    const modelId = 'yisol/IDM-VTON';
    const apiUrl = `https://api-inference.huggingface.co/models/${modelId}`;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    
    if (hfApiKey && hfApiKey !== 'YOUR_HUGGINGFACE_API_KEY') {
      headers['Authorization'] = `Bearer ${hfApiKey}`;
    }

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        inputs: {
          human: modelDataUrl,
          garment: garmentDataUrl,
          is_checked: true,
          category: 'upper_body'
        }
      })
    });

    if (!response.ok) {
      // Hugging Face might return 503 if model is loading
      if (response.status === 503) {
        const errorData = await response.json().catch(() => ({}));
        const estimatedTime = errorData.estimated_time || 20;
        throw new Error(`Model is loading. Please try again in ${Math.ceil(estimatedTime)} seconds.`);
      }
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Hugging Face API error: ${response.status}`);
    }

    const result = await response.json();
    
    // Hugging Face returns base64 image directly or in a specific format
    if (result.generated_image) {
      return {
        success: true,
        resultImage: result.generated_image
      };
    } else if (typeof result === 'string' && result.startsWith('data:image')) {
      return {
        success: true,
        resultImage: result
      };
    } else if (result[0]?.generated_image) {
      return {
        success: true,
        resultImage: result[0].generated_image
      };
    } else {
      throw new Error('Unexpected response format from Hugging Face');
    }
  } catch (error) {
    console.error('Hugging Face API error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to process try-on with Hugging Face'
    };
  }
};

/**
 * Enhanced canvas-based composition with better blending
 * Used as final fallback when APIs are unavailable
 */
export const tryOnWithCanvas = async (
  modelImage: File,
  garmentImage: string
): Promise<TryOnResponse> => {
  try {
    const modelBase64 = await fileToBase64(modelImage);
    const modelImg = new Image();
    const garmentImg = new Image();
    
    return new Promise((resolve) => {
      modelImg.onload = () => {
        garmentImg.src = garmentImage;
        garmentImg.onload = () => {
          const canvas = document.createElement('canvas');
          canvas.width = modelImg.width;
          canvas.height = modelImg.height;
          const ctx = canvas.getContext('2d');
          
          if (ctx) {
            // Draw model image
            ctx.drawImage(modelImg, 0, 0);
            
            // Enhanced blending: use multiply blend mode for more realistic overlay
            ctx.globalCompositeOperation = 'multiply';
            ctx.globalAlpha = 0.6;
            
            // Scale garment to fit model proportions better
            const scale = Math.min(canvas.width / garmentImg.width, canvas.height / garmentImg.height);
            const scaledWidth = garmentImg.width * scale;
            const scaledHeight = garmentImg.height * scale;
            const x = (canvas.width - scaledWidth) / 2;
            const y = (canvas.height - scaledHeight) / 2;
            
            ctx.drawImage(garmentImg, x, y, scaledWidth, scaledHeight);
            
            // Reset composite operation
            ctx.globalCompositeOperation = 'source-over';
            ctx.globalAlpha = 1.0;
            
            const resultUrl = canvas.toDataURL('image/png');
            resolve({
              success: true,
              resultImage: resultUrl
            });
          } else {
            resolve({
              success: false,
              error: 'Failed to create canvas context'
            });
          }
        };
        garmentImg.onerror = () => {
          resolve({
            success: false,
            error: 'Failed to load garment image'
          });
        };
      };
      modelImg.src = `data:image/jpeg;base64,${modelBase64}`;
      modelImg.onerror = () => {
        resolve({
          success: false,
          error: 'Failed to load model image'
        });
      };
    });
  } catch (error) {
    console.error('Canvas composition error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to process try-on'
    };
  }
};

/**
 * Main try-on function with multiple fallbacks
 * Tries: Fal.ai -> Hugging Face -> Enhanced Canvas
 */
export const performVirtualTryOn = async (
  modelImage: File,
  garmentImageUrl: string
): Promise<TryOnResponse> => {
  // Try Fal.ai first (most reliable, requires API key)
  const falApiKey = import.meta.env.VITE_FAL_API_KEY;
  if (falApiKey && falApiKey !== 'YOUR_FAL_API_KEY') {
    const falResult = await tryOnWithFal(modelImage, garmentImageUrl);
    if (falResult.success) {
      return falResult;
    }
    console.warn('Fal.ai failed, trying Hugging Face...', falResult.error);
  }

  // Fallback to Hugging Face (free tier available)
  const hfResult = await tryOnWithHuggingFace(modelImage, garmentImageUrl);
  if (hfResult.success) {
    return hfResult;
  }
  console.warn('Hugging Face failed, using canvas fallback...', hfResult.error);

  // Final fallback: Enhanced canvas-based composition
  return tryOnWithCanvas(modelImage, garmentImageUrl);
};

