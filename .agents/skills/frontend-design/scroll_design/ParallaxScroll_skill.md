<!-- Cuộn đa tầng có chiều sâu -->

---
name: parallax-scroll-design
description: Create deeply immersive multi-layer parallax scrolling websites. Use this skill when the user asks for websites with depth, floating elements, 3D illusions, environmental storytelling, or layered background effects.
license: Complete terms in LICENSE.txt
---

This skill guides the creation of true Parallax environments. Instead of a flat webpage, you are building a stage with a foreground, midground, and background that react to the scroll wheel at entirely different velocities.

The user provides requirements for a visually rich landing page, environmental site (nature, space, architecture), or heavily illustrated storytelling experience.

## Design Thinking

Before coding, think in the Z-axis (Depth):
- **Layering**: Define at least 3 distinct visual layers. Background (moves slowest), Content/Midground (moves normally), Foreground/Overlays (moves fastest, creating the illusion of being close to the camera).
- **Concept**: Are we diving deep into an ocean, flying through clouds, or walking through a brutalist architectural space? Match the layer speeds to the physical reality of that concept.
- **Contrast**: Parallax works best when there is high contrast between layers (e.g., sharp typography overlapping blurry background imagery).

**CRITICAL**: Restraint is key. Do not make text difficult to read by placing it on a wildly moving, noisy background. Preserve legibility while maximizing the 3D illusion.

## Parallax Aesthetics & Technical Guidelines

Focus on:
- **Implementation Logic**: Use GSAP ScrollTrigger's `data-speed` attribute or `yPercent` animations. For example, background layer `yPercent: 30`, foreground layer `yPercent: -50` over the scroll duration.
- **Scale and Blur**: Enhance the parallax effect by slightly scaling up background layers as the user scrolls, or adding a CSS `backdrop-filter: blur()` that dynamically changes intensity.
- **Composition**: Use elements that break the grid—floating shapes, overlapping cut-out images (PNGs/WebPs with transparency), or typography that slides behind images.
- **Performance**: Parallax is heavy. NEVER animate `background-position` for parallax as it forces CPU repaints. Instead, use an absolute positioned `div` with an `img` or `background-image` and animate its CSS `transform: translateY()`.

NEVER create nausea-inducing motion by making elements move too fast or in completely random, conflicting directions. Avoid generic "flat" UI components within a parallax space.

Remember: A great parallax site feels like looking out of a moving train window. Execute the math and CSS transforms flawlessly to maintain the illusion.