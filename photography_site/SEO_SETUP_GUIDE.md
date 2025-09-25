# SEO Setup Guide for Daniel Ahlberg Photography

This guide will help you optimize the website for search engines and set up Google Search Console and Bing Webmaster Tools.

## 1. Google Search Console Setup

### Step 1: Create Google Search Console Account
1. Go to [Google Search Console](https://search.google.com/search-console/)
2. Sign in with your Google account
3. Click "Add Property"
4. Choose "URL prefix" and enter your domain: `https://danielahlberg.me`

### Step 2: Verify Domain Ownership
Choose one of these verification methods:

**Method A: HTML Meta Tag (Recommended)**
1. Google will provide a meta tag like: `<meta name="google-site-verification" content="ABC123...">`
2. Add the verification code to your `.env` file:
   ```
   GOOGLE_SITE_VERIFICATION=ABC123...
   ```
3. The verification meta tag is already included in the base template

**Method B: HTML File Upload**
1. Download the HTML verification file from Google
2. The URL pattern is already set up: `/google[verification-code].html`
3. Update the verification file view if needed

### Step 3: Submit Sitemap
1. In Google Search Console, go to "Sitemaps"
2. Submit your sitemap URL: `https://danielahlberg.me/sitemap.xml`
3. Google will start indexing your pages

## 2. Bing Webmaster Tools Setup

### Step 1: Create Bing Webmaster Account
1. Go to [Bing Webmaster Tools](https://www.bing.com/webmasters/)
2. Sign in with your Microsoft account
3. Click "Add a site"
4. Enter your website URL: `https://danielahlberg.me`

### Step 2: Verify Domain Ownership
Choose verification method:

**Method A: XML File (Recommended)**
1. Download the `BingSiteAuth.xml` file from Bing
2. The URL is already set up: `/BingSiteAuth.xml`
3. Add your verification code to `.env`:
   ```
   BING_SITE_VERIFICATION=your-bing-verification-code
   ```

**Method B: Meta Tag**
1. Get the meta tag from Bing
2. Add to your `.env` file and update the base template

### Step 3: Submit Sitemap
1. In Bing Webmaster Tools, go to "Sitemaps"
2. Submit: `https://danielahlberg.me/sitemap.xml`

## 3. Environment Configuration

Update your `.env` file with verification codes:

```env
# SEO Configuration
GOOGLE_SITE_VERIFICATION=your-google-verification-code-here
BING_SITE_VERIFICATION=your-bing-verification-code-here
YANDEX_VERIFICATION=your-yandex-verification-code-here

# Site Configuration
SITE_NAME=Daniel Ahlberg Photography
SITE_DOMAIN=danielahlberg.me
```

## 4. SEO Features Implemented

### Meta Tags
- ✅ Title tags with keywords
- ✅ Meta descriptions for all pages
- ✅ Keywords meta tags
- ✅ Canonical URLs
- ✅ Robots meta tags

### Open Graph & Social Media
- ✅ Open Graph meta tags
- ✅ Twitter Card meta tags
- ✅ Social media image optimization

### Structured Data (Schema.org)
- ✅ ProfessionalService schema
- ✅ LocalBusiness schema
- ✅ Person schema (photographer)
- ✅ ImageGallery schema
- ✅ ContactPage schema
- ✅ BreadcrumbList schema

### Technical SEO
- ✅ XML Sitemap generation
- ✅ Robots.txt file
- ✅ Security.txt file
- ✅ Search engine verification files
- ✅ Proper URL structure
- ✅ Mobile-responsive design

## 5. Content Optimization

### Keywords Strategy
Primary keywords:
- "Stockholm photographer"
- "Professional photographer Sweden"
- "Portrait photography Stockholm"
- "Event photographer Sweden"

Long-tail keywords:
- "Professional photographer in Stockholm Sweden"
- "Portrait photography sessions Stockholm"
- "Wedding photographer Stockholm"
- "Commercial photography Sweden"

### Image Optimization
1. Add alt tags to all images
2. Use descriptive filenames
3. Implement image compression
4. Add structured data for images

## 6. Performance Optimization

### Page Speed
- ✅ Google Fonts preconnect
- ✅ Image lazy loading
- ✅ Minified CSS/JS
- ✅ WhiteNoise for static files

### Core Web Vitals
- Monitor in Google Search Console
- Optimize image loading
- Minimize JavaScript execution time

## 7. Local SEO

### Google My Business
1. Create Google My Business profile
2. Add photography category
3. Upload portfolio images
4. Collect customer reviews

### Local Citations
- Add business to local directories
- Ensure NAP consistency (Name, Address, Phone)
- Submit to photography directories

## 8. Social Media Integration

### Social Profiles
Update social media links in templates:
- Instagram: @danielahlberg
- LinkedIn: /in/danielahlberg
- Facebook: /danielahlbergphotography

### Social Sharing
- Implement social sharing buttons
- Optimize images for social platforms
- Create shareable content

## 9. Analytics Setup

### Google Analytics 4
1. Create GA4 property
2. Add tracking code to base template
3. Set up conversion goals
4. Monitor key metrics

### Search Console Integration
- Link Google Analytics with Search Console
- Monitor search performance
- Track click-through rates

## 10. Monitoring & Maintenance

### Weekly Tasks
- Check Search Console for errors
- Monitor keyword rankings
- Review page performance
- Update content regularly

### Monthly Tasks
- Analyze traffic reports
- Update portfolio with new photos
- Check backlink profile
- Review competitor analysis

## 11. Search Engine Submission

### Direct Submission
- Google: Submit via Search Console
- Bing: Submit via Webmaster Tools
- Yandex: https://webmaster.yandex.com/
- DuckDuckGo: Automatic indexing

### Directory Submissions
- Photography directories
- Local business directories
- Professional service directories

## 12. URL Structure

Current SEO-friendly URLs:
- Home: `/`
- Portfolio: `/portfolio/`
- About: `/about/`
- Contact: `/contact/`
- Sitemap: `/sitemap.xml`
- Robots: `/robots.txt`

## 13. Testing Tools

### SEO Testing
- Google Rich Results Test
- Google PageSpeed Insights
- Google Mobile-Friendly Test
- Screaming Frog SEO Spider

### Structured Data Testing
- Google Rich Results Test
- Schema.org Validator
- JSON-LD Validator

## 14. Implementation Checklist

- [ ] Set up Google Search Console
- [ ] Set up Bing Webmaster Tools
- [ ] Add verification codes to .env
- [ ] Submit sitemaps to both search engines
- [ ] Create Google My Business profile
- [ ] Set up Google Analytics 4
- [ ] Test all structured data
- [ ] Optimize images with alt tags
- [ ] Create social media profiles
- [ ] Monitor search console weekly

## 15. Expected Results

### Timeline
- **Week 1-2**: Search engines discover the site
- **Week 3-4**: Pages start appearing in search results
- **Month 2-3**: Improved rankings for target keywords
- **Month 3-6**: Steady organic traffic growth

### Key Metrics to Track
- Organic search traffic
- Keyword rankings
- Click-through rates
- Page load speeds
- Core Web Vitals scores
- Local search visibility

This comprehensive SEO setup will help Daniel Ahlberg Photography achieve strong search engine visibility and attract potential clients searching for photography services in Stockholm.