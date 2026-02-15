# Age-Based Prediction Filtering - Quick Reference

## Age Groups & Allowed Categories

```
┌─────────────────────────────────────────────────────────────────┐
│                     AGE CATEGORY MATRIX                         │
└─────────────────────────────────────────────────────────────────┘

Age Group       │ General │ Health │ Parents │ Education │ Career │ Marriage │ Wealth │ Children
───────────────────────────────────────────────────────────────────────────────────────────────
Child           │    ✅   │   ✅   │   ✅    │    ✅     │   ❌   │    ❌    │   ❌   │    ❌
(0-12 years)    │         │        │         │           │        │          │        │

Teenager        │    ✅   │   ✅   │   ✅    │    ✅     │   ✅   │    ❌    │   ❌   │    ❌
(13-17 years)   │         │        │         │           │  (*)   │          │        │

Young Adult     │    ✅   │   ✅   │   ✅    │    ✅     │   ✅   │    ✅    │   ✅   │    ⚠️
(18-24 years)   │         │        │         │           │        │          │        │

Adult           │    ✅   │   ✅   │   ✅    │    ✅     │   ✅   │    ✅    │   ✅   │    ✅
(25-59 years)   │         │        │         │           │        │          │        │

Senior          │    ✅   │   ✅   │   ⚠️    │    ⚠️     │   ⚠️   │    ⚠️    │   ✅   │    ✅
(60+ years)     │         │  (**)  │         │           │        │          │  (**) │

Legend:
✅ = Fully allowed
❌ = Blocked with helpful message
⚠️ = Allowed but may not be most relevant
(*) = Career guidance focuses on education & future planning only
(**) = Priority topics for this age group
```

## Prediction Focus by Age

### Children (0-12)
```
🎨 Focus Areas:
• Natural talents and abilities
• Learning capacity and style
• Educational interests
• Health and vitality
• Family relationships
• Overall development

❌ Avoid:
• Marriage timing
• Career advancement
• Financial planning
• Investment advice
```

### Teenagers (13-17)
```
📚 Focus Areas:
• Academic performance
• Suitable fields of study
• Personal development
• Future career direction
• Health patterns
• Family dynamics

❌ Avoid:
• Marriage predictions
• Wealth accumulation
• Parenting topics
```

### Young Adults (18-24)
```
🚀 Focus Areas:
• Career path selection
• Professional development
• Education completion
• Relationship prospects
• Financial basics
• Independence

⚠️ May not be relevant yet:
• Children/progeny timing
```

### Adults (25-59)
```
💼 Focus Areas:
• All life areas comprehensive
• Career progression
• Marriage/relationships
• Financial planning
• Children
• Health management
• Wealth building
```

### Seniors (60+)
```
🌟 Focus Areas:
• Health and longevity
• Wealth preservation
• Retirement planning
• Family (children/grandchildren)
• Spiritual growth
• Legacy planning

⚠️ Less relevant:
• Career growth
• Marriage timing
• New parent relationships
```

## Example Age Validations

### Test: 6-year-old requesting Marriage prediction
```
Input:
  Name: Ravi
  DOB: 2020-03-11 (6 years old)
  Category: marriage

Output:
  ⚠️ Age-Inappropriate Request
  
  Marriage predictions are not relevant for a 6-year-old child.
  Focus is on education, health, and overall development.
  
  Suggested categories: general, health, parents, education
```

### Test: 16-year-old requesting Career prediction
```
Input:
  Name: Priya
  DOB: 2010-06-15 (16 years old)
  Category: career

Output:
  ✅ Allowed (with teenage context)
  
  AI Prompt includes:
  "Priya is 16 years old (a teenager). Focus on education,
  personal growth, and early career/educational guidance."
  
  Prediction focuses on:
  • Academic strengths
  • Suitable fields of study
  • Future career direction
  • Educational opportunities
```

### Test: 35-year-old requesting any category
```
Input:
  Name: Arjun
  DOB: 1991-03-11 (35 years old)
  Category: any

Output:
  ✅ All categories allowed
  
  Full comprehensive predictions covering all life areas
```

## Implementation Flow

```
┌─────────────────┐
│  User enters    │
│  birth details  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Calculate Age  │
│  from DOB       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ User selects    │
│ category        │
└────────┬────────┘
         │
         ▼
   ┌─────────────────────┐
   │ Is category allowed │
   │   for this age?     │
   └─────────┬───────────┘
             │
      ┌──────┴──────┐
      │             │
     NO            YES
      │             │
      ▼             ▼
┌──────────┐  ┌──────────────┐
│ Return   │  │ Add age      │
│ helpful  │  │ context to   │
│ message  │  │ AI prompt    │
└──────────┘  └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ Generate     │
              │ age-relevant │
              │ prediction   │
              └──────────────┘
```

## Quick Testing Guide

1. **Create test profile at http://localhost:5173**
   - Name: Test Child
   - DOB: 2020-03-11 (or any date making them 6 years old)
   - Time: 10:30:00
   - Place: Chennai, India

2. **Navigate to Predictions page**

3. **Try different categories:**
   - ✅ Education → Should work with child-focused content
   - ✅ Health → Should work
   - ❌ Marriage → Should show blocking message
   - ❌ Career → Should show blocking message

4. **Verify the blocking message** provides:
   - Clear explanation why category is inappropriate
   - Current age of the person
   - Suggestions for relevant categories

5. **Check AI response** includes age context when allowed

## Notes

- Age calculation happens automatically on the backend
- Frontend displays all categories (filtering happens server-side)
- Future enhancement: Hide inappropriate categories on frontend
- System gracefully handles missing birth dates (skips age filtering)
