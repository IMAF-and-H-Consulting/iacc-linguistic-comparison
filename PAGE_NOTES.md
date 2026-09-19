# Public annotations for the interactive explorer

The explorer loads a separate Page Notes commenting layer. Article text, figures,
CSV results and the analysis notebook are unchanged. Comments live in a dedicated
DreamHost MySQL database, not in this repository.

## Deployment targets

- Original page: https://imaf-and-h-consulting.github.io/iacc-linguistic-comparison/
- Overlay script: https://mike.nothelp.help/page-notes/overlay.js
- Comments API: https://mike.nothelp.help/page-notes/api.php
- Owner moderation: https://mike.nothelp.help/page-notes/admin.php
- Site ID and stable page ID: `iacc-linguistic-comparison`

These are installation targets, not a claim that the backend is already live.
**Install and verify the DreamHost backend before merging the loader change.**
The existing portfolio at the root of mike.nothelp.help must remain untouched.

## Loader and rebuilds

The same loader is included in `explorer_template.html` and generated `index.html`:

```html
<script src="https://mike.nothelp.help/page-notes/overlay.js"
        data-api="https://mike.nothelp.help/page-notes/api.php"
        data-site="iacc-linguistic-comparison"
        data-page="iacc-linguistic-comparison"
        defer></script>
```

Keep it in the template when rebuilding with `python3 build_explorer.py`. The
explicit page ID prevents section hashes, tracking parameters and the default
index filename from splitting one discussion into multiple threads. Existing
section IDs support selected-text anchors. Do not rename them casually if
comments are attached to them.

The research explorer still works without the comment service, including local
file viewing. Shared comments require HTTPS hosting and a working backend; they
are not an offline feature. If the external script cannot load, the research
page stays usable. If the API is unavailable, the overlay reports a failure and
does not pretend that a comment was saved.

## DreamHost configuration

Use a new application directory under the existing site and private code/config
outside its document root. Do not upload credentials to GitHub. Configure the
backend's exact allowed origins:

```php
'sites' => [
    'iacc-linguistic-comparison' => [
        'label' => 'IACC linguistic comparison',
        'origins' => [
            'https://imaf-and-h-consulting.github.io',
            'https://mike.nothelp.help',
        ],
    ],
],
```

The origin contains no project path or trailing slash. The second entry supports
the backend-hosted demo, which should use a different page ID so its test notes
never appear on this explorer. The PHP/MySQL package has separate database setup,
private configuration and owner-password instructions.

## Comment behavior and privacy

- Any visitor can read and post without an account, under an unverified chosen name.
- A colored indicator and unique eight-character browser badge distinguish people
  with the same name. Colors themselves may repeat; text remains neutral.
- Names, comments and selected quotes are public. Do not post confidential information.
- Browser storage retains author ownership. Clearing it or changing device creates
  a new badge; old public comments remain, but that browser can no longer remove them.
- Readers can leave page notes, selected-text notes and replies. The original page
  is not edited when a comment is posted.
- If source text, section identity or surrounding context changes, a note can be
  marked unattached instead of being silently moved to a different passage. Notes
  on dynamic chart/table text may become unattached when a filter changes.
- The original browser can remove its own comments; the owner can moderate from
  the protected admin page. Removal keeps reply structure intact.
- No CAPTCHA is included. Server rate limits and owner moderation reduce casual
  spam but do not make anonymous public commenting abuse-proof.

## Pre-merge checks

1. The PHP backend and a new dedicated database are installed over HTTPS.
2. The existing portfolio still loads unchanged.
3. The API allows the GitHub origin, rejects unconfigured origins, and exposes no secrets.
4. Two independent browsers see the same comment and get different browser badges.
5. Selected-text notes, replies, reloads and owner moderation work.
6. The original chart toggles, search boxes, term selector, sorting and navigation still work.
7. No database credentials or moderator password are in the public directory or repository.

Do not treat a locally passing browser test as a production deployment check.
