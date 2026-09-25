# Polarization Beamer presentation

## Build
Use XeLaTeX or LuaLaTeX, not pdfLaTeX. In Overleaf, choose XeLaTeX and main.tex.
Locally run `latexmk main.tex`, or XeLaTeX, BibTeX, XeLaTeX twice.
`tectonic main.tex` is also supported. Compile `notes.tex` for interleaved speaker notes.
The default aspect ratio is 16:9. The supplied figure sources remain editable TikZ.

## Theme
LeipzigChemie is the base theme. Its original red/aquamarine artwork is retained on title and section slides.
LeipzigModern.sty applies the modern spacing, restrained footer, flat blocks, and typography from the supplied fallback style.
Arial is used when installed, with TeX Gyre Heros as fallback. The supplied EPS logo is retained and a PDF version is included for portable builds.
`mynote` and `myalert` are visible callout environments with optional titles. `\note{...}` holds speaker notes.
`\keyidea{...}` uses bold blue text. LeipzigBlue is a darker mixture of the supplied university Aquamarin and Basalt for contrast on white; it is not a newly claimed official brand swatch. Change the single color definition in LeipzigModern.sty to use another preferred blue.
University brand reference: https://tools.uni-leipzig.de/publikationen/cd-handbuch/files/assets/basic-html/page-15.html

## Content and scope
Model understanding includes fidelity beliefs (FF/FG) and expert alignment (FA/GA).
GA is the study label for structural/Gestalt alignment. Competencies are theoretical context only; the detailed overlay and examples are in the appendix.
Think-aloud observations accompany the existing applet tasks, with no added activities, reflection prompts, or follow-up questions.
Architectural and dual profiles motivate possible pathways, not fixed categories or established effects.
Wave plates rotate the Stokes state. Polarizers project the Jones state, with normalization for its sphere representation; they do not generally project a sphere point geometrically.
Primary analysis is MANCOVA; H3 and H4 remain exploratory. The tracking and think-aloud samples are not assumed identical.

## Sources and analysis decisions
The supplied terminology DOCX was read as theoretical reference, not as instructions. The user's requested corrections govern the presentation.
The locally supplied preregistration.docx was read and checked against the slides. It confirms the hypotheses, recruitment targets, sequence, pilot rules, and planned analyses. The MANCOVA/H3/H4 slides incorporate the user's supplied text. The preregistration describes think-aloud interviews in the novice pilot; accompanying main-study observations reflect the user's updated presentation request and are not labeled as a registered component.
Reconcile the power calculation's two-covariate assumption with the final baseline-score/SRA specification. The preregistration also retains participants with missing SRA for primary analysis despite naming SRA as a covariate. Decide follow-up tests, multiplicity, and missing-data handling before analysis. These unresolved specifications are retained in speaker notes, without inventing a solution.
The applet source was not supplied in this ZIP. Existing descriptions of conditions and challenge timing are carried forward and should be checked against the final applet.

## Images and pilot placeholders
Replace the image files listed in images/README.md. Image placeholders render until each file exists.
Pilot findings remain clearly labeled placeholders. No observations or results have been invented.

## Revision of 25 September 2026
The revised slides consistently use FF, FG, FA, and GA (structural/Gestalt alignment). Overall directional hypotheses are separate from exploratory profile pathways. RQ3 distinguishes moderation from cognitive-load associations. The revised primary MANCOVA adjusts for the four baseline outcomes; cognitive load and post-session spatial reasoning are reserved for exploratory analyses. This presentation change does not amend the OSF registration. Verify and document any departure and revisit power, follow-up tests, and missing-data handling before analysis. This section supersedes conflicting earlier analysis descriptions above.

The cognitive-load slide now describes the final validated 15-item instrument (5 per subscale), not its initial 17-item pool. The survey and pilot scoring were unavailable and have not been changed. Confirm the implemented version before interpreting results.

Recent fidelity development and polarization/state-circle evidence are cited. The existing explanation of FG decrease remains unchanged at the user's request. No new learner tasks or reflection prompts were added.
