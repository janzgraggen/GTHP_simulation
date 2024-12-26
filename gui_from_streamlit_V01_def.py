##-------------------------------------- Description ------------------------------------------------------------------##
'''
EPFL - Environmental Sciences and Engineering 
Semester: BA3 - Autumn 22
course: ENG-270 Computational Methods and Tools
Teacher: Satoshi Takahama
Student: Jan Zgraggen 

Filename: "gui_from_streamlit_V01_def.py"
File-Purpose:
    uses streamlit library in order to get parameter inputs with a GUI
    Writes GUI inputs to file for further use
    Terminates GUI proces such that the GTHP_simulation_VO4_def.py file can continue to wite comands via os.system to the terminal.
Reference: https://streamlit.io
'''

##-------------------------------------- Import libraries -------------------------------------------------------------##
import os as os
import sys as sys
import streamlit as st #Reference: https://streamlit.io

##-------------------------------------- Import Segment Parametrisations ----------------------------------------------##
from path_parameters_V02_def import path1 as p1
from path_parameters_V02_def import path2 as p2
from path_parameters_V02_def import path3 as p3
from path_parameters_V02_def import path4 as p4
from path_parameters_V02_def import path5 as p5
from path_parameters_V02_def import path6 as p6

#*-------------------------------------- GUI with streamlit -----------------------------------------------------------##
def get_param_from_GUI():
    '''
    What does this function do?
        Short:  this function uses the library streamlit in order to create an GUI where parameters for this simulation can be specified

    Input:
        None
    Return: 
        Tuples of the parameters specified in the GUI
    '''
    ## create a title for the GUI 
    st.title('Geothermal Heat Pump Simulation')
    
    #Choose Path (Boxes to tick)
    st.header('Path selection')
    path_choice = st.radio("Select desired path:",(p1.Parameters.name, p2.Parameters.name, p3.Parameters.name, p4.Parameters.name, p5.Parameters.name,p6.Parameters.name))
    if path_choice == p1.Parameters.name:
        path = 1
    if path_choice == p2.Parameters.name:
        path = 2
    if path_choice == p3.Parameters.name:
        path = 3
    if path_choice == p4.Parameters.name:
        path = 4
    if path_choice == p5.Parameters.name:
        path = 5
    if path_choice == p6.Parameters.name:
        path = 6
    
    # create a title for the fluid paramertisation
    st.header('Fluid Parametrisation')

    # Choose Fluid Parameters (text input)
    rho = st.text_input('Density rho =',value=1000)
    Cp = st.text_input('Heat capacity Cp =',value=4100)
    q = st.text_input('Flow rate Q =',value="1")
    T_initial = st.text_input('Initial temperature =',value= "10")

    #create a title for the pipe paramertisation
    st.header('Pipe Parametrisation')

    # Choose pipe parameters: (text input)
    r = st.text_input('Pipe radius r =',value="0.1")
    delta_r = st.text_input('Pipe thicknes =',value="0.01")
    k_mat = st.text_input('Heat conductivity of the material k_mat =',value="110")

    st.header('Execute simulation')
    ## choose if want preview plot:
    path_preview = st.checkbox('Preview path', value= False)
    if path_preview == True:
        pathpreview= 1
    else:
        pathpreview = 0
    ## chose if want to show parameters on plot
    show_param = st.checkbox('Show patameters in Graph', value= True)
    if show_param == True:
        graph_w_param = 1
    else:
        graph_w_param = 0
    
    result_filename = st.text_input('Save the result-file under the following filename [do not specify format]:',value="resultfile")
    overwrite_if_exist= st.checkbox('Overwrite if filename exists in "root" folder', value= True)

    ## if defined everything and pressed "simulate" return the parameters that have been set:
    
    #Note:  For every adjustement made, a running stremlit script instantly returns the values. 
    #       To get the return we want, at the time we wand I introduced the following if statemet structure that only returns the values declared,
    #       once the button "simulate" is pressesd.
    
    go = False
    go = st.button('Simulate')
    if go:
        return ([path]) ,(rho,Cp,q,T_initial),(r,delta_r,k_mat),(pathpreview, graph_w_param, result_filename,overwrite_if_exist)
        
##-------------------------------------- Function to write generated data to csv file ---------------------------------##
def writeToFile(filename,parameter):
    '''
    What does this function do?
        Short:  This function writes the parameters returned by get_param_from_GUI() into the rows of a file

    Input:
        filename =      string how the file should be named
        parameter =     tuple of tuples with parameters of format: ( (path-properties), (fluid-properties),(pipe-parameters),(setting-parameters) )

    Return: 
        0
        (creates: csv file with mentioned data)
    '''
    with open(filename, "w") as file:
        for i in range(0,len(parameter)):
            for j in range(0,len(parameter[i])):
                file.write(f'{parameter[i][j]}\n')
    return 0

##-------------------------------------- Function to collect data from streamlit GUI ----------------------------------##
def collect_param_form_GUI():
    '''
    What does this function do?
        Short: calls get_parameter_from_GUI 
               Writes retrieved Data to file
               Terminates the current proces (streamlit run) -> shuts down the GUI

    Input:
        None
    
    Return:
        (0)
        Creates file with parameters

    '''
    parameter =  (get_param_from_GUI()) 
    
    #if structutre neded as get_param_from_GUI returns None for each adjustement made in the GUI if its running
    if parameter:
        writeToFile("GUI_parameter.csv", parameter)
        '''
        streamlit run terminates only by sending ctrl-C to the terminal: 
        os.kill(process, signal) alows to send ctrl.C as a signal (signal) via terminal comand line
        
        the signal SIGINT  (interrupt) is sent by the signal specifier 2
        the process id is obtained by os.getpid()
        
        References:
        https://www.geeksforgeeks.org/python-os-getpid-method/
        https://bytes.com/topic/python/answers/474006-sending-ctrl-c-program
        https://unix.stackexchange.com/questions/317492/list-of-kill-signals
        '''
        os.kill(os.getpid(),2)   
    return 0

##-------------------------------------- MAIN-EXECUTION ---------------------------------------------------------------##
collect_param_form_GUI()

##-------------------------------------- End of script ----------------------------------------------------------------##



