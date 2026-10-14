<!-- Cuộn dọc cách tân & Pinning -->

---
name: stacked-cards-scroll
description: Create clean, modern stacked card (overlapping) scroll layouts. Use this skill when the user asks for pricing pages, feature lists, editorial chapters, or interfaces where sections dynamically stack on top of one another.
license: Complete terms in LICENSE.txt
---

This skill focuses on precision and elegance through the "Stacked Cards" or "Sticky Overlap" technique. It creates a highly organized, tactile feeling where sections of the website behave like physical cards stacking on a desk.

The user provides requirements for structured content: a list of services, a step-by-step process, or a multi-tier pricing section.

## Design Thinking

Before coding, structure the tactile interaction:
- **Mechanics**: Will the cards stack exactly on top of each other, or will they leave a small offset (like a folder tab) visible at the top? 
- **Aesthetic**: Choose a bold, high-contrast style. Bento-box layouts, thick borders, vibrant solid colors, or sleek glassmorphism work best here to distinguish one card from another.
- **Interaction**: What happens to the older card when a new one covers it? Does it darken? Does it shrink slightly? 

**CRITICAL**: This effect relies heavily on exact CSS positioning and Z-indexing. The hierarchy of information must be perfectly clear, as the user will literally be stacking the content as they read.

## Stacked Cards Aesthetics & Technical Guidelines

Focus on:
- **CSS-First Approach**: Whenever possible, prioritize native CSS for this specific effect using `position: sticky`, `top: 0` (or `top: 2rem` for offsets), and incrementally higher `z-index` for each subsequent card.
- **Visual Distinction**: Each card MUST have a distinct visual boundary. Use strong `border-radius` (e.g., `rounded-3xl`), subtle `box-shadow`, and alternating background colors/themes to ensure they don't blend into one another.
- **GSAP Enhancements**: If using GSAP, add an effect where the underlying card scales down slightly (e.g., `scale: 0.95`) and reduces opacity as the new card slides over it, mimicking physical depth.
- **Content Formatting**: Keep the content inside the cards concise. If a card's content is taller than the viewport (`100vh`), the sticky effect will break or feel broken. Ensure cards are self-contained visual units.

NEVER use this technique for massive walls of text. Avoid identical background colors for adjacent cards, as it destroys the overlapping illusion. 

IMPORTANT: Elegance comes from restraint. The stacking motion should feel snappy and satisfying, not sluggish. Ensure perfect responsive behavior on mobile by adjusting the `top` offset values.