# tools/dev-docs/NEWPROJECT.md

1. **Create Project Folder**
   <pre lang="markdown">
   create new project directory
   copy project starter files from another project
   rename project references as needed (example: find/replace "CodeIt" → "BakeIt")
   </pre>

1. **Update Project Configuration**
   <pre lang="markdown">
   update / verify .env (Dashboard)
   update / verify tests/
   update / verify pytest.ini
   </pre>

1. **Create Virtual Environment**
   <pre lang="markdown">
   python -m venv .venv
   source /p/dev.mukmuk/BakeIt/.venv/Scripts/activate
   pip list
   python.exe -m pip install --upgrade pip
   pip install argparse dotenv results pyinstaller pytest
   </pre>

1. **Initialize Git**
   <pre lang="markdown">
   git config --global init.defaultBranch main
   git init
   git add .
   git commit -m "Initial Commit"
   </pre>

1. **Connect to GitHub**
   <pre lang="markdown">
   git remote add origin https://github.com/devmukmuk/bakeit.git
   git remote -v
   git status
   git branch -M main (if branch is master)
   git push -u origin main
   git branch
   </pre>

1. **Create First Issue**
   <pre lang="markdown">
   create at lease one new issues with SP:1
   </pre>  

1. **Create Project Milestones and Labels**
   <pre lang="markdown">
   python ./tools/create_milestones_from_csv.py --csv ./tools/milestones.csv --weeks 12
   python ./tools/create_labels_from_csv.py --csv ./tools/points.csv
   </pre>   

1. **First Tag**
   <pre lang="markdown">
   python -m tools.build --autobuild --publish --os win
   </pre>


<br>Author: Mike Mattinson  
<br>Updated: Feb/28/2026