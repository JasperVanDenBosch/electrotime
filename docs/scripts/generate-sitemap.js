const fs = require('fs');
const path = require('path');

// Configuration
const SITE_URL = 'https://jaspervandenbosch.github.io/latency-recorder';
const OUT_DIR = path.join(__dirname, '..', 'out');
const SITEMAP_PATH = path.join(OUT_DIR, 'sitemap.xml');

// Pages to include with their priorities
const staticPages = [
  { path: '/', priority: 1.0, changefreq: 'weekly' },
  { path: '/developers', priority: 0.9, changefreq: 'weekly' },
  { path: '/hackathon', priority: 0.9, changefreq: 'weekly' },
  { path: '/api-docs', priority: 0.8, changefreq: 'monthly' },
];

// Function to get all HTML files from the out directory
function getAllPages(dir, basePath = '') {
  const pages = [];
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory() && file !== '_next' && file !== 'docs-api') {
      pages.push(...getAllPages(filePath, path.join(basePath, file)));
    } else if (file === 'index.html' && basePath) {
      // Dynamic pages
      const urlPath = '/' + basePath.replace(/\\/g, '/');
      const priority = urlPath.includes('developers') || urlPath.includes('hackathon') ? 0.7 : 0.6;
      pages.push({
        path: urlPath,
        priority,
        changefreq: 'monthly'
      });
    }
  });

  return pages;
}

// Generate sitemap XML
function generateSitemap() {
  // Get all pages
  const dynamicPages = getAllPages(OUT_DIR);
  const allPages = [...staticPages, ...dynamicPages];

  // Remove duplicates
  const uniquePages = Array.from(new Map(allPages.map(page => [page.path, page])).values());

  // Generate XML
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${uniquePages.map(page => `  <url>
    <loc>${SITE_URL}${page.path}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  // Ensure out directory exists
  if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
  }

  // Write sitemap
  fs.writeFileSync(SITEMAP_PATH, xml);
  console.log(`✅ Sitemap generated at: ${SITEMAP_PATH}`);
  console.log(`   Total pages: ${uniquePages.length}`);
}

// Run the generator
generateSitemap();