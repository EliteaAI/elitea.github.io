---
paths:
  - "docs/**/*.mdx"
  - "elitea.github.io/docs/**/*.mdx"
---
# Navigation, accessibility & inclusive language (from styleguide: language)

## Navigation
- Be brief and specific; do not explain the obvious: "Select **Start**.", not "Select **Start** to run the wizard."
- Location, then action; reason, then action: "In **Settings**, select **Project Context**." "To view the top 5 AI adopters, go to **Analytics**."
- No directional language: name the element. "Select **Publish**.", not "Select the button below."

## Sensitive data
- No real usernames or email addresses, in text or in visual aids (images, GIFs, videos).
- Diverse, non-gendered names with common surnames; fake emails ending in `@email.com` or `@example.com`; fake sites like `example.com`.
- Fake tokens: `<your_app_token>`, for example `<your_jira_token>`, `<your_confluence_token>`.
- Illustrations must not show personal data. If an image or video seems to show it, report it (masking is done by humans).

## Accessible language
- Avoid unnecessary font formatting. No forced line breaks inside sentences or paragraphs.
- Break up long paragraphs; use short sentences; state the important information first (first-sentence rule).
- Add alt text to images (see mdx-media). Use tables sparingly and pre-announce them.
- Never use color, size, location or another visual cue as the main carrier of information.

## Inclusive & bias-free
- *They* for a generic person; no gendered language; diverse, non-gendered names.
- No figurative language: idioms, jargon, metaphors. No ableist words (crazy, insane, blind, cripple, dumb).
- Be culturally neutral: no specific holidays, cultural practices or culture-bound figures of speech.

## Localization
- Avoid: phrases that hide the subject ("there is", "there are"); ambiguous pronouns like "it"; words with several meanings where the meaning is unclear (better, always); easily confused words; culture-specific references; strings of three or more nouns.
- Use explicit subjects and single-meaning words.
- Do not let list items complete an introductory phrase:
  - Worse: "You can get the license key by: - Copying it from the email. - Downloading the file."
  - Better: "You can get the license key by one of these methods: - Copy the license key from the email. - Download the file."
