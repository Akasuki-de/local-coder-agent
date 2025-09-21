#!/usr/bin/env python3
"""
Pure Local Coder-Buddy using DeepSeek via curl (no external deps)
Lovable-like experience with local models
"""
import os
import json
import time
import subprocess
import shutil
from typing import Optional

def test_ollama_running():
    """Test if Ollama is running"""
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/tags'],
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def generate_with_curl(prompt: str) -> Optional[dict]:
    """Generate using curl to Ollama API"""

    generation_prompt = f"""You are an expert web developer. Create a complete, functional web application.

Task: {prompt}

Return EXACTLY this JSON structure with NO extra text:
{{
  "files": [
    {{"filename": "index.html", "content": "COMPLETE_HTML_CODE"}},
    {{"filename": "style.css", "content": "COMPLETE_CSS_CODE"}},
    {{"filename": "script.js", "content": "COMPLETE_JS_CODE"}}
  ]
}}

Requirements:
- Write complete, valid HTML/CSS/JavaScript
- Use modern web standards
- Include responsive design and animations
- Ensure all functionality works
- No external dependencies

Generate ONLY the JSON response."""

    try:
        # Create temp file for the prompt
        with open('/tmp/ollama_prompt.txt', 'w') as f:
            f.write(generation_prompt)

        # Use curl to call Ollama API
        curl_command = [
            'curl', '-s', '--max-time', '120',
            'http://localhost:11434/api/generate',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps({
                'model': 'deepseek-coder:latest',
                'prompt': generation_prompt,
                'stream': False,
                'options': {
                    'temperature': 0.3,
                    'top_p': 0.9
                }
            })
        ]

        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=150)

        if result.returncode == 0:
            try:
                response_data = json.loads(result.stdout)
                output = response_data.get('response', '')

                # Extract JSON from response
                start_idx = output.find('{')
                end_idx = output.rfind('}') + 1

                if start_idx != -1 and end_idx > start_idx:
                    json_str = output[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    print("⚠️ No valid JSON found in response")
                    return None

            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing failed: {e}")
                return None
        else:
            print(f"❌ Curl failed: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print("⏰ Local generation timed out")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def create_premium_fallback(prompt: str) -> dict:
    """Create a premium quality fallback"""
    app_type = "portfolio"
    if "calculator" in prompt.lower():
        app_type = "calculator"
    elif "todo" in prompt.lower() or "task" in prompt.lower():
        app_type = "todo"
    elif "weather" in prompt.lower():
        app_type = "weather"

    if app_type == "calculator":
        return create_calculator_app()
    elif app_type == "todo":
        return create_todo_app()
    elif app_type == "weather":
        return create_weather_app(prompt)
    else:
        return create_portfolio_app(prompt)

def create_weather_app(prompt: str) -> dict:
    """Create a weather dashboard app"""
    return {
        "files": [
            {
                "filename": "index.html",
                "content": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">Weather Dashboard</h1>
            <div class="search-container">
                <input type="text" id="cityInput" placeholder="Enter city name..." class="search-input">
                <button onclick="searchWeather()" class="search-btn">Search</button>
            </div>
        </header>

        <main class="main-content">
            <div class="current-weather" id="currentWeather">
                <div class="current-info">
                    <h2 class="location">New York, NY</h2>
                    <div class="temperature">22°C</div>
                    <div class="description">Sunny</div>
                    <div class="details">
                        <span>Feels like: 25°C</span>
                        <span>Humidity: 60%</span>
                        <span>Wind: 15 km/h</span>
                    </div>
                </div>
                <div class="weather-icon">☀️</div>
            </div>

            <div class="forecast">
                <h3 class="forecast-title">5-Day Forecast</h3>
                <div class="forecast-grid" id="forecastGrid">
                    <div class="forecast-item">
                        <div class="day">Mon</div>
                        <div class="icon">⛅</div>
                        <div class="temps">24° / 18°</div>
                    </div>
                    <div class="forecast-item">
                        <div class="day">Tue</div>
                        <div class="icon">🌧️</div>
                        <div class="temps">19° / 12°</div>
                    </div>
                    <div class="forecast-item">
                        <div class="day">Wed</div>
                        <div class="icon">☀️</div>
                        <div class="temps">26° / 20°</div>
                    </div>
                    <div class="forecast-item">
                        <div class="day">Thu</div>
                        <div class="icon">🌤️</div>
                        <div class="temps">23° / 17°</div>
                    </div>
                    <div class="forecast-item">
                        <div class="day">Fri</div>
                        <div class="icon">⛈️</div>
                        <div class="temps">18° / 11°</div>
                    </div>
                </div>
            </div>
        </main>
    </div>
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
    background: linear-gradient(135deg, #74b9ff, #0984e3);
    min-height: 100vh;
    color: white;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    text-align: center;
    margin-bottom: 40px;
}

.title {
    font-size: 3rem;
    margin-bottom: 30px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    animation: fadeIn 1s ease-in;
}

.search-container {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
}

.search-input {
    padding: 12px 20px;
    border: none;
    border-radius: 25px;
    width: 300px;
    font-size: 16px;
    background: rgba(255,255,255,0.9);
    color: #333;
}

.search-btn {
    padding: 12px 25px;
    border: none;
    border-radius: 25px;
    background: #00b894;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.search-btn:hover {
    background: #00a085;
    transform: translateY(-2px);
}

.main-content {
    display: grid;
    gap: 30px;
}

.current-weather {
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(10px);
    animation: slideIn 0.8s ease-out;
}

.location {
    font-size: 2rem;
    margin-bottom: 10px;
}

.temperature {
    font-size: 4rem;
    font-weight: bold;
    margin-bottom: 10px;
}

.description {
    font-size: 1.5rem;
    margin-bottom: 20px;
    opacity: 0.9;
}

.details {
    display: flex;
    flex-direction: column;
    gap: 5px;
    opacity: 0.8;
}

.weather-icon {
    font-size: 6rem;
    animation: bounce 2s infinite;
}

.forecast {
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 30px;
    backdrop-filter: blur(10px);
    animation: slideIn 1s ease-out;
}

.forecast-title {
    font-size: 1.8rem;
    margin-bottom: 20px;
    text-align: center;
}

.forecast-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.forecast-item {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    transition: transform 0.3s ease;
}

.forecast-item:hover {
    transform: translateY(-5px);
}

.day {
    font-size: 1.2rem;
    margin-bottom: 10px;
    font-weight: bold;
}

.icon {
    font-size: 2.5rem;
    margin: 15px 0;
}

.temps {
    font-size: 1.1rem;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

@media (max-width: 768px) {
    .current-weather { flex-direction: column; text-align: center; }
    .search-input { width: 250px; }
    .forecast-grid { grid-template-columns: repeat(2, 1fr); }
    .title { font-size: 2rem; }
}'''
            },
            {
                "filename": "script.js",
                "content": '''// Weather app functionality
const weatherData = {
    "new york": { city: "New York, NY", temp: 22, desc: "Sunny", icon: "☀️", feels: 25, humidity: 60, wind: 15 },
    "london": { city: "London, UK", temp: 15, desc: "Cloudy", icon: "☁️", feels: 17, humidity: 75, wind: 12 },
    "tokyo": { city: "Tokyo, JP", temp: 28, desc: "Hot", icon: "🌡️", feels: 32, humidity: 45, wind: 8 },
    "paris": { city: "Paris, FR", temp: 18, desc: "Rainy", icon: "🌧️", feels: 20, humidity: 80, wind: 18 },
    "sydney": { city: "Sydney, AU", temp: 25, desc: "Partly Cloudy", icon: "⛅", feels: 27, humidity: 55, wind: 14 }
};

const forecastData = {
    "new york": [
        { day: "Mon", icon: "⛅", high: 24, low: 18 },
        { day: "Tue", icon: "🌧️", high: 19, low: 12 },
        { day: "Wed", icon: "☀️", high: 26, low: 20 },
        { day: "Thu", icon: "🌤️", high: 23, low: 17 },
        { day: "Fri", icon: "⛈️", high: 18, low: 11 }
    ]
};

function searchWeather() {
    const cityInput = document.getElementById("cityInput");
    const cityName = cityInput.value.toLowerCase().trim();

    if (!cityName) {
        alert("Please enter a city name");
        return;
    }

    const weather = weatherData[cityName];

    if (weather) {
        updateCurrentWeather(weather);
        updateForecast(cityName);
        cityInput.value = "";
    } else {
        // Show demo data for unknown cities
        const demoWeather = {
            city: cityInput.value,
            temp: Math.floor(Math.random() * 30) + 5,
            desc: ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"][Math.floor(Math.random() * 4)],
            icon: ["☀️", "☁️", "🌧️", "⛅"][Math.floor(Math.random() * 4)],
            feels: Math.floor(Math.random() * 35) + 5,
            humidity: Math.floor(Math.random() * 40) + 40,
            wind: Math.floor(Math.random() * 25) + 5
        };
        updateCurrentWeather(demoWeather);
        generateRandomForecast();
        cityInput.value = "";
    }
}

function updateCurrentWeather(weather) {
    const currentWeather = document.getElementById("currentWeather");

    currentWeather.innerHTML = `
        <div class="current-info">
            <h2 class="location">${weather.city}</h2>
            <div class="temperature">${weather.temp}°C</div>
            <div class="description">${weather.desc}</div>
            <div class="details">
                <span>Feels like: ${weather.feels}°C</span>
                <span>Humidity: ${weather.humidity}%</span>
                <span>Wind: ${weather.wind} km/h</span>
            </div>
        </div>
        <div class="weather-icon">${weather.icon}</div>
    `;

    // Add animation
    currentWeather.style.animation = "none";
    setTimeout(() => currentWeather.style.animation = "slideIn 0.8s ease-out", 10);
}

function updateForecast(cityName) {
    const forecast = forecastData[cityName] || generateRandomForecast();
    const forecastGrid = document.getElementById("forecastGrid");

    forecastGrid.innerHTML = forecast.map(day => `
        <div class="forecast-item">
            <div class="day">${day.day}</div>
            <div class="icon">${day.icon}</div>
            <div class="temps">${day.high}° / ${day.low}°</div>
        </div>
    `).join("");
}

function generateRandomForecast() {
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri"];
    const icons = ["☀️", "☁️", "🌧️", "⛅", "🌤️", "⛈️"];

    return days.map(day => ({
        day,
        icon: icons[Math.floor(Math.random() * icons.length)],
        high: Math.floor(Math.random() * 20) + 15,
        low: Math.floor(Math.random() * 15) + 5
    }));
}

// Allow Enter key to search
document.getElementById("cityInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        searchWeather();
    }
});

// Initialize with demo data
document.addEventListener("DOMContentLoaded", function() {
    console.log("Weather Dashboard loaded successfully!");
});'''
            }
        ]
    }

def create_portfolio_app(prompt: str) -> dict:
    """Create a portfolio app as fallback"""
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
    <header class="hero">
        <div class="hero-content">
            <h1 class="hero-title">Local Portfolio</h1>
            <p class="hero-subtitle">Generated with DeepSeek</p>
            <p class="prompt-display">"{prompt}"</p>
            <button class="cta-btn" onclick="scrollToSection('contact')">View Projects</button>
        </div>
    </header>

    <section id="projects" class="section">
        <div class="container">
            <h2>Projects</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <h3>Local AI Generation</h3>
                    <p>This portfolio was generated locally using DeepSeek via Ollama</p>
                </div>
                <div class="project-card">
                    <h3>Zero Dependencies</h3>
                    <p>No external APIs, completely private and fast</p>
                </div>
                <div class="project-card">
                    <h3>Modern Design</h3>
                    <p>Responsive layout with smooth animations</p>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="section">
        <div class="container">
            <h2>Contact</h2>
            <form class="contact-form" onsubmit="handleSubmit(event)">
                <input type="text" placeholder="Name" required>
                <input type="email" placeholder="Email" required>
                <textarea placeholder="Message" required></textarea>
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
                "content": '''* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; line-height: 1.6; color: white; background: linear-gradient(135deg, #667eea, #764ba2); }
.hero { height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center; }
.hero-title { font-size: 3.5rem; margin-bottom: 1rem; animation: fadeIn 1s ease-in; }
.hero-subtitle { font-size: 1.5rem; margin-bottom: 1rem; opacity: 0.9; }
.prompt-display { font-size: 1rem; margin-bottom: 2rem; opacity: 0.8; font-style: italic; }
.cta-btn { padding: 12px 30px; background: linear-gradient(45deg, #4facfe, #00f2fe); color: white; border: none; border-radius: 50px; cursor: pointer; transition: transform 0.3s; }
.cta-btn:hover { transform: translateY(-2px); }
.section { padding: 80px 0; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
h2 { font-size: 2.5rem; text-align: center; margin-bottom: 3rem; }
.projects-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
.project-card { background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; transition: transform 0.3s; }
.project-card:hover { transform: translateY(-5px); }
.contact-form { max-width: 600px; margin: 0 auto; }
.contact-form input, .contact-form textarea { width: 100%; padding: 15px; margin-bottom: 1rem; border: none; border-radius: 10px; background: rgba(255,255,255,0.1); color: white; }
.contact-form button { width: 100%; padding: 15px; background: linear-gradient(45deg, #4facfe, #00f2fe); color: white; border: none; border-radius: 10px; cursor: pointer; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
@media (max-width: 768px) { .hero-title { font-size: 2.5rem; } .projects-grid { grid-template-columns: 1fr; } }'''
            },
            {
                "filename": "script.js",
                "content": '''function scrollToSection(id) { document.getElementById(id).scrollIntoView({ behavior: 'smooth' }); }
function handleSubmit(e) { e.preventDefault(); alert('Thank you! Message sent successfully.'); e.target.reset(); }
document.addEventListener('DOMContentLoaded', () => console.log('Local portfolio loaded!'));'''
            }
        ]
    }

def pure_local_generate(prompt: str) -> bool:
    """Pure local generation using curl"""
    print(f"🏠 PURE LOCAL CODER-BUDDY")
    print(f"🧠 Using: DeepSeek via curl (no deps)")
    print(f"📝 Generating: {prompt}")
    print("=" * 50)

    # Check if Ollama is running
    if not test_ollama_running():
        print("❌ Ollama not running. Start with: ollama serve")
        return False

    start_time = time.time()

    # Clean previous project
    if os.path.exists("generated_project"):
        shutil.rmtree("generated_project")
        print("🧹 Cleaned previous project")

    print("⚡ Generating with pure local DeepSeek...")

    # Try DeepSeek generation
    files_data = generate_with_curl(prompt)

    # Use premium fallback if DeepSeek fails
    if not files_data:
        print("⚠️ DeepSeek failed, using premium fallback...")
        files_data = create_premium_fallback(prompt)

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

    print(f"\n🎉 Pure local generation completed in {duration:.1f} seconds!")
    print(f"📁 Generated {len(files_list)} files")

    # Auto-open in browser
    import webbrowser
    html_path = "generated_project/index.html"
    full_path = os.path.abspath(html_path)

    try:
        webbrowser.open(f"file://{full_path}")
        print("🌐 Opened in browser automatically!")
    except Exception as e:
        print(f"🌐 Manual open: open {html_path}")

    return True

def main():
    """Main function"""
    import sys

    print("🏠 PURE LOCAL CODER-BUDDY")
    print("Zero dependencies, maximum privacy")
    print("=" * 40)

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        print("📝 Enter your project description:")
        prompt = input("➤ ").strip()
        if not prompt:
            prompt = "Create a weather dashboard with city search"

    success = pure_local_generate(prompt)

    if success:
        print("\n✅ Pure local generation successful!")
        print("🚀 Benefits: No rate limits, complete privacy, unlimited complexity!")
    else:
        print("\n❌ Local generation failed")

if __name__ == "__main__":
    main()