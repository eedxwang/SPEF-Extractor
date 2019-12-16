cd /home/mahfouz/Desktop/DD2_ws/SPEF-Extractor-master/Testing/TestsUsingOpenROAD/rle_rec
read_liberty osu035.lib
read_lef osu035.lef
read_def rle_enc.def
link_design rle_enc
create_clock -name clk -period 10 {clk}
report_checks
set_wire_rc -layer metal1 
report_checks
