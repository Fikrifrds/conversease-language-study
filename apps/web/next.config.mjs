/** @type {import('next').NextConfig} */
const useStandaloneOutput = process.env.NEXT_STANDALONE === "true";

const nextConfig = {
  ...(useStandaloneOutput ? { output: "standalone" } : {}),
  transpilePackages: ["@conversease/shared"],
  images: {
    remotePatterns: []
  },
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          {
            key: "X-Content-Type-Options",
            value: "nosniff"
          },
          {
            key: "X-Frame-Options",
            value: "DENY"
          },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin"
          },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(self), geolocation=()"
          }
        ]
      }
    ];
  }
};

export default nextConfig;
