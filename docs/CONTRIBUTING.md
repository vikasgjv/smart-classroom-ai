# 🤝 Contributing to ClassAI

Thank you for your interest in contributing to ClassAI! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints
- Show empathy towards others

## 🚀 How to Contribute

### Types of Contributions

1. **Bug Fixes** - Fix issues in existing code
2. **New Features** - Add new functionality
3. **Documentation** - Improve or add documentation
4. **Testing** - Add or improve tests
5. **Performance** - Optimize existing code
6. **UI/UX** - Improve user interface and experience

## 💻 Development Setup

### 1. Fork the Repository
Click the "Fork" button on GitHub to create your copy.

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR-USERNAME/ClassAI.git
cd ClassAI
```

### 3. Add Upstream Remote
```bash
git remote add upstream https://github.com/ORIGINAL-OWNER/ClassAI.git
```

### 4. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

## 📝 Coding Standards

### Python Code Style
- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Maximum line length: 100 characters

**Example:**
```python
def calculate_attention_score(face_detected: bool, eyes_detected: int) -> float:
    """
    Calculate attention score based on face and eye detection.
    
    Args:
        face_detected: Whether a face was detected
        eyes_detected: Number of eyes detected (0, 1, or 2)
    
    Returns:
        Attention score between 0.0 and 1.0
    """
    if not face_detected:
        return 0.0
    
    base_score = 0.5
    eye_bonus = eyes_detected * 0.25
    
    return min(base_score + eye_bonus, 1.0)
```

### JavaScript Code Style
- Use ES6+ features
- Use `const` and `let`, avoid `var`
- Use arrow functions where appropriate
- Add JSDoc comments for functions
- Use meaningful variable names

**Example:**
```javascript
/**
 * Update the attention display with new data
 * @param {number} attention - Attention score (0-100)
 * @param {boolean} noFace - Whether no face was detected
 */
function updateAttentionDisplay(attention, noFace = false) {
    const element = document.getElementById('attentionValue');
    
    if (noFace) {
        element.textContent = 'No face detected';
        element.classList.add('no-face');
    } else {
        element.textContent = `${attention}%`;
        updateAttentionColor(attention);
    }
}
```

### CSS Code Style
- Use CSS variables for colors and common values
- Follow BEM naming convention where appropriate
- Group related properties
- Add comments for complex sections

**Example:**
```css
/* Attention Circle Component */
.attention-circle {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--info));
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
```

## 🔍 Testing

### Before Submitting
1. Test your changes thoroughly
2. Ensure webcam functionality works
3. Test in multiple browsers
4. Check both light and dark modes
5. Verify responsive design

### Manual Testing Checklist
- [ ] Start/stop class session
- [ ] Face detection works correctly
- [ ] Attention scores are accurate
- [ ] Reports generate successfully
- [ ] PDF export works
- [ ] Dark mode toggles properly
- [ ] Absence alerts trigger correctly
- [ ] No console errors

## 📤 Submitting Changes

### 1. Commit Your Changes
```bash
git add .
git commit -m "Add: Brief description of changes"
```

**Commit Message Format:**
- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for updates to existing features
- `Docs:` for documentation changes
- `Style:` for formatting changes
- `Refactor:` for code refactoring
- `Test:` for adding tests

### 2. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request
1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template
5. Submit the pull request

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tested locally
- [ ] Tested in multiple browsers
- [ ] No console errors
- [ ] All features working

## Screenshots (if applicable)
Add screenshots here

## Additional Notes
Any additional information
```

## 🐛 Reporting Bugs

### Before Reporting
1. Check if the bug has already been reported
2. Try to reproduce the bug
3. Gather relevant information

### Bug Report Template
```markdown
**Describe the bug**
Clear description of what the bug is

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment:**
- OS: [e.g., Windows 10, macOS 12]
- Browser: [e.g., Chrome 96]
- Python Version: [e.g., 3.9.7]

**Additional context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
Clear description of what you want to happen

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Any other relevant information
```

## 🎯 Priority Areas

We're especially interested in contributions for:

1. **Multi-Student Support** - Monitor multiple students simultaneously
2. **WebSocket Integration** - Real-time updates without polling
3. **Emotion Detection** - Detect student emotions (happy, confused, bored)
4. **Mobile App** - iOS/Android companion app
5. **LMS Integration** - Connect with Canvas, Moodle, etc.
6. **Advanced Analytics** - More detailed insights and visualizations
7. **Accessibility** - Improve accessibility features
8. **Internationalization** - Multi-language support

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [JavaScript MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Python PEP 8](https://pep8.org/)

## ❓ Questions?

- Open an issue for questions
- Join our discussions
- Email: your.email@example.com

## 🙏 Thank You!

Every contribution, no matter how small, is valuable and appreciated. Thank you for helping make ClassAI better!

---

**Happy Coding! 🚀**
