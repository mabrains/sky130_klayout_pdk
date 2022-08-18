# Skywater 130nm Technology PDK for KLayout

[<img src="https://raw.githubusercontent.com/mabrains/sky130_ubuntu_setup/main/logo.svg" width="150">](http://mabrains.com/)

Mabrains is excited to share with you our Skywater 130nm PDK for Klayout. These files are not qualified. Please use with caution.

## KLayout technology files for Skywater SKY130

* sky130.lyt   : technology and connections description
* sky130.lyp   : layers color and shape description
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
