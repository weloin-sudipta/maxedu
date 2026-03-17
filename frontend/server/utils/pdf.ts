import { chromium } from "playwright"
import fs from "fs"

export async function generatePDF(filePath: string, variables:any={}) {

  let html = fs.readFileSync(filePath, "utf8")

  Object.keys(variables).forEach(key => {
    const regex = new RegExp(`{{\\s*${key}\\s*}}`, "g")
    html = html.replace(regex, variables[key])
  })

  const browser = await chromium.launch()
  const page = await browser.newPage()

  await page.setContent(html, { waitUntil: "networkidle" })

  const pdf = await page.pdf({
    format: "A4",
    printBackground: true
  })

  await browser.close()

  return pdf
}