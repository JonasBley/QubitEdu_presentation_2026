#!/usr/bin/env python3
"""Descriptive polarization-pilot analysis (pandas, numpy, matplotlib).

Run:
    python analyze_pilot.py 'results-survey658185(2).csv'
    python analyze_pilot.py survey.csv --include-incomplete

Default mapping follows the user's instruction, not earlier applet versions:
Polarization 1 = WITHOUT sphere; Polarization 2 = WITH sphere.
Use --without-group 2 to reverse it.

Scale scores are unweighted participant means, requiring ALL items by default.
--min-item-fraction 0.8 permits means with >=80% of items answered.
No imputation, reverse coding, significance tests, or pooled load/TAM score.
The supplied item wording is positively keyed to each named construct.
All nonempty free-text responses are exported, including incomplete records.
"""
import argparse
import csv
import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SCALES = {
    'ICL': ('Intrinsic cognitive load', 5, 9),
    'ECL': ('Extraneous cognitive load', 5, 9),
    'GCL': ('Germane cognitive load', 5, 9),
    'PU': ('Perceived usefulness', 6, 7),
    'PEOU': ('Perceived ease of use', 6, 7),
    'SE': ('Self-efficacy', 3, 7),
    'ENJ': ('Enjoyment', 3, 7),
}
TEXT_CODES = ['MostInt', 'Help', 'Hinder', 'LikeMost', 'Dislike', 'Others',
              'Gender[comment]', 'FieldofStudy']
COLORS = {'Without Poincaré sphere': '#2363A0', 'With Poincaré sphere': '#D16B28'}


def read_export(path):
    # The supplied .csv is actually tab-delimited. Detect common export formats.
    with path.open(encoding='utf-8-sig', newline='') as f:
        first_line = f.readline()
    delimiter = csv.Sniffer().sniff(first_line, delimiters='\t,;').delimiter
    frame = pd.read_csv(path, sep=delimiter, dtype=str, keep_default_na=False,
                        encoding='utf-8-sig')
    codes = [c.split('. ', 1)[0].strip() for c in frame.columns]
    if len(codes) != len(set(codes)):
        raise ValueError('Duplicate question codes in export.')
    questions = dict(zip(codes, frame.columns))
    frame.columns = codes
    for key in ['id', 'ExpGroup', 'submitdate']:
        if key not in frame:
            raise ValueError(f'Missing required column: {key}')
    return frame, questions, delimiter


def rating(value, upper, response_id, item):
    if not value.strip():
        return np.nan
    # Accept plain numbers and labelled choices such as "9 - fully applicable".
    match = re.fullmatch(r'\s*(\d+(?:\.\d+)?)(?:\s*[-–:]\s*.*)?\s*', value)
    if not match:
        raise ValueError(f'Unrecognized response {value!r}, ID {response_id}, {item}')
    result = float(match.group(1))
    if not (1 <= result <= upper) or not result.is_integer():
        raise ValueError(f'Out-of-range response {value!r}, ID {response_id}, {item}')
    return result


def export_comments(frame, questions, out):
    records = []
    for _, row in frame.iterrows():
        for code in TEXT_CODES:
            if code in frame and row[code].strip():
                records.append(dict(response_id=row['id'], raw_group=row['ExpGroup'],
                                    group=row['group'], submitted=bool(row['submitted']),
                                    question_code=code, question=questions[code],
                                    comment=row[code]))
    comments = pd.DataFrame(records, columns=['response_id', 'raw_group', 'group',
        'submitted', 'question_code', 'question', 'comment'])
    comments.to_csv(out / 'comments.csv', index=False, encoding='utf-8-sig')
    lines = ['# All text comments', '',
             'Verbatim responses, grouped by question and experimental condition.',
             'Includes incomplete responses and optional field-of-study text.', '']
    for code in TEXT_CODES:
        if code not in questions:
            continue
        subset = comments[comments.question_code.eq(code)]
        lines += [f'## {questions[code]}', '']
        if subset.empty:
            lines += ['No non-empty responses.', '']
        for group in COLORS:
            part = subset[subset.group.eq(group)]
            if part.empty:
                continue
            lines += [f'### {group}', '']
            for row in part.itertuples():
                status = 'submitted' if row.submitted else 'incomplete'
                lines += [f'**Response {row.response_id} ({row.raw_group}; {status})**', '']
                lines += ['> ' + line for line in row.comment.splitlines()]
                lines += ['']
    (out / 'comments.md').write_text('\n'.join(lines), encoding='utf-8')
    return len(records)


def plot_scores(scores, selected, filename, title, upper, out):
    fig, axes = plt.subplots(1, len(selected), figsize=(3.5 * len(selected), 5.2),
                             sharey=True, squeeze=False)
    rng = np.random.default_rng(2026)
    for ax, code in zip(axes.flat, selected):
        for x, (group, color) in enumerate(COLORS.items()):
            values = scores.loc[scores.group.eq(group), code].dropna().to_numpy()
            if len(values):
                ax.scatter(x + rng.uniform(-.13, .13, len(values)), values,
                           color=color, edgecolors='white', linewidths=.6, s=48, zorder=3)
                mean = values.mean()
                ax.plot([x-.23, x+.23], [mean, mean], color=color, lw=3, zorder=4)
                if len(values) > 1:
                    ax.errorbar(x, mean, yerr=values.std(ddof=1), fmt='none',
                                ecolor=color, elinewidth=1.5, capsize=6, zorder=2)
            ax.text(x, .97, f'n = {len(values)}', transform=ax.get_xaxis_transform(),
                    ha='center', va='top', fontsize=10)
        ax.set_title(SCALES[code][0], fontsize=11, pad=14)
        ax.set_xticks([0, 1], ['Without\nsphere', 'With\nsphere'])
        ax.set_xlim(-.5, 1.5)
        ax.set_ylim(.6, upper+.8)
        ax.set_yticks(range(1, upper+1))
        ax.grid(axis='y', alpha=.18)
        ax.spines[['top', 'right']].set_visible(False)
    axes[0, 0].set_ylabel(f'Participant mean item score (1–{upper})')
    # fig.suptitle(title, fontsize=16, fontweight='bold', y=.98)
    # fig.text(.5, .02, 'Dots: participants   |   Horizontal bars: means   |   Whiskers: ±1 sample SD (not confidence intervals)',
    #          ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .08, 1, .9))
    for extension in ['png', 'svg', 'pdf']:
        fig.savefig(out / f'{filename}.{extension}', dpi=200, bbox_inches='tight')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('csv', type=Path)
    parser.add_argument('--output', type=Path, default=Path('pilot_results'))
    parser.add_argument('--without-group', choices=['1', '2'], default='1')
    parser.add_argument('--include-incomplete', action='store_true')
    parser.add_argument('--min-item-fraction', type=float, default=1.0)
    args = parser.parse_args()
    if not 0 < args.min_item_fraction <= 1:
        parser.error('--min-item-fraction must be in (0, 1].')
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    frame, questions, delimiter = read_export(args.csv)
    def group_label(raw):
        match = re.fullmatch(r'(?:Polarization\s+)?([12])(?:\.0)?', raw.strip(), re.I)
        if not match:
            raise ValueError(f'Unknown experimental group: {raw!r}')
        return 'Without Poincaré sphere' if match[1] == args.without_group else 'With Poincaré sphere'
    frame['group'] = frame.ExpGroup.map(group_label)
    # Submission presence indicates completion; do not interpret anonymized dates chronologically.
    frame['submitted'] = frame.submitdate.str.strip().ne('')
    count_comments = export_comments(frame, questions, out)
    included = frame if args.include_incomplete else frame.loc[frame.submitted]
    if included.empty:
        raise ValueError('No submitted responses; consider --include-incomplete.')
    scores = included[['id', 'ExpGroup', 'group', 'submitted']].copy()
    item_records = []
    for code, (label, expected, upper) in SCALES.items():
        columns = sorted(c for c in frame if re.fullmatch(re.escape(code)+r'\[SQ\d+\]', c))
        if len(columns) != expected:
            raise ValueError(f'{code}: expected {expected} items, found {len(columns)}.')
        numeric = pd.DataFrame(index=included.index)
        for col in columns:
            numeric[col] = [rating(v, upper, rid, col) for v, rid in zip(included[col], included.id)]
            for group in COLORS:
                vals = numeric.loc[included.group.eq(group), col].dropna()
                item_records.append(dict(scale=code, item=col, question=questions[col], group=group,
                    n=len(vals), mean=vals.mean(), sd=vals.std(ddof=1)))
        counts = numeric.notna().sum(axis=1)
        scores[code] = numeric.mean(axis=1).where(counts >= math.ceil(expected * args.min_item_fraction))
        scores[code+'_answered'] = counts
    scores.to_csv(out / 'participant_scores.csv', index=False, encoding='utf-8-sig')
    summary = scores.melt(id_vars=['id', 'group'], value_vars=list(SCALES),
                         var_name='scale', value_name='score').groupby(
                         ['scale', 'group'], sort=False).score.agg(
                         n='count', mean='mean', sd='std', median='median', minimum='min', maximum='max').reset_index()
    summary.to_csv(out / 'scale_summary.csv', index=False, encoding='utf-8-sig')
    pd.DataFrame(item_records).to_csv(out / 'item_summary.csv', index=False, encoding='utf-8-sig')
    plot_scores(scores, ['ICL', 'ECL', 'GCL'], 'cognitive_load', 'Cognitive load — pilot study', 9, out)
    plot_scores(scores, ['PU', 'PEOU', 'SE', 'ENJ'], 'technology_acceptance', 'Technology acceptance — pilot study', 7, out)
    audit = dict(input=str(args.csv), delimiter=repr(delimiter), total_responses=len(frame),
                 submitted=int(frame.submitted.sum()), quantitative_included=len(included),
                 included_by_group=included.group.value_counts().to_dict(),
                 without_sphere_raw_group=args.without_group, text_responses=count_comments,
                 minimum_item_fraction=args.min_item_fraction,
                 scoring='Unweighted participant means; no imputation or reverse coding.',
                 comment_scope='All nonempty free-text responses, regardless of submission status.')
    (out / 'analysis_settings.json').write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    print('\n'+summary.round(3).to_string(index=False))
    print(f'\nAll comments: {out / "comments.md"}\nFigures and tables: {out.resolve()}')


if __name__ == '__main__':
    main()
