<!-- Cuộn ngang sáng tạo -->

---
name: horizontal-scroll-design
description: Create distinctive horizontal scroll interfaces driven by vertical mouse scrolling. Use this skill when the user asks for timelines, galleries, exhibition-style layouts, or side-scrolling websites.
license: Complete terms in LICENSE.txt
---

This skill guides the creation of horizontal scrolling interfaces that feel intuitive and unbreakable. It transforms the standard vertical mouse wheel interaction into a smooth, horizontal journey, perfect for visual-heavy or chronological content.

The user provides requirements for a gallery, portfolio, historical timeline, or product lineup.

## Design Thinking

Before coding, establish the continuous horizontal flow:
- **Spatial Awareness**: The web is typically vertical. When forcing horizontal flow, how do we indicate to the user that they need to keep scrolling? 
- **Tech Stack**: Use GSAP ScrollTrigger to pin a massive vertical container and translate an inner wrapper horizontally (`xPercent: -100`). Include Lenis for smooth momentum.
- **Rhythm**: Break the horizontal monotony. Alternate between wide imagery, dense text blocks, and empty negative space to create a rhythmic pacing.
- **Constraints**: Ensure this experience doesn't break on mobile. Decide whether to keep horizontal on mobile or gracefully degrade to standard vertical.

**CRITICAL**: Calculate widths flawlessly. The fake vertical scroll height must perfectly match the total horizontal width to prevent dead scroll zones or abrupt endings.

## Horizontal Scroll Aesthetics & Technical Guidelines

Focus on:
- **The Core Illusion**: Wrap the content in a `.scroll-section` (width: 100vw, height: 100vh, overflow: hidden). Inside, place a `.horizontal-container` (width: auto, flex/grid). Pin the `.scroll-section` and animate the `.horizontal-container`'s `x` or `xPercent` based on scroll.
- **Typography Direction**: Use massive, oversized typography that bleeds off the screen to visually pull the user's eye to the right. 
- **Parallax within Horizontal**: While the main container moves left, make internal images move slightly right or left at different speeds to create incredible depth (a 2.5D effect).
- **Visual Cues**: Add custom cursors (e.g., "Drag" or arrows) or progress bars at the bottom of the screen to show how far along the horizontal journey the user is.

NEVER leave the user confused about how to navigate. Avoid horizontal scrollbars; hide them using CSS (`::-webkit-scrollbar { display: none; }`). Do not use messy grid layouts that break the strict horizontal axis.

IMPORTANT: Horizontal scrolling feels awful if it's rigid. Smooth scrolling (Lenis) and GSAP scrubbing are absolute requirements here to make it feel like sliding on ice.