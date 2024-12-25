# Code Consolidator

A modern GUI application that helps prepare your codebase for ChatGPT code review by consolidating multiple source files into a single, well-formatted text file.

Created by Waleed Faruki © 2024

## Features

- 🎨 Modern, dark-themed interface with tabbed organization
- 📁 Smart file pattern matching for inclusion/exclusion
- 🔍 Real-time pattern preview
- ⚙️ Configurable settings with persistence
- 📝 Custom GPT instructions support
- 🚀 Background processing with progress indication
- 💾 Automatic settings backup and restore

## Installation

1. Ensure you have Python 3.8+ installed
2. Install the required dependencies:
```bash
pip install ttkbootstrap
```

## Usage

1. Run the application:
```bash
python code_consolidator.py
```

2. Select your project directory using the "Browse" button

3. Configure file patterns:
   - **Include Patterns**: Specify which files to include (e.g., `*.py`, `*.js`)
   - **Exclude Patterns**: Specify which files to exclude (e.g., `node_modules/*`, `*.pyc`)

4. Write custom instructions for GPT in the instructions text area

5. Set your output file name (defaults to `consolidated_code.txt`)

6. Click "Generate Consolidated Code" to create the file

## File Patterns

The application uses glob patterns to match files:

- **Include Examples**:
  - `*.py` - All Python files
  - `*.{js,jsx}` - All JavaScript and JSX files
  - `src/*.ts` - All TypeScript files in the src directory

- **Exclude Examples**:
  - `node_modules/*` - All files in node_modules
  - `*.pyc` - All Python compiled files
  - `__pycache__/*` - All Python cache files

## Default Settings

The application comes with sensible defaults:

### Include Patterns
- `*.py` - Python files
- `*.js` - JavaScript files
- `*.jsx` - React JSX files
- `*.ts` - TypeScript files
- `*.tsx` - React TypeScript files
- `*.html` - HTML files
- `*.css` - CSS files
- `*.java` - Java files
- `*.cpp` - C++ files
- `*.h` - Header files
- `*.c` - C files

### Exclude Patterns
- `node_modules/*` - Node.js dependencies
- `venv/*` - Python virtual environments
- `*.pyc` - Python compiled files
- `__pycache__/*` - Python cache
- `*.git/*` - Git files
- `build/*` - Build outputs
- `dist/*` - Distribution files

## Output Format

The generated file will have the following structure:

```
# Your GPT Instructions Here

================================================================================

File: path/to/first/file.py
================================================================================
[Content of first file]


File: path/to/second/file.js
================================================================================
[Content of second file]

...
```

## Settings

All settings are automatically saved to `consolidator_settings.json` and include:
- Include/exclude patterns
- Default GPT instructions
- Theme preferences

## Tips

1. Use the pattern preview in the Settings tab to verify your file patterns
2. Write clear, specific instructions for GPT in the instructions area
3. Exclude unnecessary files (like node_modules) to keep the output focused
4. Use the progress bar to track large consolidation tasks
5. Save your commonly used patterns using the Settings tab

## Troubleshooting

1. **File not included**: Check the Settings tab pattern preview
2. **Unicode errors**: Ensure source files are UTF-8 encoded
3. **Large files**: For very large projects, be specific with include patterns
4. **Missing files**: Verify file permissions and paths

## Contributing

Feel free to submit issues and enhancement requests!

## License

Copyright © 2024 Waleed Faruki. All rights reserved.
