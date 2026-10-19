Review this small feature spec before we implement it.

---

# Spec: Show "last updated" timestamp on the project settings page

## Context
Project admins asked to see when the settings were last changed, to know if a colleague changed something recently. Each project already has a `settings_updated_at` column (timestamptz, NOT NULL, set by the existing `update_project_settings` function in the same transaction as the change; covered by existing tests).

## Change
- On the project settings page (only visible to project admins, existing authorization unchanged), add one line under the page title: "Last updated <relative time>" (e.g. "Last updated 3 hours ago").
- Hovering the relative time shows the absolute time in the viewer's locale and time zone, formatted with the existing `formatDateTime` helper already used across the app.
- The value comes from the existing `GET /projects/:id/settings` response, which already includes `settings_updated_at`; no API or schema change.
- Relative time uses the existing `formatRelative` helper (already used in the activity feed).

## Acceptance criteria
- AC1: Given a project whose settings were changed 3 hours ago, when an admin opens the settings page, then the page shows "Last updated 3 hours ago".
- AC2: Given the same page, when the admin hovers the relative time, then a tooltip shows the absolute date and time in the admin's locale and time zone.
- AC3: Given an admin saves a settings change, when the save succeeds, then the line updates to "Last updated just now" without a page reload (the page already refetches settings after save).

## Out of scope
- Showing who made the change.
- A history of changes.
