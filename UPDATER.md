# PressBox daily updater — reference

PressBox is a private artifact web app tracking sports-journalism opportunities for
Olivia (UC Berkeley Class of 2028, Media Studies + Sociology, competitive volleyball
background, video/social-analytics skills). The published artifact:
https://claude.ai/code/artifact/a84b631c-2070-4705-a503-91aa432be735

## Files
- `ui_data.json` — canonical dataset: `{meta: {updated, count, note}, rows: [...]}`
- `pressbox_template.html` — the app shell; `__DATA__` placeholder gets the JSON
- `build.py` — injects the JSON into the template → `pressbox.html`

## Row schema
```
id, rank            ints; reassigned after every re-sort (rank 1 = best)
name, org, cat      cat is one of: "Cal campus / athletics", "National sports media",
                    "Teams & leagues", "General journalism", "Programs & fellowships",
                    "Bay Area & digital outlets"
role                free text (internship / fellowship / student media / freelance / ...)
loc, remote         remote is "yes" | "hybrid" | "no"
regions             array from: Berkeley / on campus, San Francisco, East Bay,
                    North Bay / Marin, South Bay / San Jose, Sacramento, SoCal / LA,
                    New York City, Other US, National / varies, Remote,
                    Remote-friendly (hybrid)
pay, payType,       payType one of: Salaried, Paid hourly $19+, Paid (hourly / unspecified),
payScore            Stipend / scholarship, Freelance / per piece, Unpaid / for credit.
                    payScore 1-10: salaried=10, $22+/hr=9, $19-21=8, $15-18=7, paid
                    unspecified=7, stipend=5, scholarship=6, per-piece=4, unpaid=2, costs money=1
time, window        window = application-window text. Prefix verified facts with
                    "Verified <Mon D, YYYY>: "; keep projections labeled "expected".
deadline            ISO date or null — ONLY when a real calendar date is known/projected
deadlineLabel       short human label for the deadline chip (required if deadline set)
buckets             array from: open-now, closing-soon (<=30 days), fall-2026,
                    nov-dec-2026, spring-2027, rolling, watch, future
elig, desc          eligibility text; desc = "why it's on the list" + how to get in
email, contact      ONLY published contacts — never guess an email
link                official apply/details URL
s                   {prestige, fit, pay, loc, timing, overall} each 1-10 except overall
tags                subset of: sophomore-ok, volleyball, womens-sports, on-campus,
                    has-contact, verified
```

## Scoring (recompute after any change)
`overall = 3.5*prestige + 2.5*fit + 1.5*pay + 1.5*loc + 1.0*timing` (max 100).
Then sort rows by overall desc and reassign id/rank = position.

## Update rules
1. Never delete rows. A dead opportunity gets `buckets: ["watch"]` or `["future"]`,
   deadline null, and a dated note in `window` (e.g., "Verified Sep 1, 2026: fall
   cycle closed Aug 21; next cycle expected ~May 2027").
2. A deadline in the past means the cycle closed: clear `deadline`, update `window`,
   re-bucket, and if the next cycle's timing is known, set the new expected deadline.
3. New opportunities found during verification get full rows with conservative scores
   and a `window` starting "Verified <date>:".
4. Facts only from primary sources (the org's own site/careers page) or two agreeing
   secondary sources. Anything else stays labeled "expected"/"unverified".
5. Keep every date's year explicit (e.g., "Feb 4, 2027") — ambiguity breaks the parser.
6. `meta.updated` = today (YYYY-MM-DD); `meta.note` = one-line changelog.
7. Validate before building: `python3 -c "import json; json.load(open('ui_data.json'))"`.

## Key context for verification priorities
- Olivia is Class of 2028: programs keyed to graduation year (rising junior in
  summer 2027, rising senior in summer 2028) may admit her earlier than her
  "sophomore" label suggests. Note this in `elig` where relevant.
- Big recurring watches: ESPN summer postings (Sept-Nov), AWSM Scholars (opens
  "late 2026"), SJI (opens ~mid-Oct, deadline ~Nov 3), DJNF (~Nov 5), KQED cohort
  postings (~Nov and ~May), NBCU summer apps (~Nov), Warriors/Valkyries window
  (Feb 1-15), NHL (Mar 1), Daily Cal recruitment (late Aug + January), LOVB seasonal
  roles (~Sept-Oct), MLV NorCal content roles (2027 launch), Giants Lever board
  (~Dec-Feb), ESPN/AAJA + CBS/AAJA internships (~Dec-Jan, deadline ~Feb 4).
