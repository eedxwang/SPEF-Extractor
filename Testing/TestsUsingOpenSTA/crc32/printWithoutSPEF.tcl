# sdf example
read_liberty osu035.lib
read_verilog crc32.rtl.v
link_design crc32
create_clock -name clk -period 10 {clk}
report_checks