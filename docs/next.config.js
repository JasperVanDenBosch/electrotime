/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/electrotime',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
}

module.exports = nextConfig