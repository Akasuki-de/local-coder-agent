#!/usr/bin/env python3
"""
Pre-built project templates for faster generation
Lovable-style quick project creation
"""

PROJECT_TEMPLATES = {
    "landing": {
        "name": "Modern Landing Page",
        "prompt": """Create a modern, responsive landing page with:
- Hero section with compelling headline and call-to-action button
- Features section with 3 key benefits
- About section with team or company info
- Contact section with form
- Clean, professional design with smooth animations
- Mobile-first responsive layout
- Modern color scheme and typography""",
        "complexity": "medium",
        "estimated_time": "5-8 minutes"
    },

    "todo": {
        "name": "Todo List App",
        "prompt": """Create a feature-rich todo application with:
- Add new tasks with enter key support
- Mark tasks as complete/incomplete
- Edit tasks inline by double-clicking
- Delete tasks with confirmation
- Filter tasks: All, Active, Completed
- Local storage persistence
- Clean, modern interface
- Keyboard shortcuts for productivity
- Task counter and bulk actions""",
        "complexity": "medium",
        "estimated_time": "5-10 minutes"
    },

    "calculator": {
        "name": "Advanced Calculator",
        "prompt": """Build a fully functional calculator with:
- Basic arithmetic operations (+, -, *, /)
- Advanced functions (sqrt, power, percentage)
- Memory functions (MC, MR, M+, M-)
- History of calculations
- Keyboard input support
- Clear and backspace functionality
- Scientific mode toggle
- Responsive design for mobile and desktop
- Error handling for invalid operations""",
        "complexity": "medium",
        "estimated_time": "8-12 minutes"
    },

    "portfolio": {
        "name": "Developer Portfolio",
        "prompt": """Create a professional developer portfolio with:
- Header with navigation and contact info
- Hero section with photo and introduction
- Skills section with technology icons
- Projects gallery with filtering by category
- About page with detailed background
- Contact form with validation
- Responsive design across all devices
- Smooth scrolling and animations
- Dark/light mode toggle
- Social media links""",
        "complexity": "complex",
        "estimated_time": "15-20 minutes"
    },

    "dashboard": {
        "name": "Admin Dashboard",
        "prompt": """Build a comprehensive admin dashboard with:
- Sidebar navigation with collapsible menu
- Top header with user profile and notifications
- Key metrics cards with icons and numbers
- Interactive charts and graphs
- Data tables with sorting and filtering
- Recent activity feed
- Quick action buttons
- Responsive layout for tablet and mobile
- Clean, modern design with consistent spacing
- Mock data for demonstration""",
        "complexity": "complex",
        "estimated_time": "20-25 minutes"
    },

    "blog": {
        "name": "Blog Platform",
        "prompt": """Create a complete blog platform with:
- Homepage with featured articles and recent posts
- Individual article pages with full content
- Article listing page with pagination
- Search functionality across all posts
- Category and tag filtering
- Author profiles and bio pages
- Comment system (front-end only)
- Responsive design for all devices
- Reading time estimation
- Social sharing buttons""",
        "complexity": "complex",
        "estimated_time": "20-30 minutes"
    },

    "ecommerce": {
        "name": "E-commerce Store",
        "prompt": """Build an e-commerce storefront with:
- Product catalog with grid and list views
- Product detail pages with image gallery
- Shopping cart with add/remove functionality
- Checkout process with form validation
- User account pages (login/register forms)
- Product search and filtering
- Category navigation
- Responsive design for mobile shopping
- Price calculation and tax handling
- Order summary and confirmation""",
        "complexity": "complex",
        "estimated_time": "25-35 minutes"
    },

    "weather": {
        "name": "Weather App",
        "prompt": """Create a weather application with:
- Current weather display with location
- 5-day forecast with daily highs/lows
- Hourly forecast for today
- Weather icons and condition descriptions
- Search for different cities
- Geolocation support for current location
- Temperature unit toggle (°C/°F)
- Beautiful background images based on weather
- Responsive design for mobile and desktop
- Mock weather data with realistic values""",
        "complexity": "medium",
        "estimated_time": "10-15 minutes"
    },

    "quiz": {
        "name": "Interactive Quiz App",
        "prompt": """Build an engaging quiz application with:
- Multiple choice questions with 4 options
- Progress bar showing quiz completion
- Score tracking and final results
- Question timer with countdown
- Different question categories
- High score leaderboard (local storage)
- Explanations for correct answers
- Restart quiz functionality
- Responsive design for all devices
- Smooth animations between questions""",
        "complexity": "medium",
        "estimated_time": "12-18 minutes"
    },

    "chat": {
        "name": "Chat Interface",
        "prompt": """Create a modern chat application interface with:
- Chat window with message bubbles
- Message input with send button
- Timestamp display for messages
- User avatars and names
- Typing indicator animation
- Message status (sent, delivered, read)
- Emoji picker integration
- File attachment UI
- Responsive layout for mobile and desktop
- Mock conversation data for demonstration""",
        "complexity": "complex",
        "estimated_time": "18-25 minutes"
    }
}

def list_templates():
    """Display all available templates"""
    print("🎨 Available Project Templates:")
    print("=" * 50)

    for key, template in PROJECT_TEMPLATES.items():
        print(f"📁 {key.upper()}: {template['name']}")
        print(f"   Complexity: {template['complexity'].title()}")
        print(f"   Time: {template['estimated_time']}")
        print()

def get_template(template_key: str) -> dict:
    """Get a specific template by key"""
    return PROJECT_TEMPLATES.get(template_key.lower())

def create_custom_template(name: str, prompt: str, complexity: str = "medium") -> dict:
    """Create a custom template"""
    return {
        "name": name,
        "prompt": prompt,
        "complexity": complexity,
        "estimated_time": {
            "simple": "3-6 minutes",
            "medium": "6-12 minutes",
            "complex": "15-30 minutes"
        }[complexity]
    }

if __name__ == "__main__":
    list_templates()