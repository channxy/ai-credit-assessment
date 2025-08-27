#!/bin/bash

echo "🚀 Setting up AI Credit Assessment Platform..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p logs
mkdir -p models

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL=sqlite:///./data/credit_assessment.db

# OpenAI API Key (optional for demo)
OPENAI_API_KEY=your_openai_api_key_here

# Environment
ENVIRONMENT=development
EOF
    echo "✅ .env file created. Please update with your API keys."
fi

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Backend: python -m uvicorn backend.main:app --reload"
echo "2. Frontend: cd frontend && npm start"
echo ""
echo "Or use Docker: docker-compose up"
