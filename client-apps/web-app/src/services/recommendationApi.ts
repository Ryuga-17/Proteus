const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface RecommendationRequest {
  query: string;
  user_id?: string;
}

export interface Recommendation {
  product_id: string;
  title: string;
  price: number;
  score: number;
  reasoning: string;
  category?: string;
  brand?: string;
  images?: string[];
  sizes?: string[];
  colors?: string[];
}

export interface RecommendationResponse {
  success: boolean;
  recommendations: Recommendation[];
  query: string;
  message?: string;
}

export const getVoiceRecommendations = async (
  query: string,
  user_id: string = "default_user"
): Promise<RecommendationResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/recommendations/voice`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        user_id
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    const data: RecommendationResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
};

export const queryAgent = async (
  request: string,
  user_id: string = "default_user"
): Promise<{ success: boolean; response: string; agent_used?: string }> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/agent/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        request,
        user_id
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error querying agent:', error);
    throw error;
  }
};

export const getProducts = async (
  category?: string,
  search?: string,
  limit: number = 50
): Promise<{ products: any[] }> => {
  try {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search);
    if (limit) params.append('limit', limit.toString());

    const response = await fetch(`${API_BASE_URL}/api/products?${params.toString()}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

export const getProduct = async (product_id: string): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/products/${product_id}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching product:', error);
    throw error;
  }
};

export const getCategories = async (): Promise<{ categories: string[] }> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/categories`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw error;
  }
};

export interface PurchaseItem {
  product_id: string;
  sku?: string;
  quantity: number;
  size?: string;
}

export const processPurchase = async (
  items: PurchaseItem[],
  user_id: string = "default_user",
  location_id: string = "store_main_street"
): Promise<{
  success: boolean;
  message: string;
  order_id?: string;
  items_processed?: any[];
  errors?: string[];
}> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/purchase`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        items,
        user_id,
        location_id
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error processing purchase:', error);
    throw error;
  }
};

export const getStock = async (sku: string): Promise<{
  sku: string;
  stock_by_location: Record<string, number>;
  total_stock: number;
  available: boolean;
}> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/inventory/stock/${encodeURIComponent(sku)}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching stock:', error);
    throw error;
  }
};

