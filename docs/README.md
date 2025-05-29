# 📚 Documentation Site

This folder contains the source files for the Latency Recorder documentation website, built with [Syrinx](https://github.com/JasperVanDenBosch/syrinx) static site generator.

## 🏗️ Structure

- `content/` - Markdown source files for the documentation
- `theme/` - HTML templates and CSS styles
- `dist/` - Generated static site (created by build process)
- `requirements.txt` - Python dependencies

## 🚀 Building Locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Build the site:

   ```bash
   syrinx .
   ```

3. Serve locally:

   ```bash
   python -m http.server -d dist [port (default: 8000)]
   ```

Then visit <http://localhost:8000>

## 📝 Adding Content

1. Create or edit markdown files in the `content/` directory
2. Add TOML frontmatter at the top:

   ```toml
   +++
   title = "Page Title"
   description = "Brief description"
   SequenceNumber = 1
   +++
   ```

3. Write content in markdown format

## 🤖 CI/CD

The site is automatically built and deployed to GitHub Pages when changes are pushed to the main branch. See `.github/workflows/docs.yml` for the workflow configuration.

## 🔗 Live Site

Once deployed, the documentation will be available at: <https://jaspervandenbosch.github.io/latency-recorder/>
