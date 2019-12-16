cd /home/mahfouz/Desktop/DD2_ws/SPEF-Extractor-master/Testing/TestsUsingOpenROAD/o8_cpu
read_liberty osu035.lib
read_lef osu035.lef
read_def o8_cpu.def
read_verilog o8_cpu.rtl.v
link_design o8_cpu
create_clock -name clk -period 10 {clk_i}
report_checks
set_wire_rc -layer metal1 
report_checks
