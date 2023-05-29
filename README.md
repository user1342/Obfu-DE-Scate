<p align="center">
    <img width=100% src="/assets/cover.png">
  </a>
</p>
<p align="center"> 🤖 <b> Obfu[DE]scate: A De-obfuscation and Comparison tool for Android APKs. 📱 </b> </p>

<br>
<div align="center">

![GitHub contributors](https://img.shields.io/github/contributors/user1342/Obfu-DE-Scate)
![GitHub Repo stars](https://img.shields.io/github/stars/user1342/Obfu-DE-Scate?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/user1342/Obfu-DE-Scate?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/user1342/Obfu-DE-Scate)
<br>
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P7C2MM6)
</div>

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

| Shorthand | Parameter         | Description                                                                                                                                            | Required |
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

# 🙏 Contributions
Obfu[DE]scate is an open-source project and welcomes contributions from the community. If you would like to contribute to Obfu[DE]scate, please follow these guidelines:

- Fork the repository to your own GitHub account.
- Create a new branch with a descriptive name for your contribution.
- Make your changes and test them thoroughly.
- Submit a pull request to the main repository, including a detailed description of your changes and any relevant documentation.
- Wait for feedback from the maintainers and address any comments or suggestions (if any).
- Once your changes have been reviewed and approved, they will be merged into the main repository.

# ⚖️ Code of Conduct
Obfu[DE]scate follows the Contributor Covenant Code of Conduct. Please make sure [to review](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md). and adhere to this code of conduct when contributing to Obfu[DE]scate.

# 🐛 Bug Reports and Feature Requests
If you encounter a bug or have a suggestion for a new feature, please open an issue in the GitHub repository. Please provide as much detail as possible, including steps to reproduce the issue or a clear description of the proposed feature. Your feedback is valuable and will help improve Obfu[DE]scate for everyone.

# 💛 Thanks
This tool wouldn't work without [APKTool](https://ibotpeaches.github.io/Apktool/documentation/)! Secondly, many of the examples in this README use the Chess.com app as a base, check it out [here](https://play.google.com/store/apps/dev?id=5068259210636929122).

# 📜 License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
