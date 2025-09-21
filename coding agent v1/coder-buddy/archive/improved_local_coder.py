#!/usr/bin/env python3
"""
Improved Local Coder-Buddy using DeepSeek via Ollama
Better prompting for Lovable-like experience
"""
import os
import json
import time
import subprocess
import shutil
import requests
from typing import Optional

def test_deepseek_available():
    """Test if DeepSeek is available via Ollama"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        return 'deepseek-coder' in result.stdout
    except:
        return False

def generate_with_ollama_api(prompt: str) -> Optional[dict]:
    """Generate using Ollama REST API for better control"""

    generation_prompt = f"""You are an expert web developer. Create a complete, functional web application.

Task: {prompt}

Return EXACTLY this JSON structure with NO extra text:
{{
  "files": [
    {{"filename": "index.html", "content": "FULL_HTML_HERE"}},
    {{"filename": "style.css", "content": "FULL_CSS_HERE"}},
    {{"filename": "script.js", "content": "FULL_JS_HERE"}}
  ]
}}

Requirements:
- Write complete, valid HTML/CSS/JavaScript
- Use modern web standards (HTML5, CSS3, ES6+)
- Include responsive design
- Add smooth animations/transitions
- Ensure all functionality works
- No external dependencies
- Clean, production-ready code

Generate ONLY the JSON response."""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'deepseek-coder:latest',
                'prompt': generation_prompt,
                'stream': False,
                'options': {
                    'temperature': 0.3,
                    'top_p': 0.9,
                    'max_tokens': 8192
                }
            },
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            output = result.get('response', '')

            # Extract JSON from response
            start_idx = output.find('{')
            end_idx = output.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = output[start_idx:end_idx]
                return json.loads(json_str)
            else:
                print("⚠️ No valid JSON found in Ollama response")
                return None

        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection to Ollama failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON parsing failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def create_high_quality_fallback(prompt: str) -> dict:
    """Create a high-quality fallback project"""
    return {
        "files": [
            {
                "filename": "index.html",
                "content": f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio - Local Generated</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <h1 class="nav-logo">Portfolio</h1>
            <div class="nav-menu">
                <a href="#home" class="nav-link">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#contact" class="nav-link">Contact</a>
            </div>
        </div>
    </nav>

    <section id="home" class="hero">
        <div class="hero-content">
            <h1 class="hero-title fade-in">Welcome to My Portfolio</h1>
            <p class="hero-subtitle fade-in">Generated with Local DeepSeek</p>
            <p class="hero-description fade-in">Request: {prompt}</p>
            <button class="cta-button" onclick="scrollToSection('contact')">Get In Touch</button>
        </div>
    </section>

    <section id="about" class="section">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <p class="section-text">This portfolio was generated using a local DeepSeek model via Ollama.</p>
        </div>
    </section>

    <section id="projects" class="section">
        <div class="container">
            <h2 class="section-title">Projects</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <h3>Project 1</h3>
                    <p>Local AI-generated web application</p>
                </div>
                <div class="project-card">
                    <h3>Project 2</h3>
                    <p>Modern responsive design</p>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="section">
        <div class="container">
            <h2 class="section-title">Contact</h2>
            <form class="contact-form" onsubmit="handleSubmit(event)">
                <input type="text" placeholder="Your Name" required>
                <input type="email" placeholder="Your Email" required>
                <textarea placeholder="Your Message" rows="5" required></textarea>
                <button type="submit">Send Message</button>
            </form>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>'''
            },
            {
                "filename": "style.css",
                "content": '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #fff;
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    overflow-x: hidden;
}

.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(10px);
    z-index: 1000;
    padding: 1rem 0;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
}

.nav-logo {
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-menu {
    display: flex;
    gap: 2rem;
}

.nav-link {
    color: #fff;
    text-decoration: none;
    transition: color 0.3s ease;
}

.nav-link:hover {
    color: #4facfe;
}

.hero {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, #667eea, #764ba2);
}

.hero-content {
    max-width: 800px;
    padding: 0 2rem;
}

.hero-title {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    opacity: 0.9;
}

.hero-description {
    font-size: 1rem;
    margin-bottom: 2rem;
    opacity: 0.8;
}

.cta-button {
    padding: 12px 30px;
    font-size: 1.1rem;
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    color: white;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.cta-button:hover {
    transform: translateY(-2px);
}

.section {
    padding: 80px 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.section-title {
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 3rem;
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.project-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 2rem;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease;
}

.project-card:hover {
    transform: translateY(-5px);
}

.contact-form {
    max-width: 600px;
    margin: 0 auto;
}

.contact-form input,
.contact-form textarea {
    width: 100%;
    padding: 15px;
    margin-bottom: 1rem;
    border: none;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 1rem;
}

.contact-form input::placeholder,
.contact-form textarea::placeholder {
    color: rgba(255, 255, 255, 0.7);
}

.contact-form button {
    width: 100%;
    padding: 15px;
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.contact-form button:hover {
    transform: translateY(-2px);
}

.fade-in {
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    .nav-menu { display: none; }
    .projects-grid { grid-template-columns: 1fr; }
}'''
            },
            {
                "filename": "script.js",
                "content": '''// Smooth scrolling function
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Add click listeners to nav links
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
        });
    });

    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 1s ease-in forwards';
            }
        });
    }, observerOptions);

    // Observe all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        observer.observe(section);
    });
});

// Handle contact form submission
function handleSubmit(event) {
    event.preventDefault();

    // Get form data
    const formData = new FormData(event.target);
    const name = formData.get('name') || event.target.querySelector('input[type="text"]').value;
    const email = formData.get('email') || event.target.querySelector('input[type="email"]').value;
    const message = formData.get('message') || event.target.querySelector('textarea').value;

    // Simulate form submission
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;

    submitButton.textContent = 'Sending...';
    submitButton.disabled = true;

    setTimeout(() => {
        alert(`Thank you ${name}! Your message has been received.\\n\\nEmail: ${email}\\nMessage: ${message}`);

        submitButton.textContent = originalText;
        submitButton.disabled = false;
        event.target.reset();
    }, 1500);
}

// Add some interactive animations
document.addEventListener('mousemove', function(e) {
    const cursor = document.querySelector('.cursor');
    if (!cursor) {
        const cursorElement = document.createElement('div');
        cursorElement.className = 'cursor';
        cursorElement.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            background: radial-gradient(circle, rgba(79,172,254,0.3) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.1s ease;
        `;
        document.body.appendChild(cursorElement);
    }

    const cursorElement = document.querySelector('.cursor');
    cursorElement.style.left = e.clientX - 10 + 'px';
    cursorElement.style.top = e.clientY - 10 + 'px';
});'''
            }
        ]
    }

def improved_local_generate(prompt: str) -> bool:
    """Improved local generation with better error handling"""
    print(f"🏠 IMPROVED LOCAL CODER-BUDDY")
    print(f"🧠 Using: DeepSeek via Ollama API")
    print(f"📝 Generating: {prompt}")
    print("=" * 50)

    # Check DeepSeek availability
    if not test_deepseek_available():
        print("❌ DeepSeek not available. Run: ollama pull deepseek-coder")
        return False

    start_time = time.time()

    # Clean previous project
    if os.path.exists("generated_project"):
        shutil.rmtree("generated_project")
        print("🧹 Cleaned previous project")

    print("⚡ Generating with improved DeepSeek prompting...")

    # Try Ollama API first
    files_data = generate_with_ollama_api(prompt)

    # Fallback to high-quality template if needed
    if not files_data:
        print("⚠️ DeepSeek generation failed, using high-quality fallback...")
        files_data = create_high_quality_fallback(prompt)

    # Create project directory
    os.makedirs("generated_project", exist_ok=True)

    # Write files
    files_list = files_data.get("files", [])
    for file_info in files_list:
        filename = file_info.get("filename", "index.html")
        content = file_info.get("content", "<!-- No content -->")

        file_path = os.path.join("generated_project", filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"📁 Created: {filename}")

    end_time = time.time()
    duration = end_time - start_time

    print(f"\n🎉 Improved local generation completed in {duration:.1f} seconds!")
    print(f"📁 Generated {len(files_list)} files")
    print(f"🌐 Open: open generated_project/index.html")

    return True

def main():
    """Main function"""
    import sys

    print("🏠 IMPROVED LOCAL CODER-BUDDY")
    print("Powered by DeepSeek + Ollama API")
    print("=" * 40)

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        print("📝 Enter your project description:")
        prompt = input("➤ ").strip()
        if not prompt:
            prompt = "Create a modern portfolio website with dark theme and animations"

    success = improved_local_generate(prompt)

    if success:
        print("\n✅ Improved local generation successful!")
        print("💡 Benefits: No rate limits, privacy, unlimited complexity!")
    else:
        print("\n❌ Local generation failed")

if __name__ == "__main__":
    main()