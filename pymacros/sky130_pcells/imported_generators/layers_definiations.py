########################################################################################################################
##
# Mabrains Company LLC ("Mabrains Company LLC") CONFIDENTIAL
##
# Copyright (C) 2018-2021 Mabrains Company LLC <contact@mabrains.com>
##
# This file is authored by:
#           - <Mina Maksimous> <mina_maksimous@mabrains.com>
##
# This code is provided solely for Mabrains use and can not be sold or reused for any other purpose by
# any person or entity without prior authorization from Mabrains.
##
# NOTICE:  All information contained herein is, and remains the property of Mabrains Company LLC.
# The intellectual and technical concepts contained herein are proprietary to Mabrains Company LLC
# and may be covered by U.S. and Foreign Patents, patents in process, and are protected by
# trade secret or copyright law.
# Dissemination of this information or reproduction of this material is strictly forbidden
# unless prior written permission is obtained
# from Mabrains Company LLC.  Access to the source code contained herein is hereby forbidden to anyone except current
# Mabrains Company LLC employees, managers or contractors who have executed Confidentiality and Non-disclosure
# agreements explicitly covering such access.
#
##
# The copyright notice above does not evidence any actual or intended publication or disclosure
# of  this source code, which includes
# information that is confidential and/or proprietary, and is a trade secret, of  Mabrains Company LLC.
# ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC  PERFORMANCE, OR PUBLIC DISPLAY OF OR THROUGH USE
# OF THIS  SOURCE CODE  WITHOUT THE EXPRESS WRITTEN CONSENT OF Mabrains Company LLC IS STRICTLY PROHIBITED,
# AND IN VIOLATION OF APPLICABLE LAWS AND INTERNATIONAL TREATIES.  THE RECEIPT OR POSSESSION OF  THIS SOURCE CODE
# AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY RIGHTS TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS,
# OR TO MANUFACTURE, USE, OR SELL ANYTHING THAT IT  MAY DESCRIBE, IN WHOLE OR IN PART.
##
# Mabrains retains the full rights for the software which includes the following but not limited to: right to sell,
# resell, repackage, distribute, creating a Mabrains Company LLC using that code, use, reuse or modify the code created.
##
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL
# MABRAINS COMPANY LLC OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT,TORT OR OTHERWISE, ARISING FROM
# , OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# MABRAINS COMPANY LLC DOES NOT HOLD ANY RESPONSIBILITIES THAT MIGHT RISE DUE TO LOSE OF MONEY OR DIGITAL ASSETS USING
# THIS SOFTWARE AND IT IS SOLELY THE RESPONSIBILITY OF THE SOFTWARE USER.
#
# This banner can not be removed by anyone other than Mabrains Company LLC.
##
########################################################################################################################

import pandas as pd
import pya
import os

# print(os.system('pwd'))
lay_csv_map = os.path.join(os.path.expanduser(
    "~"), ".klayout", "tech", "sky130", "pymacros", "sky130_pcells", "gds_layers.csv")
lay_df = pd.read_csv(lay_csv_map)

# print(lay_df)
nsdm_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "nsdm") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]
psdm_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "psdm") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

diff_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "diff") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]
poly_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "poly") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]
licon_lay_str = lay_df.loc[
    (lay_df["Layer name"] == "licon1") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[0]
npc_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "npc") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]
li_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "li1") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]
mcon_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "mcon") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]
met1_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met1") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]
tap_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "tap") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

nwell_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "nwell") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

dnwell_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "dnwell") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]


via_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "via") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

met2_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met2") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

met3_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met3") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

met4_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met4") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

met5_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met5") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

via2_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "via2") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

via3_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "via3") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

via2_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "via2") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

via3_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "via3") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

via4_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "via4") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]
urpm_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "urpm") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]
poly_res_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "poly") & (lay_df["Purpose"].str.contains("resistor")), "GDS layer:datatype"].values[
        0]

prbndry_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "prBndry") & (lay_df["Purpose"].str.contains("boundary")), "GDS layer:datatype"].values[
        0]

poly_label_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "poly") & (lay_df["Purpose"].str.contains("label")), "GDS layer:datatype"].values[
        0]

met1_label_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met1") & (lay_df["Purpose"].str.contains("label")), "GDS layer:datatype"].values[
        0]

me1_pin_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met1") & (lay_df["Purpose"].str.contains("pin")), "GDS layer:datatype"].values[
        0]
met2_label_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met2") & (lay_df["Purpose"].str.contains("label")), "GDS layer:datatype"].values[
        0]


met4_label_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met4") & (lay_df["Purpose"].str.contains("label")), "GDS layer:datatype"].values[
        0]

met5_label_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "met5") & (lay_df["Purpose"].str.contains("label")), "GDS layer:datatype"].values[
        0]


l_capm_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "capm") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

l_cap2m_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "cap2m") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
        0]

l_hvntm_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "hvntm") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]

l_hvi_lay_str = \
    lay_df.loc[(lay_df["Layer name"] == "hvi") & (lay_df["Purpose"].str.contains("drawing")), "GDS layer:datatype"].values[
    0]


# print(diff_lay_str)

diff_lay_num = int(diff_lay_str.split(":")[0])
diff_lay_dt = int(diff_lay_str.split(":")[1])

poly_lay_num = int(poly_lay_str.split(":")[0])
poly_lay_dt = int(poly_lay_str.split(":")[1])

licon_lay_num = int(licon_lay_str.split(":")[0])
licon_lay_dt = int(licon_lay_str.split(":")[1])

nsdm_lay_num = int(nsdm_lay_str.split(":")[0])
nsdm_lay_dt = int(nsdm_lay_str.split(":")[1])

psdm_lay_num = int(psdm_lay_str.split(":")[0])
psdm_lay_dt = int(psdm_lay_str.split(":")[1])

npc_lay_num = int(npc_lay_str.split(":")[0])
npc_lay_dt = int(npc_lay_str.split(":")[1])

li_lay_num = int(li_lay_str.split(":")[0])
li_lay_dt = int(li_lay_str.split(":")[1])

mcon_lay_num = int(mcon_lay_str.split(":")[0])
mcon_lay_dt = int(mcon_lay_str.split(":")[1])

met1_lay_num = int(met1_lay_str.split(":")[0])
met1_lay_dt = int(met1_lay_str.split(":")[1])

tap_lay_num = int(tap_lay_str.split(":")[0])
tap_lay_dt = int(tap_lay_str.split(":")[1])

nwell_lay_num = int(nwell_lay_str.split(":")[0])
nwell_lay_dt = int(nwell_lay_str.split(":")[1])

dnwell_lay_num = int(dnwell_lay_str.split(":")[0])
dnwell_lay_dt = int(dnwell_lay_str.split(":")[1])

via_lay_num = int(via_lay_str.split(":")[0])
via_lay_dt = int(via_lay_str.split(":")[1])

met2_lay_num = int(met2_lay_str.split(":")[0])
met2_lay_dt = int(met2_lay_str.split(":")[1])



met3_lay_num = int(met3_lay_str.split(":")[0])
met3_lay_dt = int(met3_lay_str.split(":")[1])

met4_lay_num = int(met4_lay_str.split(":")[0])
met4_lay_dt = int(met4_lay_str.split(":")[1])

met5_lay_num = int(met5_lay_str.split(":")[0])
met5_lay_dt = int(met5_lay_str.split(":")[1])

via2_lay_num = int(via2_lay_str.split(":")[0])
via2_lay_dt = int(via2_lay_str.split(":")[1])

via3_lay_num = int(via3_lay_str.split(":")[0])
via3_lay_dt = int(via3_lay_str.split(":")[1])

via4_lay_num = int(via4_lay_str.split(":")[0])
via4_lay_dt = int(via4_lay_str.split(":")[1])

urpm_lay_num = int(urpm_lay_str.split(":")[0])
urpm_lay_dt = int(urpm_lay_str.split(":")[1])

poly_res_lay_num = int(poly_res_lay_str.split(":")[0])
poly_res_lay_dt = int(poly_res_lay_str.split(":")[1])

prbndry_lay_num = int(prbndry_lay_str.split(":")[0])
prbndry_lay_dt = int(prbndry_lay_str.split(":")[1])

poly_label_lay_num = int(poly_label_lay_str.split(":")[0])
poly_label_lay_dt = int(poly_label_lay_str.split(":")[1])

met1_label_lay_num = int(met1_label_lay_str.split(":")[0])
met1_label_lay_dt = int(met1_label_lay_str.split(":")[1])

met1_pin_lay_num = int(me1_pin_lay_str.split(":")[0])
met1_pin_lay_dt = int(me1_pin_lay_str.split(":")[1])

met2_label_lay_num = int(met2_label_lay_str.split(":")[0])
met2_label_lay_dt = int(met2_label_lay_str.split(":")[1])

met4_label_lay_num = int(met4_label_lay_str.split(":")[0])
met4_label_lay_dt = int(met4_label_lay_str.split(":")[1])

met5_label_lay_num = int(met5_label_lay_str.split(":")[0])
met5_label_lay_dt = int(met5_label_lay_str.split(":")[1])

capm_lay_num = int(l_capm_lay_str.split(":")[0])
capm_lay_dt = int(l_capm_lay_str.split(":")[1])

cap2m_lay_num = int(l_cap2m_lay_str.split(":")[0])
cap2m_lay_dt = int(l_cap2m_lay_str.split(":")[1])

hvntm_lay_num = int(l_hvntm_lay_str.split(":")[0])
hvntm_lay_dt = int(l_hvntm_lay_str.split(":")[1])

hvi_lay_num = int(l_hvi_lay_str.split(":")[0])
hvi_lay_dt = int(l_hvi_lay_str.split(":")[1])
