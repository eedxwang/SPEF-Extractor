# sdf example
read_liberty osu035.lib
read_verilog o8_cpu.rtl.v
link_design o8_cpu
read_spef data/RC_for_o8_cpu.spef
create_clock -name clk -period 10 {clk_i}
report_checks
