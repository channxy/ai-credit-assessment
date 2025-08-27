from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class RiskCategory(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    VERY_POOR = "very_poor"

class EmploymentStatus(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"

class HousingStatus(str, Enum):
    RENTING = "renting"
    OWNED = "owned"
    MORTGAGED = "mortgaged"

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class CreditAssessmentRequest(BaseModel):
    user_id: int
    include_social_signals: bool = False
    include_career_analysis: bool = True
    include_housing_analysis: bool = True

class CreditAssessmentResponse(BaseModel):
    id: int
    user_id: int
    credit_score: float = Field(..., ge=300, le=850)
    risk_category: RiskCategory
    confidence_score: float = Field(..., ge=0, le=1)
    
    # Factor Scores
    financial_score: float
    career_score: float
    housing_score: float
    social_score: float
    
    # Detailed Analysis
    factor_breakdown: Dict[str, Any]
    recommendations: List[str]
    risk_factors: List[str]
    
    # Metadata
    assessment_date: datetime
    model_version: str

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    transaction_type: TransactionType
    category: str
    description: Optional[str] = None
    merchant: Optional[str] = None
    transaction_date: datetime

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: TransactionType
    category: str
    description: Optional[str]
    merchant: Optional[str]
    transaction_date: datetime
    created_at: datetime

class UserProfileCreate(BaseModel):
    user_id: int
    age: Optional[int] = Field(None, ge=18, le=100)
    education_level: Optional[str] = None
    degree_field: Optional[str] = None
    
    # Career Information
    job_title: Optional[str] = None
    industry: Optional[str] = None
    years_experience: Optional[int] = Field(None, ge=0)
    salary: Optional[float] = Field(None, ge=0)
    employment_status: Optional[EmploymentStatus] = None
    
    # Housing Information
    housing_status: Optional[HousingStatus] = None
    monthly_rent: Optional[float] = Field(None, ge=0)
    mortgage_payment: Optional[float] = Field(None, ge=0)
    property_value: Optional[float] = Field(None, ge=0)
    
    # Financial Information
    monthly_income: Optional[float] = Field(None, ge=0)
    monthly_expenses: Optional[float] = Field(None, ge=0)
    savings_balance: Optional[float] = None
    investment_balance: Optional[float] = None

class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int]
    education_level: Optional[str]
    degree_field: Optional[str]
    job_title: Optional[str]
    industry: Optional[str]
    years_experience: Optional[int]
    salary: Optional[float]
    employment_status: Optional[EmploymentStatus]
    housing_status: Optional[HousingStatus]
    monthly_rent: Optional[float]
    mortgage_payment: Optional[float]
    property_value: Optional[float]
    monthly_income: Optional[float]
    monthly_expenses: Optional[float]
    savings_balance: Optional[float]
    investment_balance: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]

class SimulationRequest(BaseModel):
    user_id: int
    scenario_type: str
    parameters: Dict[str, Any]

class SimulationResponse(BaseModel):
    id: int
    user_id: int
    scenario_type: str
    parameters: Dict[str, Any]
    original_score: float
    simulated_score: float
    score_change: float
    factor_changes: Dict[str, Any]
    recommendations: List[str]
    created_at: datetime
    model_version: str
