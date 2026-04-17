### 1.How many layers does your image have? What does the largest layer contain?
10 and largest image probably update related

### 2.The error you get when importing `requests`
ModuleNotFound Error: No module named "requests"

### 1. What is the size of your image? Is it large or small — and why do you think that is?
179 MB, I think it’s small since the PC version is 1.25 GB.

### 2. How many layers does your image have? What does each major layer add?
10 and they are setting up the environment.

### 3. What operating system and architecture does your image use? (from `docker inspect`)
Os: Linux and Architecture: amd64

### 4. **Image-specific question:**
   - 🐍 Python: What error did you get when trying `import requests`? What does this tell you about how Docker containers work?
ModuleNotFoundError: No module named "requests". Docker containers are isolated environments, so they can't access the host machine's packages. Each container needs its own dependencies installed.

### 5. In one paragraph: what surprised you most about this lab?
Nothing. :D