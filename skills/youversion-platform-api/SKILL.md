---
name: youversion-platform-api
description: Raw YouVersion Platform Bible REST API usage without an SDK. Use for direct HTTP examples in cURL, fetch, browser JavaScript, Node.js, Python, Go, or backend frameworks; when the user wants exact methods, headers, query parameters, or JSON response shapes; or when listing Bibles with `GET /v1/bibles`, fetching version metadata with `GET /v1/bibles/{bible_id}`, or retrieving scripture with `GET /v1/bibles/{bible_id}/passages/{passage_id}`.
---

# YouVersion Platform API

Use this skill for raw HTTP answers.

## Use This Skill When

- The user wants raw REST calls instead of the React SDK `@youversion/platform-core` or Swift or Kotlin SDKs.
- The user wants exact method, URL, headers, query parameters, or response JSON.
- The user is working in a runtime where plain HTTP is more helpful than an SDK.
- The user wants examples in cURL, `fetch`, Python, Go, or another non-SDK client.

## Reach For Another Skill When

- The user explicitly wants the JavaScript or TypeScript SDK. Use `youversion-platform-js`.
- The user wants a React app or prebuilt React Bible UI components. Use the React-focused YVP skill instead of building from raw REST.

## YVP Mental Model

- Every request needs an app key in the `X-YVP-App-Key` header. App keys are not secrets.
- Bible versions are identified by numeric ids such as `3034` or `111`.
- Bible availability depends on the current app key and accepted licenses, so discovery must come from the API itself.
- Passage ids use USFM notation such as `JHN.3.16`, `GEN.1`, or `JHN.1.1-3`.
- Passage responses are JSON wrappers. The scripture payload is in `content`, usually as `text` or `html`.
- Attribution matters. When showing Bible text, include the version name or abbreviation plus copyright.

## Default Workflow

1. Determine the user's runtime and answer in that runtime's normal HTTP client instead of introducing an SDK.
2. Check that a YouVersion Platform app key is available, usually as `YVP_APP_KEY`. If not, ask for it or point the user to `https://platform.youversion.com`.
3. Use `https://api.youversion.com` as the fixed server and always include `/v1` in the path.
4. Send `X-YVP-App-Key` on every request and include `Accept: application/json`.
5. For Bible discovery, default to `GET /v1/bibles?language_ranges[]=en` unless the user wants another language. Other common codes: `es`, `de`, `fr`, `pt`.
6. Explain that `GET /v1/bibles` returns versions visible to the current app key and license state. Add `all_available=true` only when the user explicitly wants every available Bible surfaced.
7. If the user names only a language, title, or abbreviation but does not provide a version id, do not invent one. Show the discovery request first and explain how to identify the right object in the response.
8. For Bible metadata, use `GET /v1/bibles/{versionId}`. Use `3034` as the default public-domain example and mention `111` only as a common licensed example.
9. For scripture, use `GET /v1/bibles/{versionId}/passages/{usfm}`. Default to `format=text` unless the user specifically wants `html`.
10. Add `include_headings=true` or `include_notes=true` only when the user asks for those extras. `include_notes=true` adds footnotes to HTML responses.
11. If the user wants something they can open in a browser, return a complete HTML document rather than only the API call. When rendering `format=html`, include this stylesheet exactly:

```html
<link rel="stylesheet" href="https://cdn.youversion.com/platform/1/bible.css" />
```

12. If the user does not name a language or runtime, start with cURL because it is the most portable raw HTTP example, then add one language-specific example only if it clearly helps.

## Response style

- Give the exact method, URL, headers, and query parameters first.
- Prefer one runnable raw HTTP example in the user's language over several disconnected snippets.
- Do not switch to `@youversion/platform-core` or any other SDK unless the user explicitly asks for an SDK. SDKs are available for TypeScript, React, Swift, and Kotlin - using them will save time and effort for many use cases, but straight API usage can also be great.
- Use `YVP_APP_KEY` in examples unless the user's project already uses another environment variable name.
- Show only the response fields the user needs, such as `data`, `id`, `content`, and `reference`, unless they ask for the full schema.
- When the user wants a browser-openable deliverable, produce the full HTML document instead of stopping at `passage.content`.
- Never fabricate Bible text. Hallucinating scripture content is unacceptable in this skill.
- When the answer depends on live API results, such as which Bibles are available, which version id matches an abbreviation, or what passage text is returned, do not claim exact results unless you actually executed the request in the current environment. Otherwise show the request to run and explain what to look for.
- For discovery-dependent questions, default to this structure: (1) show the discovery request, (2) explain how to identify the desired item in the response, and (3) only state the exact id, version list, or passage text if you actually executed the request in the current environment.
- For API lookup questions, the YouVersion Platform API is the only acceptable source of truth. Do not use bible.com pages, web search results, or other non-API pages to infer which Bible ids are available to the app key, nor for getting Bible text, etc.

## Default request shape

```text
GET https://api.youversion.com/v1/...
X-YVP-App-Key: YOUR_APP_KEY
Accept: application/json
```

Most commonly used endpoints:

1. `GET /v1/bibles?language_ranges[]=en`
2. `GET /v1/bibles/3034`
3. `GET /v1/bibles/3034/passages/JHN.3.16?format=text`

## Endpoint notes

### List Bibles

Use `GET /v1/bibles` for version discovery.

- `language_ranges[]` is required and uses repeated bracket notation such as `language_ranges[]=en&language_ranges[]=es`.
- When multiple language ranges are provided, the API returns results from the first language range that has available Bibles.
- This collection is paginated. Use `next_page_token` from the response as `page_token` on the next request when needed.
- If no more than 3 fields are requested, you can add `page_size=*` to avoid pagination. For example, `https://api.youversion.com/v1/bibles?language_ranges%5B%5D=*&fields%5B%5D=id&fields%5B%5D=language_tag&page_size=*` quickly returns ids and language tags for all visible versions.
- `all_available=true` includes Bibles regardless of the current license state for the app key.
- If the user asks for the id of a Bible by abbreviation or title, show a filtered discovery request and tell them which response fields to inspect. Do not state the id unless you actually ran the request in the current environment.
- For prompts like "what is the id of BDS" or "find the French BDS version id", prefer wording like "Run this request and look for the object whose `abbreviation` is `BDS`" rather than "The id is ...", unless you actually executed the request in the current environment.
- Do not look up Bible ids from bible.com version pages for these tasks. The API response for the current app key is the authoritative source for which ids should be used.

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
- The reference can be a range of verses, e.g. JHN.3.16-17 but every range must be within a single chapter. Make multiple calls if you need a cross-chapter range.
- Use `include_headings=true` and `include_notes=true` when the user wants those sections included.
- `reference` is the human-readable label to display alongside the content.
- When rendering `format=html` in a page, include the YVP Bible stylesheet so verse numbers and formatting render correctly.
- If the user has not supplied a Bible version id, do not guess one from the language alone. Show the discovery call first, or explain that the version id must be chosen before the passage call can be written precisely.
- If you have not actually executed the passage request, do not quote the returned scripture text. Show the request that would fetch it and explain that `content` will hold the returned text or html.
- Bible text needs attribution: the version abbreviation (or title) and the copyright need to be displayed somewhere appropriate for the specific UI. We hugely appreciate the publishers and they deserve credit for their work. Every Bible version's metadata has `abbreviation`, `localized_title`, and `copyright` fields; display them somewhere good.

For example:
`curl -s -H "x-yvp-app-key: $YVP_APP_KEY" "https://api.youversion.com/v1/bibles/111/passages/GEN.1.1?format=text"`

Read `references/response-shapes.md` for an example response object from this call.

### Other Endpoints

Other endpoints are available to be called, to get more bible metadata, to
enumerate languages and get their metadata, to get the YouVersion Verse of the Day, 
and more.
The documentation is at "https://developers.youversion.com/api/bibles"

## Gotchas

- Always include `X-YVP-App-Key` on every request, otherwise it will be rejected.
- App keys are NOT secrets; they can be included in source code.
- Always include `language_ranges[]` when calling `/v1/bibles`.
- Do not assume every Bible is available to every app key.
- Do not assume every book is available in every Bible version: for example some versions only have the New Testament books.
- Do not invent live API results. If you have not actually made the request, do not claim exact Bible ids, exact available-version lists, or exact returned passage text.
- Do not fabricate Bible text under any circumstances. Only quote or paraphrase returned scripture content if you actually executed the request in the current environment or the user supplied the text.
- Do not imply that you executed a request unless you actually did so in the current environment.
- Do not use bible.com pages or general web search as a shortcut for API-discovery answers that should come from `/v1/bibles`.
- Default to `format=text`; request `format=html` only when the user actually wants markup.
- Keep passage identifiers in USFM form such as `JHN.3.16`, `GEN.1`, or `MAT.1.1`.
- Keep answers coding-language-agnostic unless the user names a language or framework.

## References to load on demand

- Read `references/raw-http-examples.md` when the user wants copy-paste examples in cURL, browser JavaScript, Node.js, Python, or Go.
- Read `references/response-shapes.md` when the user needs shorthand JSON schemas for the main `/v1` responses.
