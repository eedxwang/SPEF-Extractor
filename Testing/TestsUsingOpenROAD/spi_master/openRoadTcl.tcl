cd /home/mahfouz/Desktop/DD2_ws/SPEF-Extractor-master/Testing/TestsUsingOpenROAD/spi_master
read_liberty osu035.lib
read_lef osu035.lef
read_def spi_master.def
create_clock -name clk -period 10 {clk}
report_checks
set_wire_rc -layer metal1 
report_checks
