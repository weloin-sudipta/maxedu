import express from "express";
import { chromium } from "playwright";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const PORT = 3001;

app.use(express.json({ limit: "10mb" }));

// ─────────────────────────────────────────────
//  Health check
// ─────────────────────────────────────────────
app.get("/health", (_req, res) => {
  res.json({ status: "ok", service: "MaxEdu PDF Service", version: "1.0.0" });
});

// ─────────────────────────────────────────────
//  Core engine: HTML  → PDF buffer
// ─────────────────────────────────────────────
async function htmlToPdf(html, options = {}) {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  const page = await browser.newPage();

  await page.setContent(html, { waitUntil: "networkidle" });

  const pdf = await page.pdf({
    format: options.format || "A4",
    landscape: options.landscape || false,
    printBackground: true,
    margin: options.margin || {
      top: "0mm",
      right: "0mm",
      bottom: "0mm",
      left: "0mm",
    },
  });

  await browser.close();
  return pdf;
}

// ─────────────────────────────────────────────
//  POST /generate-pdf
//  Body: { html, options? }
//  Returns: application/pdf binary
// ─────────────────────────────────────────────
app.post("/generate-pdf", async (req, res) => {
  const { html, options = {} } = req.body;

  if (!html) {
    return res.status(400).json({ error: "html is required" });
  }

  try {
    const pdfBuffer = await htmlToPdf(html, options);
    res.setHeader("Content-Type", "application/pdf");
    res.setHeader("Content-Disposition", 'attachment; filename="document.pdf"');
    res.send(pdfBuffer);
  } catch (err) {
    console.error("[PDF Service] Error:", err.message);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`✅ MaxEdu PDF Service running on http://localhost:${PORT}`);
  console.log(`📄 POST /generate-pdf  — HTML to PDF`);
  console.log(`❤️  GET  /health        — Health check`);
});
