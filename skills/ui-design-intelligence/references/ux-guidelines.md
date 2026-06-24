# UX Guidelines — UI Design Intelligence

99 diretrizes de UX curadas: boas práticas, anti-patterns e acessibilidade. Organizadas por domínio.

---

## AI Interaction

**Disclaimer** _(High)_  
✅ Clearly label AI generated content  
❌ Present AI as human  

**Streaming** _(Medium)_  
✅ Stream text response token by token  
❌ Show loading spinner for 10s+  

**Feedback Loop** _(Low)_  
✅ Thumps up/down or 'Regenerate'  
❌ Static output only  

## Accessibility

**Color Contrast** _(High)_  
✅ Minimum 4.5:1 ratio for normal text  
❌ Low contrast text  

**Color Only** _(High)_  
✅ Use icons/text in addition to color  
❌ Red/green only for error/success  

**Alt Text** _(High)_  
✅ Descriptive alt text for meaningful images  
❌ Empty or missing alt attributes  

**Heading Hierarchy** _(Medium)_  
✅ Use sequential heading levels h1-h6  
❌ Skip heading levels or misuse for styling  

**ARIA Labels** _(High)_  
✅ Add aria-label for icon-only buttons  
❌ Icon buttons without labels  

**Keyboard Navigation** _(High)_  
✅ Tab order matches visual order  
❌ Keyboard traps or illogical tab order  

**Screen Reader** _(Medium)_  
✅ Use semantic HTML and ARIA properly  
❌ Div soup with no semantics  

**Form Labels** _(High)_  
✅ Use label with for attribute or wrap input  
❌ Placeholder-only inputs  

**Error Messages** _(High)_  
✅ Use aria-live or role=alert for errors  
❌ Visual-only error indication  

**Skip Links** _(Medium)_  
✅ Provide skip to main content link  
❌ No skip link on nav-heavy pages  

**Motion Sensitivity** _(High)_  
✅ Respect prefers-reduced-motion  
❌ Force scroll effects  

## Animation

**Excessive Motion** _(High)_  
✅ Animate 1-2 key elements per view maximum  
❌ Animate everything that moves  

**Duration Timing** _(Medium)_  
✅ Use 150-300ms for micro-interactions  
❌ Use animations longer than 500ms for UI  

**Reduced Motion** _(High)_  
✅ Check prefers-reduced-motion media query  
❌ Ignore accessibility motion settings  

**Loading States** _(High)_  
✅ Use skeleton screens or spinners  
❌ Leave UI frozen with no feedback  

**Hover vs Tap** _(High)_  
✅ Use click/tap for primary interactions  
❌ Rely only on hover for important actions  

**Continuous Animation** _(Medium)_  
✅ Use for loading indicators only  
❌ Use for decorative elements  

**Transform Performance** _(Medium)_  
✅ Use transform and opacity for animations  
❌ Animate width/height/top/left properties  

**Easing Functions** _(Low)_  
✅ Use ease-out for entering ease-in for exiting  
❌ Use linear for UI transitions  

## Content

**Truncation** _(Medium)_  
✅ Truncate with ellipsis and expand option  
❌ Overflow or broken layout  

**Date Formatting** _(Low)_  
✅ Use relative or locale-aware dates  
❌ Ambiguous date formats  

**Number Formatting** _(Low)_  
✅ Use thousand separators or abbreviations  
❌ Long unformatted numbers  

**Placeholder Content** _(Low)_  
✅ Use realistic sample data  
❌ Lorem ipsum everywhere  

## Data Entry

**Bulk Actions** _(Low)_  
✅ Allow multi-select and bulk edit  
❌ Single row actions only  

## Feedback

**Loading Indicators** _(High)_  
✅ Show spinner/skeleton for operations > 300ms  
❌ No feedback during loading  

**Empty States** _(Medium)_  
✅ Show helpful message and action  
❌ Blank empty screens  

**Error Recovery** _(Medium)_  
✅ Provide clear next steps  
❌ Error without recovery path  

**Progress Indicators** _(Medium)_  
✅ Step indicators or progress bar  
❌ No indication of progress  

**Toast Notifications** _(Medium)_  
✅ Auto-dismiss after 3-5 seconds  
❌ Toasts that never disappear  

**Confirmation Messages** _(Medium)_  
✅ Brief success message  
❌ Silent success  

## Forms

**Input Labels** _(High)_  
✅ Always show label above or beside input  
❌ Placeholder as only label  

**Error Placement** _(Medium)_  
✅ Show error below related input  
❌ Single error message at top of form  

**Inline Validation** _(Medium)_  
✅ Validate on blur for most fields  
❌ Validate only on submit  

**Input Types** _(Medium)_  
✅ Use email tel number url etc  
❌ Text input for everything  

**Autofill Support** _(Medium)_  
✅ Use autocomplete attribute properly  
❌ Block or ignore autofill  

**Required Indicators** _(Medium)_  
✅ Use asterisk or (required) text  
❌ No indication of required fields  

**Password Visibility** _(Medium)_  
✅ Toggle to show/hide password  
❌ No visibility toggle  

**Submit Feedback** _(High)_  
✅ Show loading then success/error state  
❌ No feedback after submit  

**Input Affordance** _(Medium)_  
✅ Use distinct input styling  
❌ Inputs that look like plain text  

**Mobile Keyboards** _(Medium)_  
✅ Use inputmode attribute  
❌ Default keyboard for all inputs  

## Interaction

**Focus States** _(High)_  
✅ Use visible focus rings on interactive elements  
❌ Remove focus outline without replacement  

**Hover States** _(Medium)_  
✅ Change cursor and add subtle visual change  
❌ No hover feedback on clickable elements  

**Active States** _(Medium)_  
✅ Add pressed/active state visual change  
❌ No feedback during interaction  

**Disabled States** _(Medium)_  
✅ Reduce opacity and change cursor  
❌ Confuse disabled with normal state  

**Loading Buttons** _(High)_  
✅ Disable button and show loading state  
❌ Allow multiple clicks during processing  

**Error Feedback** _(High)_  
✅ Show clear error messages near problem  
❌ Silent failures with no feedback  

**Success Feedback** _(Medium)_  
✅ Show success message or visual change  
❌ No confirmation of completed action  

**Confirmation Dialogs** _(High)_  
✅ Confirm before delete/irreversible actions  
❌ Delete without confirmation  

## Layout

**Z-Index Management** _(High)_  
✅ Define z-index scale system (10 20 30 50)  
❌ Use arbitrary large z-index values  

**Overflow Hidden** _(Medium)_  
✅ Test all content fits within containers  
❌ Blindly apply overflow-hidden  

**Fixed Positioning** _(Medium)_  
✅ Account for safe areas and other fixed elements  
❌ Stack multiple fixed elements carelessly  

**Stacking Context** _(Medium)_  
✅ Understand what creates new stacking context  
❌ Expect z-index to work across contexts  

**Content Jumping** _(High)_  
✅ Reserve space for async content  
❌ Let images/content push layout around  

**Viewport Units** _(Medium)_  
✅ Use dvh or account for mobile browser chrome  
❌ Use 100vh for full-screen mobile layouts  

**Container Width** _(Medium)_  
✅ Limit max-width for text content (65-75ch)  
❌ Let text span full viewport width  

## Navigation

**Smooth Scroll** _(High)_  
✅ Use scroll-behavior: smooth on html element  
❌ Jump directly without transition  

**Sticky Navigation** _(Medium)_  
✅ Add padding-top to body equal to nav height  
❌ Let nav overlap first section content  

**Active State** _(Medium)_  
✅ Highlight active nav item with color/underline  
❌ No visual feedback on current location  

**Back Button** _(High)_  
✅ Preserve navigation history properly  
❌ Break browser/app back button behavior  

**Deep Linking** _(Medium)_  
✅ Update URL on state/view changes  
❌ Static URLs for dynamic content  

**Breadcrumbs** _(Low)_  
✅ Use for sites with 3+ levels of depth  
❌ Use for flat single-level sites  

## Onboarding

**User Freedom** _(Medium)_  
✅ Provide Skip and Back buttons  
❌ Force linear unskippable tour  

## Performance

**Image Optimization** _(High)_  
✅ Use appropriate size and format (WebP)  
❌ Unoptimized full-size images  

**Lazy Loading** _(Medium)_  
✅ Lazy load below-fold images and content  
❌ Load everything upfront  

**Code Splitting** _(Medium)_  
✅ Split code by route/feature  
❌ Single large bundle  

**Caching** _(Medium)_  
✅ Set appropriate cache headers  
❌ No caching strategy  

**Font Loading** _(Medium)_  
✅ Use font-display swap or optional  
❌ Invisible text during font load  

**Third Party Scripts** _(Medium)_  
✅ Load non-critical scripts async/defer  
❌ Synchronous third-party scripts  

**Bundle Size** _(Medium)_  
✅ Monitor and minimize bundle size  
❌ Ignore bundle size growth  

**Render Blocking** _(Medium)_  
✅ Inline critical CSS defer non-critical  
❌ Large blocking CSS files  

## Responsive

**Mobile First** _(Medium)_  
✅ Start with mobile styles then add breakpoints  
❌ Desktop-first causing mobile issues  

**Breakpoint Testing** _(Medium)_  
✅ Test at 320 375 414 768 1024 1440  
❌ Only test on your device  

**Touch Friendly** _(High)_  
✅ Increase touch targets on mobile  
❌ Same tiny buttons on mobile  

**Readable Font Size** _(High)_  
✅ Minimum 16px body text on mobile  
❌ Tiny text on mobile  

**Viewport Meta** _(High)_  
✅ Use width=device-width initial-scale=1  
❌ Missing or incorrect viewport  

**Horizontal Scroll** _(High)_  
✅ Ensure content fits viewport width  
❌ Content wider than viewport  

**Image Scaling** _(Medium)_  
✅ Use max-width: 100% on images  
❌ Fixed width images overflow  

**Table Handling** _(Medium)_  
✅ Use horizontal scroll or card layout  
❌ Wide tables breaking layout  

## Search

**Autocomplete** _(Medium)_  
✅ Show predictions as user types  
❌ Require full type and enter  

**No Results** _(Medium)_  
✅ Show 'No results' with suggestions  
❌ Blank screen or '0 results'  

## Spatial UI

**Gaze Hover** _(High)_  
✅ Scale/highlight element on look  
❌ Static element until pinch  

**Depth Layering** _(Medium)_  
✅ Use glass material and z-offset  
❌ Flat opaque panels blocking view  

## Sustainability

**Auto-Play Video** _(Medium)_  
✅ Click-to-play or pause when off-screen  
❌ Auto-play high-res video loops  

**Asset Weight** _(Medium)_  
✅ Compress and lazy load 3D models  
❌ Load 50MB textures  

## Touch

**Touch Target Size** _(High)_  
✅ Minimum 44x44px touch targets  
❌ Tiny clickable areas  

**Touch Spacing** _(Medium)_  
✅ Minimum 8px gap between touch targets  
❌ Tightly packed clickable elements  

**Gesture Conflicts** _(Medium)_  
✅ Avoid horizontal swipe on main content  
❌ Override system gestures  

**Tap Delay** _(Medium)_  
✅ Use touch-action CSS or fastclick  
❌ Default mobile tap handling  

**Pull to Refresh** _(Low)_  
✅ Disable where not needed  
❌ Enable by default everywhere  

**Haptic Feedback** _(Low)_  
✅ Use for confirmations and important actions  
❌ Overuse vibration feedback  

## Typography

**Line Height** _(Medium)_  
✅ Use 1.5-1.75 for body text  
❌ Cramped or excessive line height  

**Line Length** _(Medium)_  
✅ Limit to 65-75 characters per line  
❌ Full-width text on large screens  

**Font Size Scale** _(Medium)_  
✅ Use consistent modular scale  
❌ Random font sizes  

**Font Loading** _(Medium)_  
✅ Reserve space with fallback font  
❌ Layout shift when fonts load  

**Contrast Readability** _(High)_  
✅ Use darker text on light backgrounds  
❌ Gray text on gray background  

**Heading Clarity** _(Medium)_  
✅ Clear size/weight difference  
❌ Headings similar to body text
