from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from ..database import get_db
from ..schemas.credit_schemas import (
    CreditAssessmentRequest, CreditAssessmentResponse,
    TransactionCreate, TransactionResponse,
    UserProfileCreate, UserProfileResponse
)
from ..services.ai_models import CreditScoringModel
from ..models import credit_models, user_models
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

# Initialize AI model
credit_model = CreditScoringModel()

@router.post("/assess", response_model=CreditAssessmentResponse)
async def assess_credit(
    request: CreditAssessmentRequest,
    db: Session = Depends(get_db)
):
    """Perform credit assessment for a user"""
    try:
        logger.info(f"Starting credit assessment for user {request.user_id}")
        
        # Get user profile
        user_profile = db.query(user_models.UserProfile).filter(
            user_models.UserProfile.user_id == request.user_id
        ).first()
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        # Get user's credit history
        credit_history = db.query(credit_models.CreditHistory).filter(
            credit_models.CreditHistory.user_id == request.user_id
        ).first()
        
        # Prepare user data for AI model
        user_data = {
            'monthly_income': user_profile.monthly_income or 0,
            'monthly_expenses': user_profile.monthly_expenses or 0,
            'savings_balance': user_profile.savings_balance or 0,
            'investment_balance': user_profile.investment_balance or 0,
            'age': user_profile.age or 30,
            'education_level': 'bachelors',  # Default for demo
            'job_title': user_profile.job_title or '',
            'industry': user_profile.industry or '',
            'years_experience': user_profile.years_experience or 0,
            'salary': user_profile.salary or 0,
            'employment_status': user_profile.employment_status or 'full_time',
            'housing_status': user_profile.housing_status or 'renting',
            'monthly_rent': user_profile.monthly_rent or 0,
            'mortgage_payment': user_profile.mortgage_payment or 0,
            'property_value': user_profile.property_value or 0,
            'job_stability_score': 0.7,  # Default for demo
            'social_score': 0.6,  # Default for demo
        }
        
        # Add credit history data if available
        if credit_history:
            user_data.update({
                'credit_card_balance': credit_history.credit_card_balance or 0,
                'credit_card_limit': credit_history.credit_card_limit or 1,
                'loan_balance': credit_history.loan_balance or 0,
                'late_payments': credit_history.late_payments or 0,
                'missed_payments': credit_history.missed_payments or 0,
            })
        else:
            # Default credit values
            user_data.update({
                'credit_card_balance': 0,
                'credit_card_limit': 5000,
                'loan_balance': 0,
                'late_payments': 0,
                'missed_payments': 0,
            })
        
        # Get AI prediction
        prediction = credit_model.predict_credit_score(user_data)
        
        # Save assessment to database
        assessment = credit_models.CreditAssessment(
            user_id=request.user_id,
            credit_score=prediction['credit_score'],
            risk_category=prediction['risk_category'],
            confidence_score=prediction['confidence_score'],
            financial_score=prediction['financial_score'],
            career_score=prediction['career_score'],
            housing_score=prediction['housing_score'],
            social_score=prediction['social_score'],
            factor_breakdown=prediction['factor_breakdown'],
            recommendations=prediction['recommendations'],
            risk_factors=prediction['risk_factors'],
            model_version=prediction['model_version']
        )
        
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        logger.info(f"Credit assessment completed for user {request.user_id}")
        
        return CreditAssessmentResponse(
            id=assessment.id,
            user_id=assessment.user_id,
            credit_score=assessment.credit_score,
            risk_category=assessment.risk_category,
            confidence_score=assessment.confidence_score,
            financial_score=assessment.financial_score,
            career_score=assessment.career_score,
            housing_score=assessment.housing_score,
            social_score=assessment.social_score,
            factor_breakdown=assessment.factor_breakdown,
            recommendations=assessment.recommendations,
            risk_factors=assessment.risk_factors,
            assessment_date=assessment.assessment_date,
            model_version=assessment.model_version
        )
        
    except Exception as e:
        logger.error(f"Error in credit assessment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing credit assessment: {str(e)}"
        )

@router.get("/assessments/{user_id}", response_model=List[CreditAssessmentResponse])
async def get_user_assessments(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all credit assessments for a user"""
    try:
        assessments = db.query(credit_models.CreditAssessment).filter(
            credit_models.CreditAssessment.user_id == user_id
        ).order_by(credit_models.CreditAssessment.assessment_date.desc()).all()
        
        return [
            CreditAssessmentResponse(
                id=assessment.id,
                user_id=assessment.user_id,
                credit_score=assessment.credit_score,
                risk_category=assessment.risk_category,
                confidence_score=assessment.confidence_score,
                financial_score=assessment.financial_score,
                career_score=assessment.career_score,
                housing_score=assessment.housing_score,
                social_score=assessment.social_score,
                factor_breakdown=assessment.factor_breakdown,
                recommendations=assessment.recommendations,
                risk_factors=assessment.risk_factors,
                assessment_date=assessment.assessment_date,
                model_version=assessment.model_version
            )
            for assessment in assessments
        ]
        
    except Exception as e:
        logger.error(f"Error getting user assessments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving assessments: {str(e)}"
        )

@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    """Create a new transaction"""
    try:
        db_transaction = credit_models.Transaction(
            user_id=transaction.user_id,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type,
            category=transaction.category,
            description=transaction.description,
            merchant=transaction.merchant,
            transaction_date=transaction.transaction_date
        )
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        return TransactionResponse(
            id=db_transaction.id,
            user_id=db_transaction.user_id,
            amount=db_transaction.amount,
            transaction_type=db_transaction.transaction_type,
            category=db_transaction.category,
            description=db_transaction.description,
            merchant=db_transaction.merchant,
            transaction_date=db_transaction.transaction_date,
            created_at=db_transaction.created_at
        )
        
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating transaction: {str(e)}"
        )

@router.get("/transactions/{user_id}", response_model=List[TransactionResponse])
async def get_user_transactions(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all transactions for a user"""
    try:
        transactions = db.query(credit_models.Transaction).filter(
            credit_models.Transaction.user_id == user_id
        ).order_by(credit_models.Transaction.transaction_date.desc()).all()
        
        return [
            TransactionResponse(
                id=transaction.id,
                user_id=transaction.user_id,
                amount=transaction.amount,
                transaction_type=transaction.transaction_type,
                category=transaction.category,
                description=transaction.description,
                merchant=transaction.merchant,
                transaction_date=transaction.transaction_date,
                created_at=transaction.created_at
            )
            for transaction in transactions
        ]
        
    except Exception as e:
        logger.error(f"Error getting user transactions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving transactions: {str(e)}"
        )

@router.post("/profiles", response_model=UserProfileResponse)
async def create_user_profile(
    profile: UserProfileCreate,
    db: Session = Depends(get_db)
):
    """Create or update user profile"""
    try:
        # Check if profile already exists
        existing_profile = db.query(user_models.UserProfile).filter(
            user_models.UserProfile.user_id == profile.user_id
        ).first()
        
        if existing_profile:
            # Update existing profile
            for field, value in profile.dict(exclude_unset=True).items():
                setattr(existing_profile, field, value)
            db_profile = existing_profile
        else:
            # Create new profile
            db_profile = user_models.UserProfile(**profile.dict())
            db.add(db_profile)
        
        db.commit()
        db.refresh(db_profile)
        
        return UserProfileResponse(
            id=db_profile.id,
            user_id=db_profile.user_id,
            age=db_profile.age,
            education_level=db_profile.education_level,
            degree_field=db_profile.degree_field,
            job_title=db_profile.job_title,
            industry=db_profile.industry,
            years_experience=db_profile.years_experience,
            salary=db_profile.salary,
            employment_status=db_profile.employment_status,
            housing_status=db_profile.housing_status,
            monthly_rent=db_profile.monthly_rent,
            mortgage_payment=db_profile.mortgage_payment,
            property_value=db_profile.property_value,
            monthly_income=db_profile.monthly_income,
            monthly_expenses=db_profile.monthly_expenses,
            savings_balance=db_profile.savings_balance,
            investment_balance=db_profile.investment_balance,
            created_at=db_profile.created_at,
            updated_at=db_profile.updated_at
        )
        
    except Exception as e:
        logger.error(f"Error creating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user profile: {str(e)}"
        )

@router.get("/profiles/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user profile"""
    try:
        profile = db.query(user_models.UserProfile).filter(
            user_models.UserProfile.user_id == user_id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        return UserProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            age=profile.age,
            education_level=profile.education_level,
            degree_field=profile.degree_field,
            job_title=profile.job_title,
            industry=profile.industry,
            years_experience=profile.years_experience,
            salary=profile.salary,
            employment_status=profile.employment_status,
            housing_status=profile.housing_status,
            monthly_rent=profile.monthly_rent,
            mortgage_payment=profile.mortgage_payment,
            property_value=profile.property_value,
            monthly_income=profile.monthly_income,
            monthly_expenses=profile.monthly_expenses,
            savings_balance=profile.savings_balance,
            investment_balance=profile.investment_balance,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user profile: {str(e)}"
        )
