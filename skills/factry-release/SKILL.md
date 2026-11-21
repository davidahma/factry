---
name: factry-release
description: Prepare, publish, or verify a versioned software release using the repository’s release policy. Use for tags, release assets, package registries, and checks of the artifact users actually install.
---

# Release a version

Identify the requested endpoint, source repository, destination, version, and release policy. Preparing release notes or verifying an existing release can be completed without publishing. Check whether pushing a tag triggers publication before performing that action.

1. Resolve the intended commit and verify the required tests and release metadata for it. Check the remote tag, existing release or registry version, and any in-progress publication. Peel an annotated tag to its commit before comparing. If an existing tag targets a different commit or an existing version contains different artifacts, report the conflict. Preserve the existing version and tag.
2. Build or select the intended artifacts from the verified source using the repository’s release path. Inspect their contents, version, and any required license or metadata. Capture expected digests from the build or trusted provenance when available. Exercise the packaged entry point in a clean environment. Keep build and consumer testing isolated from publication credentials.
3. For an authorized publication, use the repository’s release workflow. Confirm the tag still targets the intended commit before publishing. If publication times out or partially succeeds, read the destination and workflow state first. Reconcile the version, tag, asset set and digests. Resume only the authorized missing work when it is safe to repeat.
4. Read back the published version and commit from the destination. Fetch the assets or package by that version through the consumer-facing path. Compare downloaded bytes with the expected artifacts or independently verified digests. Follow the documented clean install or extraction path and run the smallest meaningful smoke check. For a source-only release, inspect the downloaded source archive and exercise its documented usage.

Report the observed release state, version, commit, destination, and artifact and consumer checks. A partial upload, pending publish job, or unavailable install check needs an explicit status and next step.
