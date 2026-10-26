# Data provenance

## Dataset
NASA C-MAPSS Turbofan Engine Degradation Simulation Data Set, subset FD001.

## Source
- Provider: NASA Ames Prognostics Center of Excellence (Prognostics Data Repository)
- Obtained from: https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data
- Downloaded on: 26/10/26
- Original archive: CMAPSSData.zip (contains FD001 to FD004; only FD001 is used here)

## Citation
- Dataset: Saxena, A. and Goebel, K. (2008). "Turbofan Engine Degradation
  Simulation Data Set", NASA Ames Prognostics Data Repository, NASA Ames
  Research Center, Moffett Field, CA.
- Simulation method: Saxena, A., Goebel, K., Simon, D. and Eklund, N. (2008).
  "Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation",
  Proceedings of the 1st International Conference on Prognostics and Health
  Management (PHM08), Denver, CO.

## Usage terms
 No explicit licence or usage terms were stated on the NASA repository page
   when checked on 26/10/26. The data is publicly released by NASA for
   prognostics research. It is used here for non-commercial educational
   purposes with attribution (see Citation). The repository's software licence
   does not apply to these data files.

## Files in this folder
| File | Description |
| --- | --- |
| train_FD001.txt | 100 engines, run to failure (20,631 rows) |
| test_FD001.txt | 100 engines, truncated before failure (13,096 rows) |
| RUL_FD001.txt | True remaining useful life for each test engine (100 values, in test engine order) |
| readmeFD001.txt | NASA's original readme (renamed from readme.txt; it describes all four subsets) |

## Format
- Plain text, space-separated, no header, 26 columns per row.
- Columns: engine ID, cycle number, operational settings 1 to 3, sensors 1 to 21.
- Training data has no RUL column. It is derived in code as
  (last cycle of the engine) minus (current cycle).

## Characteristics (FD001)
- Simulated data, not measurements from real engines.
- One operating condition (sea level), one fault mode (HPC degradation).
- Data contains sensor noise. Seven columns are constant in the training set
  (setting_3, sensors 1, 5, 10, 16, 18, 19).

## Integrity
SHA-256 checksums of the files as extracted from the original zip:
- train_FD001.txt: 963b5e22825b34d8b21c69e1aeb4af3e647050eb672ee8834ba4b5d91d2de0f8
- test_FD001.txt:  3cda7109ce17bafb5443f2ac926cfcf88154b941b8c4cf95eb55d1ddd6f52851
- RUL_FD001.txt:   a19c8ec94931949d0485bdc35118206e9c81c4547b422efb9cf86f4ceddbceca
Note: Git on Windows may alter line endings in your working copy, so checksums
of local files can differ from these. Compare against the original zip.

## Known issues
- NASA's readme refers to "sensor measurement 26" for the last column. The
  layout is 2 ID columns + 3 settings + 21 sensors = 26 columns.
- NASA's readme is not UTF-8 encoded (read it as latin-1 if needed).