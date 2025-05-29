+++
title = "Syrinx"
description = "Documentation for the Syrinx static site generator used for this documentation"
SequenceNumber = 7
+++

# 🦜 Syrinx Static Site Generator

## 📋 Overview

[Syrinx](https://github.com/JasperVanDenBosch/syrinx) is a simple static site generator written in Python that transforms markdown files into HTML websites. It's been used for several EEGManyLabs project websites and offers a straightforward approach to creating documentation sites.

**Key Features:**

- 🐍 Written in Python (78.9%)
- 📝 Markdown to HTML conversion
- 🎨 Uses Jinja templating
- 🚀 Simple deployment options
- 📄 MIT License
- 🌐 Official website: <https://syrinx.site>

## 🚀 Quick Start

Syrinx is a super simple python package for generating a static website.

```bash
pip install syrinx
touch content/index.md
syrinx .
python -m http.server -d dist
```

## 📁 Conventions

Organize your content with some standard structure and syrinx will interpret it.

### Content Structure

- A `content/` directory with markdown file `index.md`
- **TOML-style frontmatter**: Markdown files start with a standard header or "frontmatter" that is surrounded by triple pluses `+++`
- In content directories other than root, `index.md` is optional. Leaving it out signifies that you do not want a separate page built for this branch

### Special Frontmatter Entries

- **SequenceNumber**: Used by templates to order child items in menus and lists
- **Archetype**: The name of the template used to import table data

### Templating and Style

- Templates are written in **jinja2** and go into the `theme/templates/` directory
- The default template used is `page.jinja2`
- If a template is found matching the name of the node (e.g. `foo.jinja2`), or `root.jinja2` for the top-most page, this takes precedence
- CSS, images and other assets go into `theme/assets/`

### Table Data

Syrinx can generate content (markdown) files from CSV tables in the `data/` directory:

- The archetype file used will be based on the filename of the data file
- Each row is considered one record
- The header (1st) row will be used as keys
- The first column is used as name for the content item
- Each column will be converted to a variable in the front matter

## 🔧 Technology Stack

- **Python** - Core language
- **Jinja2** - Templating engine
- **CSS** - Styling
- **Docker** - For containerized deployment (optional)

## 🚀 Deployment Options

### Option 1: DigitalOcean App Platform "Pull" Method 📥

Simple deployment approach:

1. Generate your site locally
2. Commit HTML files and assets to the `dist` directory
3. Create an App Platform app pointing to your GitHub repository
4. Configure the app to serve files from the `dist` directory

### Option 2: DigitalOcean App Platform "Push" Method 📤

Advanced deployment with more control:

1. Create a `Dockerfile` for your site
2. Write a DigitalOcean App specification in YAML
3. Build and push Docker container to a registry
4. Use `doctl` command-line tool to deploy

## 💡 Why Use Syrinx?

- **Simplicity** - Easy to get started with basic Python knowledge
- **Markdown-based** - Write content in familiar markdown format
- **Flexibility** - Jinja templates allow customization
- **Proven** - Successfully used for multiple EEGManyLabs websites
- **Open Source** - MIT licensed for freedom to modify

## 🏗️ Potential Use Cases for Latency Recorder

1. **Project Documentation Site** - Create a comprehensive website documenting the hardware, software, and usage instructions
2. **Tutorial Hub** - Build step-by-step guides for assembling and using the device
3. **Community Portal** - Share updates, contributor information, and project news
4. **API Documentation** - If the project develops APIs, document them clearly

## 🔗 Resources

- **GitHub Repository:** <https://github.com/JasperVanDenBosch/syrinx>
- **Official Website:** <https://syrinx.site>
- **License:** MIT

## 📝 Getting Started

To use Syrinx for the Latency Recorder documentation:

1. Clone the Syrinx repository
2. Create markdown files for your content
3. Configure templates as needed
4. Generate the static site
5. Deploy using your preferred method

For detailed usage instructions, refer to the [official Syrinx repository](https://github.com/JasperVanDenBosch/syrinx) and documentation.
