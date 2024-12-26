EPFL - Environmental Sciences and Engineering 
Semester: BA3 - Autumn 22
course: ENG-270 Computational Methods and Tools
Teacher: Satoshi Takahama
Student: Jan Zgraggen 

Filename: "README.txt"
File-Purpose:
    File describes each of the files in the folder, provides Software versions, declares needed installations and a manual on how to use the code.

File-Content:
    • Software used
    • Libraries & required installations
    • Short user manual
    • Description of files


SOFTWARE USED:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
python:     3.10.4 64-bit
gcc:        Apple clang version 14.0.0 (clang-1400.0.29.202) #Note: gcc installed via Xcode (MacOs)  
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


LIBRARIES & REQUIRED INSTALLATIONS:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
–––––––-–––
Python Libraries: 
    standart:
        sys
        os
        numpy
        mathplothlib.pyplot
        math 
    installation needed:
        streamlit 
            installation:
                PIP install command: "$ pip install streamlit"
            usage:
                the CLI command  "$ streamlit run filename.py " launches a local http which interactively reacts with the python-file, if the module is imported to the file.
                that is: inputs given to the http are instantaneously returned to the python file.
                This allows to take user inputs via the GUI of streamlit. 

–––––––-–––
–––––––-–––
C header-files:
    <stdio.h>       // header file needed to use inputs and outputs of functions)
    <string.h>      // string manipulation
    <stdlib.h>      // standard library
    <math.h>        // pi, trig., etc.
–––––––-–––
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


SHORT USER MANUAL:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
–––––––-–––
Step by step:
    Note: 
        •Do steps 0-4 if you want do run the simulation upon an input file:
        •Do stems 1,2,4 if you want to run the simulation upon input from a GUI:

    0)  [optional]: 
            open Input_file.csv: Modify parameters according to the explanation note in brackets:
            example line of the Input_file document: 
                value = MODIFY_ME    [explanation: Type a number instead of MODIFY_ME to assign it to value]
    1)  [mandatory]:
            In the terminal change the directory to the "root" (top folder) of the program
    2)  [mandatory]:
            Enter the the following to the command-line: $ python3.10  GTHP_simulation_V04_def.py 
    3)  [optional]:
            Add the name of the input-file to the command-line after the above typed: $ python3.10  GTHP_simulation_V04_def.py Input_file.csv
    4)  [mandatory]:
            Press enter to run simulation with the typed command-line input
    5)  [optional]:
            Save the generated file to the desired location
–––––––-–––
–––––––-–––
Process flow:
    •"GTHP_simulation_V04_def.py" is run by user via terminal

    •"GTHP_simulation_V04_def.py"  [if no commandline args given] runs "gui_from_streamlit_V01_def.py" (with streamlit run)   
        •"gui_from_streamlit_V01_def.py" creates "GUI_parameter.csv" file
        •"GTHP_simulation_V04_def.py" reads "GUI_parameter.csv" file  
        
    •"GTHP_simulation_V04_def.py"  [if filename provided as CL-arg] reads "Input:file.csv"                                        
    
    •"GTHP_simulation_V04_def.py" runs "pipe_param_V06_def.py" 
        •"pipe_param_V06_def.py" imports classes from "path_parameters_V02_def.py"
        •"pipe_param_V06_def.py" creates "xz_coords.csv" 
    
    •"GTHP_simulation_V04_def.py" compiles "heat_propagation_V03_def.c"
    
    •"GTHP_simulation_V04_def.py" runs "heat_propagation_V03_def.c"
        •"heat_propagation_V03_def.c" reads "xz_coords.csv" 
        •"heat_propagation_V03_def.c" creates "output_file.csv" 
    
    •"GTHP_simulation_V04_def.py" runs "visualisation_V01_def.py"
        •"visualisation_V01_def.py" reads "output_file.csv" 
        •"visualisation_V01_def.py" creates "GTHP Visualisation" figure
    
    Note: "GTHP_simulation_V04_def.py" uses os.system("CL-input") in order to "run" or "compile" other scripts
–––––––-–––
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


FILE DESCRIPTION:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
–––––––-–––
info: 
    status:         Declares whether user interacts with file (ACTIVE or PASSIVE), and how its manipulated
    (argv):	    (For source files:) These command-line arguments have to be given in order to avoid the raise of an error, when running the script isolated. 
    Description:    Describes what the file does
–––––––-–––
–––––––-–––
Files:
    –––––––-–––
    README.txt
        status:
            (PASSIVE) read for informations
        Description:
            Information & Instructions
    –––––––––––
    –––––––––––
    Input_file.csv
        status:
            (ACTIVE): Create input-files according to the Description, 
                      or change Parameters of the provided input-file according to the syntax in the description.
                      In order to run the Simulation with the parameters from the input-file
                      pass the filename of the input-file as command-line argument to "GTHP_simulation_V04_def.py" (see: TASK "GTHP_simulation_V04_def.py")
        Description:
            Input file contains the parameters that are fed to the simulation.
            The file structure is the following: the parameters:
                path, rho, Cp, q, Ti, r, thickness, k, PreviewPath, ShowParamInGraph, output_filename
            have are specified in the following syntax row by row:
                Name of the variable = value [explanation, order of magnitude]
            comments or titles can be arbitrarily introduced if succeeding by "#" as well as empty lines

            Note:
                In order to avoid errors in the execution of the program the parameters should be given in the correct syntax and according to the physics of the problem (oder of magnitude).
    –––––––––––
    –––––––––––
    GTHP_simulation_V04_def.py
        status:
            (ACTIVE) TASK: run this file trough the command-line using: "python3.10 GTHP_simulation_V04_def.py inputFilename(optional)"
                    -if a filename(optional) is specified as a comand-line argument the simulation takes the parameters from it,
                    -otherwise the simulation will open a GUI to ask for the parameters. Note: for this the streamlit library has to be installed.
        Argv:
            "inputfile_name" or None
        Description:
            Links together all the subprocesses by calling terminal commands via the os module os.system
            subprocesses:
                Decides whether a GUI is used or not: (where to get the parameters from; GUI or input file if specified)
                Runs simulation with received parameters
                Shows result in a Graphic
    –––––––––––
    –––––––––––
    gui_from_streamlit_V01_def.py
        status:
            (PASSIVE) Gets called with streamlit by "GTHP_simulation_V04_def.py"
        Argv:
            None (CLI: "streamlit run filename.py" required rather than "python3.10 filename.py")
        Description
            uses streamlit library in order to get parameter inputs with a GUI
            Writes GUI inputs to file for further use
            Terminates GUI process such that the GTHP_simulation_VO4_def.py file can continue to with commands via os.system to the terminal.
    –––––––––––
    –––––––––––
    path_parameters_V02_def.py
        status:
            (PASSIVE) Gets imported to "gui_from_streamlit_V01_def.py" , "pipe_param_V06_def.py", "visualisation_V01_def.py"
        Argv:
            None (script does not return anything)
        Description:
            Contains Classes of Paths:
            These Paths are hard coded and meant to give the user an overview of the possibilities of the simulation
            Note:
                -If requested: paths can be modified. 
                -The addition of paths is possible but requires minor adjustment of the code 
                (e.g additional import). It is therefore not intended to be done within the scope of the product of this project.

            Classes of paths contain (1x) Class of Parameters, (Nx) Classes of segments
            The content of the Segment classes specifies the functions and length used to "draw" the curve part by part
            The content of the Parameter Segmentation specifies name, inter-punctual distance and initial point.
    –––––––––––
    –––––––––––
    pipe_param_V06_def.py
        status:
            (PASSIVE) Gets called by "GTHP_simulation_V04_def.py"
        Argv:
            "path" "Plot_preview_yes_no" (path = 1,2,3,4,5; Plot_preview_yes_no = 0,1) 
        Description:
            import path-classes form: "path_parameters_V02_def.py"
            Uses given data to generate equidistant coordinates (x,z) along the specified path
            Information about which path to choose is passed by command line arguments
            A graphic with a preview of the drawn path is returned if correct specifier is passed by command line arguments
            These coordinates are written to a csv-file along with a header that contains informations about the parameters
    –––––––––––
    –––––––––––
    visualisation_V01_def.py
        status:
            (PASSIVE) Gets called by "GTHP_simulation_V04_def.py" 
        Argv:
            "path" "display_parameter_yes_no" "r" "output_filename" (path = 1,2,3,4,5; Plot_preview_yes_no = 0,1; r > 0) 
        Description:
            reads in file with calculated data
            Generates a graphic that visualises the obtained calculation where the Temperature is shown by color
    –––––––––––
    –––––––––––
    heat_propagation_V03_def.c
        status:
            (PASSIVE) Gets compiled and executed by "GTHP_simulation_V04_def.py"
        Argv:
            "rho" "Cp" "q" "T_initial" "r" "delta_r" "k_mat" "filename" (rho,Cp,q,r,delta_r,k_mat > 0)
        Description
            Reads in coordinates and Parameters form a csv-file
            assigns Soil environment temperature to coordinates 
            calculates the temperature of a flowing fluid as a function of distance along the path
            writes calculated data to csv-file and passes as well read in parameters as header to that file
    –––––––––––
    (xz_coords.csv)
        status:
            (PASSIVE -generated during simulation) Is created by "pipe_param_V06_def.py" and read in to "heat_propagation_V03_def.c"
        Description
            CSV file that contains the (x,z) coordinates of equidistant points along the curve specified in GUI or input-file.
            In it's header there is information about the increment along the path between the points and the number of total points (of which the coordinates are stored)
    –––––––––––
    –––––––––––
    (result_file.csv)
        status: 
            (PASSIVE - generated during simulation) Filename is given in parametrisation. File is created by "heat_propagation_V03_def.c" and read in to "visualisation_V01_def.py"
        description:
            CSV file that contains (x,z) coordinates of of equidistant points along the curve, specified in GUI or input-file, 
            the number of the point,
            the soli temperature at height z: T_soil, 
            the fluid temperature at the Point of the pipe specified by the coordinates.
    –––––––––––
    –––––––––––
    (GUI_parameter.csv)
        status:
            (PASSIVE - generated during simulation) Is created by "gui_from_streamlit_V01_def.py" and read into "GTHP_simulation_V04_def.py" if no input-file is given and the parameters are taken from the GUI, 
        description:
            contains parameters needed to run the simulation, in the order of necessity for the read-in function (one per line, FLTR(*)):  path, rho, Cp ,q ,T_initial ,r ,delta_r ,k_mat ,Plot_preview_yes_no, display_parameter_yes_no 
        (*) Abbrev. for "from left to right"
    –––––––––––
–––––––-–––
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––