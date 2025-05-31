# 📚 ElectroTime Documentation Site

This folder contains the source files for the Latency Recorder documentation website, built with Next.js 15 and React.

## 🏗️ Structure

- `app/` - Next.js App Router pages and layouts
- `components/` - React components (navigation, markdown renderer, etc.)
- `content/` - Markdown documentation content
- `public/` - Static assets and API documentation
- `scripts/` - Build scripts for sitemap and documentation packaging
- `styles/` - Global CSS styles
- `out/` - Generated static site (created by build process)

## 🚀 Development

### Prerequisites

- Node.js 20 or later
- npm or yarn
- Dart SDK (for generating Flutter docs)
- Rust toolchain (for generating Rust docs)

### Running Locally

1. Install dependencies:
   ```bash
   npm install
   ```

2. Generate API documentation (optional):
   ```bash
   npm run generate-docs
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

4. Visit <http://localhost:3000>

### Building for Production

```bash
npm run build
```

This will:
- Build the Next.js static site
- Generate sitemap.xml
- Package API documentation into downloadable ZIP files
- Output everything to the `out/` directory

### Serving the Production Build

```bash
npm start
```

## 📝 Content Management

### Adding Documentation Pages

1. Create or edit markdown files in the `content/` directory
2. Add TOML frontmatter at the top:
   ```toml
   +++
   title = "Page Title"
   description = "Brief description"
   SequenceNumber = 10
   +++
   ```
3. Write content in markdown format

### Navigation Structure

The navigation is automatically generated from the file structure:
- `content/hackathon/` - Hackathon-related documentation
- `content/developers/` - Developer documentation
- Files are ordered by their `SequenceNumber` in frontmatter

## 🔧 API Documentation

### Generating API Docs

```bash
# Generate all API documentation
npm run generate-docs

# Package docs into ZIP files
npm run package-docs
```

This creates:
- **Flutter/Dart docs**: Full API reference with search functionality
- **Rust firmware docs**: Documentation for latreclib, recorder, and simulator crates

### Accessing API Documentation

API documentation is available in two ways:
1. **Download as ZIP**: Recommended for Flutter docs (full functionality)
2. **View online**: Limited functionality, suitable for quick reference

## 🎨 Features

- **Dark mode by default** with light mode toggle
- **Responsive design** for mobile and desktop
- **Syntax highlighting** for code blocks
- **Breadcrumb navigation** for easy orientation
- **SEO optimized** with metadata and sitemap
- **Static export** for GitHub Pages hosting

## 🤖 CI/CD

The site is automatically built and deployed to GitHub Pages when changes are pushed to the main branch. The workflow:
1. Generates Rust and Flutter API documentation
2. Builds the Next.js site
3. Packages documentation as ZIP files
4. Deploys to GitHub Pages

See `.github/workflows/docs.yml` for the complete workflow.

## 🔗 Live Site

The documentation is available at: <https://jaspervandenbosch.github.io/latency-recorder/>

## 🛠️ Technology Stack

- **Framework**: Next.js 15.3 with App Router
- **UI Components**: Radix UI with Tailwind CSS
- **Markdown**: react-markdown with GitHub Flavored Markdown
- **Syntax Highlighting**: react-syntax-highlighter
- **Documentation Generation**: 
  - Rust: `cargo doc`
  - Flutter: `dart doc`
- **Deployment**: GitHub Pages with static export

## 📦 Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Serve production build
- `npm run lint` - Run ESLint
- `npm run generate-docs` - Generate API documentation
- `npm run package-docs` - Create downloadable ZIP files

## 🤝 Contributing

When contributing to the documentation:
1. Follow the existing markdown style
2. Ensure all links work correctly
3. Test on both desktop and mobile
4. Verify the build passes before submitting PR