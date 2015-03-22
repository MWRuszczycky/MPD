# MPD: Make Project Directory

## Overview

**M**ake **P**roject **D**irectory is a script for creating a new project directory based on templates kept in a seperate project template directory. The directory layout is described by a JSON file also kept in the project template directory.

When run from the command line, the user is asked to pick a project template directory corresponding to the project to be created. The user is then presented with a series of menus from which the different file templates can be selected. Unwanted templates can be skipped. Once the templates are chosen, a project name is entered, and the project directory is created in the current working directory. If the directory already exists, it is just populated with the selected templates. If files with the same names as the templates already exist, they are not overwritten, and the templates are simply ignored. The user is informed about how the directory is being built.

## Usage

### The Resource Directory

The resource directy should contain a collection of project template subdirectories that correspond to the different project types (e.g., a LaTeX, C++, Python, etc.). Each project template directory should have a series of subdirectories containing the possible alternatives for each file template as well as a single JSON file describing the directory structure. The JSON file can have any name and extension, but there can only be one. An example resource directory that contains a LaTeX project and two other project types might look like (only the LaTeX project template directory is expanded)
```
ResourceDir/
|   New_LaTeX_Project/
|   |   LaTeX_MainTemplates/
|   |   |   JournalXDoc.tex
|   |   |   GenericTwoColDoc.tex
|   |   |   GenericOneColDoc.tex
|   |   BibTeX_ReferenceTemplates/
|   |   |   Complete.bib
|   |   |   Unpublished.bib
|   |   BibTeX_StyleTemplates/
|   |   |   JournalXFormat.bst
|   |   |   JournalYFormat.bst
|   |   LaTeX.json
|   New_Python_Project/
|   New_CPP_Project/
```
The location of the resource directory from the user's home directory is set by editing the `MPD_RESDIR_FROM_HOME` variable found in the first few lines of the script.

### The JSON File

The JSON file (e.g., `LaTeX.json`) has two objects. The first, named `FILE_KEYS`, maps the template directories to template file names. The second, named `DIR_STRUCT`, describes the structure of the project directory. Each subdirectory is just an object, the members of which are either arrays or more subdirectory objects. Files in each subdirectory are named in an array named `FILES`. This array is left empty if there are no files. File names in the array are replaced by the templates as per the directory they are found in. Their names are replaced by the name given in the `FILE_KEYS` object. If a file name is present that does not map to a template (e.g., the `sectionone.tex` file below), an empty file with that name is created. For example, the `LaTeX.json` file from the above example could have the form:
```json
{
    "FILE_KEYS": {
        "LaTeX_MainTemplates": "main.tex",
        "BibTeX_ReferenceTemplates": "references.bib",
        "BibTeX_StyleTemplates": "refstyle.bst"
  },

    "DIR_STRUCT": {
        "FILES": [],
        "tex": {
            "FILES": ["LaTeX_MainTemplates"],
            "sec": {
                "FILES": ["sectionone.tex"],
                "scratch": {"FILES": []}
            },
            "ref": {
                "FILES": ["BibTeX_ReferenceTemplates", "BibTeX_StyleTemplates"]
            },
            "img": {"FILES": []}
        },
        "build": {"FILES": []},
        "design": {"FILES": []}
    }
}
```

### Selecting Templates

When run, the user is first asked which project type to create and and then presented with menus of the form (assuming the LaTeX project was selected in the example above):
```
Choose template for main.tex in the LaTeX_MainTemplates directory.
    1: JournalXDoc.tex
    2: GenericTwoColDoc.tex
    3: GenericOneColDoc.tex
    0: Do not create this template
    q: Quit
Selection:
```
If the user selects `JournalXDoc.tex` for `main.tex`, `Complete.bib` for `references.bib` and `JournalXFormat.bst` for `refstyle.bst`, then the following directory will be created for a project named `MyNewProject`
```
MyNewProject/
|   tex/
|   |   sec/
|   |   |   scratch/
|   |   |   sectionone.tex          # new, empty file
|   |   ref/
|   |   |   references.tex          # copy of Complete.bib
|   |   |   refstyle.bst            # copy of JournalXFormat.bst
|   |   img/
|   |   main.tex                    # copy of JournalXDoc.tex
|   build/
|   design/
```

## Issues/To Do
  * Port to Windows

## Requirements

Python 3 (tested with Python 3.4.0). Runs on Linux.
