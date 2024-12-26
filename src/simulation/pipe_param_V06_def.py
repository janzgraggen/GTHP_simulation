##-------------------------------------- Description -----------------------------------------------------------------##
'''
EPFL - Environmental Sciences and Engineering 
Semester: BA3 - Autumn 22
course: ENG-270 Computational Methods and Tools
Teacher: Satoshi Takahama
Student: Jan Zgraggen 

Filename: "pipe_param_V06_def.py"
File-Purpose:
    import path-classes form: "path_parameters_V02_def.py"
    Uses given data to generate equidistand coordinates (x,z) along the specified path
    Information about which path to choose is passed by conmand line arguments
    A graphic with a preview of the drawn path is returned if correct specifier is passed by comand line arguments
    These coordinates are written to a csv file along with a header that contains informations about the parameters
'''

##-------------------------------------- Import libraries -------------------------------------------------------------##
import numpy as np
import math as m
import matplotlib.pyplot as plt
import sys as sys
import os as os

##-------------------------------------- Import Segment Parametrisations ----------------------------------------------##
from input.path_parameters_V02_def import path1 as p1
from input.path_parameters_V02_def import path2 as p2
from input.path_parameters_V02_def import path3 as p3
from input.path_parameters_V02_def import path4 as p4
from input.path_parameters_V02_def import path5 as p5
from input.path_parameters_V02_def import path6 as p6

##-------------------------------------- Import Boundary & Increments -------------------------------------------------##
## arbitraty small increment (used to "shift" away form zero to avoid div by 0 error, where needed)
INCR = 0.001 

##-------------------------------------- Select path-------------------------------------------------------------------##
def select_path(comandline_args,path1,path2,path3,path4,path5,path6):
    '''
    What does this function do?
        Short:  Takes in command line arguments (needs 1) that serves as specifier, as a function of which the Pre-"imported" path is selected

    Input: 
    (path options)
        path1 =     list of segments of path 1
        path2 =     list of segments of path 1
        path3 =     list of segments of path 1
        
    Return: 
        pathi (= selected path)
    '''

    if int(comandline_args[1]) == 1:
        return ([path1.Segment1,path1.Segment2,path1.Segment3], path1.Parameters.DELTA_L, path1.Parameters.P_0, path1.Parameters.name)
    elif int(comandline_args[1]) == 2:
        return ([path2.Segment1,path2.Segment2,path2.Segment3], path2.Parameters.DELTA_L, path2.Parameters.P_0, path2.Parameters.name)
    elif int(comandline_args[1]) == 3:
        return ([path3.Segment1,path3.Segment2,path3.Segment3,path3.Segment4], path3.Parameters.DELTA_L, path3.Parameters.P_0, path3.Parameters.name)
    elif int(comandline_args[1]) == 4:
        return ([path4.Segment1,path4.Segment2,path4.Segment3], path4.Parameters.DELTA_L, path4.Parameters.P_0, path4.Parameters.name)
    elif int(comandline_args[1]) == 5:
        return ([path5.Segment1,path5.Segment2,path5.Segment3], path5.Parameters.DELTA_L, path5.Parameters.P_0, path5.Parameters.name)
    elif int(comandline_args[1]) == 6:
        return ([path6.Segment1,path6.Segment2,path6.Segment3], path6.Parameters.DELTA_L, path6.Parameters.P_0, path6.Parameters.name)
    else:
        print(" ERROR: Path specifier incorrece")
        sys.exit()
    

##-------------------------------------- Definition of Numerical Derrivative funcion ----------------------------------##
def num_deriv( function, value, delta_var):
    '''
    What does this function do?
        Short:  This function evaluated the numerical derrivative of a function at a given value
        
        Method: Numerical deriviation: f'(x) =  (f(x+dx)-f(x))/dx 

    Input:
        function:   function of which numerical derrivative should be evaluated
        value:      value where the numerical derrivative should be evaluated
        delta_var:  increment of over which small intervall the derrivative approx should be carried out

    Return: 
        Numerical terrivative at value
    '''
    return (function(value+delta_var) - function(value) ) / delta_var

##-------------------------------------- Numerical integration to find eqidistant points along path -------------------##
def path_integr(segment, initial_point_tuple,delta_L):
    '''
    What does this function do?
        Short:  This function takes in the Parametrision of a curvesegment in R2 and 
                returns the coordinates of equidistant points along that segment
                in two separate list aswell as the coordinates of the last point
        
        Method: Numerical integration of the path by P(i) = P(i-1) + d/dt * gamma(t) * dl/dt * dl

    Input:
    (from segm)
        gamma_1:                    gamma(t) is the parametrisation for the functuon that mapps the interval [0,t] to R2:   This is: gamma(t) = |gamma_1(t)|
        gamma_2:                                                                                                                                |gamma_2(t)|
        
        segment_len                 lenght: this is the desired arclengh that the engeneer asigns to the curve parametrized by gamma
        
        inf_gamma_1=0               inverse function of either gamma_1 or gamma_2 (there is only one needed) 
        (or!!)                      used to reverseengineer the t value after each step in order to find the INCONSTANT (retarded) incerment in t
        inf_gamma_2           
    (other)
        delta_L:                    size of the increment along the path, = distance between the datapoints       
        
        initial_point_tuple         coordinates of where the segment should start      

    Return:
        array of x coords
        array of y coords
        last Point (x,y) of this array
    '''

    ## retrieve parametrisations from segment
    #–––––
    segment_len = segment.len
    gamma_1 = segment.x
    gamma_2 = segment.z
    ## retrieve an inverse function (need to have given at least 1 inverse)
    check_next = True
    if segment.x_inv:
        inv = segment.x_inv #-> if inv of param 1 is specified -> take it store in inv
        inv_specifier = 0 #-> store specifier = 0 (will refere to row where x values are stored) 
        check_next= False
    #if inv to param #1 not given: idem for #2
    if check_next and segment.z_inv:
        inv = segment.z_inv
        inv_specifier = 1
        check_next= False
    #if both not given: error -> no inverse specified
    if check_next:
        print("ERROR: no inverse specified!")
        return None
    #–––––
    
    # Numerical integration
    #–––––
    ## calculate steps needed to reach segment length ( how many times do I have to sum up delta_L to reach the lenght of the pipe) ;given: N* delta_L = segment length
    n_steps= int(segment_len/delta_L)
    
    #create a 2xN matrix to fill up with values 
    coords_array = np.zeros(2*n_steps)
    coords_array = coords_array.reshape((2,n_steps)) # the first row servers as a place holder where the x values are stored and the second row serves as a placeholder for the z walues

    # SET initial Point -> if want to start somewhere else than at (0,0)
    coords_array[:,0]= initial_point_tuple

    # initialize t to 0
    t = 0 
    #integration
    for i in range(1,n_steps):
        # store old t value, before changing it -> permits to calculate delta_t (retarded)(*) = t[step i] -t[step(i-1)] 
        t_previous_step = t                        

        #to avoid a division by ZERO the folowing special case has to be treated: 
        '''
        WHY?
        if we start with (0,0) the reverse engineerd t will be 0
        equally the t intervall that is mapped with the function gamma is initioated at 0
        this will lead to a delta_t of 0 -> as we are numerically differating we devide by 0     
        to fix this we randomly asing a small increment to t to ofset it from T
        '''                                                                   
        if t == 0 and (coords_array[0,0]== 0 or coords_array[1,0]==0) :           
            t = INCR                                                       
    
        else:
            ## reverse engineer t form the value before in x or y (determinded by specifier) using the inverse function of gamma_i 
            t = inv(coords_array[inv_specifier,(i-1)]) 
            
        #calculate (retarded) increment on the t-intervall
        '''
        (*)Note that dt for each step is calculated by t[step (i)] - t[step i-1], 
        As there is no means of getting t[step (i)] from the numerical integration,
        we calculate delta t by t[step (i-1)] - t[step i-2].
        As the increments are very small w.r.t to the lenght and 
        as the curvature is changing by very little between two "infinitesimally" close points Points, 
        taking the "retarded"(from one step earlier as supposed to) is good enough as approximation
        '''
        delta_t = t - t_previous_step 
        

        ## calculate derivative of gamma 1 and gamma 2 at t..
        gamma_1_prime = num_deriv(gamma_1,t,delta_t)
        gamma_2_prime = num_deriv(gamma_2,t,delta_t)

        
        ## derived formula for adjustement factor: dl/dt (when non constant path)
        if (num_deriv(gamma_1,t,delta_t) or num_deriv(gamma_2,t,delta_t)):
            dt_over_dl = 1 / ( m.sqrt((num_deriv(gamma_1,t,delta_t))**2 + (num_deriv(gamma_2,t,delta_t))**2))
        
        # if path is constant in x or z: dt/dL falls to deltaT/deltaL as deltaL is a linear segment in that case
        else:
            dt_over_dl = delta_t/delta_L
        
        
        ## derived formula for the numerical integration - using the adjustment factor
        coords_array[0,i]= coords_array[0,i-1]+ gamma_1_prime* dt_over_dl * delta_L # x coordinate of new point
        coords_array[1,i]= coords_array[1,i-1] + gamma_2_prime * dt_over_dl * delta_L # y coordinate of new point

        ##check if the increments along the created path are constatn and of size DELTA_L
        if (coords_array[0,i] - coords_array[0,i-1])**2 + (coords_array[1,i] - coords_array[1,i-1])**2 - delta_L**2 > 10**(-15):
            print("WARNING: incremet has NOT size DELTA_L, precistion = 10**(-15)")
            
    #–––––
    ## return: x-coords , y-coords, tuple of coords of last points, 
    return coords_array[0,:] , coords_array[1,:] , (coords_array[0,n_steps-1],coords_array[1,n_steps-1]) 

##-------------------------------------- Function to fuse generated segment coordinates -------------------------------##
def fuse_segments(segmentlist,P_initial, delta_L):
    '''
    What does this function do?
        Short:  This function thakes a list of the segment classes, calls the path_integr for each segment, and fuses the 
                extracted coords, in order to create arrays of x and z coordinates over the whole path.
                The length of the pipe and the number of datapoints are also calculated
        
        Method: calling path_integr in a loop over the number of segments

    Input:
        segmentlist:   list of segment classes
        delta_L:       size of the increment along the path, = distance between the datapoints       
        P_initial      tuple ofcoordinates of where the path should start      

    Return: 
        x_path:         array of x coordinates of equidistant points along path
        z_path:         array of z coordinates of equidistant points along path
        L_tot_path      total lenght of the path
        N               number of datapoints


    '''
    #retieve the number of segments over the lenght of the segment list
    nrofsegments = len(segmentlist)
    #create empty arrays to fill with coordinates
    x_path= np.array([])
    z_path= np.array([])
    L_tot_path = 0
    
    #iterate over the segments to fill the coordinate arrays
    for i in range(nrofsegments):
        #For the first segment we have to take the given Initial point as the segment starting point
        if i == 0:
            x,z,last_cords= path_integr(segmentlist[i],P_initial,delta_L)
        #For all other points the last_cordinates of the segments before is the segment starting points (->connecting the segments)
        else:
            x,z,last_cords= path_integr(segmentlist[i],last_cords,delta_L)
        L_tot_path += (segmentlist[i]).len
        x_path = np.append(x_path,x)
        z_path = np.append(z_path,z)
    #calculates the number of datapoints in x and z (faster than w/ len):
    n = int( L_tot_path/delta_L) 

    
    return x_path, z_path, n

##-------------------------------------- Function to plot the created path --------------------------------------------##
def plot_pipe(x,z):
    '''
    What does this function do?
        Short:  This function plots the obtained path
        
        Method: plot using mathplotlib.pyplot library

    Input:
        x = x coordinates of points along pipe
        z = z coordinates of points aling pipe

    Return: 
        mathplotlib.pyplot plot of path of the pipe
    '''
    fig = plt.figure("Path Preview")
    plt.plot(x,z,marker='')
    plt.suptitle('Geothermal Heat pump simulation', fontsize=14)
    plt.title("Path Preview")
    plt.ylabel("Soil depth [m]")
    
    return plt.show()

##-------------------------------------- Function to write generated data to csv file ---------------------------------##
def writeToFile(filename,x,z,delta_L,N):
    '''
    What does this function do?
        Short:  This function writes the data of a "x" and a "y" array into columns of a csv file called filename
                Additionaly It writes information about the length and the increment into 2 headerlines
        
        Method: fileIO

    Input:
        filename =      string how the file should be named
        x =             1D array
        z =             1D array
        deltaL =        Size of the increment in L 
        N =             Lenght of the pipe
    Return: 
        0
        (creates: csv file with mentioned data)
    '''
    with open(filename, "w") as file:
        file.write(f'Delta_L={delta_L}\nTotalPoints={N}\n')
        for i in range(0,N):
            file.write(f'{x[i]};{z[i]}\n')
    return 0

##-------------------------------------- Funct to do calculations and write results to file (and plot if specified)----##
def execute(filename,path,ifPreview_SetTo1: bool):
    '''
    What does this function do?
        Short:  This function calls the functions fuse_segments, plotpipe(if desired) and writeToFile

    Input:
        filename =          string how the file should be named

    (from path (tuple) = return of select_path function)
        segmentlist =       list of segment classes
        delta_L =           size of the increment along the path, = distance between the datapoints       
        P_initial =         tuple ofcoordinates of where the path should start    

        ifPreview_SetTo1 =  bool, if set true-> plots

    Return: 
        calls fuse_segments/plot_pipe/writeToFile
    '''
    segmentlist = path[0]
    delta_L = path[1]
    P_initial = path[2]

    
    ## create (x,z) coordinates of path
    x,z ,N = fuse_segments(segmentlist,P_initial,delta_L)
    #if want preview: plotpath
    if ifPreview_SetTo1 == 1:
        plot_pipe(x,z)
    ## write data to csv file named "xz_coords.csv"
    writeToFile(filename,x,z,delta_L,N)
    return 0 

##--------------------------------------- MAIN - Execution ------------------------------------------------------------##
## this statement needed as recalling this file when importiong to "visualisation_V01_def.py"
if sys.argv[0] == "src/simulation/pipe_param_V06_def.py":
    PATH = select_path(sys.argv,p1,p2,p3,p4,p5,p6)
    execute("data/xz_coords.csv",PATH,int(sys.argv[2])) 

    
##-------------------------------------- End of script ----------------------------------------------------------------##