# sdf example
read_liberty osu035.lib
read_verilog cpu.rtl.v
link_design cpu
create_clock -name clk -period 10 {clk}
report_checks