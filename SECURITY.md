# Security Policy

## Supported versions

Only the latest released version receives security fixes.

## Reporting a vulnerability

Please **do not open a public issue** for security problems. Use GitHub's
private vulnerability reporting ("Security" tab → "Report a vulnerability").

Include a description, a minimal reproduction, and the affected version. You
can expect an acknowledgement within 7 days.

## Scope

`pertext` processes untrusted text, so reports about the following are
especially welcome:

- Regular-expression denial of service (catastrophic backtracking) on crafted input
- Crashes or unbounded memory use on malformed Unicode
- Incorrect normalization that could bypass validation or filtering built on top of it
