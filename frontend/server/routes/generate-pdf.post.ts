import { generatePDF } from "../utils/pdf"
import path from "path"
import fs from "fs"

// Static absolute path — no import.meta.url needed
const TEMPLATES_DIR = path.join(process.cwd(), 'templates')
export default defineEventHandler(async (event) => {
  try {
    const body = await readBody(event)
    const { template, variables } = body

    if (!template) {
      throw createError({ statusCode: 400, statusMessage: "Template name is required" })
    }

    // Sanitize: strip any directory traversal
    const safeName = path.basename(template)
    const filePath = path.join(TEMPLATES_DIR, safeName)

    if (!fs.existsSync(filePath)) {
      throw createError({
        statusCode: 404,
        statusMessage: `Template "${safeName}" not found. Looking in: ${TEMPLATES_DIR}`
      })
    }

    const pdf = await generatePDF(filePath, variables)

    setHeader(event, 'Content-Type', 'application/pdf')
    setHeader(event, 'Content-Disposition', `attachment; filename="${path.basename(safeName, '.html')}.pdf"`)

    return pdf

  } catch (error: any) {
    if (error.statusCode) throw error
    throw createError({
      statusCode: 500,
      statusMessage: error.message || 'Failed to generate PDF'
    })
  }
})