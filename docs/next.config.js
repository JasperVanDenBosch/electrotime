/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/latency-recorder',
  assetPrefix: '/latency-recorder',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
}

module.exports = nextConfig