---
name: youversion-platform-api
description: Calls the YouVersion Platform Bible API without any SDK. Use when Codex needs raw REST examples from any language or runtime, including cURL, browser JavaScript, Node.js, Python, Go, or backend frameworks, especially for listing available Bibles with `GET /v1/bibles`, fetching Bible version metadata with `GET /v1/bibles/{bible_id}`, or retrieving scripture passages with `GET /v1/bibles/{bible_id}/passages/{passage_id}`. Use this skill when the user wants direct HTTP requests, headers, query parameters, or JSON response shapes rather than an SDK.
---

# YouVersion Platform API (raw REST API usage)

## Default workflow

1. Determine the user's target runtime and use its normal HTTP client instead of introducing an SDK.
2. Check that a YouVersion Platform app key is available, e.g. in a YVP_APP_KEY env var. If not, ask for it or direct the user to register at `https://platform.youversion.com`.
3. Use `https://api.youversion.com` as the fixed server and always include `/v1` in the path.
4. Send the `X-YVP-App-Key` header on every request.
5. For Bible discovery, default to `GET /v1/bibles?language_ranges[]=en` unless the user wants another language. Other common language codes: "es", "de", "fr", "pt".
6. Explain that `GET /v1/bibles` returns versions visible to the current app key and license state. Add URL parameter `all_available=true` only when the user explicitly wants every available Bible surfaced.
7. For Bible metadata, use `GET /v1/bibles/{versionId}`. Use `3034` as the default example version because it is a known-good public domain bible (the Berean Standard Bible), but treat it as an example rather than a required default.
8. For scripture, use `GET /v1/bibles/{versionId}/passages/{usfm}`. Default format is text unless the user wants html, in which case add url parameter `format=html`.
9. Add `include_headings=true` and `include_notes=true` when the user wants those extras, but not by default. "include_notes=true" adds footnotes to the html.
10. If the user does not name a language, start with cURL because it is the most portable raw HTTP example, then add one language-specific example only if it helps.

## Response style

- Give the exact method, URL, headers, and query parameters first.
- Prefer one runnable raw HTTP example in the user's language over several disconnected snippets.
- Do not switch to `@youversion/platform-core` or any other SDK unless the user explicitly asks for an SDK. SDKs are available for TypeScript, React, Swift, and Kotlin - using them will save time and effort for many use cases, but straight API usage can also be great.
- Use `YVP_APP_KEY` in examples unless the user's project already uses another environment variable name.
- Show only the response fields the user needs, such as `data`, `id`, `content`, and `reference`, unless they ask for the full schema.

## Default request shape

```text
GET https://api.youversion.com/v1/...
X-YVP-App-Key: YOUR_APP_KEY
Accept: application/json
```

Use these three endpoints by default:

1. `GET /v1/bibles?language_ranges[]=en`
2. `GET /v1/bibles/3034`
3. `GET /v1/bibles/3034/passages/JHN.3.16?format=text`

## Endpoint notes

### List Bibles

Use `GET /v1/bibles` for version discovery.

- `language_ranges[]` is required and uses repeated bracket notation such as `language_ranges[]=en&language_ranges[]=es`.
- When multiple language ranges are provided, the API returns results from the first language range that has available Bibles.
- This collection is paginated. Use `next_page_token` from the response as `page_token` on the next request when needed.
- If not more than 3 fields are requested, you can add "page_size=*" to avoid the results being paginated. For example "https://api.youversion.com/v1/bibles?language_ranges%5B%5D=*&fields%5B%5D=id&fields%5B%5D=language_tag&page_size=*" is a great way to get the ids and language_tags of all the bible versions, in a single small and therefore quick download.
- `all_available=true` includes Bibles regardless of the current license state for the app key.

For example:
`curl -s -H "x-yvp-app-key: $YVP_APP_KEY" 'https://api.youversion.com/v1/bibles?language_ranges[]=fr'`

Read `references/response-shapes.md` for an example response object from this call.

### Get Bible metadata

Use `GET /v1/bibles/{bible_id}` to fetch metadata for one version.

- Default example: `GET /v1/bibles/3034`
- Useful response fields include `id`, `abbreviation`, `title`, `localized_title`, `language_tag`, `copyright`, `promotional_content`, `books`, and `youversion_deep_link`.

For example:
`curl -s -H "x-yvp-app-key: $YVP_APP_KEY" 'https://api.youversion.com/v1/bibles/3034'`

Read `references/response-shapes.md` for an example response object from this call.

### Get passage text or html

Use `GET /v1/bibles/{bible_id}/passages/{passage_id}` for scripture content.

- Default example: `GET /v1/bibles/3034/passages/JHN.3.16?format=text`
- `format` supports `text` and `html`. The default is `text`.
- The response is JSON. The actual passage payload is in `content`.
- Use `include_headings=true` and `include_notes=true` when the user wants those sections included.
- `reference` is the human-readable label to display alongside the content.

For example:
`curl -s -H "x-yvp-app-key: $YVP_APP_KEY" "https://api.youversion.com/v1/bibles/111/passages/GEN.1.1?format=text"`

Read `references/response-shapes.md` for an example response object from this call.

### Other Endpoints

Other endpoints are available to be called, to get more bible metadata, to
enumerate languages and get their metadata, to get the YouVersion Verse of the Day, 
and others.
See the documentation at "https://developers.youversion.com/api/bibles" for details.

## Gotchas

- Always include `X-YVP-App-Key` on every request, otherwise it will be rejected.
- App keys are NOT secrets; they generally can be included in source code.
- Always include `language_ranges[]` when calling `/v1/bibles`.
- Do not assume every Bible is available to every app key.
- Do not assume every book is available in every Bible version: for example some versions only have the New Testament books.
- Default to `format=text`; request `format=html` only when the user actually wants markup.
- Keep passage identifiers in USFM form such as `JHN.3.16`, `GEN.1`, or `MAT.1.1`.
- Keep answers coding-language-agnostic unless the user names a language or framework.

## References to load on demand

- Read `references/raw-http-examples.md` when the user wants copy-paste examples in cURL, browser JavaScript, Node.js, Python, or Go.
- Read `references/response-shapes.md` to see shorthand JSON schemas for the main `/v1` API responses.
