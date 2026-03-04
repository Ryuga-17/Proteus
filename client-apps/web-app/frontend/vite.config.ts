import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import * as path from "path";
import * as fs from "fs";

// Copy index.html to 404.html after build so Vercel serves SPA on 404
function copy404Plugin() {
  return {
    name: "copy-404",
    closeBundle() {
      const out = path.resolve(__dirname, "dist");
      const index = path.join(out, "index.html");
      const notFound = path.join(out, "404.html");
      if (fs.existsSync(index)) {
        fs.copyFileSync(index, notFound);
        console.log("Copied index.html to 404.html for SPA fallback");
      }
    },
  };
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(), copy404Plugin()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
