---
paths:
  - "docs/**/*.mdx"
  - "docs/img/**"
  - "elitea.github.io/docs/**/*.mdx"
  - "elitea.github.io/docs/img/**"
---
# Images & media

Full standard: `docs/styleguides/visual standards.mdx`.

- Store in `docs/img/<section>/<feature>/`, mirroring the page path: `img/integrations/toolkits/tavily/`.
- Name files kebab-case, prefixed by the feature: `tavily-cred-navigate.png`.
- Formats: `.png` screenshots, `.gif` multi-step flows, `.svg` diagrams, `.mp4` videos.
- Reference with relative paths from the page, never absolute or external.
- Full-width: `![Alt text.](../../img/section/feature/name.png)`.
- Sized: `<img src="../../img/section/feature/name.png" alt="Alt text." width="400"/>`.
- Video: `<video controls><source src="../../img/section/feature/name.mp4" type="video/mp4"/></video>`.
- Alt text: describe context, sentence case, end with a period, 155 characters or fewer, no bold.
- Indent an image inside a numbered step to the step's text.
- Missing screenshot: insert the final reference with the planned filename and list it under Open questions.
- Do not screenshot text, code or terminal output.
