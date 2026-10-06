# Contributing

Open an issue before proposing a change that affects syntax, processing order,
security boundaries, persistence semantics, or namespace compatibility.

Proposals should include:

- the use case and why standard SSML does not already cover it;
- proposed syntax and processing behavior;
- failure, cancellation, and resource-limit behavior;
- backward-compatibility impact;
- privacy and security considerations; and
- at least one valid and one invalid example.

Backward-compatible additions can remain in the 1.0 namespace. Incompatible
changes require a new major-version namespace. Implementations must not claim a
proposal as supported until the specification and capability contract are
settled.

Changes to parser or builder behavior belong in
[`ssml-h-tools`](https://github.com/hangry-labs/ssml-h-tools) after the
specification change is accepted.
