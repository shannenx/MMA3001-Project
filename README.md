# MMA3001 Project: Predicting Remaining Useful Life of Turbofan Engines (C-MAPSS FD001)

Numerical Methods and Machine Learning (MMA3001), 2026. Author: **[YOUR NAME / STUDENT ID]**

## 1. Summary

This project predicts the **Remaining Useful Life (RUL)**, the number of operating cycles left before failure, of simulated turbofan engines using the NASA C-MAPSS **FD001** subset (Saxena and Goebel, 2008). It compares a mean baseline, linear regression, ridge regression, random forest and histogram gradient boosting, first on single-cycle sensor readings and then on **windowed features** (last value, mean and slope of each sensor over the final 30 cycles). Models are validated with engine-grouped cross-validation, the test set is used once, and the cost (time, memory, scaling) of the selected pipeline is analysed.

The project scope (FD001 only) was approved by the Unit Coordinator.

## 2. Scope and limitations

- **FD001 only.** One operating condition and one fault mode (high-pressure compressor degradation). Results do not claim to carry over to FD002 to FD004.
- **Simulated data.** The engines are simulated, not real, so performance on real engines may differ.
- **RUL cap.** Training targets are capped at 125 cycles because sensor readings are flat early in an engine's life. Scoring against a capped target favours caps near the one chosen, so this is a modelling choice, not a neutral one (see notebook 02).
- **Window length.** Windows need `W` complete cycles, so `W` is limited to the shortest test engine (31 cycles). `W = 30` was chosen. No padding is applied.
- **Memory figures** come from `tracemalloc`, which is a lower bound on true memory use. FLOP and arithmetic-intensity figures are hand estimates.

## 3. Inputs and outputs

**Inputs**

| File (in `data/`) | Contents |
|---|---|
| `train_FD001.txt` | 100 engines run to failure (20,631 rows) |
| `test_FD001.txt` | 100 engines stopped before failure (13,096 rows) |
| `RUL_FD001.txt` | True remaining life at the end of each test engine (100 values) |

Each row has 26 columns: engine, cycle, 3 operational settings and 21 sensors.

**Outputs**

- A predicted RUL for each of the 100 test engines.
- Metrics: RMSE, MAE and the asymmetric PHM08 NASA score (late predictions are penalised more).
- Validation diagnostics, performance measurements and the decision tables in the notebooks.

Function-level inputs and outputs are documented in `docs/api/` (see section 9).

## 4. Repository structure

```
MMA3001-Project/
├── data/                 NASA C-MAPSS FD001 files + provenance note (data/README.md)
├── src/                  Source code (documented with docstrings)
│   ├── data_loader.py    Load and validate FD001, build RUL labels
│   ├── features.py       Sensor selection
│   ├── windows.py        Windowed features (last, mean, std, slope)
│   ├── models.py         Baseline and tree models
│   ├── evaluation.py     Metrics and engine-grouped cross-validation
│   └── benchmark.py      Timing, memory and scaling helpers
├── tests/                pytest test suite
├── notebooks/            Analysis, run in order 01 to 05
├── docs/
│   ├── api/              HTML documentation generated with pdoc
│   └── test_report.txt   pytest report
├── pytest.ini
├── requirements.txt
├── LICENSE
└── README.md
```

## 5. Setup

Developed with **Python 3.14.7** on Windows (Git Bash).

```bash
git clone https://github.com/shannenx/MMA3001-Project.git
cd MMA3001-Project

py -m venv .venv                # on Linux/macOS: python3 -m venv .venv
source .venv/Scripts/activate   # on Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Package versions are pinned in `requirements.txt`. Different scikit-learn versions can change cross-validation splits and therefore the exact numbers.

## 6. Reproducing the results

1. Run the tests: `python -m pytest` (expected: all tests pass; the saved report is `docs/test_report.txt`).
2. Start Jupyter from the repository root (so `import src` works): `python -m jupyter notebook`
3. Run the notebooks **in order**, using Kernel > Restart & Run All:

| Notebook | Purpose |
|---|---|
| `01_exploration.ipynb` | Data checks, constant sensors, correlations with RUL |
| `02_baselines.ipynb` | RUL cap, feature choice, baseline model comparison |
| `03_validation_diagnostics.ipynb` | Train vs validation gap, out-of-fold errors, error by RUL band |
| `04_windowed_features.ipynb` | Window length, statistics, decision table, one-time test evaluation |
| `05_performance.ipynb` | Timing, memory, profiling, scalability, accuracy vs cost |

4. Regenerate the HTML documentation: `python -m pdoc src -o docs/api`

All random seeds are fixed (`RANDOM_SEED = 0` in `src/models.py`). Timing results depend on the machine and will vary between runs.

## 7. Data

The data is the NASA C-MAPSS turbofan engine degradation simulation data set (Saxena and Goebel, 2008), downloaded from the NASA Prognostics Data Repository. See `data/README.md` for provenance. No explicit licence was found on the NASA page; the data is redistributed here for coursework only. **The MIT licence in this repository covers the code, not the NASA data.**

## 8. Method and validation design

- **RUL labels:** last cycle minus current cycle for each training engine, capped at 125.
- **Features:** 14 informative sensors. Sensors 1, 5, 6, 10, 16, 18 and 19 are constant or near-constant, and the operational settings are dropped (single operating condition, no relationship with RUL).
- **Windowed features:** last value, mean and least-squares slope of each sensor over the last 30 cycles of one engine, with no look-ahead.
- **Validation:** `GroupKFold` by engine (never row splits, which would leak an engine's cycles across folds). Scalers live inside pipelines so they are fit on training folds only.
- **Test set:** touched once, after all decisions were recorded in notebook 04.
- **Model choice:** histogram gradient boosting, chosen over random forest for similar accuracy at far lower training cost.

## 9. Results

Test-set results (100 engines, single evaluation, histogram gradient boosting):

| Features | RMSE | MAE | NASA score |
|---|---|---|---|
| Single cycle | 18.72 | 13.42 | 1031.72 |
| 30-cycle window (last + mean + slope) | 13.82 | 10.24 | 268.33 |

Windowed features reduce error and, more importantly, cut the NASA score sharply, meaning far fewer dangerous late predictions. Full validation tables, error-by-band analysis, performance measurements and the decisions behind each choice are in the notebooks.

Validation results (5-fold engine-grouped cross-validation, notebook 05):

| Configuration | RMSE (mean ± std) | NASA score | Fit time | Model size |
|---|---|---|---|---|
| Baseline: single cycle, gradient boosting | 19.54 ± 0.71 | 47,843 | 0.66 s | 320 KiB |
| Selected: 30-cycle window, gradient boosting | 13.12 ± 0.28 | 11,278 | 1.22 s | 425 KiB |
| 30-cycle window, linear regression | 16.99 ± 0.88 | 16,037 | 0.03 s | 1 KiB |

**Performance analysis (notebook 05).** Timings are medians of repeated runs on one computer and vary by about 5% between runs.

- The selected model builds its features in about 0.06 s, fits in about 1.2 s, predicts in under 0.2 ms per engine, and peaks at about 14 MiB during fitting (`tracemalloc`, a lower bound). Compared with the baseline it costs about 1.9x the fit time and 2.2x the peak memory, which is small in absolute terms.
- Fit time is dominated by tree growing (finding the best split at each node), not by feature construction.
- Window feature construction is memory bound by an order-of-magnitude estimate: about 0.18 FLOP/byte as implemented (2.7 if each value were moved once), against an assumed typical machine balance of roughly 5 FLOP/byte.
- Optimisation: the vectorised window code is about 249x faster than a straightforward loop (10 engines), and removing per-engine pandas overhead (found by profiling) sped up the training windows 3.2x and the test final windows 17x, with identical output. This has little effect on total run time because fitting dominates.
- Scalability (25 to 100 engines): gradient boosting fit time grows with an empirical exponent of about 0.16 and linear regression about 0.72. Four points over a narrow range, so treat these as approximate.

> **[CHECK]** These numbers come from your own notebook runs. Confirm they match your final outputs before submitting.

## 10. Documentation and tests

- **API documentation (HTML):** open `docs/api/src.html` (generated with pdoc from the docstrings).
- **Tests:** `tests/` (unit tests for the loader, evaluation, windowing and benchmarking helpers); report in `docs/test_report.txt`.

## 11. Use of AI

AI assistance was permitted for this project. Every AI interaction is recorded in the AI use log: **[LINK TO AI LOG DOCUMENT]**. All decisions recorded in the notebooks were reviewed and checked by the author.

## 12. References

- Saxena, A. and Goebel, K. (2008). *Turbofan Engine Degradation Simulation Data Set*. NASA Prognostics Data Repository, NASA Ames Research Center.
- Saxena, A., Goebel, K., Simon, D. and Eklund, N. (2008). Damage propagation modeling for aircraft engine run-to-failure simulation. *International Conference on Prognostics and Health Management (PHM08)*.

## 13. Notes

- **Line endings:** Git on Windows may print "LF will be replaced by CRLF" warnings. These are harmless.

## 14. Licence

Code: MIT (see `LICENSE`). NASA data: see section 7.
