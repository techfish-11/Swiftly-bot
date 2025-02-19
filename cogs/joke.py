import discord
from discord.ext import commands
import random
import time


prog_langs = ["C++", "Rust", "Python", "JavaScript", "Go", "Java", "TypeScript", "Swift", "Kotlin", "PHP", "Ruby"]
nice_lang = {"C++": "Rust", "Rust": "Python", "Python": "JavaScript", "JavaScript": "Go", "Go": "Java", "Java": "TypeScript", "TypeScript": "Swift", "Swift": "Kotlin", "Kotlin": "PHP", "PHP": "Ruby", "Ruby": "C++"}
bad_lang = {"Rust": "C++", "Python": "Rust", "JavaScript": "Python", "Go": "JavaScript", "Java": "Go", "TypeScript": "Java", "Swift": "TypeScript", "Kotlin": "Swift", "PHP": "Kotlin", "Ruby": "PHP", "C++": "Ruby"}

cpus = ["Ryzen Threadripper PRO 7995WX", "Ryzen Threadripper PRO 7985WX", "Xeon w9-3495X", "Ryzen Threadripper PRO 7975WX", "Ryzen Threadripper PRO 5995WX", "Xeon Platinum 8470", "Ryzen Threadripper PRO 3995WX", "Ryzen Threadripper PRO 7965WX", "Ryzen Threadripper 3990X", "Ryzen Threadripper PRO 5975WX", "Core Ultra 9 285K", "Xeon w7-3465X", "Ryzen 9 9950X", "Xeon w9-3475X", "Ryzen Threadripper PRO 5965WX", "Ryzen Threadripper 3970X", "Core i9-14900KS", "Ryzen 9 7950X", "Ryzen 9 7950X3D", "Ryzen Threadripper PRO 3975WX", "Core i9-13900KS", "Core i9-14900KF", "Core i9-14900K", "Xeon Gold 6448Y", "Core Ultra 7 265K", "Core Ultra 7 265KF", "Core i9-13900K", "Xeon w7-2495X", "Xeon W-3375X", "Core i9-13900KF", "Ryzen Threadripper 3960X", "Ryzen 9 9900X", "Core Ultra 9 285", "Xeon w7-2475X", "Core i7-14700K", "Core i7-14700KF", "Ryzen 9 7900X", "Ryzen Threadripper PRO 5955WX", "Core i9-13900F", "Ryzen 9 7900X3D", "Ryzen 9 7900", "Ryzen 9 5900XT", "Core Ultra 7 265", "Core Ultra 7 265F", "Core i9-14900F", "Core i9-14900", "Core i9-13900", "Core i7-13700K", "Core i7-13700KF", "Ryzen 9 5950X", "Core i9-12900KS", "Core i7-14700F", "Core i7-14700", "Core i9-13900T", "Core Ultra 5 245K", "Core Ultra 5 245KF", "Core i9-12900K", "Ryzen Threadripper PRO 5945WX", "Core i9-12900KF", "Apple M1 Ultra", "Ryzen 7 9800X3D", "Apple M3 Max 16コア", "Ryzen 9 5900X", "Ryzen 9 3950X", "Core i7-13700F", "Core i5-14600KF", "Core i5-14600K", "Core i5-13600K", "Core i5-13600KF", "Core i7-13700", "Core i9-12900", "Ryzen 7 9700X", "Ryzen 7 7700X", "Core i9-12900F", "Ryzen 7 7700", "Apple M3 Max 14コア", "Ryzen 9 5900", "Ryzen 7 7800X3D", "Core i7-12700K", "Core i7-12700KF", "Core i9-10980XE", "Ryzen 9 3900XT", "Core Ultra 5 235", "Ryzen 9 3900X", "Core i5-14500", "Core i5-13500", "Core i9-9980XE", "Ryzen 7 8700G", "Core Ultra 5 225F", "Core Ultra 5 225", "Core i9-12900T", "Ryzen 7 8700F", "Ryzen 9 3900", "Core i7-12700", "Core i7-12700F", "Core i9-9960X", "Core i9-10940X", "Ryzen 5 9600X", "Ryzen Threadripper 2950X", "Core i9 7980XE", "Ryzen 5 7600X", "Ryzen 7 5800X", "Ryzen 7 5800X3D", "Core i9-9940X", "Ryzen 5 7600", "Core i5-12600K", "Core i5-12600KF", "Core i7-13700T", "Apple M3 Pro 12コア", "Ryzen 5 7500F", "Ryzen 7 5700X", "Core i9-10920X", "Ryzen Threadripper 1950X", "Ryzen 7 5700X3D", "Core i9 7940X", "Apple M2 Max", "Ryzen 7 5800", "Core i5-14400", "Core i5-14400F", "Core i9-11900KF", "Core i9-11900K", "Ryzen 7 PRO 5750G", "Core i9-9920X", "Ryzen 5 8600G", "Ryzen Threadripper 2920X", "Core i5-13400F", "Core i7-11700K", "Core i5-13400", "Ryzen 7 5700G", "Core i7-11700KF", "Ryzen 5 8400F", "Ryzen 7 5700", "Ryzen 7 3800XT", "Core i9-10900K", "Core i9-11900F", "Apple M3 Pro 11コア", "Core i9-10900KF", "Core i9-11900", "Core i9 7920X", "Ryzen 7 3800X", "Core i9-10900X", "Core i9-10850K", "Ryzen Threadripper 1920X", "Ryzen 7 3700X", "Ryzen 5 5600X", "Ryzen 5 5600T", "Apple M1 Max", "Ryzen 5 5600X3D", "Core i5-12600", "Apple M1 Pro 10コア", "Core i9-9900X", "Ryzen 5 8500G", "Ryzen 5 5600", "Core i7-12700T", "Core i9 7900X", "Apple M2 Pro 10コア", "Ryzen 7 4700G", "Core i7-11700F", "Core i7-11700", "Ryzen 5 PRO 5650G", "Core i9-10900", "Ryzen 7 PRO 4750G", "Core i9-10900F", "Core i9-9820X", "Core i5-12500", "Ryzen 5 5600GT", "Ryzen 5 5600G", "Ryzen 5 5500GT", "Core i9-9900KS", "Core i5-11600K", "Core i5-12400", "Core i5-11600KF", "Ryzen 7 PRO 4750GE", "Core i5-12400F", "Ryzen 5 5500", "Core i7-10700K", "Core i7-10700KF", "Ryzen 5 3600XT", "Core i9-9900K", "Core i9-9900KF", "Ryzen 5 3600X", "Core i7-9800X", "Core i7-10700", "Core i7-10700F", "Core i5-11500", "Core i7-7820X", "Ryzen 5 3600", "AMD 4700S", "Core i5-11400", "Core i5-11400F", "Ryzen 7 2700X", "Core i9-9900", "Ryzen 5 4600G", "Apple M1 Pro 8コア", "Ryzen Threadripper 1900X", "Ryzen 5 PRO 4650G", "Ryzen 7 1800X", "Ryzen 5 PRO 4650GE", "Ryzen 5 4500", "Ryzen 7 2700", "Ryzen 7 1700X", "Apple M2", "Core i5-10600K", "Core i5-10600KF", "Core i3-14100", "Core i3-14100F", "Core i3-13100", "Core i3-13100F", "Core i7-9700K", "Core i7-9700KF", "Core i7-6900K", "Core i7-8086K", "Ryzen 7 1700", "Core i3-12100F", "Ryzen 5 2600X", "Core i7-9700F", "Apple M1", "Core i5-10600", "Ryzen 3 PRO 5350G", "Core i9-9900T", "Ryzen 3 5300G", "Core i7-9700", "Core i3-12100", "Core i7-8700K", "Ryzen 5 3500X", "Core i5-10500", "Core i7-8700", "Ryzen 5 2600", "Core i5-10400", "Core i5-10400F", "Ryzen 5 1600X", "Ryzen 5 1600 AF", "Ryzen 3 3300X", "Core i7-7800X", "Ryzen 5 3500", "Ryzen 5 1600", "Ryzen 3 3100", "Ryzen 3 4300G", "Core i7-6850K", "Ryzen 3 PRO 4350G", "Ryzen 3 4100", "Core i7-9700T", "Core i5-9600K", "Core i5-9600KF", "Core i7-8700T", "Core i7-5930K", "Core i7-6800K", "Core i5-9600", "Core i5-8600K", "Core i5-8600", "Core i7-5820K", "Core i7-7700K", "Core i5-9500", "Core i5-9400F", "Core i5-9400", "Core i7-4960X", "Ryzen 5 3400G", "Core i7-4930K", "Core i3-10300", "Core i5-8500", "Core i5-8400", "Core i3-10105F", "Core i3-10105", "Core i7-6700K", "Ryzen 5 1500X", "Core i3-10100", "Ryzen 5 2400G", "Core i7-3960X", "Core i3-10100F", "Core i7-7700", "Core i7-3970X", "Ryzen 5 3400GE", "Core i7-4790K", "Core i7-6700", "Core i7-3930K", "Core i7-7700T", "Core i7-7820HK", "Ryzen 5 1400", "Core i5-8400T", "Core i7-5775C", "Core i5-9400T", "Ryzen 3 3200GE", "Core i7-6700T", "Ryzen 3 3200G", "Core i7-990X", "Core i7-4790", "Ryzen 3 1300X", "Intel 300", "Core i7-4770K", "Core i7-4770", "Pentium Gold G7400", "Core i7-7700HQ", "Core i3-8350K", "Core i3-9100F", "FX-9590", "Core i7-4770S", "Ryzen 3 2200G", "Core i5-7600K", "Core i7-4790S", "Core i5-7600", "Core i3-8300", "Core i7-6700HQ", "Core i7-3770K", "Core i7-3770", "Ryzen 3 1200", "Core i5-6600K", "Core i5-7600T", "Core i3-8100", "Core i3-8100F", "Core i7-3770S", "Core i5-7500", "Core i5-6600", "FX-8370", "FX-9370", "FX-8350", "Core i5-5675C", "Core i5-6500", "Core i5-4690", "Core i5-4690K", "Core i7-4785T", "Core i7-2700K", "Core i5-7400", "Core i5-4670", "Core i7-2600K", "Core i5-7500T", "Core i7-2600", "Core i5-4590", "Core i5-4690S", "FX-8300", "FX-8320", "Core i5-4590S", "Core i5-4570", "Core i5-6400", "Core i3-7350K", "Core i5-4570S", "FX-8370E", "FX-8320E", "Core i5-6500T", "Core i3-7320", "Core i3-7300", "Core i5-3570", "Core i5-4460", "Athlon 240GE", "Core i3-6320", "Core i5-3470", "Core i7-4712HQ", "Core i5-4430", "Athlon 3000G", "Core i5-4440", "Core i5-6400T", "Pentium Gold G6605", "Core i3-6300", "Core i5-7400T", "Athlon 220GE", "Core i5-3450", "Core i7-2600S", "Core i5-4440S", "Core i3-7100", "Core i5-4430S", "Core i5-3470S", "Pentium Gold G6400", "Core i3-6100", "Core i5-4590T", "Athlon 200GE", "Core i3-6098P", "FX-6300", "Core i5-2500K", "Core i5-3330", "Core i3-6300T", "Pentium G5500", "Core i3-4370", "Pentium G4620", "Pentium G5600", "Core i5-3330S", "Pentium G5420", "Core i5-2400", "Phenom II X6 1090T", "Core i3-7100T", "Pentium G5400", "Athlon X4 880K", "Core i3-6100T", "Core i3-4170", "Core i5-4460T", "A10-7870K", "A10-7890K", "Core i5-2320", "Core i5-2310", "Core i3-4360", "Pentium G4560", "Pentium Silver J5040", "Pentium G4600", "Core i3-4160", "A10-8750", "Core i3-4150", "A8-7670K", "A12-9800E", "Phenom II X6 1055T", "A10-9700E", "Core i3-4130", "Phenom II X6 1065T", "Core i5-2400S", "Core i7-960", "A8-7600", "A10-7860K", "Celeron J4125", "A10-7700K", "Pentium Silver J5005", "Phenom II X6 1055T", "A10-6700", "Core i3-4160T", "Core i7-870", "Core i7-950", "Core i7-875K", "A10 PRO-7800B", "FX-4300", "A10-7800", "Pentium G4520", "Core i7-930", "A10-5800K", "Core i7-860", "A8-7650K", "Pentium G4500", "Celeron G6900", "Celeron G5905", "Celeron G5900", "Core i7-860S", "Celeron J4115", "A10-5700", "A8-5600K", "Core i7-920", "A8 PRO-7600B", "Pentium G4400", "Pentium G4500T", "A8-5500", "Core i5-760", "Phenom II X4 955", "Pentium G3470", "Celeron G4900", "Celeron G3950", "Core i5-750", "A8-3870K", "Core i3-3240", "Pentium G3460", "Celeron G3930", "Celeron G3900", "Pentium G3440", "Core i3-3220", "Core i5-650", "Celeron G3920", "Pentium G3258", "Core i3-3240T", "Pentium G3260", "Core 2 Quad Q6700", "Core i3-3210", "Core 2 Quad Q9400", "Core i3-3220T", "Core 2 Quad Q8400", "Celeron G1850", "Core i3-2120", "Celeron J4025", "Core 2 Quad Q9450", "Pentium G2120", "Pentium G3240", "Celeron G1840", "Core i3-2100", "Athlon Quad-Core 5350", "Core 2 Quad Q6600", "Athlon Quad-Core 5370", "Core 2 Quad Q8300", "Core 2 Quad Q8200", "Pentium G2030", "Pentium G2020", "A6-7400K", "Phenom 9650", "Core i3-550", "Celeron G1830", "Core i3-2120T", "Core i3-530", "Core i3-540", "Celeron G1610", "A4-7300", "Core 2 Duo E8600", "Athlon Quad-Core 5150", "Celeron G1620", "Celeron J3160", "A6-5400K", "Pentium E5800", "A4 PRO-5300B", "Core 2 Duo E7600", "Celeron J3355", "Core 2 Duo E8400", "Core 2 Duo E6700", "A4-5300", "Athlon II X2 255", "Pentium E5700", "Sempron 3850", "Athlon II X2 250", "Core 2 Duo E7500", "Phenom 8400", "Athlon II X2 235e", "A6-1450", "Core 2 Duo E6300", "Core 2 Duo P8700", "Athlon II X2 220", "Athlon II X2 215", "Core 2 Duo E6750", "Core 2 Duo E7400", "Core 2 Duo E7200", "Core 2 Duo E6600", "Core 2 Duo T7500", "Pentium E5200", "Core 2 Duo P8400", "Core 2 Duo E6400", "Pentium E2220", "Core 2 Duo T8100", "Core 2 Duo E4600", "Core 2 Duo E4500", "Celeron J3060", "Core 2 Duo T7100", "Celeron J1800", "Core 2 Duo E4400", "E1-2500", "Sempron 2650", "Atom 330", "Sempron 3800+", "E1-6010", "Pentium D 940", "Core 2 Duo T5500", "Core Duo T2300", "Core 2 Duo E4300", "Pentium D 830", "Sempron 3100+", "Pentium 4 550", "E2-1800", "E-350", "E-450", "E1-1200", "Pentium 4 630", "Atom 230", "Celeron M 420", "Ryzen 9 7945HX", "Ryzen 9 7940HX", "Core i9-13980HX", "Ryzen 9 7845HX", "Core i9-14900HX", "Core i9-13950HX", "Core i9-13900HX", "Apple M4 Max 16コア", "Apple M3 Max 16コア", "Core i7-14650HX", "Apple M4 Max 14コア", "Apple M4 Pro 14コア", "Ryzen AI 9 HX 370", "Apple M3 Max 14コア", "Core i9-12900HX", "Core i7-13700HX", "Core i7-12800HX", "Core i9-12950HX", "Apple M4 Pro 12コア", "Ryzen 7 7745HX", "Core i7-13650HX", "Ryzen AI 9 365", "Ryzen 9 7940HS", "Core i9-13900H", "Ryzen 7 8845HS", "Ryzen 7 7840HS", "Core i9-12900H", "Core i7-13700H", "Core Ultra 9 185H", "Core i9-12900HK", "Apple M3 Pro 12コア", "Core i7-12700H", "Apple M2 Pro 12コア", "Ryzen Z1 Extream", "Apple M2 Max", "Ryzen 7 8840U", "Ryzen 7 7840U", "Apple M4 10コア", "Core Ultra 7 155H", "Core i7-12800H", "Ryzen 9 6900HX", "Ryzen 7 7735HS", "Ryzen AI 7 PRO 360", "Ryzen 9 6900HS", "Apple M3 Pro 11コア", "Core i7-12650H", "Ryzen 9 5980HX", "Ryzen 7 6800H", "Snapdragon X Elite X1E-84-100", "Snapdragon X Elite X1E-78-100", "Ryzen 5 7640HS", "Core Ultra 5 135H", "Core i9-11980HK", "Snapdragon X Elite X1E-80-100", "Ryzen 7 6800HS", "Core i5-13500H", "Ryzen 9 5900HX", "Snapdragon X Plus X1P-64-100", "Core i7-1370P", "Apple M4 9コア", "Apple M1 Max", "Apple M2 Pro 10コア", "Ryzen 9 5900HS", "Apple M1 Pro 10コア", "Core Ultra 5 125H", "Core i5-12500H", "Ryzen 5 7640U", "Ryzen 9 5980HS", "Ryzen 7 5800H", "Ryzen 7 7735U", "Core i9-11900H", "Ryzen 7 PRO 6850U", "Core i7-11800H", "Core i7-11850H", "Ryzen 5 8640U", "Core i5-1340P", "Core Ultra 9 288V", "Ryzen 7 6800U", "Ryzen 7 5800HS", "Core i7-1280P", "Core Ultra 7 266V", "Core Ultra 7 256V", "Core i7-1360P", "Core Ultra 7 258V", "Snapdragon X Plus X1P-42-100", "Snapdragon X X1-26-100", "Ryzen 8540U", "Ryzen 9 4900H", "Ryzen 7 4800H", "Ryzen 9 4900HS", "Ryzen 7 7730U", "Ryzen 7 4800HS", "Apple M3", "Ryzen 7 5800U", "Core Ultra 5 226V", "Ryzen 5 6600H", "Ryzen 7 5825U", "Core i5-1250P", "Core i5-12450H", "Core i7-1270P", "Core Ultra 7 165U", "Core Ultra 5 125U", "Ryzen 5 5600H", "Ryzen 5 7535U", "Core i5-1240P", "Core i7-1260P", "Core 7 150U", "Core 5 120U", "Apple M1 Pro 8コア", "Ryzen 5 6600U", "Ryzen 7 4800U", "Ryzen 5 PRO 6650U", "Core Ultra 7 155U", "Ryzen 5 7530U", "Core i5-11400H", "Ryzen 7 5700U", "Core i9-10980HK", "Ryzen 7 PRO 4750U", "Core i7-1355U", "Ryzen 5 5600U", "Apple M2", "Ryzen 5 5625U", "Core i9-10885H", "Ryzen 5 7430U", "Core i7-10875H", "Core i9-9980HK", "Core i5-1335U", "Ryzen 5 4600H", "Core i7-10870H", "Ryzen 5 4600HS", "Core i3-1220P", "Core i5-1334U", "Apple M1", "Core i7-1265U", "Core i7-1255U", "Core i9-9880H", "Ryzen 7 4700U", "Core i3-1315U", "Ryzen 5 4600U", "Core i5-1235U", "Ryzen 5 5500U", "Ryzen 5 PRO 4650U", "Core i7-1250U", "Core i7-10750H", "Core i7-11375H", "Snapdragon 8cx Gen 3", "Core i7-11370H", "Ryzen 3 5400U", "Core i5-10500H", "Core i7-9850H", "Core i3-1215U", "Core i7-1195G7", "Core 3 100U", "Ryzen 5 4500U", "Core i5-11300H", "Core i7-9750H", "Ryzen 3 7330U", "Core i5-1230U", "Core i3-1210U", "Core i9-8950HK", "Core i7-1185G7", "Core i7-1165G7", "Core i5-1155G7", "Core i7-8850H", "Core i3-N305", "Core i7-8750H", "Core i5-1145G7", "Core i5-1135G7", "Ryzen 5 7520U", "Core i7-10710U", "Ryzen 3 5300U", "Core i7-1068NG7", "Ryzen 3 7320U", "Core i5-1038NG7", "Core i7-1160G7", "Pentium Gold 8505", "Core i5-10400H", "Core i5-10300H", "Core i3-N300", "Core i7-1065G7", "Core i5-1035G7", "Intel U300", "Ryzen 7 3750H", "Core i5-1035G4", "Ryzen 5 3550H", "Ryzen 5 2600H", "Core i7-8705G", "Core i5-9300H", "Ryzen 7 2800H", "Ryzen 3 4300U", "Core i5-1035G1", "Core i5-8300H", "Ryzen 7 3780U", "Ryzen 7 3700U", "Ryzen 5 3580U", "Ryzen 5 3500U", "Ryzen 7 2700U", "Core i7-7700HQ", "Ryzen 5 3450U", "Core i7-10510U", "Core i7-1060NG7", "Core i7-6700HQ", "Ryzen 5 2500U", "Core i7-8650U", "Core i5-8365U", "Core i5-10210U", "Core i5-8350U", "Core i3-1115G4", "Core i7-8565U", "Core i5-8265U", "Core i7-8550U", "Core i5-8250U", "Core i5-1030NG7", "Microsoft SQ2", "Core i7-4710MQ", "Ryzen 3 3300U", "Core i7-4700HQ", "Intel N100", "Core i7-4722HQ", "Ryzen 3 2300U", "Intel N95", "Microsoft SQ1", "Core i7-4702HQ", "Core i7-4712HQ", "Pentium Gold 7505", "Core i7-3630QM", "Core i7-3610QM", "Core i5-7300HQ", "Core i7-10510Y", "Core i3-1005G1", "Core i5-6300HQ", "Core i7-3632QM", "Core i5-10210Y", "Core i7-3612QM", "Athlon Gold 3150U", "Core i3-10110U", "Athlon 300U", "Ryzen 3 3250U", "Ryzen 3 3200U", "Core i5-6287U", "Core i3-8145U", "Core i7-6567U", "Core i3-1000NG4", "Core i7-2670QM", "Ryzen 3 2200U", "Core i7-7500U", "Core i3-8130U", "Core i7-2630QM", "Core i5-7200U", "Celeron N5100", "Core i7-6500U", "Core i5-6300U", "Core i5-6260U", "Pentium Silver N6000", "Core i7-5600U", "Pentium Gold 6500Y", "Athlon Silver 3050U", "Core i5-6200U", "Core i3-10100Y", "Core m3 8100Y", "Core i5-4210M", "Core i7-3520M", "Core i7-5500U", "Core i5-7Y54", "Core i3-7100U", "Core i7-4600U", "AMD 3015e", "Core i7-7Y75", "Core i3-6100U", "Core i7-3687U", "Pentium Silver N5030", "Pentium Silver N5000", "Core m3 7Y30", "Core i7-4510U", "Core i3-7020U", "Celeron N4120", "FX 9800P", "Core i5-5200U", "Core i3-4100M", "Core i7-4500U", "Core i7-8500Y", "AMD 3020e", "Core i7-4610Y", "Core i5-3210M", "Celeron N4100", "A12-9700P", "Core m5 6Y57", "Core i7-2620M", "Core i7-3537U", "Core i7-2640M", "Core i7-4650U", "Core i7-3667U", "Pentium 6405U", "Core m5 6Y54", "A10-9600P", "Core m7 6Y75", "Core i3-6006U", "Core i5-8200Y", "Pentium Gold 5405U", "A8-8600P", "Core i5-4200U", "PRO A8-8600B", "Core i3-5010U", "Pentium N4200", "Core i7-3517U", "Celeron 6305", "Core i3-5015U", "Pentium 4415U", "Core i5-2450M", "Core i3-5005U", "Core M-5Y71", "Celeron N4500", "Core i5-2430M", "A8-5550M", "Core i5-3317U", "Core i3-4025U", "Core i5-2410M", "A10-4600M", "Core M-5Y10", "A8-7410", "A10-5750M", "Core i3-4030U", "Celeron N3450", "Core i3-4000M", "Celeron N4020", "Core i7-2677M", "Core m3 6Y30", "A8-5545M", "Core i3-4010U", "Core i7-720QM", "A8-4500M", "Core i3-4005U", "Core i7-740QM", "Core i5-520M", "A6-7310", "Pentium Gold 4425Y", "A10-4655M", "Pentium Gold 4415Y", "A10-7300", "Core i3-3110M", "Celeron 3955U", "A6-5200", "Celeron N4000", "Core M-5Y51", "A9-9420", "E2-7110", "Core i3-4020Y", "A8 PRO-7150B", "Celeron 3867U", "Celeron 5205U", "A4-6210", "Atom x7-Z8750", "A6-9225", "A6-8500P", "Pentium 4410Y", "PRO A6-9500B", "Core i7-620LM", "A8-3520M", "A6-9220", "Celeron 4205U", "A4-9125", "Atom x7-Z8700", "Core i5-480M", "A8-4555M", "Celeron 2950M", "Core i3-3227U", "Core i5-460M", "Core i5-430M", "A8-3500M", "Celeron 3865U", "A6-9420e", "A4-5000", "Core i3-2350M", "A4-5100", "A6-3420M", "Celeron 3965Y", "Core 2 Duo P9700", "Core i3-2330M", "Core i3-3217U", "Core i3-380M", "Core i3-370M", "Atom x5-Z8550", "Celeron 3215U", "E2-6110", "Core i3-2310M", "Celeron N3350", "A6-3400M", "Atom Z3795", "Celeron 1005M", "Pentium B970", "Celeron 3855U", "Celeron 1037U", "A6-9220e", "Core i7-640UM", "A4-4300M", "Core 2 Duo T9550", "Core i3-2367M", "Core i3-350M", "Celeron 3205U", "A4 Micro-6400T", "A6-1450", "Celeron 1000M", "Core 2 Duo P8700", "Core i3-2377M", "Atom x5-Z8350", "Athlon64 X2 TK-57", "Core i3-330M", "Pentium 2117U", "Pentium B950", "Core 2 Duo P9500", "Core i3-2357M", "Atom x5-Z8300", "Celeron 2957U", "E2-9000e", "A4-3305M", "Celeron B820", "E2-9000", "Atom Z3775", "Athlon II P360", "Athlon II P340", "Celeron 2955U", "Core i3-380UM", "Core 2 Duo T8100", "Celeron N3060", "Celeron B815", "Celeron T3100", "Core 2 Duo T7250", "Celeron 1007U", "E1-7010", "Atom Z3740", "Celeron T3000", "Atom Z3745", "Celeron B800", "Celeron N3050", "E1-2500", "Core 2 Duo L7500", "Athlon X2 QL-64", "Celeron N2840", "Pentium U5600", "Turion64 X2 TL-50", "Atom Z2760", "Atom N570", "Athlon II M300", "Celeron N2830", "Core 2 Duo SU9400", "E1-6010", "Atom Z3735F", "E1-6015", "Athlon Neo X2 L335", "Celeron N2815", "Core Duo U2400", "Atom Z3736F", "Core 2 Duo T5500", "Celeron T1600", "Celeron SU2300", "Celeron 847", "Celeron N2810", "Athlon Neo MV-40", "E2 1800", "Athlon X2 L310", "A4-1250", "A4-1200", "Athlon II Neo K325", "Athlon64 X2 QL-62", "E-350", "Athlon X2 QL-60", "E-450", "Core Duo L2300", "E1-2100", "E1-1200", "C-60", "Atom N280", "Atom N455", "Atom N270", "C-50", "Atom Z670", "Atom Z520", "Sempron SI-42", "Sempron SI-40", "Core Solo U1300"]
gpus = ["GeForce RTX 5090", "GeForce RTX 4090", "GeForce RTX 5080", "Radeon RX 7900 XTX", "GeForce RTX 4080 SUPER", "GeForce RTX 4080", "Radeon RX 7900 XT", "GeForce RTX 4070 Ti SUPER", "GeForce RTX 4070 Ti", "Radeon RX 7900 GRE", "GeForce RTX 3090 Ti", "Radeon RX 6950 XT", "GeForce RTX 4070 SUPER", "Radeon RX 6900 XT", "Radeon RX 7800 XT", "GeForce RTX 3090", "GeForce RTX 3080 Ti", "Radeon RX 6800 XT", "GeForce RTX 3080 12GB", "GeForce RTX 4070", "GeForce RTX 3080 10GB", "Radeon RX 7700 XT", "Radeon RX 6800", "GeForce RTX 3070 Ti", "Arc B580", "GeForce RTX 2080 Ti", "GeForce RTX 3070", "Arc A770 8GB", "Radeon RX 6750 XT", "GeForce RTX 4060 Ti 8GB", "Arc A770 16GB", "GeForce RTX 4060 Ti 16GB", "Radeon RX 6700 XT", "Arc B570", "Arc A750", "GeForce RTX 3060 Ti GDDR6X", "GeForce RTX 3060 Ti", "GeForce RTX 2080 SUPER", "Radeon RX 6700", "Radeon RX 7600 XT", "GeForce RTX 2080", "Radeon RX 7600", "GeForce RTX 4060", "Arc A580", "GeForce RTX 2070 SUPER", "GeForce GTX 1080 Ti", "Radeon RX 6650 XT", "Radeon RX 6600 XT", "Radeon RX 5700 XT", "GeForce RTX 2070", "GeForce RTX 3060 12GB", "GeForce RTX 2060 SUPER", "Radeon RX 5700", "Radeon RX 6600", "GeForce RTX 2060 12GB", "GeForce RTX 2060 6GB", "GeForce GTX 1080", "Radeon RX 5600 XT(14Gbps)", "GeForce RTX 3060 8GB", "Radeon RX 5600 XT(12Gbps)", "Radeon RX 5600", "GeForce GTX 1070 Ti", "GeForce GTX 1660 Ti", "GeForce RTX 3050 8GB", "GeForce GTX 1660 SUPER", "GeForce GTX 1070", "GeForce GTX 1660", "Radeon RX 6500 XT 4GB", "GeForce RTX 3050 6GB", "Radeon RX 5500 XT 8GB", "Radeon RX 5500 XT 4GB", "GeForce GTX 1650 SUPER", "Arc A380", "GeForce GTX 1060 6GB", "GeForce GTX 1060 3GB", "GeForce GTX 1650 GDDR6", "Radeon RX 6400", "GeForce GTX 1650 GDDR5", "Radeon 780M", "Arc A310", "Radeon 760M", "GeForce GTX 1050 Ti", "Intel Graphics (Core Ultra 200 / 4コア)", "GeForce GTX 1630", "Intel Graphics (Core Ultra 200 / 3コア)", "Radeon 740M", "Radeon RX Vega 8(Ryzen 5000)", "Radeon RX Vega 7(Ryzen 5000)", "Radeon RX Vega 8(Ryzen 4000)", "Radeon RX Vega 7(Ryzen 4000)", "Radeon RX Vega 11(Ryzen 2,3000)", "Radeon RX Vega 6(Ryzen 4000)", "GeForce GT 1030", "Intel Graphics (Core Ultra 200 / 2コア)", "Radeon RX Vega 8(Ryzen 2,3000)", "Intel UHD Graphics 770", "Radeon Graphics (Raphael 2CU)", "Intel UHD Graphics 750", "GeForce GT 1030(DDR4)", "Intel UHD Graphics 730", "Iris Pro Graphics 6200", "Intel UHD Graphics 730 (12世代)", "Radeon RX Vega 3", "Intel UHD Graphics 630", "Intel HD Graphics 630", "Intel HD Graphics 530", "Radeon R7 Graphics", "Radeon HD 8670D", "Radeon HD 7660D", "Radeon HD 7560D", "Radeon HD 6550D", "Intel HD Graphics 4600", "Intel HD Graphics 510", "Intel HD Graphics 4400", "Intel HD Graphics 4000", "Intel HD Graphics 3000", "Intel HD Graphics 2500", "GeForce RTX 4090", "Radeon RX 7900M", "GeForce RTX 4080", "GeForce RTX 3080 Ti", "GeForce RTX 4070", "GeForce RTX 3080", "Radeon RX 6800M", "GeForce RTX 3070 Ti", "Intel Arc A770M", "GeForce RTX 3070", "GeForce RTX 4060", "Radeon RX 7700S", "GeForce RTX 2080 Super", "GeForce RTX 2080", "Radeon RX 7600M XT", "Radeon RX 6700M", "Radeon RX 7600S", "Radeon RX 6800S", "Radeon RX 6650M", "Intel Arc A730M", "GeForce RTX 2080 Super Max-Q", "GeForce RTX 4050", "GeForce RTX 2070 Super", "GeForce RTX 3060", "Radeon RX 6600M", "GeForce RTX 2080 Max-Q", "Radeon RX 6700S", "GeForce RTX 2070", "GeForce RTX 2070 Super Max-Q", "GeForce GTX 1080", "GeForce RTX 2070 Max-Q", "GeForce GTX 1080 Max-Q", "GeForce RTX 2060", "GeForce RTX 2060 Max-Q", "GeForce GTX 1660 Ti", "GeForce GTX 1070", "GeForce RTX 3050 6GB", "GeForce RTX 3050 Ti", "Intel Arc A550M", "GeForce GTX 1660 Ti Max-Q", "GeForce GTX 1070 Max-Q", "GeForce RTX 3050 4GB", "Intel Arc 140V", "Radeon RX 580", "GeForce RTX 2050", "GeForce GTX 1060", "GeForce GTX 1650 Ti", "Radeon 890M", "GeForce GTX 1060 Max-Q", "GeForce GTX 1650", "Intel Arc A370M", "Intel Arc 8コア GPU", "Radeon 880M", "GeForce GTX 1650 Ti Max-Q", "Intel Arc 7コア GPU", "Intel Arc A350M", "GeForce GTX1650 Max-Q", "Radeon 780M", "Radeon 680M", "GeForce GTX 1050 Ti Max-Q", "GeForce GTX 1050 Ti", "GeForce GTX 1050 Max-Q", "Radeon 760M", "GeForce GTX 1050", "Adreno X1-85", "Intel Graphics 4コア(Arc)", "Radeon RX 560X", "Adreno X1-85", "Radeon Pro 560X", "Iris Xe Graphics G7 (96EU)", "Radeon 660M", "Radeon 740M", "Radeon RX Vega 8 (Ryzen 4,5000)", "Iris Xe Graphics G7 (80EU)", "Radeon RX Vega 7 (Ryzen 4,5000)", "Radeon Pro 560", "Adreno X1-45", "Radeon RX Vega 6 (Ryzen 4,5000)", "Radeon RX Vega 5 (Ryzen 4,5000)", "Iris Plus Graphics G7", "Radeon RX Vega 10 (Ryzen 2,3000)", "Radeon RX Vega 8 (Ryzen 2,3000)", "UHD Xe Graphics G4 (48EU)", "Radeon RX Vega 6 (Ryzen 2,3000)", "Iris Plus Graphics G4", "Iris Plus Graphics 655", "Iris Plus Graphics 645", "Iris Plus Graphics 650", "Iris Plus Graphics 640", "Radeon HD 8790M", "Radeon 610M", "UHD Gpradhics G1", "Radeon R7 M260", "Radeon RX Vega 3 (Ryzen 2,3000)", "UHD Graphics 620", "HD Graphics 620", "HD Graphics 6000", "UHD Graphics 617", "Radeon 8570M", "UHD Graphics 615", "HD Graphics 520", "HD Graphics 615", "HD Graphics 5500", "UHD Graphics 610", "HD Graphics 610", "HD Graphics 5000", "GeForce GT 630M", "HD Graphics 4400 Mobile", "HD Graphics 510", "UHD Graphics 605", "HD Graphics 4000 Mobile", "UHD Graphics 600", "HD Graphics 500", "HD Graphics 505", "HD Graphics 400"]

class LoveCalculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="love-calculator", description="2人のユーザーを選択して愛の相性を計算します")
    async def love_calculator(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User):
        if user1 == user2:
            embed = discord.Embed(title="💖 Love Calculator 💖", color=discord.Color.pink())
            embed.add_field(name="メッセージ", value="1人目と2人目で同じユーザーが選択されています。", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            name1 = user1.name
            name2 = user2.name
            love_score = self.K7LoveCalc(name1, name2)
            message = self.get_love_message(name1, name2, love_score[0], love_score[1], love_score[2])
            embed = discord.Embed(title="💖 Love Calculator 💖", color=discord.Color.pink())
            embed.add_field(name="ユーザー1", value=name1, inline=True)
            embed.add_field(name="ユーザー2", value=name2, inline=True)
            embed.add_field(name="相性結果", value=f"**{name1} → {name2}**\n好感度：{love_score[1]}%\n**{name2} → {name1}**\n好感度：{love_score[2]}%", inline=False)
            embed.add_field(name="総合相性（好感度平均）", value=f"{love_score[0]}%", inline=False)
            embed.add_field(name="メッセージ", value=message, inline=False)
            await interaction.response.send_message(embed=embed)
    
    @discord.app_commands.command(name="fantasy-status", description="特定の人の装備品、攻撃力、守備力、体力を表示する")
    async def fantasy_status(self, interaction: discord.Interaction, user: discord.User):
        name = user.name
        stats = self.K7StatsCalc(name)
        embed = discord.Embed(title="⚔ 異世界ステータスジェネレーター ⚔", color=discord.Color.blue())
        embed.add_field(name="名前", value=name, inline=False)
        embed.add_field(name="装備", value=stats[0], inline=True)
        embed.add_field(name="攻撃力", value=stats[1], inline=True)
        embed.add_field(name="守備力", value=stats[2], inline=True)
        embed.add_field(name="最大HP", value=stats[3], inline=True)
        embed.add_field(name="相性の良い言語（攻撃力 x1.2）", value=nice_lang[stats[0]], inline=True)
        embed.add_field(name="相性の悪い言語（攻撃力 x0.87）", value=bad_lang[stats[0]], inline=True)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="your-cpu-gpu", description="特定の人をCPU、GPUで例えると...？")
    async def your_cpu(self, interaction: discord.Interaction, user: discord.User):
        name = user.name
        random.seed(name)
        cpu = random.choice(cpus)
        gpu = random.choice(gpus)
        embed = discord.Embed(title="💻 "+name+"をCPU、GPUで例えると...？ 🖥", color=discord.Color.blue())
        embed.add_field(name="CPU", value=cpu, inline=True)
        embed.add_field(name="GPU", value=gpu, inline=True)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="versus", description="fantasy-statusのステータスをもとに対戦させます。ステータスは固定ですがそれ以外はランダム。")
    async def versus(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User):
        if user1 == user2:
            embed = discord.Embed(title="⚔ Versus ⚔", color=discord.Color.dark_red())
            embed.add_field(name="メッセージ", value="1人目と2人目で同じユーザーが選択されています。", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            random.seed(time.time())
            name1 = user1.name
            name2 = user2.name
            stats1 = self.K7StatsCalc(name1)
            stats2 = self.K7StatsCalc(name2)
            hp1 = stats1[3]
            hp2 = stats2[3]
            embed = discord.Embed(title="⚔ Versus ⚔", color=discord.Color.dark_red())
            turn = random.randint(0,1)
            for i in range(20):
                crit = False
                crit_chance = 0.1
                if turn:
                    turn_atk = stats1[1]
                    turn_def = stats2[2]
                    if nice_lang[stats1[0]] == stats2[0]:
                        crit_chance = 0.2
                        turn_atk *= 1.2
                    elif bad_lang[stats1[0]] == stats2[0]:
                        crit_chance = 0.05
                        turn_atk *= 0.87
                    if random.random() <= crit_chance:
                        turn_atk *= 2
                        turn_def = 0
                        crit = True
                    damage = math.floor(max(0, turn_atk*(1-(turn_def/100))))
                    hp2 -= damage
                    if crit:
                        embed.add_field(name=name1+"のターン", value="クリティカルヒット！"+name2+"に"+str(damage)+"のダメージ！残りHP："+str(hp2), inline=False)
                    else:
                        embed.add_field(name=name1+"のターン", value=name2+"に"+str(damage)+"のダメージ！残りHP："+str(hp2), inline=False)
                    if hp2 <= 0:
                        embed.add_field(name=name1+"の勝利！", value=name1+"は"+str(hp1)+"の体力を残して勝利した！", inline=False)
                        break
                else:
                    turn_atk = stats2[1]
                    crit_chance = 0.1
                    turn_def = stats1[2]
                    if nice_lang[stats2[0]] == stats1[0]:
                        crit_chance = 0.2
                        turn_atk *= 1.2
                    elif bad_lang[stats2[0]] == stats1[0]:
                        crit_chance = 0.05
                        turn_atk *= 0.87
                    if random.random() <= crit_chance:
                        turn_atk *= 2
                        turn_def = 0
                        crit = True
                    damage = math.floor(max(0, turn_atk*(1-(turn_def/100))))
                    hp1 -= damage
                    if crit:
                        embed.add_field(name=name2+"のターン", value="クリティカルヒット！"+name1+"に"+str(damage)+"のダメージ！残りHP："+str(hp1), inline=False)
                    else:
                        embed.add_field(name=name2+"のターン", value=name1+"に"+str(damage)+"のダメージ！残りHP："+str(hp1), inline=False)
                    if hp1 <= 0:
                        embed.add_field(name=name2+"の勝利！", value=name2+"は"+str(hp2)+"の体力を残して勝利した！", inline=False)
                        break
                turn = not turn
            if hp1 > 0 and hp2 > 0:
                embed.add_field(name="引き分け", value="10ターン以内に戦いが終わらなかった。\n"+name1+"の体力："+str(hp1)+"/n"+name2+"の体力："+str(hp2), inline=False)
            await interaction.response.send_message(embed=embed)

    def K7LoveCalc(self, name1: str, name2: str):
        # Use only day of the current date (1～31) as a slight influence
        current_day = int(time.strftime("%d"))
        if name1 > name2:
            base = name1 + name2
        else:
            base = name2 + name1
        # The date adds only a small offset to the seed
        seed_value = hash(base) + current_day
        random.seed(seed_value)

        user1_to_user2_friend = random.randint(0, 100)
        user2_to_user1_friend = random.randint(0, 100)
        love_score = (user1_to_user2_friend + user2_to_user1_friend) // 2
        if name1 > name2:
            return [love_score, user1_to_user2_friend, user2_to_user1_friend]
        else:
            return [love_score, user2_to_user1_friend, user1_to_user2_friend]

    def get_love_message(self, user1_name, user2_name, score, user1_to_user2, user2_to_user1):
        if user1_to_user2 - user2_to_user1 > 70:
            return user1_name + "よ、諦めろ。"
        elif user2_to_user1 - user1_to_user2 > 70:
            return user2_name + "よ、諦めろ。"
        elif abs(user1_to_user2 - user2_to_user1) > 50:
            return "視界に入れてない可能性があります。"
        elif abs(user1_to_user2 - user2_to_user1) > 30:
            return "片思いの可能性があります。💔"
        elif score > 80:
            return "素晴らしい相性です！💞"
        elif score > 60:
            return "とても良い相性です！😊"
        elif score > 40:
            return "まあまあの相性です。🙂"
        elif score > 20:
            return "ちょっと微妙かも...😕"
        else:
            return "残念ながら、相性はあまり良くないようです。😢"

async def setup(bot):
    await bot.add_cog(LoveCalculator(bot))
