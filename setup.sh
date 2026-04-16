# Smart NEPSE Investor
# Project initialization script

echo "======================================"
echo "Smart NEPSE Investor Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}[1/5] Checking Python installation...${NC}"
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python found"
echo ""

# Setup Backend
echo -e "${BLUE}[2/5] Setting up backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
pip install -q -r requirements.txt
echo "✅ Backend dependencies installed"
echo ""

# Initialize database
echo -e "${BLUE}[3/5] Initializing database...${NC}"
python -c "from app.database import init_db; init_db()"
echo "✅ Database initialized"
echo ""

# Go back
cd ..

# Setup Frontend
echo -e "${BLUE}[4/5] Setting up frontend...${NC}"
cd frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

# Install dependencies
npm install -q
echo "✅ Frontend dependencies installed"
echo ""

cd ..

# Final instructions
echo -e "${BLUE}[5/5] Setup complete!${NC}"
echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Smart NEPSE Investor is ready to run!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "To start the application, run these commands in separate terminals:"
echo ""
echo "🔵 Terminal 1 - Backend Server:"
echo "   cd backend"
echo "   python -m uvicorn app.main:app --reload"
echo ""
echo "🟢 Terminal 2 - Frontend Server:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "🟠 Terminal 3 - Background Scheduler (optional):"
echo "   cd backend"
echo "   python scheduler.py"
echo ""
echo "Then open: http://localhost:3000"
echo ""
