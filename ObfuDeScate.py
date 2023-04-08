import argparse
import os
import re
import shutil
import subprocess

from fuzzywuzzy import fuzz
from jinja2 import Template
from tqdm import tqdm


def is_subpath(subpath, path):
    '''
    Simple function to identify if one path is a subpath of anouther. Used for only checking directories that are
    part of the class path.
    :return: boolean (True/ False)
    '''
    subpath = os.path.normpath(subpath)
    path = os.path.normpath(path)

    # Split subpath and path into components
    subpath_parts = subpath.split(os.sep)
    path_parts = path.split(os.sep)

    # Find subpath in path
    for i in range(len(path_parts) - len(subpath_parts) + 1):
        if path_parts[i:i + len(subpath_parts)] == subpath_parts:
            return True

    return False


def create_output_file(sorted_functions):
    '''
    Function to create the output mapping file
    :param sorted_functions: a dictionary of the final sorted methods
    '''
    f = open(os.path.join(output_dir, "mapping.txt"), "w")

    for function in sorted_functions:
        app_one_function_name = function
        app_two_function_name = sorted_functions[function]['function']
        f.write("{} -> {} \n".format(app_one_function_name, app_two_function_name))

    f.close()


def create_html_file(sorted_functions):
    '''
    Sort the functions based on their score in descending order
    :param sorted_functions: a dictionary of the final sorted methods
    '''

    # Load HTML template
    template_str = '''
    <!DOCTYPE html>
    <html>

    <head>
        <title>Functions</title>
        <style>
            .codeblock-container {
                display: flex;
            }

            .codeblock {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                flex: 1;
                margin: 5px;
            }

            .codeblock h3 {
                cursor: pointer;
            }

            .codeblock pre {
                display: none;
            }

            .content {
                display: none;
            }

            .visible {
                display: block;
            }
        </style>
        <script>
            function toggleCodeBlock(id) {
                var content = document.getElementById(id);
                var codeblocks = content.getElementsByClassName("codeblock");
                var preTags = content.getElementsByTagName("pre");
                var displayValue = content.style.display === "none" ? "block" : "none";
                content.style.display = displayValue;
                for (var i = 0; i < codeblocks.length; i++) {
                    codeblocks[i].style.display = displayValue;
                }
                for (var i = 0; i < preTags.length; i++) {
                    preTags[i].style.display = "none";
                }
            }

            document.addEventListener("DOMContentLoaded", function () {
                {% for function in sorted_functions %}
                document.getElementById("{{ function }}_header").addEventListener("click", function () {
                    toggleCodeBlock("{{ function }}_content");
                });
                {% endfor %}
            });

            // Update the code block display when clicking on the code block heading
            document.addEventListener("DOMContentLoaded", function () {
                var codeBlocks = document.getElementsByClassName("codeblock");
                for (var i = 0; i < codeBlocks.length; i++) {
                    codeBlocks[i].getElementsByTagName("h3")[0].addEventListener("click", function () {
                        this.nextElementSibling.style.display = this.nextElementSibling.style.display === "none" ? "block" : "none";
                    });
                }
            });
        </script>
    </head>

    <body style="font-family: Arial, sans-serif;">
        <h1>Functions</h1>
        <ul>
            {% for function in sorted_functions %}
            {% set app_one_function_name = function %}
            {% set app_two_function_name = sorted_functions[function]['function'] %}
            {% set score = sorted_functions[function]['score'] %}
            {% set before_code = sorted_functions[function]['original method'] %}
            {% set after_code = sorted_functions[function]['new method'] %}
            <li>
                <h2 id="{{ function }}_header" style="cursor: pointer;">{{ app_one_function_name }}</h2>
                <div id="{{ function }}_content" class="content">
                    <h3>{{ app_one_function_name }} &rarr; {{ app_two_function_name }}</h3>
                    <p>Confidence: {{ score }}%</p>
                    <div class="codeblock-container">
                        <div class="codeblock" id="{{ function }}_before">
                            <h3>Before Code</h3>
                            <pre>{{ before_code }}</pre>
                        </div>
                        <div class="codeblock" id="{{ function }}_after">
                            <h3>After Code</h3>
                            <pre>{{ after_code }}</pre>
                        </div>
                    </div>
                </div>
            </li>
            {% endfor %}
        </ul>
        <script>
            // You can add additional JavaScript code here if needed
        </script>
    </body>

    </html>
    '''

    # Create Jinja2 template from the template string
    template = Template(template_str)

    # Render the template with the provided data
    html = template.render(sorted_functions=sorted_functions)

    # Write the rendered HTML to a file
    with open(os.path.join(output_dir, 'output.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def parse_arguments():
    """Parse command line arguments and return the parsed values."""
    parser = argparse.ArgumentParser(description="Compare two APKs and generate function mapping.")
    parser.add_argument("-a1", "--apk_file_path_1", type=str, help="Path to APK 1", required=True)
    parser.add_argument("-a2", "--apk_file_path_2", type=str, help="Path to APK 2", required=True)
    parser.add_argument("-cp", "--class_path", type=str, help="Optional allow list class path")
    parser.add_argument("-o", "--output_dir", type=str, help="Optional output directory for XML and TXT files")
    parser.add_argument("-apktool", "--apk_tool_path", type=str, help="Optional local path to APK Tool if not on path")
    args = parser.parse_args()
    return args


def extract_apk(apk_file_path, output_dir, apk_tool_executable):
    """Use apktool to disassemble the APK file."""
    print("Extracting APK at '{}'. This may take some time...".format(apk_file_path))
    with subprocess.Popen([apk_tool_executable, "d", apk_file_path, "-o", output_dir], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
        stdout, stderr = process.communicate(input="\n")
        if process.returncode != 0:
            print("An error occurred while running apktool for APK:")
            print(stderr)
            exit(1)


def check_apktool_on_path():
    """Check if apktool is on the path and return the executable name."""
    if shutil.which("apktool.bat"):
        return "apktool.bat"
    elif shutil.which("apktool.sh"):
        return "apktool.sh"
    elif shutil.which("apktool"):
        return "apktool"
    else:
        return None


def run_apktool(apk_tool_executable, apk_file_path, output_dir):
    """Run apktool to disassemble the APK file."""
    print("Extracting APK at '{}'".format(apk_file_path))
    with subprocess.Popen([apk_tool_executable, "d", apk_file_path, "-o", output_dir], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
        # Wait for the process to finish and capture the console output
        stdout, stderr = process.communicate(input="\n")

        # Check if the command was successful
        if process.returncode != 0:
            print("An error occurred while running apktool:")
            print(stderr)
            exit(1)


def get_smali_files(apk_dir, allow_path):
    """Get a list of all SMALI files in the disassembled APK directory."""
    smali_files = []
    file_to_path_dict = {}
    for dirpath, dirnames, filenames in os.walk(apk_dir):
        if is_subpath(allow_path, dirpath):
            for filename in filenames:
                if filename.endswith(".smali"):
                    smali_files.append(os.path.join(dirpath, filename))
                    file_to_path_dict[filename] = dirpath
    return smali_files, file_to_path_dict


if __name__ == '__main__':

    # Parse the command line arguments
    args = parse_arguments()

    # Extract values from the parsed arguments
    APK_FILE_PATH_1 = args.apk_file_path_1
    APK_FILE_PATH_2 = args.apk_file_path_2
    allow_list_class_path = args.class_path
    output_dir = args.output_dir
    apk_tool_path = args.apk_tool_path

    # If no path is provided populate with ""
    if not apk_tool_path:
        apk_tool_path = ""

    # If no path is provided set output dir to 'out'
    if not output_dir:
        output_dir = "out"

    # Set a generic class path if not set
    if not allow_list_class_path:
        allow_list_class_path = output_dir

    desired_class_path = os.path.join(*allow_list_class_path.split("."))

    # Output directories for the disassembled APKs
    OUTPUT_DIR_1 = os.path.join(output_dir, "app_1_tmp")
    OUTPUT_DIR_2 = os.path.join(output_dir, "app_2_tmp")

    # Check if apktool is on the path and use it if found
    apk_tool_executable = check_apktool_on_path()
    if apk_tool_executable is None:
        # If apktool is not found on the path, check if apk_tool_path is provided
        if apk_tool_path:
            apk_tool_executable = apk_tool_path
        else:
            print(
                "APKTool not found on the PATH. Either add 'apktool.sh'/ apktool.bat' to your path or provide a local path via the '--apk_tool_path' paramiter.")
            exit(1)

    # Run apktool to disassemble APK 1
    run_apktool(apk_tool_executable, APK_FILE_PATH_1, OUTPUT_DIR_1)

    # Run apktool to disassemble APK 2
    run_apktool(apk_tool_executable, APK_FILE_PATH_2, OUTPUT_DIR_2)

    # Get list of SMALI files from disassembled APK 1
    smali_files_1, file_to_path_dict_1 = get_smali_files(OUTPUT_DIR_1, desired_class_path)

    # Get list of SMALI files from disassembled APK 2
    smali_files_2, file_to_path_dict_2 = get_smali_files(OUTPUT_DIR_2, desired_class_path)

    app_one_method_to_smali_file = {}
    # Get a list of all SMALI methods in the disassembled APKs
    smali_methods_1 = []
    for smali_file in tqdm(smali_files_1, desc="Aggregating Methods from APK 1 SMALI"):
        with open(smali_file, "r") as f:
            content = f.read()
            methods = content.split(".method")
            for method in methods[1:]:
                method = method.strip("# virtual methods")
                smali_methods_1.append(method)
                app_one_method_to_smali_file[method] = smali_file

    app_two_method_to_smali_file = {}

    smali_methods_2 = []
    for smali_file in tqdm(smali_files_2, desc="Aggregating Methods from APK 2 SMALI"):
        with open(smali_file, "r") as f:
            content = f.read()
            methods = content.split(".method")
            for method in methods[1:]:
                method = method.strip("# virtual methods")
                smali_methods_2.append(method)
                app_two_method_to_smali_file[method] = smali_file

    app_one_path_to_method = {}
    app_two_path_to_mathod = {}

    scores = {}
    dict_of_functions = {}
    for app_one_method in tqdm(smali_methods_1, desc="Correlating comparison scores between APK1 and APK2 methods."):
        app_one_function_def = app_one_method.split("\n")[0].replace("->", ".")
        for app_two_method in smali_methods_2:
            app_two_function_def = app_two_method.split("\n")[0]
            score = fuzz.ratio(app_one_method, app_two_method)
            # score = is_same(app_one_method, app_two_method)

            app_one_function_name = re.search(r'\s*(\w+)\s*\(', app_one_function_def)
            app_two_function_name = re.search(r'\s*(\w+)\s*\(', app_two_function_def)

            app_one_file = app_one_method_to_smali_file[app_one_method]
            app_two_file = app_two_method_to_smali_file[app_two_method]
            app_one_file_path = os.path.split(app_one_file.replace(OUTPUT_DIR_1, ""))[0].split(os.sep)[2:]
            app_two_file_path = os.path.split(app_two_file.replace(OUTPUT_DIR_2, ""))[0].split(os.sep)[2:]

            app_one_class_name = os.path.split(app_one_file)[1].replace(".smali", "")
            if "$" in app_one_class_name:
                index = app_one_class_name.find("$")
                app_one_class_name = app_one_class_name[:index]

            app_two_class_name = os.path.split(app_two_file)[1].replace(".smali", "")
            if "$" in app_two_class_name:
                index = app_two_class_name.find("$")
                app_two_class_name = app_two_class_name[:index]

            if app_one_function_name and app_two_function_name:

                app_one_function_name = app_one_function_name.group(1)
                app_two_function_name = app_two_function_name.group(1)

                app_one_path = '.'.join(app_one_file_path + [app_one_class_name] + [app_one_function_name])
                app_two_path = '.'.join(app_two_file_path + [app_two_class_name] + [app_two_function_name])

                if app_one_path not in dict_of_functions:
                    dict_of_functions[app_one_path] = {}

                dict_of_functions[app_one_path][app_two_path] = score
                app_one_path_to_method[app_one_path] = app_one_method
                app_two_path_to_mathod[app_two_path] = app_two_method

    sorted_functions = {}
    matched_functions = []
    for function_def in dict_of_functions:
        related_functions = dict_of_functions[function_def]
        highest_match_function = ""
        highest_match_score = 0

        iterator = 100
        while iterator > 0:

            for related_function_def in related_functions:
                # Ensures a function isn't chosen twice.
                if related_function_def not in matched_functions:
                    score = related_functions[related_function_def]
                    if score > iterator:
                        if score > highest_match_score:
                            highest_match_score = score
                            highest_match_function = related_function_def

            if highest_match_function != "":
                matched_functions.append(highest_match_function)
                break

            iterator = iterator - 1

            # Confidence too low, so break
            if iterator < 60:
                break

        if highest_match_function != "":
            sorted_functions[function_def] = {"score": highest_match_score, "function": highest_match_function,
                                              "original method": app_one_path_to_method[function_def],
                                              "new method": app_two_path_to_mathod[highest_match_function]}
        else:
            sorted_functions[function_def] = {"score": 0, "function": "no match", "original method": "",
                                              "new method": ""}

    # Sort dict on sub-dict value score
    sorted_functions = {k: v for k, v in
                        sorted(sorted_functions.items(), key=lambda item: item[1]['score'], reverse=True)}

    # Check if output_dir exists
    if not os.path.exists(output_dir):
        # Create the output_dir folder
        os.makedirs(output_dir)

    create_html_file(sorted_functions)
    create_output_file(sorted_functions)
    print("Outputs saved in '{}'".format(output_dir))
