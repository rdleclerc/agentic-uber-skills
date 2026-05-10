# Source Resolvers

Use source-specific tools before generic summarization.

## X / Twitter

Prefer private/source-authorized bookmark caches and Type0 public read tools when available. Capture tweet ID, author, date, text, metrics, media URLs, quoted/replied context, linked article URLs, and retrieval gaps. Do not treat a tweet as the linked article unless the article/video was inspected.

## GitHub

Inspect README/docs, repo structure, release/activity signals, issues/PRs when relevant, license, install surface, tests, and examples. Avoid adopting repos because of stars alone. Note whether code was read, merely summarized, or cloned.

## arXiv / papers

Capture title, authors, date/version, abstract, PDF/text extraction status, claims, benchmark/eval basis, limitations, and whether implementation artifacts exist. Distinguish peer-reviewed, preprint, benchmark-only, and speculative claims.

## Articles / blogs

Capture publisher/date/author, primary claims, linked primary sources, paywall/403 limitations, and whether the article is primary evidence or commentary.

## Video / media

Record transcript/OCR status. If video/image content is not inspected, mark the assessment limited and avoid strong claims based on media alone.

## Resolver escalation rule

Build new tools/MCP only after repeated assessments show a stable need that cannot be met with read-only files/CLI/scripts and the benefit is clearly much greater than added cost.
