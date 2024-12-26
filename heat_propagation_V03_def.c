/*------------------------------------- Description ----------------------------------------------------------------*/
/*
EPFL - Environmental Sciences and Engineering 
Semester: BA3 - Autumn 22
course: ENG-270 Computational Methods and Tools
Teacher: Satoshi Takahama
Student: Jan Zgraggen 

Filename: "heat_propagation_V03_def.c"
File-Purpose: 
    Reads in coordinates and Parameters form a csv file
    assigns Soil environment temperature to coordinates 
    calculates the teperature of a flowing fluid as a function of distance along the path
    writes calculated data to csv file and passes aswell read in parameters as header to that file
*/  

/*------------------------------------- HEADER files ---------------------------------------------------------------*/
#include <stdio.h> // header file needed to use inputs and outputs of functions
#include <string.h> // string manipulation
#include <stdlib.h> // standart library
#include <math.h> // Pi,cos,sin,... etc

/*------------------------------------- Define Parameter Structures ------------------------------------------------*/
/* Pipe Propperties */
struct pipe{
// parameters to be assigned  in MAIN
    // radius of the pipe:
    double r; 
    // thickness of the pipe
    double delta_r;
    // heat conductivity of the material
    double k_mat;

//parameters assigned by reading in the datafile
    // number of datapoints along N
    int N;
    // length difference between datapoints = Increment along path = Control Volume height */
    double delta_l;
};

/* Fluid Properties */
struct fluid{
    // density rho of the fluid:
    double rho;
    // heat capacity at constant preassure Cp_fluid of the fluid:
    double Cp;
    // Flowrate q):
    double q;
    // initial Temperature T of the fluid:
    double T_initial;
};

/*------------------------------------- Define Coordinate Structure ------------------------------------------------*/
struct TempPoint{
    /*
    info: along the pipe in increments of delta_l we have defined points,
    such that the distance between the points with attributes T_soil and T_have is constant
    */

    // x coordinate of point
    double x;
    // z coordinate of point
    double z;
    // soil temperature(z) at height z(of this point)
    double T_soil;
    // temperature of fluid at this Point
    double T;
};

/*-------------------------------------(1) Reading file ------------------------------------------------------------*/
int readfile(char *filename, struct TempPoint* point, struct pipe* parameter) { // This function is inspired by the given function from the midterm. Reference: https://moodle.epfl.ch/mod/page/view.php?id=1230003
    /*
    What does this function do?
        Short:  Reading file input of file that contains:
                delta_l: increment of the parametriation, N: numbers of datapoints of the parametrisation
                x,z coordinates of equidistant points along paramentrzed curve.

    input/output
        Reads in data file called "filename" of format:
        1    Delta_L=0.01
        2    TotalLenght=4246
        3    4.23;-3.23
        4    9.20;0.332

        First 2 lines are read in separately into structaray of struct param called "parameter"
        Data is read into structarray of struct TempPoint called "point".

        Extrats the value total lenght N that was read into the struct param array "parameter"
        in order to know how many more lines there are to read in.
        Returns this value N (= number of datapoints) 
    */
    
    FILE *fid = fopen(filename, "r");
    if(fid == NULL) return -1;

    /* ------------read in first 2 lines-----------*/
    char buffer1[100];  
    // read first 2 lines seperately:
    fgets(buffer1,100,fid); //reads 1st line and stroes it into buffer   -> filepointer                            
    // note: the variable that is specified by specifier %? is stored at the given adress.
    sscanf(buffer1,"Delta_L=%lf", &(*parameter).delta_l); // takes type objects form scanable object and stores them under the specified adresses
    fgets(buffer1,100,fid); // reads 2nd line and stores it into buffer // buffer is overwritten
    sscanf(buffer1,"TotalPoints=%d", &(*parameter).N); 

    // extract lenght of dataset
    int N = (parameter[0]).N;
    
    /* ------------read in data--------------------*/
    int n=0;    
    while (fgets(buffer1, 100, fid) != NULL) { // fgets stores read line into buffer (is done for every iteration as while condition checks its termination condition)
        if(n >= (N)) break; // has already read 2 lines so there are N lines left.. -> as we have got the input of N = how many datapoints there are
        sscanf(buffer1, "%lf;%lf", &(point[n]).x,&(point[n]).z);
        n++;
    }
    return 0;
}

/*-------------------------------------(2) Attribute Soil temperature ----------------------------------------------*/
int soil_temperature(struct pipe* parameter,struct TempPoint* point){
    /*
    What does this function do?
        Attribute a soil temperature T_soil(z) to each temperature point structure,
        where the soil temperature is estimated with a linear increase model
        Model used:
        surface temperature of 15°C Increase of 0.1C per meter depth (negative z):  T(z) = 15 + 0.1* (-z) |if z<0 
        .                                                                           T(z) = 15             |if z> = 0

    Input:
        Takes pointer to structearray and pointer to parameter values as input
    Output:
        Adds the T_soil value to each TempPoint calculated form z 
    */

    //retrieves the value of the number of datapoints
    int N = (parameter[0]).N;
    
    // applies function 
    for (int i= 0;i < N; i++){
        if((point[i]).z <0){
            (point[i]).T_soil = 15.0 - 0.1 * (point[i]).z; // minus bc the z values are negative
        }else{
            (point[i]).T_soil = 15;
        }
    }
    return 0;
}

/* ------------------------------------(3) Caluclate fluid velocity ------------------------------------------------*/
double fluid_velocity(struct pipe* pipe , struct fluid * fluid){
    /*
    What does this function do?
        Calculating the fluid velocity from crossectional area and flowrate
    input:
        struct w/ properties of the pipe: 
        struct w/ properties of the fluid:

    output:
        velocity v from flowrate and crossection
    */
    double q = (fluid[0]).q;
    double r = (pipe[0]).r;
    // v = q/A , A = pi *r^2 
    double v = q/ (M_PI * r *r);
    return v;
}

/* ------------------------------------(4) Numerical Integration of heat propagation -------------------------------*/
int fluid_temperature(struct pipe* pipe, struct fluid* fluid, struct TempPoint* point){
    /*
    What does this function do?
        the goal of this function is to numerically integrate the formula for the energy balance, in order do recieve the Temperature at a distance l 
        for that we have given the heat q_in at a distance L and Parameters of the fluid and the soil aswell as the size of the increment

    input: 
        struct w/ properties of the pipe: 
        struct w/ properties of the fluid:

    In/Output:
        (5)Pointer to list of TepmeraturePoint structure: 
            this is a list where for all points allong L the values for the Q_in (heatflux into the pipe at this L) and temperature at this L are stored
            At this stage only the Q_in values have been added 
            We want to add the temperature values in the following steps.
    */

    /* (0) Retrieve the Velocity of the wather*/   
    double v = fluid_velocity(pipe,fluid);

    /* (1) Retreive the number of points to integrate over: */
    int N = (*pipe).N;

    /* (2) get expression for summarized constant terms accordinc to the formula derivation (for readability)*/
    double K = ((*pipe).k_mat * (*pipe).delta_l) / ((*fluid).rho * (*fluid).Cp * (*pipe).r * (*pipe).r * log(   ( (*pipe).r+((*pipe).delta_r)) / (*pipe).r ));

    /* (2) pass inital temperature as attribute to first point */ 
    point[0].T = (*fluid).T_initial;

    /* (3) Based on T of point O T_i = f(T_(i-1)) can now be computed with the derrived formula*/
    for (int i = 1; i < N ;i++){
        point[i].T = (point[i-1].T*(2-(K/v)) + (K/v)*(point[i].T_soil +point[i-1].T_soil))/(2 +(K/v));
    }

    return 0;
}

/* ------------------------------------(5) Writing calculated values to csv file------------------------------------*/
int createfile(char* filename,struct pipe*pipe, struct fluid *fluid, struct TempPoint* point){
    /*
    What does this function do?
        This function creates a csv file
        It writes parameter information in the header 
        It writes The data corresponding to each coordinate Point into the rows of the file.

    Input:
        filename = string that is going to name the csv file
        pipe = pointer to struct pipe; contains pipe parameters
        fluid = pointer to struct fluid; contains fluid parameters
        point = pointer to array of struct TempPonint; contains coordinates and assigned Temperatures of each point

    Output:
        (0)
        Creates csv file
    */

    // Ouvrir un fichier pour l'écrire ("w"),
    FILE * fid = fopen(filename, "w"); // creates a file at given repository or overwrites file present at repository

    // write first header line: parameters of the fluid
    fprintf(fid, "Fluid parameters:\n Density rho: %lf\n Heat Capacity Cp: %lf\n Flowrate q: %lf\n Initial Temperature Ti: %lf\n", (fluid[0]).rho, (fluid[0]).Cp,(fluid[0]).q, (fluid[0]).T_initial);

    // write second header line: parameters of the pipe
    fprintf(fid, "Pipe parameters:\n Radius: %lf\n Material Thickness: %lf\n Heat Conductivity k_mat: %lf\n Lenght: %lf\n Number of datapoints: %d\n Increment along path: %lf\n", (pipe[0]).r, (pipe[0]).delta_r,(pipe[0]).k_mat, ((pipe[0]).N*(pipe[0]).delta_l),(pipe[0]).N , (pipe[0]).delta_l);

    // write third header line: Column Titles
    //fprintf(fid, "Point# ; x ; z ; T_soil ; T_water\n");

    /* (1) Retreive the number of structure points: */
        int N = (*pipe).N;
    // write data:
    for (int i = 0; i<N; i++){
        fprintf(fid, "%d;%lf;%lf;%lf;%lf\n", (i+1), (point[i]).x, (point[i]).z, (point[i]).T_soil, (point[i]).T);
    }

    //close the file
    fclose(fid);
    return 0;
}

/*------------------------------------------ Create Fluid and Pip (from comand args) -------------------------------*/
int initiate_parameters(struct fluid*  fluid, struct pipe* pipe , char ** comandline_args){
    /*
    What does this function do?
        this function assigns comand line arguments to the 2 structures that contain parameters: struct pipe  and struct fluid

    Input/output:
        fluid = pointer to struct fluid
        pipe = pointer to struct pipe
        comandline_args = comandline arguments (type = char**)
    Output
        (0)
    */
    
    //info: comandlineargs[0] = name of program [1]= pointer to first element of comandline args

    // fluid parameters: rho Cp q T_initial
    (fluid[0]).rho = atof(comandline_args[1]);
    (fluid[0]).Cp = atof(comandline_args[2]);
    (fluid[0]).q = atof(comandline_args[3]);
    (fluid[0]).T_initial = atof(comandline_args[4]);

    // pipe parameters  r delta_r k_mat
    (pipe[0]).r = atof(comandline_args[5]);
    (pipe[0]).delta_r = atof(comandline_args[6]);
    (pipe[0]).k_mat = atof(comandline_args[7]);
    return 0;
}

/*------------------------------------------ Main Function ---------------------------------------------------------*/
int main( int argc, char *argv[] ) {
    //argc = number of command line argumnets  (including the argument to run file : e.g.a.out)
    //argv = command line argument (of type array of characters )
    //type /.a.out arg1 arg2 arg3 etc... for 'feeding' arguments via comand line

    // create fluid 
    struct fluid fluid;
    struct fluid * fl = &fluid; // pointer to fluid
    
    // create pipe
    struct pipe pipe;
    struct pipe * p = &pipe; // pointer to pipe

    // add comandline arguments to the parameter structures
    initiate_parameters(fl,p,argv);

    //initiate malloc array of struct points  
    /*
    Note: Need Malloc array as the size of the array depends on the user input and can therefore not be preallocated
    N= 1'000'000 corresponds to 10km of pipe, sizes bigger than that are not realistic, therefore not expected
    */
    struct TempPoint* datapoints= malloc(1000000 * sizeof(struct TempPoint));
    
    //read file into structarray
    readfile("xz_coords.csv",datapoints,p);

    //calculate soil temp as a function of z
    soil_temperature(p,datapoints);

    //calculate fluid temperature of the fluid at each positon point of the pipe (numerical integration)
    fluid_temperature(p,fl,datapoints);

    // write caluclated data to file
    createfile(argv[8],p,fl,datapoints);
    return 0;
}

/*------------------------------------------ End of script ---------------------------------------------------------*/