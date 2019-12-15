# sdf example
read_liberty osu035.lib
read_verilog rle_enc.rtl.v
link_design rle_enc
create_clock -name clk -period 10 {clk}
report_checks