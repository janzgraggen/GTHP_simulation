##-------------------------------------- Description -----------------------------------------------------------------##
'''
EPFL - Environmental Sciences and Engineering 
Semester: BA3 - Autumn 22
course: ENG-270 Computational Methods and Tools
Teacher: Satoshi Takahama
Student: Jan Zgraggen 

Filename: "visualisation_V01_def.py"
File-Purpose:
    reads in file with calculated data
    Generates a graphic that visualizes the obtained calculation where the Temperature is shown by color
'''

##-------------------------------------- Import libraries -------------------------------------------------------------##
import matplotlib.pyplot as plt
import sys as sys
import os as os

##-------------------------------------- Import Segment Parametrisations for path name recupreation---------------------##
from input.path_parameters_V02_def import path1 as p1
from input.path_parameters_V02_def import path2 as p2
from input.path_parameters_V02_def import path3 as p3
from input.path_parameters_V02_def import path4 as p4
from input.path_parameters_V02_def import path5 as p5
from input.path_parameters_V02_def import path6 as p6

##-------------------------------------- Import Path name for printing it on the Figure --------------------------------##
from simulation.pipe_param_V06_def import select_path
NAME = select_path(sys.argv,p1,p2,p3,p4,p5,p6)[3]

##-------------------------------------- header-reader function --------------------------------------------------------##
def read_param_header(line):
    '''
    What does this function do?
        Short:  Takes in a string of type: "text : number" and returns the number as a float

    Input: 
        line = string of format "text : number"
        
    Return: 
        value = float of converted number
    '''
    value = float((line).split(":")[1] ) 
    return value

##-------------------------------------- line-reader function ----------------------------------------------------------##
def getdata_from_dataline(line):
    '''
    What does this function do?
        Short:  Takes in a string of type: "number;number;number;number;number" and returns the numbers in a tuple

    Input: 
        line = string of format "number; number; number; number; number"
        
    Return: 
        number_tuple = tuple of numbers in the string converted to float type
    '''
    str_values = (line).split(";")
    number_tuple = ([float(str_values[i]) for i in range(len(str_values))])
    return number_tuple

##-------------------------------------- Read-in function --------------------------------------------------------------##
def read_data(filename):
    '''
    What does this function do?
        Short:  reads in the csv file gennerated by the previous steps: 
                First: 12 headerlines -> read parameters
                Second: Datalines of format P;X;Z:Tsoil;Tfluid

    Input: 
        filename: name of csv file
        
    Return: 
        x= list of x cordinates
        z= list of z cordinates
        T= list of T values for each cordinate pair
        fluid = class with stored parameters as class atribites
        pipe = class with stored parameters as class atributes
    '''

    # create classes to store parameters
    class fluid():
        rho: float
        Cp: float
        q: float
        Ti: float
    class pipe():
        r: float
        delta_r:float
        k_mat: float
        N: float
        L: float
        delta_L: float

    #create lists to store data
    x = []
    z = []
    T = []    

    # read in file
    with open(filename, "r") as file:
        
        # read header lines (fluid parameters)
        file.readline() # reads header title (no need to save)
        fluid.rho = read_param_header(file.readline())
        fluid.Cp = read_param_header(file.readline())
        fluid.q = read_param_header(file.readline())
        fluid.Ti = read_param_header(file.readline())

        # read header lines (pipe parameters)
        file.readline() # reeds header title (no need to save)
        pipe.r = read_param_header(file.readline())
        pipe.delta_r = read_param_header(file.readline())
        pipe.k_mat = read_param_header(file.readline())
        pipe.N = read_param_header(file.readline())
        pipe.L =read_param_header(file.readline())
        pipe.delta_L = read_param_header(file.readline())
        
        # read in data
        for row in file:
            linedata = getdata_from_dataline(row)
            x.append(linedata[1])
            z.append(linedata[2])
            T.append(linedata[4])
    return fluid, pipe, x,z,T
    
##-------------------------------------- Plotting function -------------------------------------------------------------##
def plotdata(datatuple,path_name,display_parameters: bool,pipe_radius):
    '''
    What does this function do?
        Short:  takes in parameters and x,z,T values in a tuple and plots x,z coords and T as colors, displays parameter information

    Input: 
        (datatuple)
            x= list of x cordinates
            z= list of z cordinates
            T= list of T values for each cordinate pair
            fluid = class with stored parameters as class atribites
            pipe = class with stored parameters as class atributes
        pathname: Name of the "drawn" path
        display_parameters(bool): boolean
        pipe_radius: string that contains the value of the inner radius of the pipe

    Return: 
        (0)
        Shows:
            Graphic with ploted data and information
    '''

    #unwrap datatuple
    fluid, pipe,x,z,T = datatuple

    #get Final temperature
    T_final = round(T[len(T)-1],1)
    #plot found data in a graphic
    #create figure:
    fig = plt.figure("GTHP Visualisation")
    legend = (f"T_final: {T_final} [°C]\n\nFluid parameters:\nCp: {fluid.Cp} [J/K]\nrho: {fluid.rho} [kg/m^3]\nq: {fluid.q} [m^3/s]\nTi: {fluid.Ti} [°C]\n\nPipe parameters:\nr: {pipe.r} [m]\nthickness: {pipe.delta_r} [m]\nk_mat: {pipe.k_mat} [W/(mK)]\nlength= {pipe.L} [m]")
    # Expecting a max loss of 5°C and a max gain of 20°C (For the color range)-> what is out of the range can be seen form the shown value.
    plt.scatter(x,z,c=T,cmap="RdYlBu_r",s=pipe_radius, vmin=int((fluid.Ti-5)) ,vmax= int((fluid.Ti+20)))
    plt.suptitle('Geothermal Heat pump simulation', x= 0.12, fontsize=14, fontweight='bold', ha ='left' ,va = 'top')
    plt.title(f"Pipe type: {path_name}",loc='left')
    plt.ylabel("Soil depth [m]")
    plt.colorbar(label= "Fluid Temperature [°C]")

    if display_parameters:
        #calculate boundary values of figure
        x_max = max(x)
        x_min = min(x)
        x_span = x_max-x_min
        z_min = min(z)
        #create whitespace inside of fiure on the right (1/4 of horizontal space that the graph takes up)
        plt.scatter((x_max + (x_span/3)),0,s=None,c="white")
        #add parameter information to that whitespace 
        plt.text((x_max+(2*(pipe.r))),z_min,legend,ha='left', wrap=True, va= "bottom")
    
    plt.show() 
    return 0

##-------------------------------------- MAIN-EXECUTION ----------------------------------------------------------------##
plotdata(read_data(sys.argv[4]),NAME,int(sys.argv[2]),float(sys.argv[3]))

##-------------------------------------- End of script -----------------------------------------------------------------##