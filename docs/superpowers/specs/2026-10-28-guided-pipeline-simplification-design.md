# Guided pipeline simplification and directional motion

## Scope

Reduce `how-it-was-done.html` to its primary navigation, header, description, source links, and the existing 16-stage guided pipeline. Remove the section-jump links, obsolete `measurements` and `caveats` navigation items, every explanatory section below the pipeline, the graph note, and the footer. Keep the stage-detail dialog and all existing source/result links available from it.

Fold the important interpretive limits from the removed caveats section into the relevant stage explanations: approximate heuristics, the small eight-plan z-score baseline, comparator choice, draft-versus-publication status, and the prohibition on inferring intent. Do not add stages or change the analysis.

## Directional interaction

Use a simultaneous slide-and-fade handoff when changing stages:

- Next: outgoing card moves left and fades while the incoming card enters from the right.
- Previous: outgoing card moves right and fades while the incoming card enters from the left.
- The transition lasts approximately 250 ms, with no scrolling, hash changes, or layout overflow.
- Rapid repeated navigation must not leave multiple visible cards or corrupt the current stage, counter, progress bar, or button states.
- Clicking the currently visible card still opens the centered detail dialog; dialog behavior remains unchanged.
- Under `prefers-reduced-motion: reduce`, change stages immediately without sliding or fading.

## Implementation shape

Keep all 16 anchors in the document as progressive fallbacks. Use the existing `currentIndex`, `renderStage()`, and `moveStage()` flow, adding a small transition state and a temporary outgoing-card layer during animation. The active card remains in normal layout; the outgoing card is positioned over it only for the duration of the handoff. Remove transition artifacts after completion or cancellation.

Remove CSS used only by deleted sections. Retain styles used by the header, pipeline, dialog, and shared links.

## Verification

Update structural tests to require only the pipeline section, reject deleted section IDs and obsolete navigation, and check directional animation hooks and reduced-motion handling. Run the full methodology regression suite.

Validate in headless Chrome at desktop and 375 px mobile widths:

- Only the header and pipeline remain visible.
- All 16 stages remain reachable by buttons and keyboard arrows.
- Next and Previous produce opposite transforms during the handoff.
- Rapid clicks settle on the correct single stage.
- No horizontal overflow or page scrolling occurs during navigation.
- Detail popups retain their content, focus, Close/Escape/backdrop behavior, and important caveats.
- Reduced-motion mode performs an immediate handoff.
