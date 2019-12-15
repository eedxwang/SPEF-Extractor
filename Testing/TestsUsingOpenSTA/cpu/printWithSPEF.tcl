# sdf example
read_liberty osu035.lib
read_verilog cpu.rtl.v
link_design cpu
read_spef data/RC_for_cpu.spef
create_clock -name clk -period 10 {clk}
report_checks
