# MMA3001 – AI Use Log and Reflection

**Student:** Shannen Wedding, 32491948
**Unit:** MMA3001 Numerical Methods and Machine Learning
**Project:** Predicting Remaining Useful Life of turbofan engines (NASA C-MAPSS FD001)
**GitHub repository:** https://github.com/shannenx/MMA3001-Project
**Log started:** 26 October 2026  
**Last updated:** 31 October 2026

\---

## 1\. Purpose and how to use this log

This log records every material use of AI during the project, as required by Section 7 of the project brief. It is designed so the final AI reflection in the report can be written directly from it. The brief states that disclosure does not replace verification, and that AI cannot be used during the presentation and interview. The log therefore focuses on what I checked, what I changed, and what I understood, not only on what the AI produced.

## 2\. AI tools used

|Tool and version|Access|Main purposes|
|-|-|-|
|Claude Sonnet 5.5 (claude.ai)|Web chat with code-execution and file tools|Project planning, log structure, code and test generation, notebooks, concept explanations, Git/environment troubleshooting, documentation and README drafting|

## 3\. Summary table of entries

|#|Date|Task category|AI contribution|Verified by|Commit / file|
|-|-|-|-|-|-|
|1|26 October 2026|Planning / documentation|Minimal (structure suggestions only)|Checked against project brief Section 7 and rubric|n/a|
|2|26 October 2026|Planning|Minimal|Checked against the brief; scope approved by the Unit Coordinator|n/a|
|3|26 October 2026|Other (repository set-up)|Moderate|Ran the commands; checked the NASA page for a licence|`.gitignore`, `LICENSE`, `data/README.md`|
|4|26 October 2026|Code generation, Testing, Debugging|Substantial|Ran `pytest` myself; listed folders to find the missing test file|`src/data\_loader.py`, `tests/test\_data\_loader.py`|
|5|26 October 2026|Concept explanation|Moderate|Compared statements against my own plots and tables|`notebooks/01\_exploration.ipynb`|
|6|27 October 2026|Method selection, Code generation|Substantial|Ran notebooks myself; compared against my own tables|`src/evaluation.py`, `src/models.py`, `notebooks/02\_baselines.ipynb`|
|7|27 October 2026|Validation design|Moderate|Interpreted my own train/validation table; ran random forest myself (train 6.83, validation 18.87)|`notebooks/03\_validation\_diagnostics.ipynb`|
|8|28 October 2026|Method selection, Code generation, Testing|Substantial|Ran notebook; compared my own test results from notebooks 02 and 04|`src/windows.py`, `tests/test\_windows.py`, `notebooks/04\_windowed\_features.ipynb` (commit `094d789`)|
|9|28 October 2026|Performance and profiling|Substantial|Ran notebook; checked identical outputs and tests|`src/benchmark.py`, `tests/test\_benchmark.py`, `notebooks/05\_performance.ipynb`|
|10|28 Oct 2026|Documentation|Substantial|Checked pdoc requirement against the brief; all tests passed|`docs/api/` (commit `b22701e`), `docs/test\_report.txt`, `README.md`|
|11|28 to 29 Oct 2026|Debugging, Other (environment and Git)|Moderate|Ran every command myself; checked `git status`, `pytest` and the notebook outputs|`requirements.txt`, notebooks 01 and 04|
|12|30 to 31 Oct 2026|Report writing|Substantial (drafts)|Rewrote in my own words \[CHECK]; compared every number with my notebook outputs|Report (`MMA3001\_project`), `docs/AI\_USE\_LOG.md`|
|13|31 Oct 2026|Validation, Testing (review and fact-checking)|Substantial|Re-ran checks myself; compared the report with the brief and the notebooks|Report, notebooks 02, 03 and 05|
|14|29 to 31 Oct 2026|Concept explanation, presentation preparation|Moderate|Asked follow-up questions; compared answers with my notebooks and Week 5 notes|n/a|

**Task categories:** Planning, Concept explanation, Method selection, Code generation, Debugging, Testing, Validation design, Performance and profiling, Documentation, Report writing, Other.
**AI contribution levels:** None, Minimal (suggestions only), Moderate (AI drafted, student substantially rewrote), Substantial (AI drafted, student reviewed and adapted), Majority (AI produced most of it).

## 4\. Detailed log entries

### Entry 1: Setting up the AI log

* **Date:** 26 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Planning / documentation
* **Prompt (summary):** Said I was starting a project for a numerical methods and machine learning unit and wanted a log to track all my conversations with AI. Then uploaded the MMA3001 project brief and asked for the log to be integrated into a document I can use at the end of the discussion.
* **AI response (summary):** Suggested logging date and tool, prompt, response, how it was used, verification and reflection. Offered format options (Markdown/Word, spreadsheet, Git repo). After the brief was uploaded, built this document with fields mapped to the brief's AI reflection requirements.
* **What I kept / changed / rejected:** I kept the suggested outline for the log, and suggested to only generate the log at the end of larger milestones throughout the project, rather than after each step.
* **Verification:** Compared the fields against the eight reflection points in Section 7 of the brief and the AI rubric row.
* **Errors or limitations noticed:** None so far
* **Decisions that remained my responsibility:** Choice of project, scope, and what to record in the log.
* **Effect on my understanding or workflow:** Setting up the AI log, creating a running log of my interaction with AI.
* **Approximate AI contribution:** Minimal to moderate (structure of the log document).

### Entry 2: Dataset choice and scope

* **Date:** 26 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Planning
* **Prompt (summary):** Asked whether NASA C-MAPSS FD001 (Saxena and Goebel, 2008) matches the brief's requirements, and whether I could use FD001 alone instead of all four subsets.
* **AI response (summary):** Compared the dataset against the brief's criteria and explained the four subsets (FD001: one operating condition, one fault mode).
* **What I kept / changed / rejected:** I chose FD001 only.
* **Errors or limitations noticed:** The AI could not confirm the approval itself; that came from my own discussion with the coordinator.
* **Decisions that remained my responsibility:** Dataset and scope.
* **Effect on my understanding or workflow:** Helped set-up the beginning of my task.
* **Approximate AI contribution:** Minimal.

### Entry 3: Repository set-up, `.gitignore`, licence and data provenance

* **Date:** 
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Other (repository set-up)
* **Prompt (summary):** Asked how to add a Python `.gitignore` afterwards and why it matters, how to import the FD001 data, how to commit and push from Git Bash, and what a data provenance note should say.
* **AI response (summary):** Step-by-step Git commands, an explanation of `.gitignore`, and a template provenance note for `data/README.md`.
* **What I kept / changed / rejected:** I moved the data files into `data/` and wrote the provenance note myself. I chose the MIT licence for my **code only**; it does not cover the NASA data.
* **Verification:** Checked the NASA page and found **no explicit licence**, so the note says so honestly. Asked about a garbled push in my terminal; the AI explained the output and that out-of-order commits are acceptable, so I did not rewrite history.
* **Errors or limitations noticed:** -
* **Decisions that remained my responsibility:** Licence choice, what to state about the data's licence, and what to commit.
* **Effect on my understanding or workflow:** Setting up the repo, and how my actual coding was going to be organised. Helped me understand how this worked.
* **Approximate AI contribution:** Moderate.

### Entry 4: Python environment and data loader

* **Date:** 26 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Code generation, Testing, Debugging
* **Prompt (summary):** Asked for help creating the data loader and getting `pip` and `pytest` working in Git Bash on Windows.
* **AI response (summary):** `load\_fd001` and `add\_rul` with validation checks (26 columns, no NaNs, consecutive cycles, RUL file length), plus explanations of the `py` launcher, `.venv` and `requirements.txt`.
* **What I kept / changed / rejected:** I created and activated `.venv`, installed the packages and ran the tests myself.
* **Verification:** My `pytest` count was lower than the AI predicted (21, then 40). The AI's first guess about the cause was wrong; the real cause was that `test\_data\_loader.py` was in the repo root instead of `tests/`. I moved it and then saw 40 passed. I confirmed the cause by listing the folder rather than trusting the guess.
* **Errors or limitations noticed:** The AI's wrong guess about the missing tests (above).
* **Decisions that remained my responsibility:** What to commit, and accepting the loader's validation rules.
* **Effect on my understanding or workflow:** Helped me understand how to debug and use the git bash.
* **Approximate AI contribution:** Substantial.

### Entry 5: Exploration (notebook 01) and sensor decisions

* **Date:** 26 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Concept explanation
* **Prompt (summary):** Asked for feedback on my own written takeaways from notebook 01, and whether to drop operational settings 1 and 2.
* **AI response (summary):** Corrected parts of my reading, explained the rules for constant sensors, why a small standard deviation alone is not a valid reason to drop a feature, and why sensors 4, 7, 11, 12, 15 and 21 correlate most strongly with RUL.
* **What I kept / changed / rejected:** I dropped constant or near-constant sensors (1, 5, 6, 10, 16, 18, 19). I wanted to drop the settings because of their small standard deviation; I replaced that reasoning with the AI's point that they have no relationship with RUL and the data has a single operating condition. \[CHECK]
* **Verification:** Compared the statements against my own plots and tables.
* **Errors or limitations noticed:** -
* **Decisions that remained my responsibility:** Which sensors and settings to keep.
* **Effect on my understanding or workflow:** Notebooks assisted in the way I was able to break down the task, and understand all the parameters in isolation. It grew my understanding significantly, and tied in the theory I had been learning to the actual use of these parameters and concepts.
* **Approximate AI contribution:** Moderate.

### Entry 6: Baselines (notebook 02) and model choice

* **Date:** 27 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Method selection, Code generation
* **Prompt (summary):** Asked what `fit\_s` means, how histogram gradient boosting and random forest work (tied back to my Week 5 decision-tree notes), and which baseline to carry forward.
* **AI response (summary):** `src/evaluation.py` (RMSE, MAE, PHM08 NASA score, engine-grouped cross-validation), `src/models.py`, and plain-language explanations.
* **What I kept / changed / rejected:** I summarised forests as averaged overfit trees and boosting as sequential underfit trees. I chose gradient boosting (lowest RMSE, much faster), briefly considered random forest as more reliable, and stayed with gradient boosting after the AI ran the comparison. I chose a RUL cap of 125 because it gave the lowest error.
* **Verification:** Ran the notebook myself and compared the results with my own tables.
* **Errors or limitations noticed:**

  1. Cross-validation compared RUL caps against different evaluation targets, which is unfair. The AI added an `eval\_cap` option.
  2. The AI labelled sensors 8, 13 and 17 "noisy". That was wrong: removing them **raised** validation error. It acknowledged this and I did not use the label.
  3. I first misunderstood the cap result and the sensor-removal result; the AI clarified them.
* **Decisions that remained my responsibility:** Model choice, RUL cap, sensor set.
* **Effect on my understanding or workflow:** Same as entry 5.
* **Approximate AI contribution:** Substantial.

### Entry 7: Validation diagnostics (notebook 03)

* **Date:** 27 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Validation design
* **Prompt (summary):** Asked whether linear regression looked better than gradient boosting, whether gradient boosting had memorised noise, whether linear regression overfits, and whether OLS is adequate versus ridge.
* **AI response (summary):** Added plain linear regression, training-error measurement and an error-versus-RUL plot to the code, and explained train-versus-validation gaps.
* **What I kept / changed / rejected:** My conclusions from my own table: gradient boosting overfits mildly (train 15.97 vs validation 18.73); linear regression underfits (21.47 vs 21.66) and ridge gives identical numbers, so OLS is adequate. I wrote these in my observation boxes. \[CHECK: numbers match your table]
* **Verification:** Interpreted my own train/validation table and plots. Later I switched on `INCLUDE\_RANDOM\_FOREST` in notebook 03 and ran it myself: random forest training RMSE 6.83 against validation 18.87 (gap 12.04), against 15.97 and 18.73 for gradient boosting. This matched the AI's own run, but I quote only my numbers.
* **Errors or limitations noticed:** The AI misread "add this first" and began adding the wrong cells; I interrupted and clarified what I meant.
* **Decisions that remained my responsibility:** Interpretation of the diagnostics and the OLS-versus-ridge conclusion.
* **Effect on my understanding or workflow:** Same as entry 5.
* **Approximate AI contribution:** Moderate.

### Entry 8: Windowed features (notebook 04)

* **Date:** 28 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Method selection, Code generation, Testing
* **Prompt (summary):** Asked why the window must be shorter than the shortest engine, the benefit of larger windows, how null values affect averages, what the sensitivity table means, what the statistics (last, mean, std, slope) mean, and which to choose.
* **AI response (summary):** `src/windows.py` (windows use one engine only, never look ahead, complete windows only, error if an engine is shorter than the window) with tests, and notebook 04.
* **What I kept / changed / rejected:** W = 30 (the shortest test engine has 31 cycles); all 14 sensors and no operational settings; statistics last + mean + slope. I noticed that adding the mean changed the values significantly and asked about it. I corrected my decision table after review (statistics row, window row, model name typo).
* **Verification:** Ran the notebook myself and compared my own test-set results from notebooks 02 and 04 (single-cycle RMSE 18.72 vs windowed 13.82).
* **Errors or limitations noticed:** My numbers differed from the AI's own runs because of a scikit-learn version difference, so I used only my own outputs.
* **Decisions that remained my responsibility:** Window length, statistics, sensor set and the decision table.
* **Effect on my understanding or workflow:** Same as entry 5.
* **Approximate AI contribution:** Substantial.

### Entry 9: Performance analysis (notebook 05)

* **Date:** 28 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Performance and profiling
* **Prompt (summary):** Asked to start the performance analysis, for help running the notebook, and for explanations of the profiler output, the optimisation table, and how to tell compute-bound from memory-bound.
* **AI response (summary):** `src/benchmark.py` (timing, tracemalloc memory, scaling exponent) with tests, notebook 05, and explanations of `cProfile` columns, arithmetic intensity and machine balance.
* **What I kept / changed / rejected:** I ran the notebook, quoted my own numbers and wrote my own observations and summary table.
* **Verification:** Checked that the old and new window code give identical output and that all tests pass.
* **Errors or limitations noticed:**

  1. The AI first blamed the slow `last\_window\_rows` on building too many windows. Profiling showed the real cause was pandas overhead; the code was rewritten with NumPy arrays (identical outputs, tests still pass).
  2. In my summary table I used "about 0.4 FLOP/byte", which was only the AI's illustrative example. My notebook's own values are 2.7 (ideal) and 0.18 (as implemented); the AI pointed this out and I corrected it.
  3. The AI flagged that my accuracy-versus-cost row described the trade-off in the wrong direction.
* **Decisions that remained my responsibility:** Conclusions in the summary table, and which numbers to report.
* **Effect on my understanding or workflow:** Same as entry 5.
* **Approximate AI contribution:** Substantial.

### Entry 10: Documentation, test report and README

* **Date:** 28 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Documentation
* **Prompt (summary):** Asked whether pdoc was actually required, how pdoc differs from Sphinx and MkDocs, for a draft main README, and for the notebook 05 findings to be added to it.
* **AI response (summary):** pdoc and pytest-report commands, a comparison of documentation tools, and the draft README. When I questioned whether pdoc was required, the AI checked the project brief and quoted the relevant lines (HTML documentation of source code; test functions and test report).
* **What I kept / changed / rejected:** I generated `docs/api` with pdoc, saved the pytest report, and committed and pushed. I edit and take responsibility for the README text. 
* **Verification:** Confirmed the requirement in the brief; confirmed all 76 tests passed in `docs/test\_report.txt`.
* **Errors or limitations noticed:** The README draft contained placeholders and results I had to confirm against my own outputs.
* **Decisions that remained my responsibility:** Final README content and what to include.
* **Effect on my understanding or workflow:** Understood how pdoc was used, and had assistance in writing documentation that accompanied the code and report.
* **Approximate AI contribution:** Substantial.

### Entry 11: Environment, Git and notebook troubleshooting

* **Date:** 28 to 29 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Debugging, Other (environment and Git)
* **Prompt (summary):** Asked how to run the notebooks in a browser, how to open a new Git Bash, how to push my notebook 4 changes, how to refresh `requirements.txt`, what a screenshot of Git output meant, and what to do when notebook 01 question 4 failed because `scipy` was not installed.
* **AI response (summary):** Step-by-step commands for the `.venv` and Git, an explanation of each Git message, and the fix for the missing package (`python -m pip install scipy`, restart the kernel, refresh `requirements.txt`).
* **What I kept / changed / rejected:** I ran every command myself and decided what to commit.
* **Verification:** Checked the output of `git status` and `pytest` after each step.
* **Errors or limitations noticed:** -
* **Decisions that remained my responsibility:** What to commit and when to push.
* **Effect on my understanding or workflow:** Helped understand troubleshooting, and using Git.
* **Approximate AI contribution:** Moderate.

### Entry 12: Report writing

* **Date:** 30 to 31 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai), including its document tool
* **Task category:** Report writing
* **Prompt (summary):** Asked for a structured outline for the report and for help writing each section: the engineering context (from my own notes and four sources), the inputs, outputs and invalid-input handling, the computational approach, the alternative-methods tables, validation, performance (including the arithmetic-intensity working), the limitations and lessons learned, and a tidy-up of my own AI-reflection notes. I also asked for the explanation of the NASA score equation to be set out for Word.
* **AI response (summary):** Drafted sections and replacement text in a separate document from my notes, notebooks and README, with brackets where I had to decide or verify something. For the Word draft it suggested a layout for sections 5 and 6, corrected wording, and gave split equations and a picture fallback when the equation would not convert.
* **What I kept / changed / rejected:** I chose which text to use and reworded it. The profiling paragraph and the limitations and lessons-learned section are AI-drafted text that I have kept with only light changes so far (shown in red in my draft). I rejected suggestions I could not support from my own results.
* **Verification:** Compared every number with my own notebook outputs; used the brief to check that each required point was covered; looked at the four sources myself.
* **Errors or limitations noticed:**

  1. The AI stated that random forest was "about 70 times slower" and quoted a node count from its own run. My table showed about 12 times (5.489 s against 0.459 s). I used my own numbers and the AI corrected the document.
  2. The AI could not open the ScienceDirect article cited as source \[3], so it could not confirm what it says; it flagged the reference for me to check. It also pointed out that one claim in my notes (variation in lifespan) went beyond what the NASA source supports.
  3. The equation conversion for Word 2016/2019 did not work and I needed a fallback.
  4. Some explanations written by the AI for my own understanding were pasted into my draft as report text (for example, "For the report, you can say..."). The AI's review flagged them as notes, not report text.
* **Decisions that remained my responsibility:** The structure of the report, which claims to make, which text to keep, and every interpretation of the results.
* **Effect on my understanding or workflow:** Helped draft as had many dot points that needed to be put into the paragraphs and checked against the brief.
* **Approximate AI contribution:** Substantial (drafts); Initial wording was written by me, and final wording is also checked and altered by me.

### Entry 13: Review of the report against the brief, and fact-checking

* **Date:** 31 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Validation and verification (review), Testing
* **Prompt (summary):** Sent my draft report and asked for the fixes needed and whether it adheres to the brief, then asked for the windowed linear regression column of the performance table to be filled in, and for the arithmetic-intensity calculation to be explained again.
* **AI response (summary):** Checked the draft against each item of the brief and listed about 35 specific fixes, suggested which content to move to an appendix to stay within the page limit, filled the table column from my notebook 05 output, and re-derived the arithmetic-intensity values (22,341,060 FLOPs; 2.7 FLOP/byte if each value moved once; 0.18 as implemented) from the notebook's own formulas.
* **What I kept / changed / rejected:** I merged the windowed linear regression results into the performance table, moved the arithmetic-intensity working to Appendix A, and corrected the statements the AI found to be wrong (for example, the mean baseline's accuracy and the random forest RMSE comparison were written the wrong way round).
* **Verification:** Re-ran cross-validation myself to confirm that single-cycle gradient boosting scores 18.73 on all rows (Table 04) and 19.54 on rows from cycle 30 onwards (the table in section 6, where every configuration is scored on the same rows). Checked the hand calculation of memory sizes (2.2 and 5.7 MiB) against notebook 05.
* **Errors or limitations noticed:**

  1. The AI first suggested the 18.73 against 19.54 difference came from different environments or scoring targets. The real cause was the row subset, found only after re-running the cross-validation.
  2. The AI gave single-cycle linear regression as 21.76 in one fix and 21.66 elsewhere, without saying that they come from different row subsets (cycle 30 onwards and all rows).
  3. The AI wrote that the overlapping windows are copied in the "as implemented" arithmetic-intensity figure. The notebook shows the extra traffic is a temporary array used for the slope calculation (about 119 MB).
  4. The Appendix line "8 bytes per operation" was wrong (8 bytes per value), as the AI's later review noted. I corrected it.
  5. The AI-assisted wording for the statistics row of Table 02 said the mean was kept because it lowers the NASA score. My notebook 04 output shows the opposite (11,278 with the mean against 11,054 without). The AI's earlier reviews did not catch this; it was found only when the AI checked every report number against my notebooks. The mean was kept because it reduced the fold-to-fold spread (0.28 against 0.55). 
  6. My notebook 03 summary said models were biased early near failure. The AI's check against the band table showed the bias is positive (late) in the 0 to 25 band and largest at 26 to 75. I corrected the notebook.
* **Decisions that remained my responsibility:** Which corrections to accept and what the final report claims.
* **Effect on my understanding or workflow:** Reviewed my work against the brief, and tidied up report.
* **Approximate AI contribution:** Substantial.

### Entry 14: Concept explanations and presentation preparation

* **Date:** 29 to 31 October 2026
* **Tool:** Claude Sonnet 5.5 (claude.ai)
* **Task category:** Concept explanation, presentation preparation
* **Prompt (summary):** Asked for plain-language explanations of float64 against float32, RMSE and MAE, the NASA score, ridge against ordinary least squares, what a flat training and validation RMSE means, what the `src/` package and each module does, the mean baseline, no look-ahead, engine-grouped five-fold cross-validation, sweeps, the RUL cap (and why scoring against a capped target favours caps near it), compute-bound against memory-bound, arithmetic intensity, scalability exponents, and what a fixed seed means. Also asked for draft answers to practice interview questions.
* **AI response (summary):** Explanations with small worked examples, tied to my notebook numbers and Week 5 notes, and draft answers to the practice questions.
* **What I kept / changed / rejected:** I used the explanations to rewrite my own report sentences and to prepare my own answers.
* **Verification:** Asked follow-up questions until I could explain each idea; compared the explanations with my notebooks and course notes. 
* **Errors or limitations noticed:** The AI's illustrative cap example used invented numbers, which it labelled as a toy example. 
* **Decisions that remained my responsibility:** What I say in the presentation and interview, and which explanation I rely on.
* **Effect on my understanding or workflow:**-
* **Approximate AI contribution:** Moderate.

## 5\. Final AI reflection (draft structure for the report)

The report must include an AI reflection covering the points below. Draft each paragraph from the log entries above, in terms of my own decisions.

1. **Which AI tools were used.** Claude Sonnet 5.5 (Anthropic), through claude.ai, with its document tool. No other AI tool was used. 
2. **What they were used for.** Planning and scoping, code and tests, notebooks, concept explanations, Git and environment help, documentation (README, pdoc, test report), report drafting and review against the brief, and practice for the presentation (entries 1 to 14).
3. **Approximate level of AI contribution.** Moderate. Some aspects were more substantial like coding and debugging, some were moderate like report drafting and clarifications, and some were low, such as the dataset scope.
4. **Why AI was used for those tasks.** AI is efficient at coding, and is able to spot errors in document writing that I may not have been able to notice.
5. **How AI-generated material was checked.** External sources, and verification against course notes. Checking against my own data and judgement
6. **Which important decisions remained my responsibility** Interpretation of results and the initial scoping of the task, including inputs and outputs.
7. **Errors, limitations or unhelpful suggestions produced by AI.** See entries 4, 6, 7, 9, 10, 12 and 13. Examples: a wrong guess about missing tests (entry 4); an unfair comparison of caps and a wrong "noisy sensors" label (entry 6); a wrong diagnosis of slow code (entry 9); an illustrative arithmetic intensity of 0.4 FLOP/byte that I nearly copied into my summary (entry 9); a random forest fit-time ratio of about 70 times that disagreed with my own table (entry 12); a wrong first explanation of why two cross-validated RMSEs differed (entry 13); and wording that the mean statistic lowers the NASA score, which my own output contradicted (entry 13).
8. **How AI use affected my understanding or workflow.** It allowed me to break down a large task into smaller pieces, and aided in making decisions that led to a model that became iteratively better.

Because AI is not permitted during the presentation and interview, also note: **which parts of the project could I explain and defend without AI assistance, and how did I make sure of that?** After writing the report, I feel I have a substantial understanding about why I have made all the decisions I have, and how AI has assisted me in generating content for this assignment. I understand what it has generated, and why.

## 6\. Pre-submission checklist

* \[ ] Every material AI use has a log entry (entries 1 to 14)
* \[ ] Each entry records how the output was verified
* \[ ] At least some real AI errors or limitations are documented
* \[ ] AI-assisted code in the repository is identifiable (commit messages or comments)
* \[ ] The final reflection matches the log and covers all eight points
* \[ ] Reflection fits the report's 10-page limit, with the full log placed in an appendix
* \[ ] Text in my report that was drafted by the AI (shown in red) is reworded in my own words, and entry 12 says how much I changed
* \[ ] I can explain every method, parameter and result in my own words
* \[ ] Log stored in the GitHub repository (`docs/AI\_USE\_LOG.md`) or attached as an appendix

