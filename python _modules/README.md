# Python Modules for Network Engineers (Beginner Guide)
---

### 1. What is a Module?
- A module is just a Python file (`.py`) containing code (functions, classes, variables).
- Helps organize and reuse code.

### 2. Why use Modules in Network Automation?
- Keeps scripts **clean and reusable**.
- Example: One module for device functions, another for the main script.

### 3. How to Import a Module?
- **Option A:**  
  import module_name
  module_name.function()  # Must use prefix (module_name.function)

- **Option B:**  
  from module_name import function
  function()  # Use directly, no prefix

- **Option C:**  
  import module_name as mn
  mn.function() # Same as Option A but using a shorter alias (mn)

- **Option C:**  
  from module_name import *
  function()  # All functions available directly


### 4. Best Practices
- Use `import module_name` in larger projects (avoids name conflicts).
- Use `from module_name import ...` only for specific functions/variables.
- Keep module names short, lowercase, and descriptive.
