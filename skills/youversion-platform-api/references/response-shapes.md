# Response shapes to expect

This file is the shorthand documentation for the main JSON response types used by the YouVersion Bible REST API examples.

## `GET /v1/bibles`

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

## `GET /v1/bibles/3034`

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

## `GET /v1/bibles/3034/passages/JHN.3.16`

```json
{
  "id": "JHN.3.16",
  "content": "...",
  "reference": "John 3:16"
}
```
