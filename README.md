<p align="center">
    <img width=100% src="/assets/cover.png">
  </a>
</p>
<p align="center"> 🤖 <b> Obfu[DE]scate: A De-obfuscation and Comparison tool for Android APKs. 📱 </b> </p>

<br>

Obfu[DE]scate is a Python tool designed to simplify the process of de-obfuscating and comparing two versions of an Android APK - even if the functions have been renamed as part of obfuscation. With fuzzy comparison logic, Obfu[DE]scate can identify similarities between functions and help you uncover changes between APK versions.

# ➡️ Getting Started
## Installation
Getting started with Obfu[DE]scate is easy! Follow these steps:

1) Clone the repository to your local machine.
2) Install the dependencies manually or via the included requirements file using the following command:
```bash
pip install -r REQUIREMENTS.txt
```
3) **Download APKTool for your system from [their website](https://ibotpeaches.github.io/Apktool/documentation/). and make sure it's installed and available in your PATH.**


Obfu[DE]scate has been tested on *Windows 11*, but should work on other systems as well.

## Running
Obfu[DE]scate provides several command-line options to customize its behavior:

| Shorthand | Paramiter         | Description                                                                                                                                            | Required |
|-----------|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| -a1       | apk_file_path_1 | The path to the original APK. This is the APK that the second APK will be compared against (i.e. an older version of the APK)                          | True     |
| -a2       | apk_file_path_2 | The path to the newer APK. The output will show changes between APK 1 and this APK.                                                               | True     |
| -cp       | class_path      | A reverse domain notation path that will be used to filter reviewed functions (i.e. provide com.example.class to only compare functions on this path). | False    |
| -o        | output_dir      | A directory to save the output mapping, html, and dissasembled APKs to.                                                                                | False    |
| -apktool  | apk_tool_path   | If APKTool is not on your path use this parameter to tell ObfuDeScate where APKTool is located.                                                        | False    |

To compare two APK files, simply run Obfu[DE]scate with the following command:

```bash 
python ObfuDeScate.py -a1 "old_example.apk" -a2 "new_example.apk" -cp "com.example.path"
```

In the above example, Obfu[DE]scate will review all functions in the ```old_example.apk``` APK at the class path ```com.example.path``` and compare them against all functions found at the same class path in ```new_example.apk```.

# 🔎 Outputs
Obfu[DE]scate generates two output files: a mapping file in newline-separated list format, and an interactive HTML file. These output files include:
- **mapping.txt** - A newline seperated text file with each line relating to an identified match between a method in APK1 and APK2. The format for these lines are such as: ```com.chess.play.ObserveGameHelperImpl.d -> com.chess.play.ObserveGameHelperImpl.a ```.
- **output.html** - A HTML file that when opened in a web browser lists all functions in APK1. These are dropdowns that when clicked show the matched method in APK2 (if any), the confidence of them being a match, and the codeblock in SMALI for that method from APK1 and APK2. 

<p align="center">
  <img src="/assets/html_example.png" width="400" />
  <img src="/assets/mapping_example.png" width="400" />
  <img src="/assets/running.gif" width="400" />
</p>

# 📜 License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
