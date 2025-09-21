# 🚀 Coder-Buddy Quick Start Guide

## Optimized for Lovable-Style Development

### 🎯 **Three Ways to Use Coder-Buddy:**

## 1. 🎨 **QUICK TEMPLATES** (Fastest)
```bash
python coder_buddy.py --template todo
python coder_buddy.py --template portfolio
python coder_buddy.py --template dashboard
```

**Available Templates:**
- `todo` - Feature-rich todo app (5-10 min)
- `calculator` - Advanced calculator (8-12 min)
- `portfolio` - Developer portfolio (15-20 min)
- `dashboard` - Admin dashboard (20-25 min)
- `blog` - Blog platform (20-30 min)
- `ecommerce` - E-commerce store (25-35 min)
- `weather` - Weather app (10-15 min)
- `quiz` - Interactive quiz (12-18 min)
- `chat` - Chat interface (18-25 min)
- `landing` - Landing page (5-8 min)

## 2. 💬 **CUSTOM PROMPTS** (Most Flexible)
```bash
python coder_buddy.py --prompt "Create a modern todo app with dark mode"
```

## 3. 🖥️ **INTERACTIVE MODE** (Most Guided)
```bash
python coder_buddy.py
```

---

## 🤖 **Multi-Model Optimization**

Your system automatically chooses the best IONOS AI model based on project complexity:

### 🟢 **Simple Projects** → Fast Models
- **Planner**: Llama-3.1-8B (Fast planning)
- **Architect**: Mistral-Nemo (Balanced design)
- **Coder**: Llama-3.1-8B (Fast coding)
- **Time**: 2-5 minutes

### 🟡 **Medium Projects** → Balanced Models
- **Planner**: Mistral-Nemo (Smart planning)
- **Architect**: Llama-3.1-405B (Deep architecture)
- **Coder**: Llama-3.1-8B (Fast coding)
- **Time**: 5-15 minutes

### 🔴 **Complex Projects** → Powerful Models
- **Planner**: Mistral-Nemo (Smart planning)
- **Architect**: Llama-3.1-405B (Advanced architecture)
- **Coder**: Mistral-Nemo (Advanced coding)
- **Time**: 15-30 minutes

---

## 🎯 **Perfect Prompts for Best Results**

### ✅ **Excellent Prompts:**
```
"Create a todo app with add/edit/delete tasks, local storage,
filtering by status, and a clean modern interface with dark mode toggle"

"Build a portfolio website with hero section, projects gallery with
filtering, about page, contact form, and responsive design"

"Create an e-commerce product catalog with search, filtering,
shopping cart, and checkout process"
```

### ❌ **Avoid These:**
```
"Make a website"
"Create an app"
"Build something cool"
```

---

## 🚀 **Example Usage Session**

```bash
# Quick template
$ python coder_buddy.py --template todo
🎨 Using template: Todo List App
🧠 Complexity: MEDIUM (confidence: 85%)
🤖 Models selected...
⏱️ Estimated time: 5-10 minutes
🚀 Starting generation...
✅ Generation completed!
📁 Files created in: generated_project/
🌐 Open in browser: open generated_project/index.html

# Custom project
$ python coder_buddy.py --prompt "Create a weather dashboard with charts"
🧠 Detected complexity: COMPLEX (confidence: 78%)
🤖 Using powerful models for complex project
⏱️ Estimated time: 15-25 minutes
🚀 Starting generation...
```

---

## 🛠️ **Generated Project Structure**

```
generated_project/
├── index.html          # Main application
├── style.css          # Styling
├── script.js          # JavaScript logic
├── README.md          # Project documentation
└── assets/            # Images/resources (if needed)
```

---

## 🔧 **Useful Commands**

```bash
# List available templates
python templates.py

# List available AI models
python coder_buddy.py --models

# Use specific recursion limit
python coder_buddy.py --recursion-limit 50

# Non-interactive template usage
python coder_buddy.py --template portfolio

# Direct prompt without interaction
python coder_buddy.py --prompt "Your project description"
```

---

## 🎉 **You're Ready!**

Your Coder-Buddy system is now optimized with:
- ✅ IONOS AI Model Hub integration
- ✅ Multi-model optimization
- ✅ 10 pre-built templates
- ✅ Intelligent complexity detection
- ✅ Lovable-style development experience

**Start creating:**
```bash
python coder_buddy.py
```