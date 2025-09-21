# 🚀 Coder-Buddy Usage Guide - Lovable-Style Development

## Quick Start

### Basic Usage
```bash
cd "/Users/Zay/Desktop/Dev Work 2025/coding agent/coder-buddy"
source .venv/bin/activate
python main.py
```

### Interactive Mode
When prompted, describe your project in natural language:

## 🎯 **Effective Prompting Strategies**

### ✅ **Good Prompts (Lovable-Style)**
```
"Create a modern todo app with the following features:
- Add, edit, delete tasks
- Mark tasks as complete
- Filter by: all, active, completed
- Local storage persistence
- Clean, responsive design
- Dark/light mode toggle"

"Build a calculator app with:
- Basic arithmetic operations (+, -, *, /)
- Memory functions (MC, MR, M+, M-)
- History of calculations
- Keyboard input support
- Scientific mode with advanced functions"

"Create a personal portfolio website:
- Landing page with hero section
- About page with skills and experience
- Projects gallery with filtering
- Contact form with validation
- Responsive design for mobile/desktop
- Smooth animations and transitions"
```

### ❌ **Avoid Vague Prompts**
```
❌ "Make a website"
❌ "Create an app"
❌ "Build something cool"
```

### ✅ **Be Specific About:**
- **Features**: List exact functionality you want
- **Technology**: Specify frameworks if needed (React, Vue, vanilla JS)
- **Styling**: Mention design preferences (modern, minimal, colorful)
- **Responsiveness**: Mobile-first, desktop-only, etc.
- **Data**: How data should be stored (localStorage, mock API)

## 🎨 **Project Templates**

### Small Projects (5-15 minutes)
- Simple landing pages
- Basic calculators
- Todo lists
- Color generators
- Quote displays

### Medium Projects (15-30 minutes)
- Multi-page websites
- Interactive dashboards
- Form builders
- Image galleries
- Weather apps

### Large Projects (30+ minutes)
- Full web applications
- E-commerce sites
- Blog platforms
- Admin panels
- Game interfaces

## 🛠 **Generated Project Structure**

Your projects are created in:
```
generated_project/
├── index.html          # Main HTML file
├── style.css          # Styling
├── script.js          # JavaScript logic
├── assets/            # Images, fonts (if needed)
└── README.md          # Project documentation
```

## 🔄 **Iterative Development**

### Method 1: Run Again with Modifications
```bash
python main.py
# Enter: "Improve the previous todo app by adding categories and due dates"
```

### Method 2: Specific Feature Requests
```bash
python main.py
# Enter: "Add drag-and-drop functionality to the todo app"
```

## 📱 **Testing Your Generated Apps**

1. **Open in Browser**: `open generated_project/index.html`
2. **Live Server**: Use VS Code Live Server extension
3. **Local Server**: `python -m http.server 8000` in generated_project/

## 🎯 **Pro Tips for Best Results**

### 1. **Start with Core Features**
Focus on the main functionality first:
```
"Create a blog platform with:
- Article listing page
- Individual article pages
- Simple admin panel for CRUD operations
- Search functionality
- Responsive design"
```

### 2. **Specify Technology Preferences**
```
"Build a React-based dashboard with:
- Component-based architecture
- State management with hooks
- Charts using Chart.js
- API integration ready"
```

### 3. **Include Design Details**
```
"Create a modern landing page with:
- Clean, minimal design
- Blue and white color scheme
- Hero section with call-to-action
- Feature cards with icons
- Footer with social links"
```

### 4. **Request Specific Layouts**
```
"Build a portfolio with:
- Fixed navigation header
- Full-screen hero section
- Grid-based project gallery
- Side-by-side about section
- Contact form in footer"
```

## ⚡ **Speed Optimization Tips**

1. **Use Clear, Specific Language**: Reduces back-and-forth
2. **List Features Explicitly**: Helps agent understand scope
3. **Mention Constraints**: "Single page", "No external libraries"
4. **Specify File Structure**: If you have preferences

## 🔍 **Troubleshooting**

### If Generation Takes Too Long:
- Simplify your request
- Break into smaller features
- Use `recursion_limit` parameter

### If Output Isn't What You Expected:
- Be more specific about requirements
- Add examples or references
- Iterate with refinements

### If Files Aren't Generated:
- Check `generated_project/` directory
- Look for error messages in terminal
- Try simpler request first

## 🎉 **Example Session**
```
$ python main.py
Enter your project prompt: Create a weather app that shows current weather and 5-day forecast with a clean, modern interface

🚀 Using IONOS AI Model Hub
[Agent runs through Planner → Architect → Coder]
✅ Generated files in generated_project/

$ open generated_project/index.html
[Browser opens with fully functional weather app]
```