# SEO Metadata Block — Developer Handoff Template

> **This is NOT a visual design section.** It's a structured metadata template that gets applied in the `<head>` of the final HTML page by the development team. Each consulting service page should have its own completed version of this block.

---

## Page metadata

```html
<!-- Primary Meta Tags -->
<title>[Service Name] Consulting Services | Edstellar</title>
<meta name="description" content="[150-160 character description of the consulting service, including primary keyword and value proposition]">
<meta name="keywords" content="[primary keyword], [secondary keyword], [brand keyword], corporate training, consulting services, Edstellar">

<!-- URL / Slug -->
<!-- https://www.edstellar.com/consulting/[service-slug] -->

<!-- Canonical -->
<link rel="canonical" href="https://www.edstellar.com/consulting/[service-slug]">

<!-- Open Graph / Social -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.edstellar.com/consulting/[service-slug]">
<meta property="og:title" content="[Service Name] Consulting Services | Edstellar">
<meta property="og:description" content="[Same as meta description or slightly shorter for social]">
<meta property="og:image" content="https://www.edstellar.com/images/consulting/[service-slug]-og.jpg">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://www.edstellar.com/consulting/[service-slug]">
<meta property="twitter:title" content="[Service Name] Consulting Services | Edstellar">
<meta property="twitter:description" content="[Same as meta description]">
<meta property="twitter:image" content="https://www.edstellar.com/images/consulting/[service-slug]-og.jpg">

<!-- Structured Data / Schema.org -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "[Service Name] Consulting",
  "provider": {
    "@type": "Organization",
    "name": "Edstellar",
    "url": "https://www.edstellar.com"
  },
  "description": "[Full service description for schema]",
  "areaServed": "Worldwide",
  "serviceType": "[Service category — e.g. Learning and Development Consulting]"
}
</script>
```

---

## Example: L&D Consulting Page

```html
<title>Learning and Development Consulting Services | Edstellar</title>
<meta name="description" content="Transform workforce capability into business performance with Edstellar's L&D consulting. Strategic frameworks, skills gap analysis, and measurable impact for enterprises.">
<meta name="keywords" content="L&D consulting, learning and development consulting, corporate training consulting, skills gap analysis, workforce development, Edstellar">
<link rel="canonical" href="https://www.edstellar.com/consulting/learning-and-development">
```

---

## Checklist for each page

- [ ] Meta title (under 60 characters, includes primary keyword + brand)
- [ ] Meta description (150-160 characters, includes primary keyword + CTA)
- [ ] URL slug (lowercase, hyphenated, matches service name)
- [ ] Canonical URL set
- [ ] OG image created (1200x630px, service-specific)
- [ ] Schema.org Service markup added
- [ ] H1 matches or closely relates to meta title
- [ ] No duplicate meta descriptions across consulting pages
- [ ] Breadcrumb structured data matches page hierarchy

---

## Notes for dev team

1. **Each consulting page gets its own completed metadata block** — do not reuse descriptions across pages
2. **OG images** should follow Edstellar brand (navy background, lime accent, service name in Plus Jakarta Sans)
3. **URL structure:** `edstellar.com/consulting/[service-slug]` — keep slugs short and keyword-rich
4. **Schema markup** should be validated using Google's Rich Results Test before deployment
5. **The content team** (Vijay's team) will provide the final meta title and description — this template is the structure
