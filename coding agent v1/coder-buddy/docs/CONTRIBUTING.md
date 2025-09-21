# 🤝 Contributing to Coder Buddy

Thank you for your interest in contributing to Coder Buddy! We welcome all contributions that help make AI-powered development more accessible.

## 🚀 Quick Start

### Setup Development Environment
```bash
git clone https://github.com/yourusername/coder-buddy.git
cd coder-buddy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run Tests
```bash
python3 -m pytest tests/
python3 agents/simple_local_agent.py "Test generation"
```

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Check existing issues first
- Use the bug report template
- Include system info and reproduction steps
- Test with multiple agents if possible

### ✨ Feature Requests
- Search existing feature requests
- Explain the use case and value
- Consider which agent(s) would benefit
- Propose implementation approach

### 🔧 Code Contributions
- Fork the repository
- Create feature branch: `git checkout -b feature/amazing-feature`
- Follow code style guidelines (see below)
- Add tests for new functionality
- Update documentation as needed
- Submit pull request

### 📚 Documentation
- Fix typos and improve clarity
- Add examples and use cases
- Update performance benchmarks
- Create tutorials and guides

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings for functions and classes
- Keep functions focused and small
- Use type hints where helpful

### Testing
- Add unit tests for new functions
- Test all agent types with new features
- Include edge cases and error conditions
- Verify auto-preview functionality

### Documentation
- Update README for user-facing changes
- Add docstrings for developer-facing changes
- Include examples in docstrings
- Update performance benchmarks if needed

## 🏗️ Architecture Overview

### Core Components
- `agents/` - Generation systems (Simple Local, Pure Local, Cloud, Multi-Agent)
- `core/` - Shared utilities and templates
- `docs/` - Documentation and guides
- `tests/` - Test suite

### Adding New Features
1. **Templates**: Add to `core/templates.py` for fallback system
2. **Agents**: Extend existing agents or create new specialized ones
3. **Models**: Add model support in appropriate agent files
4. **Preview**: Ensure auto-preview works with new features

## 🎨 Template Contributions

### High-Impact Template Ideas
- E-commerce product pages
- Data visualization dashboards
- Interactive forms and surveys
- Browser games and animations
- Professional portfolios

### Template Guidelines
- Self-contained (HTML, CSS, JS only)
- Mobile-responsive design
- Accessibility compliant
- Modern, clean aesthetic
- Well-commented code

## 🧪 Testing Guidelines

### Manual Testing
```bash
# Test all agents
python3 agents/simple_local_agent.py "Your test prompt"
python3 agents/pure_local_coder.py "Your test prompt"
python3 agents/simple_coder.py "Your test prompt"

# Test edge cases
python3 agents/simple_local_agent.py ""  # Empty prompt
python3 agents/simple_local_agent.py "Very complex application with many features"  # Complex prompt
```

### Automated Testing
```bash
# Run test suite
python3 -m pytest tests/ -v

# Test specific components
python3 -m pytest tests/test_agents.py
python3 -m pytest tests/test_templates.py
```

## 📝 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Auto-preview works correctly

### PR Description
- Describe the change and why it's needed
- Link to related issues
- Include screenshots for UI changes
- List any breaking changes
- Add performance impact notes

### Review Process
1. Automated tests run
2. Code review by maintainers
3. Manual testing of changes
4. Documentation review
5. Merge after approval

## 🎯 Priority Areas

### High Priority
- Performance improvements
- New high-quality templates
- Better error handling
- Cross-platform compatibility

### Medium Priority
- Additional model integrations
- UI/UX improvements
- Documentation enhancements
- Test coverage expansion

### Innovation Areas
- Hot reload development server
- Web interface dashboard
- VS Code extension
- Template marketplace

## 🐛 Reporting Issues

### Bug Report Template
```markdown
**Bug Description**
Clear description of the issue

**Steps to Reproduce**
1. Run command: `python3 agents/...`
2. Use prompt: "..."
3. Observe error/issue

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**System Information**
- OS: [macOS 13.0, Ubuntu 22.04, etc.]
- Python: [3.8, 3.9, 3.10, 3.11]
- Coder Buddy: [version or commit]
- Models: [Ollama models installed]

**Additional Context**
Screenshots, logs, etc.
```

## 🌟 Recognition

### Contributors
All contributors are recognized in:
- README acknowledgments
- Release notes
- GitHub contributors page

### Significant Contributions
- Major features or improvements
- High-quality template additions
- Documentation overhauls
- Performance optimizations

## 🤔 Questions?

- **General Questions**: GitHub Discussions
- **Bug Reports**: GitHub Issues
- **Feature Requests**: GitHub Issues with enhancement label
- **Security Issues**: Email maintainers privately

## 📜 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Celebrate diverse perspectives

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or inflammatory comments
- Publishing private information
- Other unprofessional conduct

### Enforcement
Community guidelines will be enforced fairly and consistently. Violations may result in temporary or permanent ban from the project.

---

**Thank you for contributing to Coder Buddy!** 🚀

Together we're building the future of AI-powered development.