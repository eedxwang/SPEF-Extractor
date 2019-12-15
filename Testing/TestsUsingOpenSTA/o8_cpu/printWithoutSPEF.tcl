# sdf example
read_liberty osu035.lib
read_verilog o8_cpu.rtl.v
link_design o8_cpu
create_clock -name clk -period 10 {clk_i}
report_checks