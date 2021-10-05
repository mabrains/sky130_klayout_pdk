# Skywaters 130nm Technology for KLayout Device Generators

[<img src="https://raw.githubusercontent.com/mabrains/sky130_ubuntu_setup/main/logo.svg" width="150">](http://mabrains.com/)

Mabrains is excited to share with you our Device Generator Library for Skywater 130nm PDK. It's very helpful for creating layouts on Skywater 130nm Technology.


## KLayout technology files for Skywater Sky130

 * sky130.lyt   : technology and connections description
 * sky130.lyp   : layers color and shape description
 * drc/drc_sky130.lydrc : DRC script
 * lvs/lvs_sky130.lylvs : LVS script

## Installation
To use this repo, you need to do the following:
1. Move old .klayout to .klayout_old: mv .klayout .klayout_old
2. Open klayout and enable edit mode.
3. Close klayout
4. cd .klayout
5. mkdir tech
6. cd tech
7. git clone https://github.com/mabrains/sky130_klayout_pdk.git sky130
8. pip install pandas
9. close your terminal.
10. Open a new terminal and open klayout and select sky130 technology as your default.
11. Close klayout.
12. Open klayout, you should be able to see the message that sky130 technology has been loaded in the terminal.

 ## Status
| Device Name           | Status        | DRC           | LVS           | Number of Cases | Method of verification |
|-----------------------|---------------|---------------|---------------|-----------------|------------------------|
| Nmos 1.8v             | :heavy_check_mark:           | :heavy_check_mark:      | :heavy_check_mark:      | 163             | Semi automated         |
| pmos 1.8v             | :heavy_check_mark:           | :heavy_check_mark:      | :heavy_check_mark:      | 163             | Semi automated         |
| nmos 5v               | :heavy_check_mark:           | :heavy_check_mark:      | :heavy_check_mark:      | 90              | Semi automated         |
| pmos 5v               | :heavy_check_mark:           | :heavy_check_mark:      | :heavy_check_mark:      | 90              | Semi automated         |
| mimcap_1              | :heavy_check_mark:           | :heavy_check_mark:      | complete      | 122             | Semi automated         |
| mimcap_2              | :heavy_check_mark:           | :heavy_check_mark:      | :heavy_check_mark:      | 122             | Semi automated         |
| npn                   | :heavy_check_mark:           | :heavy_check_mark:      | :heavy_check_mark:      | 2               | Semi automated         |
| pnp                   | :heavy_check_mark:           | :heavy_check_mark:      | :heavy_check_mark:      | 2               | Semi automated         |
| poly_res              | :heavy_check_mark:           | :heavy_check_mark:      | not complete  | 113             | Semi automated         |
| via_generator         | :heavy_check_mark:           | :heavy_check_mark:      | N.A           | 10              | Manual                 |
| Single_inductor       | :heavy_check_mark:           | not perfect   | not complete  | 5               | Manual                 |
| rectangular_shielding | :heavy_check_mark:           | not perfect   | not complete  | 5               | Manual                 |
| diff_octagon_inductor | :heavy_check_mark:           | not perfect   | not complete  | 5               | Manual                 |
| n-diode               | :x:          | :x: | :x: | :x:            | :x:                   |
| p-diode               | :x:           | :x: | :x: | :x:            | :x:                    |
| diff_square_inductor  | :heavy_check_mark:           | not perfect   | :x:  | 5               | Manual                 |
| nmos 1.8 lvt          | :x: | :x:  | :x:  | N.A             | N.A                    |
| diff-resistor         | :x: | :x: | :x: | :x:            | :x:                    |
 
