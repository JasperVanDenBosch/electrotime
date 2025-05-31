const fs = require('fs');
const path = require('path');
const archiver = require('archiver');

const DOCS_API_DIR = path.join(__dirname, '..', 'public', 'docs-api');
const OUT_DIR = path.join(__dirname, '..', 'out');

// Ensure output directory exists
if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function createZip(sourceDir, outputFile, rootFolderName) {
  return new Promise((resolve, reject) => {
    const output = fs.createWriteStream(outputFile);
    const archive = archiver('zip', {
      zlib: { level: 9 } // Maximum compression
    });

    output.on('close', () => {
      const sizeMB = (archive.pointer() / 1024 / 1024).toFixed(2);
      console.log(`✅ Created ${path.basename(outputFile)} (${sizeMB} MB)`);
      resolve();
    });

    archive.on('error', (err) => {
      reject(err);
    });

    archive.pipe(output);

    // Add files to zip with a root folder
    archive.directory(sourceDir, rootFolderName);
    
    archive.finalize();
  });
}

async function packageDocs() {
  console.log('📦 Packaging documentation into ZIP files...\n');

  try {
    // Package Flutter/Dart documentation
    const guiDocsPath = path.join(DOCS_API_DIR, 'gui');
    if (fs.existsSync(guiDocsPath)) {
      const flutterZipPath = path.join(OUT_DIR, 'flutter-dart-docs.zip');
      await createZip(guiDocsPath, flutterZipPath, 'flutter-dart-docs');
    } else {
      console.log('⚠️  Flutter/Dart documentation not found, skipping...');
    }

    // Package Rust firmware documentation
    const firmwareDocsPath = path.join(DOCS_API_DIR, 'firmware');
    if (fs.existsSync(firmwareDocsPath)) {
      const rustZipPath = path.join(OUT_DIR, 'rust-firmware-docs.zip');
      await createZip(firmwareDocsPath, rustZipPath, 'rust-firmware-docs');
    } else {
      console.log('⚠️  Rust firmware documentation not found, skipping...');
    }

    console.log('\n✨ Documentation packaging complete!');
  } catch (error) {
    console.error('❌ Error packaging documentation:', error);
    process.exit(1);
  }
}

// Run the packaging
packageDocs();