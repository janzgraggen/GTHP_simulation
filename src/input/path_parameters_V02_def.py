##-------------------------------------- Description -----------------------------------------------------------------##
'''
EPFL - Environmental Sciences and Engineering 
Semester: BA3 - Autumn 22
course: ENG-270 Computational Methods and Tools
Teacher: Satoshi Takahama
Student: Jan Zgraggen 

Filename: "path_parameters_V02_def.py"
File-Purpose:
    Contains Classes of Paths:
    These Paths are hard coded and meant to give the user an overview of the possibilities of the simulation
    Note:
        -If requested paths can be modified. 
        -The addition of paths is possible but reqires minor adjustement of the code 
         (e.g additional import). It is therefore not intended to be done within the scope of the product of this project.

    Classes of paths contain (1x) Class of Parameters, (Nx) Classes of segments
    The content of the Segment classes specifies the functions and lenght used to "draw" the curve part by part
    The content of the Parameter Segmentation specifies name, interpunctual distance and initial point.
'''

##-------------------------------------- Import libraries ---------------------------------------------------------------------------##
import math as m

##----------------------------------- Path Parametrisations -------------------------------------------------------------------------##

##----------------------------------- Path 1 ----------------------------------------------------------------------------------------##
class path1:
    ##------------------------------------ PARAMETERS ---------------------------------------##
    class Parameters:
        name = "Demo: parabolic-sin-parabolic"
        DELTA_L= 0.01 #unit:[meters]
        P_0 = (0,0) ## initial point
    ##------------------------------------ 1ST Segment ---------------------------------------##
    class Segment1:

        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return  -(t**2)

        def x_inv(s):
            #returns the inverse funcion of gamma1
            return  m.sqrt(abs(s))

        def z(t):
            #parametisation (first entry)
            #returns function 
            return   -t

        def z_inv(s):
            #returns the inverse funcion of gamma2
            return  -s

    ##------------------------------------ 2ND Segment ---------------------------------------##
    class Segment2:
        
        len = 20*m.pi

        def x(t):
            #parametisation (first entry)
            #returns function 
            return -t

        def x_inv(s):
            #returns the inverse funcion of gamma1
            return -s

        def z(t):
            #parametisation (first entry)
            #returns function 
            return  m.sin(t)/8

        z_inv = 0 # no inverse given for z-parametisation

        
    ##------------------------------------ 3RD Segment ---------------------------------------##
    class Segment3:
        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return (t**2)

        x_inv = 0 #  no inverse given for x-parametisation

        def z(t):
            #parametisation (first entry)
            #returns function 
            return t

        def z_inv(s):
            #returns the inverse funcion of gamma1
            return s

    ##------------------------------------ 4RD Segment ---------------------------------------##
    class Segment4:
        len = 1

        def x(t):
            #parametisation (first entry)
            #returns function 
            return 

        def x_inv(s):
            #returns the inverse funcion of gamma1 or 0
            return 

        def z(t):
            #parametisation (first entry)
            #returns function 
            return 
            
        def z_inv(s):
            #returns the inverse funcion of gamma2 or 0
            return 

##----------------------------------- Path 2 ----------------------------------------------------------------------------------------##
class path2:
    ##------------------------------------ PARAMETERS ---------------------------------------##
    class Parameters:
        name = "Demo: triangle"
        DELTA_L= 0.1 #unit:[meters]
        P_0 = (30,0) ## initial point
    ##------------------------------------ 1ST Segment ---------------------------------------##
    class Segment1:

        len = m.sqrt(2)*50

        def x(t):
            #parametisation (first entry)
            #returns function 
            return  t

        x_inv = 0

        def z(t):
            #parametisation (first entry)
            #returns function 
            return   -t

        def z_inv(s):
            #returns the inverse funcion of gamma2
            return  -s

    ##------------------------------------ 2ND Segment ---------------------------------------##
    class Segment2:
        
        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return -t

        def x_inv(s):
            #returns the inverse funcion of gamma1
            return -s

        def z(t):
            #parametisation (first entry)
            #returns function 
            return  -50

        z_inv = 0 # no inverse given for z-parametisation

        
    ##------------------------------------ 3RD Segment ---------------------------------------##
    class Segment3:
        len = m.sqrt(2)*50

        def x(t):
            #parametisation (first entry)
            #returns function 
            return t

        x_inv = 0 #  no inverse given for x-parametisation

        def z(t):
            #parametisation (first entry)
            #returns function 
            return t

        def z_inv(s):
            #returns the inverse funcion of gamma1
            return s

##----------------------------------- Path 3 ----------------------------------------------------------------------------------------##
class path3:
    ##------------------------------------ PARAMETERS ---------------------------------------##
    class Parameters:
        name = "Demo: square (100mx100m)"
        DELTA_L= 0.01 #unit:[meters]
        P_0 = (0,0) ## initial point
    ##------------------------------------ 1ST Segment ---------------------------------------##
    class Segment1:

        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return  0*t

        x_inv = 0

        def z(t):
            #parametisation (first entry)
            #returns function 
            return   -t

        def z_inv(s):
            #returns the inverse funcion of gamma2
            return  -s

    ##------------------------------------ 2ND Segment ---------------------------------------##
    class Segment2:
        
        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return -t

        def x_inv(s):
            #returns the inverse funcion of gamma1
            return -s

        def z(t):
            #parametisation (first entry)
            #returns function 
            return  -50

        z_inv = 0 # no inverse given for z-parametisation

        
    ##------------------------------------ 3RD Segment ---------------------------------------##
    class Segment3:
        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return -50

        x_inv = 0 #  no inverse given for x-parametisation

        def z(t):
            #parametisation (first entry)
            #returns function 
            return t

        def z_inv(s):
            #returns the inverse funcion of gamma1
            return s

    ##------------------------------------ 4RD Segment ---------------------------------------##
    class Segment4:
        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return t

        def x_inv(s):
            #returns the inverse funcion of gamma1 or 0
            return s

        def z(t):
            #parametisation (first entry)
            #returns function 
            return 0
            
        z_inv = 0

##----------------------------------- Path 4 ----------------------------------------------------------------------------------------##
class path4:
    ##------------------------------------ PARAMETERS ---------------------------------------##
    class Parameters:
        name = "straight-sin(high-freq)-straight"
        DELTA_L= 0.01 #unit:[meters]
        P_0 = (0,0) ## initial point
    ##------------------------------------ 1ST Segment ---------------------------------------##
    class Segment1:

        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return  0*t

        x_inv = 0

        def z(t):
            #parametisation (first entry)
            #returns function 
            return   -t

        def z_inv(s):
            #returns the inverse funcion of gamma2
            return  -s

    ##------------------------------------ 2ND Segment ---------------------------------------##
    class Segment2:
        
        len = 1240

        def x(t):
            #parametisation (first entry)
            #returns function 
            return -t

        def x_inv(s):
            #returns the inverse funcion of gamma1
            return -s

        def z(t):
            #parametisation (first entry)
            #returns function 
            return  -20*m.sin(3*m.pi*t)

        z_inv = 0 # no inverse given for z-parametisation

        
    ##------------------------------------ 3RD Segment ---------------------------------------##
    class Segment3:
        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return 0 # no change in x -> constant
            

        x_inv = 0 #  no inverse given for x-parametisation

        def z(t):
            #parametisation (first entry)
            #returns function 
            return t

        def z_inv(s):
            #returns the inverse funcion of gamma1
            return s


##----------------------------------- Path 5 ----------------------------------------------------------------------------------------##
class path5:
    ##------------------------------------ PARAMETERS ---------------------------------------##
    class Parameters:
        name = "straight-sin(high-freq)-straight (shallow)"
        DELTA_L= 0.01 #unit:[meters]
        P_0 = (0,0) ## initial point
    ##------------------------------------ 1ST Segment ---------------------------------------##
    class Segment1:

        len = 30

        def x(t):
            #parametisation (first entry)
            #returns function 
            return  0*t

        x_inv = 0

        def z(t):
            #parametisation (first entry)
            #returns function 
            return   -t

        def z_inv(s):
            #returns the inverse funcion of gamma2
            return  -s

    ##------------------------------------ 2ND Segment ---------------------------------------##
    class Segment2:
        
        len = 1240

        def x(t):
            #parametisation (first entry)
            #returns function 
            return -t

        def x_inv(s):
            #returns the inverse funcion of gamma1
            return -s

        def z(t):
            #parametisation (first entry)
            #returns function 
            return  -20*m.sin(3*m.pi*t)

        z_inv = 0 # no inverse given for z-parametisation

        
    ##------------------------------------ 3RD Segment ---------------------------------------##
    class Segment3:
        len = 30

        def x(t):
            #parametisation (first entry)
            #returns function 
            return -10.4163103744
            #-41.66524149756883

        x_inv = 0 #  no inverse given for x-parametisation

        def z(t):
            #parametisation (first entry)
            #returns function 
            return t

        def z_inv(s):
            #returns the inverse funcion of gamma1
            return s


##----------------------------------- Path 6 ----------------------------------------------------------------------------------------##
class path6:
    ##------------------------------------ PARAMETERS ---------------------------------------##
    class Parameters:
        name = "straight-sin(high-freq)-straight (short)"
        DELTA_L= 0.01 #unit:[meters]
        P_0 = (0,0) ## initial point
    ##------------------------------------ 1ST Segment ---------------------------------------##
    class Segment1:

        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return  0*t

        x_inv = 0

        def z(t):
            #parametisation (first entry)
            #returns function 
            return   -t

        def z_inv(s):
            #returns the inverse funcion of gamma2
            return  -s

    ##------------------------------------ 2ND Segment ---------------------------------------##
    class Segment2:
        
        len = 600

        def x(t):
            #parametisation (first entry)
            #returns function 
            return -t

        def x_inv(s):
            #returns the inverse funcion of gamma1
            return -s

        def z(t):
            #parametisation (first entry)
            #returns function 
            return  -20*m.sin(3*m.pi*t)

        z_inv = 0 # no inverse given for z-parametisation

        
    ##------------------------------------ 3RD Segment ---------------------------------------##
    class Segment3:
        len = 100

        def x(t):
            #parametisation (first entry)
            #returns function 
            return 0 # no change in x -> constant
            

        x_inv = 0 #  no inverse given for x-parametisation

        def z(t):
            #parametisation (first entry)
            #returns function 
            return t

        def z_inv(s):
            #returns the inverse funcion of gamma1
            return s

##----------------------------------- End of script ---------------------------------------------------------------------------------##




