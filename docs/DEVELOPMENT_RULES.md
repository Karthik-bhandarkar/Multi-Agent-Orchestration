# EduPulse AI — Development Rules & Antigravity Learning Protocol

Status: LIVE. Formally adopted guidelines for AI Usage, Debugging, Testing, File Mapping, and Development Discipline.

---

## 1. Dependencies
- Don't add a library for something a few lines of native code can do.
- Before adding one, check: is it maintained, is it widely used, does it add real value here.
- Fewer dependencies = less to break, less to secure, less to update.

---

## 2. Error Handling
- Handle errors where they happen, not just at the top level.
- Never let one failure crash the whole app.
- Don't expose internal error details (stack traces, DB errors) to users.
- Every external call needs a defined failure path: what shows the user, what gets logged.
- Handle bad input, missing data, network failure, auth failure, third-party service failure explicitly, not by accident.

---

## 3. Security Baseline
- No hardcoded secrets, ever — not "temporarily," not in a comment.
- No credentials committed to version control.
- Don't bypass auth/authorization checks to save time during development.
- Validate and sanitize all user input, always.
- Don't disable a security check because it's inconvenient — fix the underlying friction instead.

---

## 4. Code Quality
- Consistent naming across the project.
- Modular — a function/component should do one thing.
- Comment why, not what (the code already shows what).
- If it's getting complicated, that's a signal to simplify, not push through.

---

## 5. AI Usage & Antigravity Learning Protocol
- **Ticket-sized prompts, not whole-feature prompts.** Break execution into clear micro-phases.
- **Review every change like an incoming PR** — read diffs fully and run verification commands.
- **Explain-it-back step:** For every created or modified file, state in plain language why it exists, what it does, where to start reading, and what was just done.
- **Durable File Mapping:** Log per-file explanations in `FILE-MAP.md` in real-time.
- **Never mark a skill "Understood"** solely because working code was generated — only when you can explain and modify it unaided.

---

## 6. Per-File Explain & File Map Protocol
Every time a new file is created, or an existing one is meaningfully changed, state before moving to the next file:
- **Why this file exists** — what gap it fills in the architecture.
- **What it does** — in plain language, not just a restatement of code.
- **Where to start** — if reading cold, which section/function to inspect first.
- **What was just done** — the specific changes made.

Log this in `FILE-MAP.md` in the same session.

---

## 7. Debugging Protocol
When a bug occurs:
1. State what you think is happening before looking anything up.
2. Reproduce it reliably — find the exact steps/input triggering it.
3. Inspect relevant code/logs directly.
4. Form a specific hypothesis about the root cause.
5. Test that hypothesis (log lines, minimal repro case).
6. Fix it once confirmed, not before.
7. Explain the root cause afterward in logs/documentation.

---

## 8. Testing Philosophy — Deliberate Challenge
- Apply rigorous edge cases, invalid input, transaction failures, and performance constraints.
- Run `pytest` and `flake8` after every meaningful file creation or modification.

---

## 9. Development Discipline & Git Policy
- **Small changes over big ones.**
- **Test after every meaningful change.**
- **Group 5 Git Push Restriction:** Complete all coding and pytest suite locally, but **DO NOT `git push`** until explicitly instructed after Render deployment verification.

---

## 10. Explicit Prompt & Plan Authorization Rule
- **NEVER generate, create, or implement code for a new Group or Phase until the user explicitly provides the detailed prompt, requirements, or plan for that specific Group.**
- Always wait for the user to paste or specify the exact plan/prompt for the upcoming group before creating any code or files for that group.

---

## 11. Lead Software Architect Conventional Commits Specification (v1.0.0)
All Git commit messages must strictly adhere to the Conventional Commits specification (v1.0.0) for elite open-source / enterprise compliance.

### 1. Format:
```text
<type>(<optional scope>): <action-oriented subject>

[optional body explaining WHY, not just what]
[optional footer for breaking changes or issue references]
```

### 2. Allowed Types:
- `feat`: A new feature
- `fix`: A bug fix
- `refactor`: Code restructuring without changing external behavior
- `perf`: Code change that improves performance
- `style`: Formatting, missing semi-colons, no code change
- `test`: Adding or refactoring tests
- `docs`: Documentation changes only
- `chore`: Build process, dependencies, or auxiliary tool changes

### 3. Style & Imperative Mood Rules:
- Use the **IMPERATIVE mood** in the subject line (`add`, `optimize`, `resolve`, NOT `added`, `adds`, `fixing`).
- Maximum 72 characters for the subject line.
- Do **NOT** end the subject line with a period.
- Do **NOT** use vague terms like `update file`, `fix bug`, `changes`, or `wip`.
---

## 12. Automated Verification, Response Fine-Tuning & Model Selection Protocol
- **Mandatory Automated Self-Testing Every Phase:** Run automated verification scripts (`pytest`, `flake8`, and custom runner scripts exporting formatted JSON output files) after implementing every single micro-phase. Analyze test execution results directly.
- **Empirical Output Response Fine-Tuning:** Inspect all JSON response outputs and fine-tune code logic, prompt templates, and system parameters to ensure high accuracy and zero false responses based strictly on empirical evidence.
- **API Key & Model Selection Protocol:** Whenever a new API key is required or an LLM/embedding model yields suboptimal responses, explicitly request the required key from the user or benchmark and recommend superior models (e.g. OpenRouter, Groq, Google Gemini), reporting all performance findings to the user.



