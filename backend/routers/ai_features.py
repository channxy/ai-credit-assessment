from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import logging

from ..database import get_db
from ..services.openai_service import OpenAIService
from ..services.ai_models import CreditScoringModel
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

# Initialize services
openai_service = None
credit_model = None

def get_openai_service():
    global openai_service
    if openai_service is None:
        openai_service = OpenAIService()
    return openai_service

def get_credit_model():
    global credit_model
    if credit_model is None:
        credit_model = CreditScoringModel()
    return credit_model

@router.post("/scenario-analysis")
async def analyze_scenario(
    scenario: str,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Analyze how a scenario would impact credit score"""
    try:
        logger.info(f"Analyzing scenario for user {user_id}: {scenario}")
        
        # Get user's current credit assessment
        from ..models import credit_models
        current_assessment = db.query(credit_models.CreditAssessment).filter(
            credit_models.CreditAssessment.user_id == user_id
        ).order_by(credit_models.CreditAssessment.assessment_date.desc()).first()
        
        if not current_assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No credit assessment found for user"
            )
        
        # Prepare current data for analysis
        current_data = {
            'credit_score': current_assessment.credit_score,
            'financial_score': current_assessment.financial_score,
            'career_score': current_assessment.career_score,
            'housing_score': current_assessment.housing_score,
            'social_score': current_assessment.social_score,
            'monthly_income': 5000,  # Default for demo
            'monthly_expenses': 3000,  # Default for demo
        }
        
        # Generate scenario analysis using OpenAI
        openai_service = get_openai_service()
        if openai_service.is_available():
            analysis = openai_service.generate_scenario_analysis(scenario, current_data)
        else:
            analysis = {
                "impact_score": "neutral",
                "estimated_score_change": 0,
                "reasoning": "OpenAI service not available for detailed analysis",
                "recommendations": ["Consult with a financial advisor for scenario planning"],
                "timeline": "short-term"
            }
        
        return {
            "scenario": scenario,
            "current_score": current_assessment.credit_score,
            "analysis": analysis
        }
        
    except Exception as e:
        logger.error(f"Error in scenario analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing scenario: {str(e)}"
        )

@router.post("/generate-synthetic-profile")
async def generate_synthetic_profile():
    """Generate a realistic synthetic user profile for testing"""
    try:
        logger.info("Generating synthetic user profile")
        
        openai_service = get_openai_service()
        if openai_service.is_available():
            profile = openai_service.generate_synthetic_user_profile()
        else:
            # Fallback to default profile
            profile = {
                "age": 35,
                "monthly_income": 5000,
                "monthly_expenses": 3000,
                "savings_balance": 10000,
                "credit_card_balance": 2000,
                "credit_card_limit": 8000,
                "loan_balance": 15000,
                "late_payments": 1,
                "missed_payments": 0,
                "years_experience": 8,
                "salary": 60000,
                "job_stability_score": 0.7,
                "housing_status": "renting",
                "monthly_rent": 1500,
                "mortgage_payment": 0,
                "property_value": 0,
                "education_level": "bachelors",
                "social_score": 0.6
            }
        
        return {
            "profile": profile,
            "ai_generated": openai_service.is_available()
        }
        
    except Exception as e:
        logger.error(f"Error generating synthetic profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating synthetic profile: {str(e)}"
        )

@router.get("/ai-status")
async def get_ai_status():
    """Check if OpenAI service is available"""
    openai_service = get_openai_service()
    return {
        "openai_available": openai_service.is_available(),
        "model": openai_service.model if openai_service.is_available() else None
    }

@router.post("/enhanced-explanation")
async def get_enhanced_explanation(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get AI-enhanced explanation of credit assessment"""
    try:
        logger.info(f"Generating enhanced explanation for user {user_id}")
        
        # Get user's latest credit assessment
        from ..models import credit_models, user_models
        assessment = db.query(credit_models.CreditAssessment).filter(
            credit_models.CreditAssessment.user_id == user_id
        ).order_by(credit_models.CreditAssessment.assessment_date.desc()).first()
        
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No credit assessment found for user"
            )
        
        # Get user profile for context
        user_profile = db.query(user_models.UserProfile).filter(
            user_models.UserProfile.user_id == user_id
        ).first()
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        # Prepare user data
        user_data = {
            'age': user_profile.age or 30,
            'monthly_income': user_profile.monthly_income or 0,
            'monthly_expenses': user_profile.monthly_expenses or 0,
            'housing_status': user_profile.housing_status or 'renting',
            'years_experience': user_profile.years_experience or 0,
            'education_level': 'bachelors',  # Default for demo
        }
        
        factor_scores = {
            'financial': assessment.financial_score,
            'career': assessment.career_score,
            'housing': assessment.housing_score,
            'social': assessment.social_score
        }
        
        # Generate AI explanation
        openai_service = get_openai_service()
        if openai_service.is_available():
            explanation = openai_service.generate_credit_explanation(
                user_data, assessment.credit_score, factor_scores
            )
        else:
            explanation = "We've calculated your credit score based on multiple factors including your financial health, career stability, housing situation, and social indicators."
        
        return {
            "explanation": explanation,
            "ai_generated": openai_service.is_available(),
            "credit_score": assessment.credit_score,
            "factor_scores": factor_scores
        }
        
    except Exception as e:
        logger.error(f"Error generating enhanced explanation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating explanation: {str(e)}"
        )

@router.post("/personalized-recommendations")
async def get_personalized_recommendations(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get AI-generated personalized recommendations"""
    try:
        logger.info(f"Generating personalized recommendations for user {user_id}")
        
        # Get user's latest credit assessment
        from ..models import credit_models, user_models
        assessment = db.query(credit_models.CreditAssessment).filter(
            credit_models.CreditAssessment.user_id == user_id
        ).order_by(credit_models.CreditAssessment.assessment_date.desc()).first()
        
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No credit assessment found for user"
            )
        
        # Get user profile
        user_profile = db.query(user_models.UserProfile).filter(
            user_models.UserProfile.user_id == user_id
        ).first()
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        # Prepare user data
        user_data = {
            'age': user_profile.age or 30,
            'monthly_income': user_profile.monthly_income or 0,
            'monthly_expenses': user_profile.monthly_expenses or 0,
            'savings_balance': user_profile.savings_balance or 0,
            'housing_status': user_profile.housing_status or 'renting',
            'years_experience': user_profile.years_experience or 0,
            'credit_card_balance': 2000,  # Default for demo
            'credit_card_limit': 8000,    # Default for demo
        }
        
        factor_scores = {
            'financial': assessment.financial_score,
            'career': assessment.career_score,
            'housing': assessment.housing_score,
            'social': assessment.social_score
        }
        
        risk_factors = assessment.risk_factors or []
        
        # Generate AI recommendations
        openai_service = get_openai_service()
        if openai_service.is_available():
            recommendations = openai_service.generate_personalized_recommendations(
                user_data, factor_scores, risk_factors
            )
        else:
            recommendations = [
                "Consider reducing your monthly expenses to improve your financial score",
                "Focus on building emergency savings",
                "Reduce credit card utilization to below 30%"
            ]
        
        return {
            "recommendations": recommendations,
            "ai_generated": openai_service.is_available(),
            "credit_score": assessment.credit_score,
            "risk_factors": risk_factors
        }
        
    except Exception as e:
        logger.error(f"Error generating personalized recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )
