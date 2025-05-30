/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/latency-recorder',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
}