# SmartQC Mechanical Reference — Aluminium CAD (22 Nov 2026)

Nov 22, 2026 · @Tawhid

## Source and scope

The aluminium-extrusion CAD exported on 22 Nov 2026 is now the mechanical reference for SmartQC. It replaces every size and position in the welded-steel layout (plan v2.2 to v2.5: brackets A to J, cloth level 290, bed plate, knurled capstan).

- **File:** `hardware/mechanical/Aluminium_ver/Assembly/ASSEMBLY_main#.STEP` (SolidWorks 2023, exported 22 Nov 2026, 20:26). 72 parts in 6 sub-assemblies: base frame, cloth roll, photo booth, two idle rollers, pinch-roll drive.
- **How the numbers were taken:** read straight from the STEP geometry (part boxes, hole centres and diameters), then a clash check of every part pair. No parts overlap except modelled springs, T-nuts in their slots and shaft fits.
- **Laser-cut plates:** already cut from `sheet_metal_ASSEMBLY lasercut 135x1250.DXF` (8 Nov). Their holes match this CAD exactly, so the problems in the "Problems found" section are in the cut plates too.
- **Team decisions (22 Nov):** the idle rollers are bare 8 mm shafts; the gantry uprights are cut from 450 to 400 mm; the camera position is not decided yet.
- **CAD vs build:** some parts in the CAD are not mated to the T-slots. Where the bolted build differs from the CAD, this doc gives the bolted position and says so.

## Coordinate system

Every position in this doc is in millimetres, in machine coordinates: X along the cloth path, Y across it, Z up from the table.

| Axis | Zero | Positive towards | From the STEP / SolidWorks axes |
| --- | --- | --- | --- |
| X | outer face of the frame at the unwind (roll) end | the way the cloth travels; the drive end is X 700 | X = 400.88 − Z(cad) |
| Y | outer face of the drive-side 2040 rail | the idle side; its outer face is Y 390 | Y = 113.32 − X(cad) |
| Z | underside of the frame (table top) | up | Z = Y(cad) + 321.46 |

- **Drive side** = the side with the motor, belt and pulleys. **Idle side** = the other side. Front and back are not fixed yet, so this doc does not use them.
- Negative Y means outside the frame on the drive side (plates, pulleys, belt).
- The axes are right-handed. The v2.5 numbers used a similar idea on a different frame, so none of them carry over.

## Key numbers at a glance

The cloth runs flat at Z 267.0 through the booth, the camera centre line is X 350.0, and the pinch nip is 290.0 further on at X 640.0.

| What | Value (mm) |
| --- | --- |
| Frame, outside | 700 long × 390 wide × 240 high (top of the 2040 rails), bolted V-slot |
| Cloth | 300 wide, centred on Y 195.0 (Y 45 to 345) |
| Cloth roll | Ø200 max × 300; shaft centre X 51.6, Z 400.0 when bolted (CAD shows 405.6) |
| Idle rollers | bare Ø8 × 425 shafts in KFL08 bearings at X 196.8 and X 510.5; centre Z 263.0, top Z 267.0 |
| Cloth plane in the booth | Z 267.0, 7.5 above the booth floor |
| Photo booth inside | 330 across × 252 along (X 224 to 476), walls up to Z 510; centre X 350.0 |
| Booth floor | 5 mm acrylic, 338 × 248, Z 254.5 to 259.5 |
| Cloth slot under the booth end walls | Z 259.5 to 274.0 (14.5 high) |
| Back-light plate | 336 × 248 × 5, Z 201.5 to 206.5; top face 48.0 below the floor underside |
| Camera centre line | X 350.0 (gantry and booth centre) |
| Camera bar underside | Z 561.25 = 294.25 above the cloth |
| Pinch rollers | Ø44 × 340 at X 640.0; lower (driven) centre Z 288.0, upper (pressure) Z 332.0 at contact; nip Z 310.0 |
| Camera line to nip | 290.0 |
| Drive | NEMA 17 → GT2 20T/40T (2:1) → lower pinch roller; 23.15 steps/mm at 1/8 step and Ø44.0 |
| Belt centre distance | 106.5 to 113.5 (motor slot); a 280 belt sits at 109.8, motor centre Z 178.2 |
| Camera lens height | not decided (see "Not in the CAD yet") |

## Frame

The base is a bolted box of V-slot: two 2040 rails standing 40 tall on four 2020 legs, with a 2020 rectangle at the bottom. Frame top = Z 240 (v2.5 said 248); width = 390 (v2.5 said 400).

| Part | Qty | Length | Position |
| --- | --- | --- | --- |
| 2040 V-slot top rail, standing (40 tall, 20 wide) | 2 | 700 | X 0 to 700; Y 0 to 20 (drive side) and 370 to 390 (idle side); Z 200 to 240 |
| 2020 leg | 4 | 200 | at the four corners under the 2040 rails; Z 0 to 200 |
| 2020 bottom side rail | 2 | 660 | X 20 to 680, between the legs; Z 0 to 20 |
| 2020 top end rail | 2 | 350 | X 0 to 20 and 680 to 700; Y 20 to 370; Z 220 to 240 (flush with the 2040 tops) |
| 2020 bottom end rail | 2 | 350 | same X and Y; Z 0 to 20 |

- **T-slots on the 2040 side faces** (outer and inner) are centred at **Z 210 and Z 230**. Every plate and printed holder bolts to these two slot lines, so a bolt hole pair must be 20 apart and land on these heights.
- The Puran Dhaka trip list (8 Nov) matches the CAD: 2040 × 700 ×2; 2020 × 200 ×4, 350 ×4, 660 ×2, 450 ×2 (cut to 400 for the uprights), 430 ×1, 390 ×1.
- Two part files have stale names: `..._370mm` is the 400 upright and `..._588mm` is the 430 top bar. `BOM.md` (6 Nov) is older than the CAD and still lists 2020 × 370 and M4 T-nuts.
- Corner brackets and bolts are not modelled; the STEP holds only 4 sample M5 T-nuts.

## Gantry (camera portal)

One portal straddles the frame at X 340 to 360, centred on the booth; its camera bar underside is 294.25 above the cloth.

| Part | Qty | Length | Position |
| --- | --- | --- | --- |
| 2020 upright | 2 | 400 (cut from 450) | X 340 to 360; Y −20 to 0 (drive side) and 390 to 410 (idle side), against the 2040 outer faces; Z 200 to 600 |
| 2020 top bar | 1 | 430 | X 340 to 360; Y −20 to 410, across both uprights; Z 600 to 620 |
| 2020 camera bar | 1 | 390 | X 340 to 360; Y 0 to 390, between the uprights; Z 561.25 to 581.25 |

- Each upright overlaps its 2040 rail over Z 200 to 240 (both T-slot lines). How it bolts on (corner brackets, count) is not in the CAD.
- The camera bar sits 51 above the booth wall tops (Z 510), so a camera hung from it can sit above or inside the booth opening.

## Cloth path and heights

The cloth runs dead flat at Z 267.0 from idle shaft 1 to idle shaft 2 (313.7 apart), through the booth's two 14.5 high slots, then climbs 43 into the pinch nip at Z 310.0.

&#91;embedded content: ASSEMBLY\_main#.STEP, 22 Nov 2026 · side view to scale, motor shown at the 280 belt position\]

Blue is the cloth: dashed where it leaves the roll (side not fixed yet) and solid from idle shaft 1 to the nip. The gantry upright stands outside the frame, so it is drawn dashed.

| Order | Point | X | Z | Note |
| --- | --- | --- | --- | --- |
| 1 | Cloth roll | shaft 51.6 | shaft 400.0 | Ø200 full roll: bottom Z 300, top Z 500. Which side the cloth leaves from is not fixed |
| 2 | Idle shaft 1 (bare Ø8) | 196.8 | top 267.0 | 145.2 after the roll shaft |
| 3 | Booth entry slot | wall 219 to 224 | slot 259.5 to 274.0 | cloth 7.5 above the floor top, 7.0 below the wall edge |
| 4 | Camera centre line | 350.0 | cloth 267.0 | booth inside X 224 to 476 |
| 5 | Booth exit slot | wall 476 to 481 | slot 259.5 to 274.0 | same clearances as the entry |
| 6 | Idle shaft 2 (bare Ø8) | 510.5 | top 267.0 | 160.5 after the camera line |
| 7 | Pinch nip | 640.0 | 310.0 | rises 43 over 129.5 (about 18°), wrapping about 19° of the lower roller before the nip |
| 8 | Exit | after 640 | — | no tray or chute in the CAD |

- A thin sheet modelled along rows 2 to 6 clears every part in the CAD, including the printed holders and booth walls.
- The idle brackets have 12 mm vertical slots, but raising them more than 7.0 makes the cloth rub the end-wall edges (Z 274). As modelled they sit at the bottom of their slots.

## Unwind roll and idle rollers

The roll and both idle rollers hang on 5 mm plates bolted to the outside of the 2040 rails, each shaft turning in two KFL08 flange bearings mounted on the plates' inner faces.

| Part | Qty | Size | Position (bolted) |
| --- | --- | --- | --- |
| Cloth-roll bracket (`Cloth_bracket_R`) | 2 | 70 along × 220 tall × 5 | X 16.6 to 86.6; Y −5 to 0 and 390 to 395; Z 200 to 420 (CAD shows 205.6 to 425.6) |
| Roll shaft, ×8 hardened | 1 | 425 | centre X 51.6, Z 400.0; Y −15.5 to 409.5 (10.5 past the drive-side plate, 14.5 past the idle-side plate) |
| Cloth roll (modelled as a solid cylinder) | 1 | Ø200 × 300, Ø10 bore | Y 45 to 345; X −48.4 to 151.6, so a full roll overhangs the unwind end by 48.4 |
| Idle-roller bracket (`roller_bracket`) | 4 | 62 along × 95 tall × 5 | X 165.8 to 227.8 and 479.5 to 541.5; Z 188.0 to 283.0 at the bottom of its slots (reaches 12 below the rail) |
| Idle shaft, ×8, bare | 2 | 425 | centres X 196.8 and 510.5, Z 263.0 (up to 275.0 in the slots); Y −22.0 to 403.0 |
| KFL08 flange bearing | 6 | 48 × 28 × 11.4 | 2 per shaft, on the plates' inner faces; bolt holes 37 apart |

- The roll shaft centre is 200 above the plate's bottom edge; the idle shaft centre is 75 above it.
- Not in the CAD: roll core and flanges, unwind brake, shaft collars.

## Photo booth and back light

The booth is an open-topped acrylic box, 330 × 252 inside, sitting on four printed holders between the 2040 rails; the back-light plate lies 48.0 below its floor.

| Part | Qty | Size | Position |
| --- | --- | --- | --- |
| Floor, `acrylic bottom(clear)` | 1 | 338 across × 248 along × 5 | X 227 to 475; Y 27 to 365; Z 254.5 to 259.5 |
| Side wall, `acrylic_side1` | 2 | 250 along × 250 tall × 5 | X 225 to 475; Y 25 to 30 and 360 to 365; Z 259.5 to 509.5 (stands on the floor) |
| End wall, `acrylic_side2` | 2 | 338 across × 236 tall × 5 | X 219 to 224 and 476 to 481; Y 26 to 364; Z 274.0 to 510.0 (leaves the cloth slot) |
| Back-light plate, `LED_strip` | 1 | 336 × 248 × 5 | X 225 to 473; Y 29 to 365; Z 201.5 to 206.5 |
| Printed holder, `enclosure_holder11/12/21/22` | 4 | 175.8 across × 135 along × 160 tall | one per quarter: X 210 to 345 and 355 to 490; Y 14.3 to 190 and 200 to 375.8; Z 186.5 to 346.5 |

- **Holder fixing:** each holder bolts to the inner face of a 2040 rail with 4 × M5, two on each slot line (Z 210 and 230), 60 apart along X. STLs and a Bambu A1 mini print setup are in `3DP/STL`.
- **Wall holes:** Ø6 in the acrylic, Ø7 in the holders. Side walls: X 234.5 and 465.5 at Z 324 and 374. End walls: Y 35 and 355 at Z 324 and 374.
- **Walls** are clear acrylic, to be spray-painted black (team decision, Nov).
- **Back-light gap:** plate top Z 206.5 to floor underside Z 254.5 = 48.0. The back-light study (`docs/backlight/README.md`, 5 Nov) chose 53.5 and found 45 to 65 works, so 48.0 is fine.
- **Floor material:** the CAD floor is clear. The same study recommends 5 mm opal (milky) acrylic, same size, so the camera does not see LED hot spots through it. Team decision still open.
- **Lit area vs view:** lit plate 336 × 248; booth inside 330 × 252; cloth 300 wide leaves 15 to each side wall.

## Pinch rollers, pressure springs and belt drive

The motor drives the lower Ø44 pinch roller through a 2:1 GT2 belt on the drive side; the upper roller rides in slots and is pushed down by four small die springs.

| Part | Qty | Size | Position |
| --- | --- | --- | --- |
| Pinch roller, `pinch_roller` | 2 | Ø44 × 340; bore Ø25 with Ø40 × 5 counterbores at both ends | X 618 to 662 (centre 640.0); Y 24.1 to 364.1; lower (driven) centre Z 288.0; upper (pressure) Z 332.0 at contact (CAD 333.0, 1 mm gap) |
| End hub, `roller_shaft_coupler` | 4 | Ø38 × 5, bore Ø8.5 | in the roller counterbores |
| Pinch shaft, Ø8 | 2 | 460 | Y −36.0 to 424.0 |
| KFL08 (lower shaft) | 2 |  | inner faces of both pinch plates, centre Z 288.0 |
| 688ZZ bearing (upper shaft) | 2 | 8 × 16 × 5 | in the pressure mounts |
| Pressure mount, `pressure_mount` | 2 | 15 thick × 45 along × 23 tall | outside each pinch plate: X 617.5 to 662.5; Z 333.0 to 356.0 |
| Screw holder, `screw_holder` | 2 | 56 across × 60 along × 70 tall | on top of each pinch plate (2 × M5): X 610 to 670; underside Z 376.0, top Z 436.0 |
| Die spring, OD 8, ID 4.5, free length 25 | 4 |  | 2 per side at X 632 and 648, on Ø4 guide pins |
| NEMA 17 | 1 |  | inside face of the drive plate, under the drive-side rail; shaft at X 640.0 |
| GT2 20T pulley | 1 |  | motor shaft, Y −26.7 to −9.7 |
| GT2 40T pulley, 8 mm bore | 1 |  | lower pinch shaft, Y −34.4 to −17.3 |
| GT2 belt, 6 wide, closed loop | 1 |  | Y −25.2 to −19.2 (17 outside the drive plate) |

- **Upper-roller travel:** Ø12 slots in both pinch plates let the upper shaft centre move from Z 325.5 to 350.5. It reaches the lower roller at Z 332.0, so the slot never limits the nip.
- **Spring preload:** seat to seat is 23.0 at the CAD position (pocket floor Z 353.0 to holder underside Z 376.0). With the rollers touching it is 24.0, so each spring is compressed only about 1 mm. Nip force = 4 × spring rate × compression; the rate is not in the CAD, so measure the nip force.
- **Motor slot:** Ø24 centre slot plus four Ø3.1 slots (31 apart), 7 long, give a motor centre of Z 174.5 to 181.5 (belt centre distance 113.5 to 106.5).
- **Belt:** a 280 belt runs at 109.8 centres (motor centre Z 178.2). Belts of 280 to 286 fit the slot. See "Problems found" for the rail clearance.
- **Wrap:** the cloth wraps about 19° of the driven roller before the nip.

## 5 mm plates: hole by hole

Four plate designs, eight plates, all already laser-cut from 5 mm sheet; every bolt hole is Ø5.5 except the motor screws. In the tables, **u** is measured from the plate's upstream edge (the edge nearer the roll) and **v** up from its bottom edge.

**Cloth-roll bracket, 70 × 220 (2 off).** Bolted bottom edge at Z 200 (flush with the rail underside).

| Feature | Size | u | v |
| --- | --- | --- | --- |
| Rail bolts (4, M5 into T-nuts) | Ø5.5 | 10 and 60 | 10 and 30 |
| KFL08 boss clearance | Ø28 | 35 | 200 |
| KFL08 bolts (2) | Ø5.5 | 16.5 and 53.5 | 200 |

**Idle-roller bracket, 62 × 95 (4 off).** Bottom edge Z 188 at the lowest slot position, up to Z 200 at the highest.

| Feature | Size | u | v |
| --- | --- | --- | --- |
| Rail-bolt slots (4) | 5.5 wide, 12 long | 10 and 52 | 10 to 22, and 30 to 42 |
| KFL08 boss clearance | Ø28 | 31 | 75 |
| KFL08 bolts (2) | Ø5.5 | 12.5 and 49.5 | 75 |

**Drive-side pinch plate, `pinchroll_bracket`, 70 × 294.04 (1 off).** Bottom edge Z 132.0.

| Feature | Size | u | v |
| --- | --- | --- | --- |
| Motor screw slots (4, M3) | 3.1 wide, 7 long | 19.5 and 50.5 | 27.0 to 34.0, and 58.0 to 65.0 |
| Motor centre slot | 24 wide, 7 long | 35 | 42.5 to 49.5 |
| Rail bolts (4) | Ø5.5 | 10 and 60 | 78.0 and 98.0 |
| KFL08 boss clearance | Ø28 | 35 | 156.0 |
| KFL08 bolts (2) | Ø5.5 | 16.5 and 53.5 | 156.0 |
| Upper-shaft slot | 12 wide | 35 | 193.5 to 218.5 |
| Screw-holder bolts (2) | Ø5.5 | 19.5 and 50.5 | 280.5 and 281.1 |

**Idle-side pinch plate, `pinchroll_bracket_still`, 70 × 215.36 (1 off).** See "Problems found": its rail holes do not suit the bearing height.

| Feature | Size | u | v |
| --- | --- | --- | --- |
| Rail bolts (4) | Ø5.5 | 10 and 62.9 | 10 and 30 |
| KFL08 boss clearance | Ø28 | 36.45 | 77.36 |
| KFL08 bolts (2) | Ø5.5 | 17.95 and 54.95 | 77.36 |
| Upper-shaft slot | 12 wide | 36.45 | 114.86 to 139.86 |
| Screw-holder bolts (2) | Ø5.5 | 19.46 and 50.54 | 202.39 |

**Fastener count from the CAD:** 48 × M5 into 2040 T-nuts (roll brackets 8, idle brackets 16, pinch plates 8, booth holders 16) plus the gantry joints; 16 × M4 bolt and nut for the eight KFL08s (their flange holes are Ø5); 4 × M3 for the motor; 4 × M5 for the screw holders.

## Problems found in the CAD

One problem must be fixed before assembly: the cut idle-side pinch plate puts the driven roller 10.7 low at that end. The rest are small or only in the model.

| # | Severity | Problem | Effect on the build | What to do |
| --- | --- | --- | --- | --- |
| 1 | Must fix | Idle-side pinch plate: rail holes are 67.4 / 47.4 below its bearing; on the drive plate they are 78.0 / 58.0 | Bolted into the Z 210 / 230 slots, the idle end of the driven roller drops to Z 277.3 against Z 288.0 on the drive side (about 1.6°). The cloth walks sideways and the nip is uneven | Re-cut or re-drill this plate (options below) |
| 2 | Assembly note | Same plate: bearing and slot sit at u 36.45, not 35.0 | 1.45 along-X offset if the plate edges are lined up | Line the plates up by their bearing holes (8 mm rod through both), not by their edges |
| 3 | Check at assembly | Motor body vs drive-side 2040 underside | With a 280 belt the motor top is about 0.5 below the rail (Z 199.5 vs 200.0); belts under about 279 push the motor into the rail | Fit by hand first; a 282 belt gives 1.5, a 286 gives 3.5. Tension by pulling the motor down |
| 4 | Check at assembly | Nothing locks the driven roller to its shaft (end hubs have Ø8.5 clearance bores) | Shaft turns, roller may not | Grub screw on a shaft flat, a clamp collar, or bond the hubs; also grind a flat for the 40T pulley's grub screws |
| 5 | Buy right | CAD 20T pulley has a 6 mm bore | NEMA 17 shaft is Ø5 | Use a 5 mm bore 20T |
| 6 | Small | Drive plate screw-holder holes are 0.6 apart in height (v 280.5 / 281.1); the printed holder's holes are level | One bolt may not pass | Open that holder hole to Ø6 |
| 7 | Measure | Nip springs compressed only about 1 at roller contact | Nip force may be too low to pull the cloth without slip | Measure the nip force; the planned M10 pressure screw makes it adjustable |
| 8 | Model only | Cloth-roll brackets float 5.6 above their slots; idle-side pressure mount 1.8 off its spring pins; motor model body is 36.5 long (real 17HS8401: 48) | None if built by the holes; no clash with a 48 body | Fix the mates so the CAD matches the build |

**Fix options for problem 1** (plate is already cut; the team decides):

1. **Re-cut the plate (best):** copy the drive plate's spacing. Height 226.0 with the bottom edge flush with the rail underside (Z 200); rail holes at v 10 and 30; bearing at v 88.0, u 35.0; upper-shaft slot v 125.5 to 150.5; screw-holder holes at v 213.0.
2. **Re-drill the cut plate (quick, less rigid):** keep it at the CAD height (bottom edge Z 210.7) and drill two new Ø5.5 holes at v 19.3 (the Z 230 slot line), for example at u 20 and 55, clear of the old holes. It then holds on one slot line only; check it is stiff enough by hand before relying on it.

## Not in the CAD yet

The camera, top light, marker, E-stop and electrical box are not modelled, so their positions are open; the camera height can go anywhere from 240 to 294 above the cloth.

**Camera height options** (estimates from the C920 view used in v2.5, 339 × 190 at 240; long image side across the cloth):

| Lens above cloth | Lens Z | View across × along | mm per pixel |
| --- | --- | --- | --- |
| 240 | 507 | 339 × 190 | 0.18 |
| 260 | 527 | 367 × 206 | 0.19 |
| 280 | 547 | 396 × 222 | 0.21 |
| 294 (lens at the bar underside, upper limit) | 561 | 415 × 233 | 0.22 |

- 240 is the lowest height that still sees wall to wall (booth inside 330). Every option sees less than the 252 booth length along the cloth.

**Open items:**

- [ ] Camera (C920) mount and lens height
- [ ] Top light: type and position
- [ ] Chalk marker and MG996R servo: position (sets D\_mark)
- [ ] E-stop and electrical box (ESP32, carrier board, PSU): where they mount
- [ ] Exit tray or chute after the nip
- [ ] Roll core and flanges, unwind brake, shaft collars, belt guard, nip finger guard
- [ ] Gantry corner brackets and all bolts in the model
- [ ] Pinch roller material (Ø44 OD, Ø25 bore)
- [ ] Booth floor: clear (CAD) or opal (back-light study)
- [ ] Team's own list (`Design changes for later.md`, 7 Nov): printed spacers to mount brackets; cloth escape gap; idle roller position; holes in acrylic for structure; M4 washer spring base for the pinch pressure; M10 pressure screw with step and bearing

## What changes for software and firmware

Steps per mm stay at 23.15 (1/8 step, 2:1 belt, Ø44.0), but the roller that sets it is now the lower pinch roller, and D\_mark and the index step wait on the marker and camera positions.

| Quantity | Value from this CAD | Notes |
| --- | --- | --- |
| Steps per mm | 1018.6 ÷ D = 23.15 at D = 44.0 | D = measured OD of the lower (driven) pinch roller; confirm with the 1 m taped run |
| Camera centre line | X 350.0 | gantry and booth centre; reference for D\_mark |
| Camera line to nip | 290.0 | the nip is the last point that holds the cloth |
| D\_mark | not known | marker not in the CAD; if v2.5's 200 were kept the pen would sit at X 550, between idle shaft 2 (510.5) and the nip |
| Index step | along-view − 30 overlap | e.g. 160 (3704 steps) with the lens 240 above the cloth |
| Focus plane | Z 267.0 | cloth, 7.5 above the floor top |
| Cloth edges | Y 45 and 345 | 15 of lit floor beside each edge, so both edges should show in the back-light photo; confirm on the first photos |

- v2.5's message `MOVE,6945` (150 at 1/16 step) is obsolete; use the 1/8-step numbers above.
- Nothing in this CAD changes the Rev E electrical design or pin map.
