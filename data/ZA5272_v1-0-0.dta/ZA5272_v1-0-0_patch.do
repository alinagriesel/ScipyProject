***********************************************************************.
* PATCHFILE FOR GGSS/ALLBUS 2018 (ZA5272).
* FOR USE WITH RELEASE  1.0.0.
* This patch corrects an inaccuracy in the ESeG 
* (European Socio-economic Groups) classification.
***********************************************************************.

*Set working directory:
cd "<PATH>"
use "ZA5272_v1-0-0.dta"

local person " "" "sc" "p" "f" "m" "
foreach x of local person {
recode `x'eseg (40 = 43) if (`x'isco08 >= 7100 & `x'isco08 <= 9129) | (`x'isco08 >= 9300 & `x'isco08 <= 9629)
label define `x'eseg 43 "CRAFT ETC. SELF-EMP.", modify
label values `x'eseg `x'eseg
}

save "ZA5272_v1-0-0_patched.dta"