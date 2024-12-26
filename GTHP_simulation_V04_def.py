##-------------------------------------- Description ------------------------------------------------------------------##
'''
EPFL - Environmental Sciences and Engineering 
Semester: BA3 - Autumn 22
course: ENG-270 Computational Methods and Tools
Teacher: Satoshi Takahama
Student: Jan Zgraggen 

Filename: "GTHP_simulation_V04_def.py"
File-Purpose:
    Links to gether all the subprocesses by calling terminal comands via the os module os.system
    Decides whether a GUI is used or not: (where to get the parameters from; GUI or comandline input)
    Runs simulation with recieved parameters
    Shows result in a Grafic
'''

##-------------------------------------- Import libraries -------------------------------------------------------------##
import os as os
import sys as sys

##-------------------------------------- Function to cut newline specifier form end of string -------------------------##
def cut_newline_specifier(line):
    '''
    What does this function do?
        Short:  Takes in a string of type: "text\n" and cuts the "\n"

    Input: 
        line = string of format "text\n"
        
    Return: 
        string = string of format "text"
    '''
    string = ((line).split("\n")[0] ) 
    return string

##-------------------------------------- Readin function (from GUI) ----------------------------------------------------##
def read_param(filename):
    '''
    What does this function do?
        Short:  Takes in a file of parameters (1 per line)

    Input: 
        filename = name of the parameter file
        
    Return: 
        params = list of all values in the file
    '''
    params= []
    with open(filename, "r") as file:
        for row in file:
            params.append(cut_newline_specifier(row))
    return params


##-------------------------------------- proces row of parameter input file ---------------------------------------------##
def process_inputfile_line(line):
    '''
    What does this function do?
        Short:  Takes a line of format: "VariableName = Number [Explenation]" 
        .                 or of format: "#Explenations ..."
        it returns "Number" of the string is of the first format and None of its of the second.
                
    Input: 
        line = string of format: "VariableName = Number [Explenation]"  or "#Explenations ..."
        
    Return: 
        string of format "Number" or none
    '''
    if line == "\n":
        return None
    else:
        line == line.strip()
    if line[0] == "#":
        return None
    else:
        return (((line.split("["))[0]).split("=")[1]).strip()

##-------------------------------------- Get parameter from inputfile ------------------------------------------------##
def read_userInput(filename):
    '''
    What does this function do?
        Short:  Reads parameters from user input file and stores them in a list
                
    Input: 
        filename = name of user input file
        
    Return: 
        list of parameters (of string type)
    '''
    params = []
    with open(filename, "r") as file:
        for row in file:
            row_str = row
            if process_inputfile_line(row_str):
                params.append(process_inputfile_line(row_str))
    return params

def filenameduplicate(filename):
    i = 2
    while os.path.isfile(filename):
        if i ==2:
            filename = filename.split(".csv")[0]+ f"_{i}.csv"
        elif i > 2:
            filename = filename.split(f"_{i-1}.csv")[0] + f"_{i}.csv"
        i += 1
    return filename


##-------------------------------------- Display GUI manual/streamlit and run simulation ------------------------------##
def dispUI_andRun(filename):
    '''
    What does this function do?
        Takes in a filename or None, if no filename specified opens GUI to collect parameter, otherwise takes them from file
        collects parameters (from "gui_from_streamlit_V01_def.py" via os.system OR from "inputfile" )
        runs simulation by running the required scripts with the system functuion of the os module.

    Input: 
        filename (str or 0): Name of the file where the parameters are to get;  or 0
        
    Return: 
        (0)
        Indirect:
            Return of called scripts
    '''
    ##check if comandline argument with valid filename is given
    if filename:
        try:
            params = read_userInput(filename)
        ## if not open GUI
        except:
            print("ERROR: input file error, get GUI input")
            os.system("streamlit run src/inputgui_from_streamlit_V01_def.py")
            params = read_param("data/GUI_parameter.csv")

    else:
        print(os.getcwd())
        os.system("streamlit run src/input/gui_from_streamlit_V01_def.py ")
        params = read_param("data/GUI_parameter.csv")

    ##unwrap parameters
    path = params[0] #path
    rho = params[1]; Cp =params[2] ;q = params[3];T_initial =params[4] #fluid
    r = params[5];delta_r = params[6];k_mat =params[7] #pipe©
    Plot_preview_yes_no =params[8];display_parameter_yes_no = params[9]; filename = params[10] + ".csv"  #settings

    ## append _i to filename if path already exists -> if overwrite is NOT specified
    if not params[11]:
        filename = filenameduplicate(filename)


    ## run the simulation: (data-flow:) py -> c -> exe -> py ->plt
    os.system(f"PYTHONPATH=src python3.10 src/simulation/pipe_param_V06_def.py {path} {Plot_preview_yes_no} ")
    os.system(f"gcc src/simulation/heat_propagation_V03_def.c")
    os.system(f"./a.out {rho} {Cp} {q} {T_initial} {r} {delta_r} {k_mat} output/{filename}")
    os.system(f"PYTHONPATH=src python3.10 src/visualisation/visualisation_V01_def.py {path} {display_parameter_yes_no} {r} output/{filename}")

##-------------------------------------- Call dispUI_andRun, ask for repetition -> repeat or end ----------------------##
def simulate(comanlineargs):
    '''
    What does this function do?
        Short: executes dispUI_andRun() function and asks for "resimulation

    Input: 
       Comand line arguments
        
    Return: 
        (0)
        Executes simulation (again) and asks for repetition if desired, otherwhise returns 0 
    '''
    try:
        filename = comanlineargs[1]
    except:
        filename = 0
    dispUI_andRun(filename)
    print(
        "\n\nThank you for using this simulation",
        "\n---------------------------------------------------------\nGeothermal Heat pump Simulation® \nby: Jan Zgraggen \nVersion: V04_def \nLatest update: 15.12.2022  \nEPFL - Computational Methods and Tools - Autumn Semester 2022 \n"
    )
    
    return 0

##-------------------------------------- Main - Execution -------------------------------------------------------------##
simulate(sys.argv)

##-------------------------------------- End of script ----------------------------------------------------------------##
