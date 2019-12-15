# sdf example
read_liberty osu035.lib
read_verilog crc32.rtl.v
link_design crc32
read_spef RC_for_spi_master.spef
create_clock -name clk -period 10 {clk}
report_checks
