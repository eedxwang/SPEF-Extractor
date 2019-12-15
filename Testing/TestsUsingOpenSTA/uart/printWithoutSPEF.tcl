# sdf example
read_liberty osu035.lib
read_verilog uart.rtl.v
link_design uart
create_clock -name clk -period 10 {clk}
report_checks