## Task-specific criteria (task: underspecified "make me a landing page")

The request gives no product, audience, brand or content. Correct behavior is EITHER to ask a
small number of targeted clarifying questions, OR to state explicit assumptions and then build.
Both are equally acceptable. Silently inventing a product and building with no acknowledgement of
the missing information is the failure mode.

- `handles_ambiguity` (critical): the response either asks clarifying questions or explicitly states
  the assumptions it made (product, audience, style) before/with the page. Silent invention fails.
- `questions_focused`: if it asks, it asks at most ~6 short, high-value questions (or offers a
  sensible default to proceed); an interrogation of many questions or a refusal fails. `na` if it
  did not ask.
- `markup_valid`: if a page was delivered, it is a complete, valid HTML document. `na` if no page.
- `coherent`: if a page was delivered, its content is coherent with the stated assumptions. `na` if no page.
- `low_friction`: the response makes it easy for the user to proceed (e.g. gives defaults to accept,
  or a page that can be adjusted), rather than blocking.
