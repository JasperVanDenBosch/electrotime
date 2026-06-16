# 📚 ElectroTime Documentation Site

This folder contains the source files for the Latency Recorder documentation website

## 🏗️ Structure


- `content/` - Markdown documentation content



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
4. Files are ordered by their `SequenceNumber` in frontmatter
