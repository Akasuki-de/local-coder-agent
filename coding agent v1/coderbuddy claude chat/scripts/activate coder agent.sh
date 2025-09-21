activate coder agent 

# Navigate to the directory
  cd "/Users/Zay/Desktop/Dev Work 2025/coding agent/coder-buddy"

  # Activate virtual environment
  source .venv/bin/activate

  # Run the simple local agent
  python3 simple_local_agent.py "Create a modern todo app with dark mode"

  Or for other options:

  # Pure local coder (12.9s average)
  python3 pure_local_coder.py "Create a weather dashboard"

  # IONOS cloud (highest quality, 25s average)
  python3 simple_coder.py "Create a portfolio website"

  # Interactive mode (just press enter to be prompted)
  python3 simple_local_agent.py
  