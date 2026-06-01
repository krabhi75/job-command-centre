#!/bin/bash

# Job Hunting System Setup Script
# Automated setup for the AI-powered job tracker

echo "=================================="
echo "🤖 Job Hunting System Setup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Setup .env file
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Apify token"
    echo "   Get it at: https://console.apify.com/settings/integrations"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Check Apify token
if grep -q "your_apify_token_here" .env 2>/dev/null; then
    echo "⚠️  WARNING: Apify token not configured!"
    echo ""
    echo "Next steps:"
    echo "1. Get Apify token: https://console.apify.com/settings/integrations"
    echo "2. Edit .env file: nano .env"
    echo "3. Replace 'your_apify_token_here' with your actual token"
    echo "4. Run the scraper: python3 job_scraper_enhanced.py"
else
    echo "✅ Apify token configured"
    echo ""
    echo "🚀 Setup complete! Ready to scrape jobs."
    echo ""
    echo "Usage:"
    echo "  python3 job_scraper_enhanced.py    # Run job scraper"
    echo ""
fi

echo ""
echo "📊 Dashboard:"
echo "  Open in Cursor: canvases/job-tracker-dashboard.canvas.tsx"
echo ""
echo "📖 Documentation:"
echo "  Read: README.md"
echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
