"""
Pydantic Models for Voice Query Processing
Defines input/output structures for the Recommendation Agent
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class VoiceQueryInput(BaseModel):
    """Input model for voice query processing"""
    raw_text: str = Field(..., description="The raw text from speech-to-text conversion")


class StructuredQuery(BaseModel):
    """Output model from NLU stage - structured representation of user intent"""
    product_type: str = Field(..., description="Main product category (e.g., 'shirt', 'dress', 'shoes')")
    occasion_tag: str = Field(..., description="Occasion or use case (e.g., 'date', 'formal', 'casual', 'workout')")
    implied_attributes: List[str] = Field(
        default_factory=list,
        description="Inferred style/attribute tags (e.g., ['smart-casual', 'fitted', 'dark_color'])"
    )


class RecommendationResult(BaseModel):
    """Result model for product recommendations"""
    item_id: str = Field(..., description="Unique identifier for the recommended item")
    score: float = Field(..., description="Relevance score (0.0 to 1.0)")
    reasoning: str = Field(..., description="Explanation of why this item was recommended")


class UserContext(BaseModel):
    """User context from Redis Cache"""
    user_id: str = Field(..., description="Unique user identifier")
    past_purchases: List[str] = Field(default_factory=list, description="List of previously purchased item IDs")
    preferred_size: Optional[str] = Field(None, description="User's preferred size (e.g., 'M', 'L', 'XL')")
    preferred_color: Optional[str] = Field(None, description="User's preferred color")
    preferred_brand: Optional[str] = Field(None, description="User's preferred brand")
    price_range: Optional[dict] = Field(None, description="User's preferred price range {'min': float, 'max': float}")




