# Security Policy

## Supported versions

Only the latest released version receives security fixes.

## Reporting a vulnerability

If GitHub's private vulnerability reporting is enabled for this repository
(Security tab → "Report a vulnerability"), please use it.

Otherwise, open a GitHub issue titled "Security: contact request" **without
any technical details**, and the maintainer will arrange a private channel.
Please do not post exploit details publicly.

Include a description, a minimal reproduction, and the affected version. You
can expect an acknowledgement within 7 days.

## Scope

`pertext` processes untrusted text, so reports about the following are
especially welcome:

- Regular-expression denial of service (catastrophic backtracking) on crafted input
- Crashes or unbounded memory use on malformed Unicode
- Incorrect normalization that could bypass validation or filtering built on top of it
