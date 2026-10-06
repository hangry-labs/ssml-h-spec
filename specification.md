# SSML-H 1.0

**Hangry Labs Speech Synthesis Markup Language extension**  
**Specification:** 1.0  
**Namespace:** `https://hangrylabs.app/ns/ssml-h/1.0`  
**Status:** Hangry Labs Editor's Draft  
**Repository:** <https://github.com/hangry-labs/ssml-h-spec>

SSML-H is the Hangry Labs extension profile for Speech Synthesis Markup
Language. It preserves standard SSML document structure and controls while
adding bounded, portable features that are useful in local generative speech
systems. The `H` stands for Hangry Labs.

The first SSML-H extension is dynamic voice definition: a document can define
characters, synthesize their local voice references, use them in standard
`<voice>` turns, and optionally persist them as reusable profiles.

## Relationship To SSML

SSML-H is based on [W3C SSML 1.1](https://www.w3.org/TR/speech-synthesis/).
It is a Hangry Labs standard, not a W3C Recommendation and not a replacement
for SSML.

An SSML-H document:

- uses the standard SSML `<speak>` root and SSML namespace;
- keeps standard speech markup in the document body;
- places Hangry Labs declarations in standard `<metadata>` using the SSML-H
  namespace; and
- is processed through an explicit SSML-H input mode rather than inferred from
  plain text.

A pure SSML 1.1 document contains no SSML-H declarations and can therefore be
accepted unchanged by an SSML-H processor. This is the guaranteed backward
compatibility direction.

A standard SSML processor can parse an SSML-H document and ignore the custom
metadata when it permits foreign metadata. It cannot be expected to create the
declared voices. A later `<voice name="Bob">` can consequently fail on that
processor unless `Bob` already exists in its own voice catalog. SSML-H does not
claim identical rendering on processors that do not implement its extensions.

## Namespaces And Versioning

The SSML namespace remains the default namespace:

```text
http://www.w3.org/2001/10/synthesis
```

The SSML-H 1.0 namespace is:

```text
https://hangrylabs.app/ns/ssml-h/1.0
```

Examples use the prefix `h`, but the prefix is only a local XML alias. The
namespace URI identifies the extension, so `hl:` or any other correctly bound
prefix has the same meaning. SSML-H belongs to Hangry Labs and is intended to
work across speech synthesis engines.

A future incompatible specification uses a new major-version namespace.
Backward-compatible additions retain the 1.0 namespace and are discoverable
through processor capabilities.

## Processing Model

Processors must keep plain text as the default input mode. Applications select
SSML-H explicitly, for example with `input_type="ssml-h"`. Implementations may
also expose `input_type="ssml"` for standard SSML without Hangry Labs
extensions.

An SSML-H processor follows this order:

1. Parse the document with DTDs, entities, and external references disabled.
2. Validate the complete document, declarations, limits, and capabilities.
3. Resolve existing and dynamically declared voices.
4. Compile the document into a typed synthesis plan.
5. Create any required temporary voice references.
6. Synthesize all turns in document order.
7. Assemble boundaries, normalize once, and encode once.
8. Commit requested persistent profiles only after successful completion.
9. Remove request-scoped and uncommitted resources on success, failure, or
   cancellation.

Validation must finish before model inference begins. Full-response and
streaming paths must use the same plan and lifecycle rules.

## Dynamic Voice Definitions

Definitions live inside `<metadata>` and one `<h:extensions>` container:

```xml
<metadata>
  <h:extensions version="1.0">
    <h:voice-definition
      name="Bob"
      gender="male"
      age="elderly"
      accent="american"
      scope="request"
      seed="4242" />
  </h:extensions>
</metadata>
```

### `h:extensions`

| Attribute | Required | Meaning |
|---|---:|---|
| `version` | Yes | SSML-H syntax version used by the declarations. Version 1.0 processors require `1.0`. |

There must be at most one `h:extensions` element in an SSML-H 1.0 document.
Unknown SSML-H elements or attributes are errors unless a future capability
explicitly declares support for them.

### `h:voice-definition`

| Attribute | Required | Meaning |
|---|---:|---|
| `name` | Yes | Portable voice identifier referenced by standard `<voice name="...">`. |
| `scope` | No | `request` by default, or `profile` for persistent storage. |
| `replace` | No | Boolean, `false` by default. Allows replacement of an existing persistent profile when `scope="profile"`. |
| `seed` | No | Unsigned 32-bit seed used by deterministic voice-design stages. |
| `gender` | No | Voice-design descriptor: `male`, `female`, or `neutral`, subject to processor capability. |
| `age` | No | Positive integer or one of `child`, `teenager`, `young-adult`, `middle-aged`, or `elderly`. |
| `pitch` | No | Inherent voice descriptor advertised by the processor, distinct from standard per-turn `<prosody pitch>`. |
| `style` | No | Inherent voice style advertised by the processor. |
| `languages` | No | Space-separated BCP 47 language ranges the voice is intended to speak. |
| `accent` | No | Accent descriptor advertised by the processor. |
| `dialect` | No | Dialect descriptor advertised by the processor. |

Names must match `[A-Za-z][A-Za-z0-9._-]{0,63}`. Names are compared exactly
inside the document. A processor may normalize persistent storage ids, but it
must return the resulting id and must not silently bind a different existing
profile.

Voice-design descriptors describe the character identity. Standard body
controls such as `<prosody rate="slow">` modify an individual turn and do not
change the stored identity.

Processors publish the descriptors and values they support. A processor must
reject unsupported requested descriptors; it must not silently ignore them.
This permits one SSML-H lifecycle and document format across engines without
pretending that every voice model has the same design controls.

### Optional Child Elements

A voice definition may contain one `h:description` and one `h:sample`:

```xml
<h:voice-definition name="Elisabeth" scope="profile" seed="8241">
  <h:description>
    An elderly woman with a calm, clear American English voice.
  </h:description>
  <h:sample xml:lang="en-US">
    My name is Elisabeth. I am ready to help with this discussion.
  </h:sample>
</h:voice-definition>
```

`h:description` is a bounded plain-text character description for processors
that advertise free-form voice design. It cannot contain nested markup.

`h:sample` is bounded plain text used as the known bootstrap transcript when a
processor must generate and then clone a voice reference. `xml:lang` identifies
its language. Because the transcript is known, this workflow must not invoke
ASR. If no sample is supplied, a processor may derive a deterministic sample
from the character's first suitable turn or reject the definition. The chosen
policy must be documented and must not fetch or translate remote content.

## Voice Resolution

Standard `<voice>` remains the only body element that selects a speaker:

```xml
<voice name="Bob" required="name">Are we ready?</voice>
```

A name resolves in this order:

1. a voice definition in the current document;
2. an existing saved profile available to the processor;
3. an enabled native or built-in voice from the processor's catalog.

Ambiguous names are rejected. A document-local definition cannot shadow an
existing persistent profile unless it declares `scope="profile"` and
`replace="true"`. Existing profiles need no `h:voice-definition`:

```xml
<voice name="roxyvoice" required="name">Welcome back.</voice>
```

## Scope And Persistence

`scope="request"` creates an in-memory voice reference available only to the
current synthesis request. It is the default. The processor must release the
reference after completion, failure, or cancellation, and it must not add the
voice to the persistent profile catalog.

`scope="profile"` requests a normal saved profile. The processor must:

- enforce its ordinary authorization and storage policy;
- reject a collision unless `replace="true"` is present;
- stage generated audio and metadata outside the active profile catalog;
- use the staged in-memory prompt during the current request; and
- atomically publish the profile only after all synthesis and output encoding
  complete successfully.

For streaming output, a client disconnect or encoder failure prevents the
commit. A failed request must not leave a partial profile or replace a working
one.

Profile persistence is a side effect and must be visible in request metadata or
the response. Builders should require callers to choose `profile` explicitly;
they should never turn persistence on as an implicit convenience.

## Complete Example

```xml
<?xml version="1.0"?>
<speak
  version="1.1"
  xmlns="http://www.w3.org/2001/10/synthesis"
  xmlns:h="https://hangrylabs.app/ns/ssml-h/1.0"
  xml:lang="en-US">

  <metadata>
    <h:extensions version="1.0">
      <h:voice-definition
        name="Bob"
        gender="male"
        age="elderly"
        accent="american"
        scope="profile"
        seed="4242">
        <h:sample xml:lang="en-US">
          My name is Bob. I have spent many years solving difficult problems.
        </h:sample>
      </h:voice-definition>

      <h:voice-definition
        name="Elisabeth"
        gender="female"
        age="elderly"
        accent="american"
        scope="request"
        seed="8241" />
    </h:extensions>
  </metadata>

  <voice name="Bob" required="name">Are we ready?</voice>
  <break time="300ms" />
  <voice name="Elisabeth" required="name">
    Yes. <prosody rate="slow">Everything is prepared.</prosody>
  </voice>
</speak>
```

## Standard Controls And Capabilities

SSML-H does not redefine standard SSML elements. A processor advertises the
SSML 1.1 elements, attributes, values, pronunciation alphabets, languages, and
extensions it implements. At minimum, the first Hangry Labs implementation is
intended to support a documented subset around:

- `<speak>` and `<metadata>`;
- `<voice>` and `<lang>` routing;
- `<break>` boundaries;
- `<prosody>` rate, pitch, and volume controls where supported;
- `<sub>` substitution;
- bounded `<say-as>` interpretations; and
- `<phoneme>` only for alphabets the underlying engine can represent correctly.

Unsupported standard controls are explicit validation errors. A product should
describe itself as supporting an "SSML 1.1-compatible subset with SSML-H 1.0
extensions" until it passes the complete W3C conformance surface.

SSML-H 1.0 does not enable remote `<audio>` fetching, external lexicons, generic
IPA conversion, script execution, or network access. Those features require
separate security and capability specifications.

## Security And Resource Limits

A conforming processor must use a hardened XML parser and enforce configured
limits before inference. Limits include at least:

- source bytes, XML elements, nesting depth, and text length;
- voice definitions and synthesis units per document;
- per-break and total break duration;
- description and bootstrap-sample length;
- generated temporary audio and persistent profile size; and
- model-specific token, phoneme, duration, queue, and request time limits.

The processor must reject unknown namespaces in synthesis content, external
entities, DTDs, external references, path traversal, and unapproved remote
resources. Errors must identify the unsupported element, attribute, value, or
limit without exposing sensitive local paths.

## Builders And Capability Discovery

SSML-H parsers and builders should target the namespace and semantics in this
document rather than an individual model API. A builder must produce valid XML,
preserve standard SSML controls, and make side effects such as profile
persistence explicit. The reference Python implementation is maintained in
[`ssml-h-tools`](https://github.com/hangry-labs/ssml-h-tools).

Processors should expose machine-readable capabilities containing:

- supported SSML-H versions and namespace URIs;
- supported standard SSML elements and attributes;
- supported voice-definition descriptors and accepted values;
- supported languages and pronunciation alphabets;
- configured document and generation limits; and
- persistence availability and authorization requirements.

Capabilities allow a builder to prevent invalid documents before submitting
them while keeping the document portable between speech engines.

## Conformance

A processor conforms to SSML-H 1.0 when it:

- accepts the SSML-H namespace and declaration grammar defined here;
- validates the complete document before synthesis starts;
- rejects unsupported descriptors and standard controls instead of silently
  ignoring them;
- publishes the supported capability subset and resource limits;
- preserves request-scoped and persistent-profile lifecycle guarantees; and
- does not claim support for model features it cannot execute.

A document conforms to SSML-H 1.0 when it uses the namespaces, declarations,
attributes, and content rules defined here and does not rely on behavior that
the target processor has not advertised.

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be
interpreted as described in BCP 14 when, and only when, they appear in all
capitals.

## References

- [W3C Speech Synthesis Markup Language 1.1](https://www.w3.org/TR/speech-synthesis11/)
- [BCP 14: Requirement Levels](https://www.rfc-editor.org/info/bcp14)
- [BCP 47: Language Tags](https://www.rfc-editor.org/info/bcp47)
- [Extensible Markup Language (XML) 1.0](https://www.w3.org/TR/xml/)

## License

Copyright 2026 Hangry Labs. This specification is available under the
[W3C Software and Document License (2023)](LICENSE.md). SSML-H is an
independent Hangry Labs specification. It is not a W3C Recommendation and is
not endorsed by W3C.
