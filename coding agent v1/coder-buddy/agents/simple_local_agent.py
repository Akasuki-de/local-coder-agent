#!/usr/bin/env python3
"""
Simplified Local Agent - Works with available Ollama models
Uses only available models: qwen2.5-coder:7b and deepseek-coder:latest
"""
import os
import json
import time
import subprocess
import shutil
from typing import Dict, List

class SimpleLocalAgent:
    """Simple local agent using available Ollama models"""

    def __init__(self):
        self.available_models = self._check_models()
        print(f"🔧 Available models: {', '.join(self.available_models)}")

    def _check_models(self) -> List[str]:
        """Check available Ollama models"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                return [line.split()[0] for line in lines if line.strip()]
        except:
            pass
        return []

    def _call_model(self, prompt: str, model: str, max_time: int = 30) -> str:
        """Call Ollama model with timeout"""
        try:
            curl_data = {
                'model': model,
                'prompt': prompt,
                'stream': False,
                'options': {'temperature': 0.3, 'num_ctx': 4000}
            }

            result = subprocess.run([
                'curl', '-s', f'--max-time', str(max_time),
                'http://localhost:11434/api/generate',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(curl_data)
            ], capture_output=True, text=True, timeout=max_time + 5)

            if result.returncode == 0:
                response = json.loads(result.stdout)
                return response.get('response', '').strip()

        except Exception as e:
            print(f"⚠️ Model call failed: {e}")

        return ""

    def generate_project(self, prompt: str) -> Dict:
        """Generate project with single model approach"""
        print(f"🚀 SIMPLE LOCAL AGENT")
        print(f"📝 Request: {prompt}")
        print("=" * 50)

        start_time = time.time()

        # Choose best available model
        if "qwen2.5-coder:7b" in self.available_models:
            model = "qwen2.5-coder:7b"
        elif "deepseek-coder:latest" in self.available_models:
            model = "deepseek-coder:latest"
        else:
            print("❌ No suitable models available")
            return {"success": False, "error": "No models available"}

        print(f"🧠 Using model: {model}")

        # Single comprehensive prompt
        generation_prompt = f"""Create a complete web project for: "{prompt}"

Generate THREE files in this exact JSON format:
{{
  "files": [
    {{"filename": "index.html", "content": "COMPLETE_HTML_CODE_HERE"}},
    {{"filename": "style.css", "content": "COMPLETE_CSS_CODE_HERE"}},
    {{"filename": "script.js", "content": "COMPLETE_JS_CODE_HERE"}}
  ]
}}

Requirements:
- Write complete, functional code for all files
- Make it responsive and modern
- Include animations and transitions
- Follow best practices
- Ensure all features work properly

Return ONLY the JSON with the files array."""

        print("⚡ Generating code...")
        response = self._call_model(generation_prompt, model, 45)

        if not response:
            print("⚠️ Model failed, using fallback...")
            return self._create_fallback(prompt)

        # Try to extract JSON
        try:
            # Find JSON in response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                files = data.get("files", [])

                if len(files) >= 3:
                    generation_time = time.time() - start_time
                    return {
                        "success": True,
                        "files": files,
                        "model_used": model,
                        "generation_time": f"{generation_time:.1f}s"
                    }

            print("⚠️ Invalid JSON response, using fallback...")

        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")

        return self._create_fallback(prompt)

    def _create_fallback(self, prompt: str) -> Dict:
        """Create smart fallback based on prompt"""
        print("🔄 Creating smart fallback...")

        prompt_lower = prompt.lower()

        if "calculator" in prompt_lower:
            files = self._calculator_fallback()
        elif "weather" in prompt_lower:
            files = self._weather_fallback()
        elif "portfolio" in prompt_lower:
            files = self._portfolio_fallback()
        elif "todo" in prompt_lower:
            files = self._todo_fallback()
        else:
            files = self._generic_fallback(prompt)

        return {
            "success": True,
            "files": files,
            "model_used": "fallback",
            "generation_time": "0.1s"
        }

    def _calculator_fallback(self) -> List[Dict]:
        return [
            {
                "filename": "index.html",
                "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="calculator">
        <input type="text" id="display" readonly>
        <div class="buttons">
            <button onclick="clearDisplay()" class="btn clear">C</button>
            <button onclick="deleteLast()" class="btn delete">DEL</button>
            <button onclick="calculate()" class="btn equals">=</button>
            <button onclick="addToDisplay('+')" class="btn operator">+</button>

            <button onclick="addToDisplay('7')" class="btn">7</button>
            <button onclick="addToDisplay('8')" class="btn">8</button>
            <button onclick="addToDisplay('9')" class="btn">9</button>
            <button onclick="addToDisplay('-')" class="btn operator">-</button>

            <button onclick="addToDisplay('4')" class="btn">4</button>
            <button onclick="addToDisplay('5')" class="btn">5</button>
            <button onclick="addToDisplay('6')" class="btn">6</button>
            <button onclick="addToDisplay('*')" class="btn operator">*</button>

            <button onclick="addToDisplay('1')" class="btn">1</button>
            <button onclick="addToDisplay('2')" class="btn">2</button>
            <button onclick="addToDisplay('3')" class="btn">3</button>
            <button onclick="addToDisplay('/')" class="btn operator">/</button>

            <button onclick="addToDisplay('0')" class="btn zero">0</button>
            <button onclick="addToDisplay('.')" class="btn">.</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
            },
            {
                "filename": "style.css",
                "content": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}

.calculator {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 30px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    animation: slideIn 0.5s ease-out;
}

#display {
    width: 100%;
    height: 80px;
    font-size: 2rem;
    text-align: right;
    padding: 20px;
    border: none;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    margin-bottom: 20px;
    font-weight: bold;
}

.buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
}

.btn {
    height: 70px;
    border: none;
    border-radius: 15px;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    background: rgba(255, 255, 255, 0.2);
    color: white;
}

.btn:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
}

.btn:active {
    transform: translateY(0);
}

.operator {
    background: linear-gradient(45deg, #ff6b6b, #ee5a24);
}

.equals {
    background: linear-gradient(45deg, #00d2d3, #54a0ff);
}

.clear {
    background: linear-gradient(45deg, #ff9ff3, #f368e0);
}

.delete {
    background: linear-gradient(45deg, #feca57, #ff9f43);
}

.zero {
    grid-column: span 2;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 480px) {
    .calculator {
        padding: 20px;
    }

    .btn {
        height: 60px;
        font-size: 1rem;
    }

    #display {
        height: 60px;
        font-size: 1.5rem;
    }
}"""
            },
            {
                "filename": "script.js",
                "content": """let display = document.getElementById('display');
let shouldResetDisplay = false;

function addToDisplay(value) {
    if (shouldResetDisplay) {
        display.value = '';
        shouldResetDisplay = false;
    }

    display.value += value;
}

function clearDisplay() {
    display.value = '';
    shouldResetDisplay = false;
}

function deleteLast() {
    display.value = display.value.slice(0, -1);
}

function calculate() {
    try {
        if (display.value === '') return;

        let result = eval(display.value);

        if (result === Infinity || result === -Infinity) {
            display.value = 'Error';
        } else if (isNaN(result)) {
            display.value = 'Error';
        } else {
            display.value = Number.isInteger(result) ? result : result.toFixed(8).replace(/\\.?0+$/, '');
        }

        shouldResetDisplay = true;
    } catch (error) {
        display.value = 'Error';
        shouldResetDisplay = true;
    }
}

// Keyboard support
document.addEventListener('keydown', function(event) {
    const key = event.key;

    if ('0123456789'.includes(key) || '+-*/.'.includes(key)) {
        addToDisplay(key);
    } else if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculate();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        clearDisplay();
    } else if (key === 'Backspace') {
        deleteLast();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('Calculator loaded successfully!');
    display.focus();
});"""
            }
        ]

    def _weather_fallback(self) -> List[Dict]:
        return [
            {
                "filename": "index.html",
                "content": """<!DOCTYPE html>
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
</html>"""
            },
            {
                "filename": "style.css",
                "content": """* {
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
}"""
            },
            {
                "filename": "script.js",
                "content": """// Weather app functionality
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
});"""
            }
        ]

    def _todo_fallback(self) -> List[Dict]:
        return [
            {
                "filename": "index.html",
                "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="title">Todo App</h1>

        <div class="add-todo">
            <input type="text" id="todoInput" placeholder="Add a new todo..." />
            <button onclick="addTodo()" class="add-btn">Add</button>
        </div>

        <div class="todo-list" id="todoList">
            <!-- Todos will be added here -->
        </div>

        <div class="stats" id="stats">
            <span id="totalTodos">0</span> total,
            <span id="completedTodos">0</span> completed
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
            },
            {
                "filename": "style.css",
                "content": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    min-height: 100vh;
    padding: 20px;
    color: white;
}

.container {
    max-width: 600px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.title {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 30px;
    animation: fadeIn 1s ease-in;
}

.add-todo {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
}

#todoInput {
    flex: 1;
    padding: 15px;
    border: none;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    font-size: 16px;
}

#todoInput::placeholder {
    color: rgba(255, 255, 255, 0.7);
}

.add-btn {
    padding: 15px 25px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: transform 0.2s;
}

.add-btn:hover {
    transform: translateY(-2px);
}

.todo-list {
    margin-bottom: 30px;
}

.todo-item {
    background: rgba(255, 255, 255, 0.1);
    margin-bottom: 10px;
    padding: 15px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 15px;
    animation: slideIn 0.3s ease-out;
    transition: all 0.3s ease;
}

.todo-item:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateX(5px);
}

.todo-item.completed {
    opacity: 0.6;
    text-decoration: line-through;
}

.todo-checkbox {
    width: 20px;
    height: 20px;
    border: 2px solid white;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.todo-checkbox.checked {
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    border-color: #4facfe;
}

.todo-checkbox.checked::after {
    content: '✓';
    color: white;
    font-weight: bold;
}

.todo-text {
    flex: 1;
    font-size: 16px;
}

.delete-btn {
    background: linear-gradient(45deg, #ff6b6b, #ee5a24);
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    transition: transform 0.2s;
}

.delete-btn:hover {
    transform: scale(1.1);
}

.stats {
    text-align: center;
    font-size: 16px;
    opacity: 0.8;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

@media (max-width: 600px) {
    .container {
        margin: 0 10px;
        padding: 20px;
    }

    .title {
        font-size: 2rem;
    }

    .add-todo {
        flex-direction: column;
    }
}"""
            },
            {
                "filename": "script.js",
                "content": """let todos = JSON.parse(localStorage.getItem('todos')) || [];
let todoId = Date.now();

function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

function addTodo() {
    const input = document.getElementById('todoInput');
    const text = input.value.trim();

    if (text === '') {
        alert('Please enter a todo!');
        return;
    }

    const todo = {
        id: todoId++,
        text: text,
        completed: false,
        createdAt: new Date().toISOString()
    };

    todos.unshift(todo);
    input.value = '';
    saveTodos();
    renderTodos();
}

function toggleTodo(id) {
    todos = todos.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
    );
    saveTodos();
    renderTodos();
}

function deleteTodo(id) {
    if (confirm('Are you sure you want to delete this todo?')) {
        todos = todos.filter(todo => todo.id !== id);
        saveTodos();
        renderTodos();
    }
}

function renderTodos() {
    const todoList = document.getElementById('todoList');

    if (todos.length === 0) {
        todoList.innerHTML = '<p style="text-align: center; opacity: 0.6; padding: 40px;">No todos yet. Add one above!</p>';
    } else {
        todoList.innerHTML = todos.map(todo => `
            <div class="todo-item ${todo.completed ? 'completed' : ''}">
                <div class="todo-checkbox ${todo.completed ? 'checked' : ''}"
                     onclick="toggleTodo(${todo.id})"></div>
                <div class="todo-text">${todo.text}</div>
                <button class="delete-btn" onclick="deleteTodo(${todo.id})">Delete</button>
            </div>
        `).join('');
    }

    updateStats();
}

function updateStats() {
    const totalTodos = todos.length;
    const completedTodos = todos.filter(todo => todo.completed).length;

    document.getElementById('totalTodos').textContent = totalTodos;
    document.getElementById('completedTodos').textContent = completedTodos;
}

// Event listeners
document.getElementById('todoInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTodo();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    renderTodos();
    console.log('Todo app loaded successfully!');
});"""
            }
        ]

    def _portfolio_fallback(self) -> List[Dict]:
        return [
            {
                "filename": "index.html",
                "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="hero">
        <h1>My Portfolio</h1>
        <p>Web Developer & Designer</p>
        <button onclick="scrollTo('#projects')">View Work</button>
    </header>
    <section id="projects">
        <h2>Projects</h2>
        <div class="project-grid">
            <div class="project">
                <h3>Project 1</h3>
                <p>Modern web application with responsive design</p>
            </div>
            <div class="project">
                <h3>Project 2</h3>
                <p>Interactive dashboard with data visualization</p>
            </div>
        </div>
    </section>
    <footer>
        <p>&copy; 2024 Portfolio</p>
    </footer>
    <script src="script.js"></script>
</body>
</html>"""
            },
            {
                "filename": "style.css",
                "content": """body{font-family:Arial;margin:0;background:linear-gradient(135deg,#667eea,#764ba2);color:white}.hero{height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}h1{font-size:3rem;margin-bottom:1rem}button{padding:12px 30px;background:transparent;border:2px solid white;color:white;border-radius:50px;cursor:pointer;transition:all 0.3s}button:hover{background:white;color:#667eea}#projects{padding:80px 20px;text-align:center}.project-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:2rem;max-width:1200px;margin:0 auto}.project{background:rgba(255,255,255,0.1);padding:2rem;border-radius:10px;transition:transform 0.3s}.project:hover{transform:translateY(-5px)}footer{text-align:center;padding:2rem}"""
            },
            {
                "filename": "script.js",
                "content": """function scrollTo(target){document.querySelector(target).scrollIntoView({behavior:'smooth'});} document.addEventListener('scroll',()=>{const elements=document.querySelectorAll('.project');elements.forEach(el=>{const rect=el.getBoundingClientRect();if(rect.top<window.innerHeight){el.style.animation='fadeIn 1s ease-in forwards';}});});"""
            }
        ]

    def _generic_fallback(self, prompt: str) -> List[Dict]:
        return [
            {
                "filename": "index.html",
                "content": f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Local Generated App</h1>
        <p class="prompt">"{prompt}"</p>
        <div class="features">
            <div class="feature">✨ Built with local AI</div>
            <div class="feature">🚀 Zero external dependencies</div>
            <div class="feature">🔒 Complete privacy</div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
            },
            {
                "filename": "style.css",
                "content": """body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);color:white;margin:0;min-height:100vh}.container{max-width:800px;margin:0 auto;padding:40px 20px;text-align:center}h1{font-size:3rem;margin-bottom:2rem;animation:fadeIn 1s ease-in}.prompt{font-style:italic;margin-bottom:3rem;opacity:0.8}.features{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:2rem;margin-top:3rem}.feature{background:rgba(255,255,255,0.1);padding:2rem;border-radius:15px;transition:transform 0.3s}.feature:hover{transform:translateY(-5px)}@keyframes fadeIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}"""
            },
            {
                "filename": "script.js",
                "content": """document.addEventListener('DOMContentLoaded',()=>{console.log('Local generated app loaded!');const features=document.querySelectorAll('.feature');features.forEach((feature,index)=>{setTimeout(()=>{feature.style.animation='fadeIn 1s ease-in forwards';},index*200);});});"""
            }
        ]

def main():
    """Main CLI function"""
    import sys

    agent = SimpleLocalAgent()

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        print("📝 Enter your project description:")
        prompt = input("➤ ").strip()
        if not prompt:
            prompt = "Create a simple portfolio website"

    # Generate project
    result = agent.generate_project(prompt)

    if not result["success"]:
        print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
        return

    # Create files
    if os.path.exists("generated_project"):
        shutil.rmtree("generated_project")
    os.makedirs("generated_project", exist_ok=True)

    files = result["files"]
    for file_info in files:
        filename = file_info["filename"]
        content = file_info["content"]

        file_path = os.path.join("generated_project", filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"📁 Created: {filename}")

    print(f"\n🎉 Simple local generation completed in {result['generation_time']}!")
    print(f"🧠 Model: {result['model_used']}")
    print(f"📁 Generated {len(files)} files")

    # Auto-open in browser
    import webbrowser

    html_path = os.path.join("generated_project", "index.html")
    full_path = os.path.abspath(html_path)

    try:
        # Try to open in default browser
        webbrowser.open(f"file://{full_path}")
        print("🌐 Opened in browser automatically!")
    except Exception as e:
        print(f"🌐 Manual open: open {html_path}")
        print(f"   (Auto-open failed: {e})")

if __name__ == "__main__":
    main()