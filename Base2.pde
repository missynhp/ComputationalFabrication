// ExampleLSystem - contains initialization functions
// to set up parameters and init the LSystem (from the main file)

import java.util.HashMap;

// This function returns an initialized LSystem for a "Square based L-System"
LSystem initSquare() {
  // initialize turtle variables
  float moveDist = 20;
  float rotateAngle = 60;
  float scaleFactor = 1;
  
  // The intial axiom / input string
  //String axiom = "FG";
  String axiom = "F+F+F+F+F+F"; 
  
  // Create any production rules
  HashMap<Character, String> rules = new HashMap<>();
  //rules.put('F', "FF-[-FF-F]+[+F+F]+[FFF]");
  //rules.put('F', "F-F-F");
  //rules.put('-', "+");
  //rules.put('+', "-");
  //rules.put('F', "FFF-FFF-FFF");
  //rules.put('G', "GG-[-GG-G]+[+G+G]+[GGG]");
  //rules.put('G', "G-G-G");
  rules.put('F', "FF+F+F+F+FF");
    
  // Create the Lsystem
  return new LSystem(axiom, rules, moveDist, rotateAngle, scaleFactor);
}

// TODO: create your own L-System initialization functions
LSystem initDiamonds() {
  float moveDist = 30;
  float rotateAngle = 60;
  float scaleFactor = 1;
  //String axiom = "FF";
  String axiom = "F+F+F+F+F+F"; 
  HashMap<Character, String> rules = new HashMap<>();
  //rules.put('F', "FFFFF+[-FF+FFF++]-[-FF+FFF++]");
  //rules.put('+', "-");
  //rules.put('-', "+");
  rules.put('F', "FF+F++F+F");
  return new LSystem(axiom, rules, moveDist, rotateAngle, scaleFactor);
}

LSystem initSpiralMandala() {
  // Initialize turtle variables
  float moveDist = 8;
  float rotateAngle = radians(360);
  float scaleFactor = 1;
  
  // Axiom and production rules
  String axiom = "F";
  HashMap<Character, String> rules = new HashMap<>();
  rules.put('F', "FFF+FF+FF+F+");
  rules.put('+', "-");
 // rules.put('+', "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF");
  rules.put('-', "+");

  return new LSystem(axiom, rules, moveDist, rotateAngle, scaleFactor);
}
