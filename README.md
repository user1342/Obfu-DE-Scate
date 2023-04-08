<p align="center">
    <img width=100% src="cover.png">
  </a>
</p>
<p align="center"> 🤖 A de-obfuscation tool for Android APKs. Allowing you to compare multiple versions of an APK to identify the same code across renamed, altered, and missing functions. 📱 </p>

<br>

Obfu[DE]scate is a Python tool designed to take two versions of an APK file and use fuzzy comparison logic to identify similarities between functions even if they've been renamed as part of obfuscation. 
- To get started, download the dependancies and ensure you have APKTool installed and on your path.
- Get two versions of an APK and run ```ObfuDeScate.py``` with then as paramiters (use ```--apk_file_path_1``` and ```--apk_file_path_2```).
- After run, an ouput directory will be created with a mapping text file and full breakdown HTML file.

# ➡️ Getting Started 
## Installation 
After cloning the repository all Obfu[DE]scate dependencies can be installed manually or via the requirements file, with:

``` bash
pip install -r REQUIREMENTS.txt
```

In addition to the above, you will also need a copy of APKTool either on your path or provided with the ```--apk_tool_path``` paramiter. Download APKTool for your system as directed on [their website](https://ibotpeaches.github.io/Apktool/).

Obfu[DE]scate has only been tested on **Windows 11**, however, should work with other systems. 
