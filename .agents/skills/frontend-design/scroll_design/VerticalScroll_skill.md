<!-- Cuộn dọc cách tân & Pinning -->

---
name: vertical-scroll-design
description: Create cinematic, production-grade vertical scroll experiences using pinning and staggered animations. Use this skill when the user asks for Apple-style product pages, narrative landing pages, or interfaces where elements lock in place while content reveals on scroll.
license: Complete terms in LICENSE.txt
---

This skill guides the creation of highly interactive vertical scrolling experiences. It rejects boring, static downward scrolling in favor of dynamic storytelling, where the user's scroll wheel acts as a timeline controller for animations.

The user provides requirements for a landing page, product showcase, or storytelling interface.

## Design Thinking

Before coding, understand the narrative flow and commit to a CINEMATIC approach:
- **Pacing**: How fast should the story unfold? Determine which sections need a quick scroll and which require the user to pause and absorb (Pinning).
- **Stack**: ALWAYS use GSAP with ScrollTrigger and a smooth scrolling library (like Lenis) for native-feeling momentum.
- **Tone**: Is it a high-tech hardware reveal (dark mode, glowing gradients, explosive 3D scale) or a luxury editorial (plenty of white space, slow elegant fades, serif typography)?
- **Differentiation**: What makes the pinning moments breathtaking? Avoid generic fade-ups. Use mask reveals, text-splitting, or extreme scaling.

**CRITICAL**: Control the layout. Do not let elements overlap messily during a pin. The scrollbar is your timeline; scrub animations smoothly based on scroll progress.
<!-- Đây là comment -->
## Vertical Scroll Aesthetics & Technical Guidelines

Focus on:
- **Pinning Logic**: Use `pin: true` on major container sections. Keep the user locked in a specific viewport while internal elements (text, images, metrics) animate in and out.
- **Scrubbing & Easing**: Tie animations directly to scroll progress using `scrub: 1` in GSAP. This adds a slight, buttery delay to the animation matching the user's scroll speed.
- **Typography Reveals**: Instead of revealing whole paragraphs, use split-text techniques. Reveal words or characters individually as the user scrolls down. Pair bold Grotesk fonts with elegant Serif accents.
- **Performance**: Animate ONLY `transform` (scale, x, y, rotation) and `opacity`. Use `will-change: transform` on heavily animated elements to prevent layout thrashing and jittering.

NEVER use native `window.addEventListener('scroll')` for these effects. Avoid jittery, un-smoothed scrolling. Do not animate layout properties like `height`, `width`, or `margin` on scroll. 

Remember: Claude is capable of crafting Apple-tier product pages. Execute with extreme precision, ensuring every pixel transitions flawlessly as the user scrolls down the page.