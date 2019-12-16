# SPEF-Extractor
A Python library that reads LEF and DEF files, extract the RC parasitics and generate their corresponding SPEF file.:<br />

## Dependancies:  
  In order to parse the lef and def files, we used [trimcao's def and lef parser](https://github.com/trimcao/lef-parser)

## Build Instructions:
   To install the library run the following commands: 
   ```
   
   pip install numpy
   
   pip install sympy
  
   pip install matplotpy   
   
   git clone https://github.com/HanyMoussa/SPEF-Extractor/
   ```

## Using the library
In order to use the project, use the terminal to run `main.py` using the following format.<br />
`main.py osu035.lef rle_rec.def` <br />
where `osu035.lef` is the provided lef file and `rle_rec.def` is its corresponding def file. Aftwards, we extract the RC parasitics and output them in a SPEF file named `RC_parasitics.spef`

## Testing
- For the initial submission, we tested the generated SPEF manually. This was done through checking a number of nets, and comparing the parasitics in the file with the theoretical value.
- For the final Submission, we tested using "openSTA" that verified that the produced SPEF file is syntax error free. "openSTA" was able to successfuly read the SPEF file and produce timing reports based on the parasitics provided.
- Additionally, we used the OpenROAD Project to verify the timing reports produced using openSTA using the SPEF files.

## Assumptions 
During our development, we had to make some assumptions to for the sake of simplicity:
  1. It is assumed that the values that do not exist in the LEF file are considered to be 0.
  2. We represented each wire segment as a single resistance and a capacitance
  3. We consider the capacitance of a segment to be at the end node of the segment 
  4. Testing was done using openSTA that verified our SPEF is syntax error free.
  5. Values testing was done using The OpenROAD Project

## Limitations
  1. We handle pins that are placed in 1 metal layer only.
  2. We manually extracted the lef-to-def conversion factor.
  
## Name Remapping
  1. We implemented an algorithm to rename long names.
  2. All nets are renamed to decrease the size of files.
  3. Names were remapped based on the standard remapping scheme of SPEF files.

## Acknowledgement:
  This was created for the Digital Design 2 Course CSCE3304 at the American University in Cairo under the supervision of Doctor Mohamed Shalan.

## Authors:
  * Ramez Moussa - [Github Profile](https://github.com/ramezmoussa)
  * Hany Moussa - [Github Profile](https://github.com/hanymoussa)
  * Mohamed Mahfouz - [Github Profile](https://github.com/Mahfouz-z)
  * Samah Hussein - [Github Prifle](https://github.com/hysamah)
  
