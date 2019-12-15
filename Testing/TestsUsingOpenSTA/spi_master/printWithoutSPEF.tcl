# sdf example
read_liberty osu035.lib
read_verilog spi_master.rtl.v
link_design spi_master
create_clock -name clk -period 10 {clk}
report_checks