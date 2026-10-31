# MMA3001 – AI Use Log and Reflection

**Student:** [Name / ID]
**Unit:** MMA3001 Numerical Methods and Machine Learning
**Project:** Predicting Remaining Useful Life of turbofan engines (NASA C-MAPSS FD001)
**GitHub repository:** https://github.com/shannenx/MMA3001-Project
**Log started:** 26 October 2026

> **DRAFT: author must verify.** Entries 2 to 10 were reconstructed from my conversation with the AI. Fill in every `[date]` and `[ ]`, change anything that does not match what actually happened, and delete the `[CHECK]` notes and this banner once confirmed.

---

## 1. Purpose and how to use this log

This log records every material use of AI during the project, as required by Section 7 of the project brief. It is designed so the final AI reflection in the report can be written directly from it. The brief states that disclosure does not replace verification, and that AI cannot be used during the presentation and interview. The log therefore focuses on what I checked, what I changed, and what I understood, not only on what the AI produced.

## 2. AI tools used

| Tool and version | Access | Main purposes |
|---|---|---|
| Claude Sonnet 5.5 (claude.ai) | Web chat with code-execution and file tools | Project planning, log structure, code and test generation, notebooks, concept explanations, Git/environment troubleshooting, documentation and README drafting |

## 3. Summary table of entries

| # | Date | Task category | AI contribution | Verified by | Commit / file |
|---|---|---|---|---|---|
| 1 | 26 Oct 2026 | Planning / documentation | Minimal (structure suggestions only) | Checked against project brief Section 7 and rubric | n/a |
| 2 | [date] | Planning | Minimal | Checked against the brief; scope approved by the Unit Coordinator | n/a |
| 3 | [date] | Other (repository set-up) | Moderate | Ran the commands; checked the NASA page for a licence | `.gitignore`, `LICENSE`, `data/README.md` |
| 4 | [date] | Code generation, Testing, Debugging | Substantial | Ran `pytest` myself; listed folders to find the missing test file | `src/data_loader.py`, `tests/test_data_loader.py` |
| 5 | [date] | Concept explanation | Moderate | Compared statements against my own plots and tables | `notebooks/01_exploration.ipynb` |
| 6 | [date] | Method selection, Code generation | Substantial | Ran notebooks myself; compared against my own tables | `src/evaluation.py`, `src/models.py`, `notebooks/02_baselines.ipynb` |
| 7 | [date] | Validation design | Moderate | Interpreted my own train/validation table | `notebooks/03_validation_diagnostics.ipynb` |
| 8 | [date] | Method selection, Code generation, Testing | Substantial | Ran notebook; compared my own test results from notebooks 02 and 04 | `src/windows.py`, `tests/test_windows.py`, `notebooks/04_windowed_features.ipynb` (commit `094d789`) |
| 9 | [date] | Performance and profiling | Substantial | Ran notebook; checked identical outputs and tests | `src/benchmark.py`, `tests/test_benchmark.py`, `notebooks/05_performance.ipynb` |
| 10 | 28 Oct 2026 | Documentation | Substantial | Checked pdoc requirement against the brief; all tests passed | `docs/api/` (commit `b22701e`), `docs/test_report.txt`, `README.md` |

**Task categories:** Planning, Concept explanation, Method selection, Code generation, Debugging, Testing, Validation design, Performance and profiling, Documentation, Report writing, Other.
**AI contribution levels:** None, Minimal (suggestions only), Moderate (AI drafted, student substantially rewrote), Substantial (AI drafted, student reviewed and adapted), Majority (AI produced most of it).

## 4. Detailed log entries

### Entry 1: Setting up the AI log

- **Date:** 26 October 2026
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Planning / documentation
- **Prompt (summary):** Said I was starting a project for a numerical methods and machine learning unit and wanted a log to track all my conversations with AI. Then uploaded the MMA3001 project brief and asked for the log to be integrated into a document I can use at the end of the discussion.
- **AI response (summary):** Suggested logging date and tool, prompt, response, how it was used, verification and reflection. Offered format options (Markdown/Word, spreadsheet, Git repo). After the brief was uploaded, built this document with fields mapped to the brief's AI reflection requirements.
- **What I kept / changed / rejected:** [Complete: e.g. kept the field structure; changed the categories to suit my project]
- **Verification:** Compared the fields against the eight reflection points in Section 7 of the brief and the AI rubric row. [Confirm and add anything else you checked]
- **Errors or limitations noticed:** [None so far / add any]
- **Decisions that remained my responsibility:** Choice of project, scope, and what to record in the log.
- **Effect on my understanding or workflow:** [Complete after reflection]
- **Approximate AI contribution:** Minimal to moderate (structure of the log document).

### Entry 2: Dataset choice and scope

- **Date:** [date]
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Planning
- **Prompt (summary):** Asked whether NASA C-MAPSS FD001 (Saxena and Goebel, 2008) matches the brief's requirements, and whether I could use FD001 alone instead of all four subsets.
- **AI response (summary):** Compared the dataset against the brief's criteria and explained the four subsets (FD001: one operating condition, one fault mode).
- **What I kept / changed / rejected:** I chose FD001 only.
- **Verification:** The scope was already approved by the Unit Coordinator. [CHECK: add approval date or wording]
- **Errors or limitations noticed:** The AI could not confirm the approval itself; that came from my own discussion with the coordinator.
- **Decisions that remained my responsibility:** Dataset and scope.
- **Effect on my understanding or workflow:** [ ]
- **Approximate AI contribution:** Minimal.

### Entry 3: Repository set-up, `.gitignore`, licence and data provenance

- **Date:** [date]
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Other (repository set-up)
- **Prompt (summary):** Asked how to add a Python `.gitignore` afterwards and why it matters, how to import the FD001 data, how to commit and push from Git Bash, and what a data provenance note should say.
- **AI response (summary):** Step-by-step Git commands, an explanation of `.gitignore`, and a template provenance note for `data/README.md`.
- **What I kept / changed / rejected:** I moved the data files into `data/` and wrote the provenance note myself. I chose the MIT licence for my **code only**; it does not cover the NASA data.
- **Verification:** Checked the NASA page and found **no explicit licence**, so the note says so honestly. Asked about a garbled push in my terminal; the AI explained the output and that out-of-order commits are acceptable, so I did not rewrite history.
- **Errors or limitations noticed:** [None noticed / add any]
- **Decisions that remained my responsibility:** Licence choice, what to state about the data's licence, and what to commit.
- **Effect on my understanding or workflow:** [ ]
- **Approximate AI contribution:** Moderate.

### Entry 4: Python environment and data loader

- **Date:** [date]
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Code generation, Testing, Debugging
- **Prompt (summary):** Asked for help creating the data loader and getting `pip` and `pytest` working in Git Bash on Windows.
- **AI response (summary):** `load_fd001` and `add_rul` with validation checks (26 columns, no NaNs, consecutive cycles, RUL file length), plus explanations of the `py` launcher, `.venv` and `requirements.txt`.
- **What I kept / changed / rejected:** I created and activated `.venv`, installed the packages and ran the tests myself.
- **Verification:** My `pytest` count was lower than the AI predicted (21, then 40). The AI's first guess about the cause was wrong; the real cause was that `test_data_loader.py` was in the repo root instead of `tests/`. I moved it and then saw 40 passed. I confirmed the cause by listing the folder rather than trusting the guess.
- **Errors or limitations noticed:** The AI's wrong guess about the missing tests (above).
- **Decisions that remained my responsibility:** What to commit, and accepting the loader's validation rules.
- **Effect on my understanding or workflow:** [ ]
- **Approximate AI contribution:** Substantial.

### Entry 5: Exploration (notebook 01) and sensor decisions

- **Date:** [date]
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Concept explanation
- **Prompt (summary):** Asked for feedback on my own written takeaways from notebook 01, and whether to drop operational settings 1 and 2.
- **AI response (summary):** Corrected parts of my reading, explained the rules for constant sensors, why a small standard deviation alone is not a valid reason to drop a feature, and why sensors 4, 7, 11, 12, 15 and 21 correlate most strongly with RUL.
- **What I kept / changed / rejected:** I dropped constant or near-constant sensors (1, 5, 6, 10, 16, 18, 19). I wanted to drop the settings because of their small standard deviation; I replaced that reasoning with the AI's point that they have no relationship with RUL and the data has a single operating condition. [CHECK]
- **Verification:** Compared the statements against my own plots and tables.
- **Errors or limitations noticed:** [None noticed / add any]
- **Decisions that remained my responsibility:** Which sensors and settings to keep.
- **Effect on my understanding or workflow:** [ ]
- **Approximate AI contribution:** Moderate.

### Entry 6: Baselines (notebook 02) and model choice

- **Date:** [date]
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Method selection, Code generation
- **Prompt (summary):** Asked what `fit_s` means, how histogram gradient boosting and random forest work (tied back to my Week 5 decision-tree notes), and which baseline to carry forward.
- **AI response (summary):** `src/evaluation.py` (RMSE, MAE, PHM08 NASA score, engine-grouped cross-validation), `src/models.py`, and plain-language explanations.
- **What I kept / changed / rejected:** I summarised forests as averaged overfit trees and boosting as sequential underfit trees. I chose gradient boosting (lowest RMSE, much faster), briefly considered random forest as more reliable, and stayed with gradient boosting after the AI ran the comparison. I chose a RUL cap of 125 because it gave the lowest error.
- **Verification:** Ran the notebook myself and compared the results with my own tables.
- **Errors or limitations noticed:**
  1. Cross-validation compared RUL caps against different evaluation targets, which is unfair. The AI added an `eval_cap` option.
  2. The AI labelled sensors 8, 13 and 17 "noisy". That was wrong: removing them **raised** validation error. It acknowledged this and I did not use the label.
  3. I first misunderstood the cap result and the sensor-removal result; the AI clarified them.
- **Decisions that remained my responsibility:** Model choice, RUL cap, sensor set.
- **Effect on my understanding or workflow:** [ ]
- **Approximate AI contribution:** Substantial.

### Entry 7: Validation diagnostics (notebook 03)

- **Date:** [date]
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Validation design
- **Prompt (summary):** Asked whether linear regression looked better than gradient boosting, whether gradient boosting had memorised noise, whether linear regression overfits, and whether OLS is adequate versus ridge.
- **AI response (summary):** Added plain linear regression, training-error measurement and an error-versus-RUL plot to the code, and explained train-versus-validation gaps.
- **What I kept / changed / rejected:** My conclusions from my own table: gradient boosting overfits mildly (train 15.97 vs validation 18.73); linear regression underfits (21.47 vs 21.66) and ridge gives identical numbers, so OLS is adequate. I wrote these in my observation boxes. [CHECK: numbers match your table]
- **Verification:** Interpreted my own train/validation table and plots.
- **Errors or limitations noticed:** The AI misread "add this first" and began adding the wrong cells; I interrupted and clarified what I meant.
- **Decisions that remained my responsibility:** Interpretation of the diagnostics and the OLS-versus-ridge conclusion.
- **Effect on my understanding or workflow:** [ ]
- **Approximate AI contribution:** Moderate.

### Entry 8: Windowed features (notebook 04)

- **Date:** [date]
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Method selection, Code generation, Testing
- **Prompt (summary):** Asked why the window must be shorter than the shortest engine, the benefit of larger windows, how null values affect averages, what the sensitivity table means, what the statistics (last, mean, std, slope) mean, and which to choose.
- **AI response (summary):** `src/windows.py` (windows use one engine only, never look ahead, complete windows only, error if an engine is shorter than the window) with tests, and notebook 04.
- **What I kept / changed / rejected:** W = 30 (the shortest test engine has 31 cycles); all 14 sensors and no operational settings; statistics last + mean + slope. I noticed that adding the mean changed the values significantly and asked about it. I corrected my decision table after review (statistics row, window row, model name typo).
- **Verification:** Ran the notebook myself and compared my own test-set results from notebooks 02 and 04 (single-cycle RMSE 18.72 vs windowed 13.82).
- **Errors or limitations noticed:** My numbers differed from the AI's own runs because of a scikit-learn version difference, so I used only my own outputs.
- **Decisions that remained my responsibility:** Window length, statistics, sensor set and the decision table.
- **Effect on my understanding or workflow:** [ ]
- **Approximate AI contribution:** Substantial.

### Entry 9: Performance analysis (notebook 05)

- **Date:** [date]
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Performance and profiling
- **Prompt (summary):** Asked to start the performance analysis, for help running the notebook, and for explanations of the profiler output, the optimisation table, and how to tell compute-bound from memory-bound.
- **AI response (summary):** `src/benchmark.py` (timing, tracemalloc memory, scaling exponent) with tests, notebook 05, and explanations of `cProfile` columns, arithmetic intensity and machine balance.
- **What I kept / changed / rejected:** I ran the notebook, quoted my own numbers and wrote my own observations and summary table.
- **Verification:** Checked that the old and new window code give identical output and that all tests pass.
- **Errors or limitations noticed:**
  1. The AI first blamed the slow `last_window_rows` on building too many windows. Profiling showed the real cause was pandas overhead; the code was rewritten with NumPy arrays (identical outputs, tests still pass).
  2. In my summary table I used "about 0.4 FLOP/byte", which was only the AI's illustrative example. My notebook's own values are 2.7 (ideal) and 0.18 (as implemented); the AI pointed this out and I corrected it.
  3. The AI flagged that my accuracy-versus-cost row described the trade-off in the wrong direction.
- **Decisions that remained my responsibility:** Conclusions in the summary table, and which numbers to report.
- **Effect on my understanding or workflow:** [ ]
- **Approximate AI contribution:** Substantial.

### Entry 10: Documentation, test report and README

- **Date:** 28 October 2026
- **Tool:** Claude Sonnet 5.5 (claude.ai)
- **Task category:** Documentation
- **Prompt (summary):** Asked whether pdoc was actually required, how pdoc differs from Sphinx and MkDocs, for a draft main README, and for the notebook 05 findings to be added to it.
- **AI response (summary):** pdoc and pytest-report commands, a comparison of documentation tools, and the draft README. When I questioned whether pdoc was required, the AI checked the project brief and quoted the relevant lines (HTML documentation of source code; test functions and test report).
- **What I kept / changed / rejected:** I generated `docs/api` with pdoc, saved the pytest report, and committed and pushed. I edit and take responsibility for the README text. [CHECK]
- **Verification:** Confirmed the requirement in the brief; confirmed all 76 tests passed in `docs/test_report.txt`.
- **Errors or limitations noticed:** The README draft contained placeholders and results I had to confirm against my own outputs.
- **Decisions that remained my responsibility:** Final README content and what to include.
- **Effect on my understanding or workflow:** [ ]
- **Approximate AI contribution:** Substantial.

## 5. Final AI reflection (draft structure for the report)

The report must include an AI reflection covering the points below. Draft each paragraph from the log entries above, in terms of my own decisions.

1. **Which AI tools were used.** [ ]
2. **What they were used for.** [ ]
3. **Approximate level of AI contribution.** [Give an overall estimate and a breakdown by task, e.g. code, report, planning]
4. **Why AI was used for those tasks.** [ ]
5. **How AI-generated material was checked.** [Cite specific tests, benchmarks or comparisons from the log]
6. **Which important decisions remained my responsibility.** [Method selection, validation design, interpretation of results, acceptance criteria]
7. **Errors, limitations or unhelpful suggestions produced by AI.** [See entries 4, 6, 7, 9 and 10]
8. **How AI use affected my understanding or workflow.** [ ]

Because AI is not permitted during the presentation and interview, also note: **which parts of the project could I explain and defend without AI assistance, and how did I make sure of that?** [ ]

## 6. Pre-submission checklist

- [ ] Every material AI use has a log entry
- [ ] Each entry records how the output was verified
- [ ] At least some real AI errors or limitations are documented
- [ ] AI-assisted code in the repository is identifiable (commit messages or comments)
- [ ] The final reflection matches the log and covers all eight points
- [ ] Reflection fits the report's 10-page limit, with the full log placed in an appendix
- [ ] I can explain every method, parameter and result in my own words
- [ ] Log stored in the GitHub repository (`docs/AI_USE_LOG.md`) or attached as an appendix
