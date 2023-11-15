"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "short"
__version__ = "2023.11.14"

import rhinoscriptsyntax as rs
import math

# Define constants for G-code commands and parameters
COMMAND_MOVE = "G1"

# GCODE PARAM Names
PARAM_X = "X"
PARAM_Y = "Y"
PARAM_Z = "Z"
PARAM_E = "E"
PARAM_F = "F"

# Separates params in a command
PARAM_DELIMITER = " "

# Separates commands
COMMAND_DELIMITER = "\n"

# Formatter for param values
NUM_FORMAT = "{value:.3f}"

def is_equal_float(f1, f2, epsilon=0.0001):
    return math.fabs(f2 - f1) <= epsilon

# Returns true if all the coordinates are the same pt
def is_same_pt(pt1, pt2):
	return is_equal_float(pt1[0], pt2[0]) and is_equal_float(pt1[1], pt2[1]) and is_equal_float(pt1[2], pt2[2])

# creates a string consisting of a G1 move command and 
# any associated parameters
#You should modify your g1_move() function to have an input “should_extrude” boolean.
def  g1_move(current_pos, next_pos, feed_rate, should_extrude=False, extrude_amount=0.0):
    params = [COMMAND_MOVE]
    
    # Compare positions and see if we have to move
    if not is_same_pt(current_pos, next_pos):
        for i, param in enumerate([PARAM_X, PARAM_Y, PARAM_Z]):
            if not is_equal_float(current_pos[i], next_pos[i]):
                params.append("{}{}".format(param, NUM_FORMAT.format(value=next_pos[i])))
    
    if feed_rate is not None:
        params.append("{}{}".format(PARAM_F, NUM_FORMAT.format(value=feed_rate)))
    if should_extrude:
        params.append("{}{}".format(PARAM_E, NUM_FORMAT.format(value=extrude_amount)))
    # Make the command from the parameters
    return PARAM_DELIMITER.join(params)

#### WARNING: DO NOT EDIT THE START GCODE! #####
start_gcode_lines = [";START GCODE",
    "M73 P0 R42",
    "M73 Q0 S43",
    "M201 X1000 Y1000 Z200 E5000 ; sets maximum accelerations, mm/sec^2",
    "M203 X200 Y200 Z12 E120 ; sets maximum feedrates, mm / sec",
    "M204 S1250 T1250 ; sets acceleration (S) and retract acceleration (R), mm/sec^2",
    "M205 X8.00 Y8.00 Z0.40 E4.50 ; sets the jerk limits, mm/sec",
    "M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec",
    ";TYPE:Custom",
    "M862.3 P \"MK3S\" ; printer model check",
    "M862.1 P0.4 ; nozzle diameter check",
    "M115 U3.13.1 ; tell printer latest fw version",
    "G90 ; use absolute coordinates",
    "M83 ; extruder relative mode",
    "M104 S215 ; set extruder temp",
    "M140 S60 ; set bed temp",
    "M190 S60 ; wait for bed temp",
    "M109 S215 ; wait for extruder temp",
    "G28 W ; home all without mesh bed level",
    "G80 ; mesh bed leveling",
    "G1 Z0.2 F720",
    "G1 Y-3 F1000 ; go outside print area",
    "G92 E0",
    "G1 X60 E9 F1000 ; intro line",
    "G1 X100 E12.5 F1000 ; intro line",
    "G92 E0",
    "M221 S95",
    "; Don't change E values below. Excessive value can damage the printer.",
    "M907 E538 ; set extruder motor current",
    "G21 ; set units to millimeters",
    "G90 ; use absolute coordinates",
    "M83 ; use relative distances for extrusion",
    "M900 K0.05 ; Filament gcode LA 1.5",
    "M900 K30 ; Filament gcode LA 1.0",
    "M107"]
##### WARNING: DO NOT EDIT THE END GCODE! ######
end_gcode_lines = ["; END Gcode", 
    "M204 S1000", 
    "M107", 
    ";TYPE:Custom", 
    "; Filament-specific end gcode", 
    "G1 Z100 F720 ; Move print head further up", 
    "G1 X0 Y200 F3600 ; park", 
    "G4 ; wait",
    "M221 S100 ; reset flow",
    "M900 K0 ; reset LA",
    "M104 S0 ; turn off temperature",
    "M140 S0 ; turn off heatbed",
    "M107 ; turn off fan",
    "M84 ; disable motors"]

if not isinstance(lines, list):
    lines = [lines]
    
def generate_gcode(lines, travel_feed_rate, extrusion_feed_rate, layer_height, extrusion_width, filament_diameter):
    gcode_lines = []
    
    # Start at the origin
    current_pos = [0, 0, 0]  

    for i in range(0, len(lines)):
         # Get pts of the line segment
        start_pt = rs.CurveStartPoint(lines[i])
        end_pt = rs.CurveEndPoint(lines[i])
        
        #Calculate distance b/w the points on the line segment
        distance = rs.CurveLength(lines[i])
        
        #If current_point.Z != start_position.Z
        if end_pt[2] != start_pt[2]:
            line_z_position = g1_move(end_pt, [end_pt[0], end_pt[1], start_pt[2]], feed_rate=travel_feed_rate)
            # Append move to line_z_position to gcode_lines
            gcode_lines.append(line_z_position)
            end_pt[2] = start_pt[2]
        
        extrude_amount = calculate_extrusion(distance, layer_height, extrusion_width, filament_diameter)
       
       #If current_point != start_point
        if not is_same_pt(current_pos, start_pt):
            line_start_point = g1_move(current_pos, start_pt, feed_rate=travel_feed_rate)
            #Add move to the line_start_point to gcode_lines
            gcode_lines.append(line_start_point)
            current_pos = start_pt
            
        gcode_lines.append( g1_move(start_pt, end_pt, extrusion_feed_rate, True, extrude_amount))
        
        # Add current_point = line_end_point
        current_pos = end_pt

    return gcode_lines

def calculate_extrusion(length, layer_height, extrusion_width, filament_diameter):
    v_out = length * layer_height * extrusion_width
    radius = filament_diameter / 2.0
    filament_area = 3.14159 * (radius ** 2)
    L = v_out / filament_area
    return L
    
    
# Here's the main procedure that uses the functions above
current_point = [0,0,0] 
gcode_lines = []

gcode_lines = generate_gcode(lines, travel_feed_rate, extrusion_feed_rate, layer_height, extrusion_width, filament_diameter)

# Combine Lines - DO NOT EDIT
# These lines will put the start gcode before your gcode, and the end gcode
# after then merge them into the gcode output using a COMMAND_DELIMETER = “\n”
gcode_lines = start_gcode_lines + gcode_lines + end_gcode_lines
gcode_output = "\n".join(gcode_lines)