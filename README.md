# Skywater 130nm Technology PDK for KLayout [![License](https://img.shields.io/github/license/mabrains/sky130_klayout_pdk)](LICENSE)

<p align="center"><img src="https://mabrains.com/assets/images/mabrains_logo.jpg" width="300" /></p>

Mabrains is excited to share with you our Skywater 130nm PDK for Klayout. These files are not qualified. Please use with caution.

## KLayout technology files for Skywater Sky130

* sky130.lyt   : technology and connections description
* sky130.lyp   : layers color and shape description
* sky130.lmp   : layer mapping of def/lef shapes
* DRC          : please use the following --> <https://github.com/efabless/mpw_precheck/blob/main/checks/tech-files/sky130A_mr.drc>
* LVS          : LVS script `lvs/lvs_sky130.lylvs` (In development)
* Pcells       : Devices generators (In development)

## Installation

To use this repo, you need to do the following:

1. Clone the repo:

    ```bash

    git clone <https://github.com/mabrains/sky130_klayout_pdk.git>

    ```

2. Go inside sky130_klayout_pdk:

    ```bash

    cd sky130_klayout_pdk

    ```

3. Open klayout using the following command:

    ```bash

    KLAYOUT_HOME=./sky130_tech klayout -e

    ```

## Status

### Devices Status

| Device Name           |  Model | Status        | DRC           | LVS           | Number of Cases | Method of verification |
|-----------------------|--------|---------------|---------------|---------------|-----------------|------------------------|
| Nmos 1.8v             |sky130_fd_pr__nfet_01v8 |:heavy_check_mark:| :heavy_check_mark:| :heavy_check_mark: | 163             | Semi automated         |
| pmos 1.8v             |sky130_fd_pr__pfet_01v8|:heavy_check_mark: | :heavy_check_mark:      | :heavy_check_mark:      | 163   | Semiautomated         |
| nmos 5v               |sky130_fd_pr__nfet_g5v0d10v5 |:heavy_check_mark:|:heavy_check_mark:  | :heavy_check_mark:      | 90    | Semi automated         |
| pmos 5v               |sky130_fd_pr__pfet_g5v0d10v5 |:heavy_check_mark:|:heavy_check_mark:  | :heavy_check_mark:      | 90    | Semi automated         |
| mimcap_1              |sky130_fd_pr__model__cap_mim |:heavy_check_mark:| :heavy_check_mark: | :heavy_check_mark:      | 122   | Semi automated         |
| mimcap_2              |sky130_fd_pr__cap_mim_m4|:heavy_check_mark:| :heavy_check_mark: | :heavy_check_mark: | 122             | Semi automated         |
| npn                   |sky130_fd_pr__npn_05v5 |:heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | 2               | Semi automated         |
| pnp                   |sky130_fd_pr__pnp_05v5 |:heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | 2               | Semi automated         |
| P- poly_res              |sky130_fd_pr__res_xhigh_po |:heavy_check_mark:| :heavy_check_mark: | not_perfect   | 113        | Semi automated|
| via_generator         | Connectivity |:heavy_check_mark:           | :heavy_check_mark:      | Connectivity   | 10              | Manual                 |
| Single_inductor       | Mabrains Device |:heavy_check_mark:           | not perfect   | No LVS Available   | 5               | Manual                 |
| rectangular_shielding | Mabrains Device |:heavy_check_mark:           | not perfect   | No LVS Available   | 5               | Manual                 |
| diff_octagon_inductor | Mabrains Device |:heavy_check_mark:           | not perfect   | No LVS Available   | 5               | Manual                 |
| diff_square_inductor  | Mabrains Device |:heavy_check_mark:           | not perfect   | No LVS Available   | 5               | Manual                 |
| n-diode               |sky130_fd_pr__diode_pw2nd_*,sky130_fd_pr__model__parasitic_* |:x: | :x: | :x: | :x:            | :x:     |
| p-diode               |ky130_fd_pr__diode_pd2nw_* |:x:           | :x: | :x: | :x:            | :x:                    |
| nmos 1.8 lvt          |sky130_fd_pr__nfet_01v8_lvt |:x: | :x:  | :x:  | :x:     | :x:             |
| diff-resistor         | |:x: | :x: | :x: | :x:     | :x:       |
| mom cap               |sky130_fd_pr__cap_vpp_* |:x: | :x: | :x: | :x:     | :x:        |
| NMOS ESD FET          |sky130_fd_pr__esd_nfet_[01v8,g5v0d10v5,g5v0d10v5_nvt] |:x: | :x: | :x: | :x:     | :x:       |
| 11V/16V NMOS FET      |sky130_fd_pr__nfet_g5v0d16v0 |:x: | :x: | :x: | :x:     | :x:   |
| 3.0V native NMOS FET     |sky130_fd_pr__nfet_03v3_nvt |:x: | :x: | :x: | :x:     | :x:   |
| 5.0V native NMOS FET     |sky130_fd_pr__nfet_05v0_nvt |:x: | :x: | :x: | :x:     | :x:   |
| 20V NMOS FET    |sky130_fd_pr__nfet_20v0 |:x: | :x: | :x: | :x:     | :x:   |
| 20V isolated NMOS FET  |sky130_fd_pr__nfet_20v0_iso |:x: | :x: | :x: | :x:     | :x:   |
| 20V native NMOS FET    |sky130_fd_pr__nfet_20v0_nvt |:x: | :x: | :x: | :x:     | :x:   |
| 20V NMOS zero-VT FET    |sky130_fd_pr__nfet_20v0_zvt |:x: | :x: | :x: | :x:     | :x:   |
| 20V NMOS zero-VT FET    |sky130_fd_pr__nfet_20v0_zvt |:x: | :x: | :x: | :x:     | :x:   |
| 10V/16V PMOS FET    |sky130_fd_pr__pfet_g5v0d16v0 |:x: | :x: | :x: | :x:     | :x:   |
| 1.8V high-VT PMOS FET    |sky130_fd_pr__pfet_01v8_hvt |:x: | :x: | :x: | :x:     | :x:   |
| 1.8V low-VT PMOS FET   |sky130_fd_pr__pfet_01v8_lvt |:x: | :x: | :x: | :x:     | :x:   |
| 20V PMOS FET   |sky130_fd_pr__pfet_20v0 |:x: | :x: | :x: | :x:     | :x:   |
| P+ poly_res    |sky130_fd_pr__res_high_po |:x:| :x: | :x:   | :x:       | :x:|
| N-pass FET (SRAM)    |sky130_fd_pr__special_nfet_pass |:x:| :x: | :x:   | :x:       | :x:|
| N-latch FET (SRAM)    |sky130_fd_pr__special_nfet_latch |:x:| :x: | :x:   | :x:       | :x:|
| P-latch FET (SRAM)    |sky130_fd_pr__special_pfet_pass |:x:| :x: | :x:   | :x:       | :x:|
| Varactors             |sky130_fd_pr__cap_var_lvt , sky130_fd_pr__cap_var_hvt |:x:| :x: | :x: | :x:| :x:|
