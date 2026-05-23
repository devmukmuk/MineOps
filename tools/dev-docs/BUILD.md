# tools/dev-docs/BUILD.md

1. **Install Build Dependencies**
   <pre lang="markdown">
   python -m pip install --upgrade pip
   pip install pyinstaller
   </pre>

1. **Choose Build Mode**
   <pre lang="markdown">
   Full Release:
       - Increment or set version
       - Update __version__ in project __init__.py
       - Create release folder
       - Run tests
       - Run project and milestone dashboards
       - Export requirements.txt
       - Build executable

   Binary Only:
       - Build executable only
       - No version changes
       - No release folder changes
   </pre>

1. **Run Build Script**
   <pre lang="markdown">
   Full autobuild (Windows):
       python -m tools.build --autobuild --os win

   Manual version build:
       python -m tools.build --major 0 --minor 19 --build 11

   Binary only (Linux):
       python -m tools.build --binary-only --os linux
   </pre>

1. **Release Folder Creation**
   <pre lang="markdown">
   The build script automatically creates a release folder:
       releases/release-vX.Y.Z
   If the folder exists, you can:
       - Overwrite (o)
       - Increment build number (i)
       - Cancel (c)
   </pre>

1. **Run Tests and Dashboards (Full Release Only)**
   <pre lang="markdown">
   - Run test suite: tools.test
   - Run project dashboard: tools.dashboard --save
   - Run milestone dashboard: tools.dashboard --save --milestone=vX.Y.0
   </pre>

1. **Export Requirements**
   <pre lang="markdown">
   Export installed packages to release folder:
       requirements_vX.Y.Z.txt
   </pre>

1. **Build Executable**
   <pre lang="markdown">
   - PyInstaller builds single-file executable
   - Excludes modules defined in tools/build.ini
   - Uses entry point from tools/build.ini (bakeit/bakeit_cli.py)
   - Adds optional data files and icons from assets/
   - Example Windows executable: BakeIt-vX.Y.Z.exe
   - Example Linux executable: BakeIt-vX.Y.Z
   </pre>

1. **Publish Release (Optional)**
   <pre lang="markdown">
   Commit, tag, push, and create GitHub release:
       python -m tools.build --autobuild --publish --os win
   </pre>

<br>Author: Mike Mattinson  
<br>Updated: Feb/28/2026