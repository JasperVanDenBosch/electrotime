import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(
  request: NextRequest,
  { params }: { params: { path?: string[] } }
) {
  const pathSegments = params.path || ['index.html'];
  const requestedPath = pathSegments.join('/');
  
  // Determine if this is for GUI or firmware docs based on the first segment
  const isGui = requestedPath.startsWith('gui/') || requestedPath === 'gui';
  const isFirmware = requestedPath.startsWith('firmware/') || requestedPath === 'firmware';
  
  let filePath: string;
  
  if (isGui) {
    // Remove 'gui/' prefix and handle the path
    const guiPath = requestedPath.replace(/^gui\/?/, '') || 'index.html';
    filePath = path.join(process.cwd(), 'public', 'docs-api', 'gui', guiPath);
  } else if (isFirmware) {
    // Remove 'firmware/' prefix and handle the path
    const firmwarePath = requestedPath.replace(/^firmware\/?/, '') || 'index.html';
    filePath = path.join(process.cwd(), 'public', 'docs-api', 'firmware', firmwarePath);
  } else {
    // Default to GUI docs if no prefix
    filePath = path.join(process.cwd(), 'public', 'docs-api', 'gui', requestedPath);
  }
  
  // Security check to prevent directory traversal
  const resolvedPath = path.resolve(filePath);
  const publicDir = path.resolve(process.cwd(), 'public', 'docs-api');
  
  if (!resolvedPath.startsWith(publicDir)) {
    return new NextResponse('Forbidden', { status: 403 });
  }
  
  try {
    // Check if file exists
    const stat = await fs.promises.stat(filePath);
    
    // If it's a directory, try to serve index.html
    if (stat.isDirectory()) {
      filePath = path.join(filePath, 'index.html');
    }
    
    // Read the file
    const fileContent = await fs.promises.readFile(filePath);
    
    // Determine content type
    const ext = path.extname(filePath).toLowerCase();
    const contentType = getContentType(ext);
    
    // For HTML files, inject a base tag to fix relative paths
    if (ext === '.html' && (isGui || isFirmware)) {
      const basePath = isGui ? '/api-viewer/gui/' : '/api-viewer/firmware/';
      const htmlContent = fileContent.toString('utf-8');
      
      // Inject base tag if not already present
      if (!htmlContent.includes('<base')) {
        const modifiedHtml = htmlContent.replace(
          '<head>',
          `<head>\n  <base href="${basePath}">`
        );
        
        return new NextResponse(modifiedHtml, {
          headers: { 'Content-Type': contentType },
        });
      }
    }
    
    return new NextResponse(fileContent, {
      headers: { 'Content-Type': contentType },
    });
  } catch (error) {
    // File not found
    return new NextResponse('Not Found', { status: 404 });
  }
}

function getContentType(ext: string): string {
  const contentTypes: { [key: string]: string } = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.md': 'text/markdown',
  };
  
  return contentTypes[ext] || 'application/octet-stream';
}