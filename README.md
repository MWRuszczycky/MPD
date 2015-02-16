# MPD: Make Project Directory

## Overview

**M**ake **P**roject **D**irectory is a script for creating a new project directory based on templates kept in a seperate resource directory. The directory layout is described by a JSON file also kept in the resource directory.

When run from the command line, the user is presented with a series of menus from which the different templates can be selected. Unwanted templates can be skipped. Once the templates are chosen, a project name is entered, and the project directory is created in the current working directory. If the directory already exists, it is just populated with the selected templates. If files with the same names as the templates already exist, they are not overwritten, and the templates are simply ignored. The user is informed about how the directory is being built.

## Usage

### The Resource Directory

The resource directory should have a series of subdirectories containing the possible alternatives for each template as well as a single JSON file describing the directory structure. The JSON file can have any name and extension, but there can only be one. An example resource directory for a LaTeX project might look like
```
ResourceDir/
|   LaTex_MainTemplates/
|   |   JournalXDoc.tex
|   |   GenericTwoColDoc.tex
|   |   GenericOneColDoc.tex
|   BibTeX_ReferenceTemplates/
|   |   Complete.bib
|   |   Unpublished.bib
|   BibTeX_StyleTemplates/
|   |   JournalXFormat.bst
|   |   JournalYFormat.bst
|   LaTeX.json
```
The location of the resource directory from the user's home directory is set by editing the `MPD_RESDIR_FROM_HOME` variable found in the first few lines of the script.

### The JSON File

The JSON file (e.g., `LaTeX.json`) has two objects. The first, named `FILE_KEYS`, maps the template directories to template file names. The second, named `DIR_STRUCT`, describes the structure of the project directory. Each subdirectory is just an object, the members of which are either arrays or more subdirectory objects. Files in each subdirectory are named in an array named `FILES`. This array is left empty if there are no files. File names in the array are replaced by the templates as per the directory they are found in. Their names are replaced by the name given in the `FILE_KEYS` object. If a file name is present that does not map to a template (e.g., the `sectionone.tex` file below), an empty file with that name is created. For example, the `LaTeX.json` file from above could have the form:
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

When run, the user is presented with menus of the form
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
  * Allow user to choose from different project directories, so a different script is not required for each project type
  * Allow different templates to have the same name in the project directory (e.g., CMakeLists.txt files)
  * Improve checking for poorly formatted JSON files

## Requirements

Python 3 (tested with Python 3.4.0). Runs on Linux.
