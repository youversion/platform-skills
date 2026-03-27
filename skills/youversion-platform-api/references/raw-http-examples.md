# Raw HTTP Examples

Use this reference when the user wants copy-paste examples for the YouVersion Bible REST API without any SDK.

## Core rules

- Fixed server: `https://api.youversion.com`
- Always include `/v1` in the request path.
- Send `X-YVP-App-Key` on every request.
- Keep passage references in USFM form such as `JHN.3.16`.
- `GET /v1/bibles` requires at least one `language_ranges[]` query parameter.

## cURL

### List available Bibles

```bash
curl -sS \
  -H "X-YVP-App-Key: $YVP_APP_KEY" \
  "https://api.youversion.com/v1/bibles?language_ranges[]=en"
```

Use repeated `language_ranges[]` parameters for fallbacks:

```bash
curl -sS \
  -H "X-YVP-App-Key: $YVP_APP_KEY" \
  "https://api.youversion.com/v1/bibles?language_ranges[]=en&language_ranges[]=es"
```

### Get metadata for Bible 3034

```bash
curl -sS \
  -H "X-YVP-App-Key: $YVP_APP_KEY" \
  "https://api.youversion.com/v1/bibles/3034"
```

### Get John 3:16 from Bible 3034

```bash
curl -sS \
  -H "X-YVP-App-Key: $YVP_APP_KEY" \
  "https://api.youversion.com/v1/bibles/3034/passages/JHN.3.16?format=text"
```

### Get HTML for browser rendering

```bash
curl -sS \
  -H "X-YVP-App-Key: $YVP_APP_KEY" \
  "https://api.youversion.com/v1/bibles/3034/passages/JHN.3.16?format=html&include_headings=true"
```

## JavaScript with `fetch`

This example uses the standard `fetch` API. It works in Node.js 18+ and can be adapted to browser JavaScript by changing how the app key is provided.

```js
const API_BASE = "https://api.youversion.com";
const appKey = process.env.YVP_APP_KEY;

async function yvGet(path) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "X-YVP-App-Key": appKey,
      "Accept": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`YouVersion API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

const bibles = await yvGet("/v1/bibles?language_ranges[]=en");
console.log(bibles.data.map((b) => [b.id, b.abbreviation, b.title]));

const bible = await yvGet("/v1/bibles/3034");
console.log(bible.title);

const passage = await yvGet("/v1/bibles/3034/passages/JHN.3.16?format=text");
console.log(passage.reference, passage.content);
```

If the user specifically wants browser JavaScript, replace `process.env.YVP_APP_KEY` with the app key source used in that page or app.

## Python with `requests`

```python
import os
import requests

API_BASE = "https://api.youversion.com"
HEADERS = {
    "X-YVP-App-Key": os.environ["YVP_APP_KEY"],
    "Accept": "application/json",
}

def yv_get(path: str):
    response = requests.get(f"{API_BASE}{path}", headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()

bibles = yv_get("/v1/bibles?language_ranges[]=en")
print([(b["id"], b["abbreviation"], b["title"]) for b in bibles["data"][:5]])

bible = yv_get("/v1/bibles/3034")
print(bible["title"])

passage = yv_get("/v1/bibles/3034/passages/JHN.3.16?format=text")
print(passage["reference"])
print(passage["content"])
```

## Go with `net/http`

```go
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

const apiBase = "https://api.youversion.com"

func yvGet(path string, target any) error {
	req, err := http.NewRequest(http.MethodGet, apiBase+path, nil)
	if err != nil {
		return err
	}

	req.Header.Set("X-YVP-App-Key", os.Getenv("YVP_APP_KEY"))
	req.Header.Set("Accept", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return fmt.Errorf("youversion api error: %s", resp.Status)
	}

	return json.NewDecoder(resp.Body).Decode(target)
}

func main() {
	var bibles struct {
		Data []struct {
			ID           int    `json:"id"`
			Abbreviation string `json:"abbreviation"`
			Title        string `json:"title"`
		} `json:"data"`
	}

	if err := yvGet("/v1/bibles?language_ranges[]=en", &bibles); err != nil {
		panic(err)
	}

	for _, bible := range bibles.Data {
		fmt.Println(bible.ID, bible.Abbreviation, bible.Title)
	}

	var passage struct {
		ID        string `json:"id"`
		Content   string `json:"content"`
		Reference string `json:"reference"`
	}

	if err := yvGet("/v1/bibles/3034/passages/JHN.3.16?format=text", &passage); err != nil {
		panic(err)
	}

	fmt.Println(passage.Reference)
	fmt.Println(passage.Content)
}
```

## Response shapes to expect

### `GET /v1/bibles`

This example is intentionally abbreviated; actual items include additional fields.

```json
{
  "data": [
    {
      "id": 3,
      "abbreviation": "acr",
      // more fields here
    },
    {
      "id": 4,
      "abbreviation": "acuNT",
      // more fields here
    }
  ],
  "next_page_token": "..."
}
```

### `GET /v1/bibles/3034`

```json
{
  "id": 3034,
  "abbreviation": "BSB",
  "promotional_content": "Public Domain",
  "copyright": "Public Domain",
  "language_tag": "en",
  "localized_abbreviation": "BSB",
  "localized_title": "Berean Standard Bible",
  "publisher_url": null,
  "title": "Berean Standard Bible",
  "books": [
    "GEN", "EXO", "LEV", "NUM", "DEU", "JOS",
    "JDG", "RUT", "1SA", "2SA", "1KI", "2KI",
    "1CH", "2CH", "EZR", "NEH", "EST", "JOB",
    "PSA", "PRO", "ECC", "SNG", "ISA", "JER",
    "LAM", "EZK", "DAN", "HOS", "JOL", "AMO",
    "OBA", "JON", "MIC", "NAM", "HAB", "ZEP",
    "HAG", "ZEC", "MAL", "MAT", "MRK", "LUK",
    "JHN", "ACT", "ROM", "1CO", "2CO", "GAL",
    "EPH", "PHP", "COL", "1TH", "2TH", "1TI",
    "2TI", "TIT", "PHM", "HEB", "JAS", "1PE",
    "2PE", "1JN", "2JN", "3JN", "JUD", "REV"
  ],
  "youversion_deep_link": "https://www.bible.com/versions/3034"
}
```

### `GET /v1/bibles/3034/passages/JHN.3.16`

```json
{
  "id": "JHN.3.16",
  "content": "...",
  "reference": "John 3:16"
}
```
