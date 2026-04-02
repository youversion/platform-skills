# platform-skills
Skills for agentic usage of YouVersion Platform APIs and SDKs.

Each of these skills explain to an Agent how to get Bible text, html, and information. They instruct Agents in writing code using best practices for accessing YouVersion Platform.

## Available skills

- `youversion-platform-api`: REST API usage
- `youversion-platform-js`: TypeScript and Node.js usage
- `youversion-platform-react`: React, for visual components: BibleTextView, BibleCard, and BibleReader.

## Installation

The easy way: run `npx skills add youversion/platform-skills` and choose your preferred agentic tool or tools.

Alternatively, follow the instructions for your preferred agentic coder, as installation methods vary widely. For example:
- [Claude Code](https://code.claude.com/docs/en/skills): copy this repo's skill folders into `.claude/skills/` in your repo.
- [Codex](https://developers.openai.com/codex/skills#install-curated-skills-for-local-use): in the CLI, run `$skill-installer install youversion/platform-skills`
- [Cursor](https://cursor.com/docs/skills#installing-skills-from-github): Open Cursor Settings → Rules, click "New", import from Github, enter this repo's URL.
- [Gemini CLI](https://geminicli.com/docs/cli/skills/): in the CLI, run `gemini skills install https://github.com/youversion/platform-skills`
