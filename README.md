<div align="center">
  <h1>🎓 Maxedu</h1>
  <p><strong>Next-Gen Campus & Library Management Ecosystem</strong></p>
</div>

---

## 📖 What is Maxedu?

**Maxedu** is a comprehensive, production-grade educational management system deeply integrating a modern **Nuxt 3 Vue frontend** with a robust **Frappe Database backend**. 

It is designed to handle complex institutional workflows efficiently—from end-to-end library circulation (requests, issuances, returns, caching, AI recommendation) to an enterprise-grade dynamic **Approval Desk** routing system that powers any custom application or form life-cycle.

---

## 🏗️ Core Module Flow & Documentation

### 1. Library Management System 📚
Maxedu's Library Engine tracks physical book inventory at the ISBN level, enabling high-precision tracking across four primary user personas (Students, Teachers, Staff, Admins).

**Workflow:**
1. **Discovery & AI Recommendation:** Users explore the `/library` catalog. A 5-factor AI-scoring system suggests books based on major, past borrowing history, and peer popularity.
2. **Request & Queue:** Students hit **Request**. If copies are available, it hits the Staff queue. If unavailable, they are added to a Smart Reservation Queue.
3. **Staff Approvals & Issuance:** Library Staff uses `/library/staff-issuance` to process lists of pending requests. They select the exact physical copy (by ISBN) and issue it with an auto-calculated `due_date`.
4. **Circulation & Renewals:** Users monitor their current borrowed materials via role-specific tracking boards. If no one has reserved the book, users can 1-click **Renew** to extend their borrowing period.
5. **Returns & Overdue Penalties:** Fines are automatically accrued based on days overdue. Return transactions instantly increment inventory stock and trigger notifications to the next pending member in the reservation queue.

### 2. Approval Desk Engine ⚙️
Maxedu comes equipped with a completely dynamic, headless workflow engine called the **Approval Desk**, designed to replace paper forms.

**Workflow:**
1. **Form Creation:** Custom forms and field mappings are generated dynamically.
2. **Policy Definitions:** Routing paths (`Approval Policies`) are configured with `Approval Steps` containing `Any One` or `All` requirements.
3. **Application Lifecycle:** When users submit a form, the `Application` automatically populates the `Application Approval Log` for requisite Roles or Specific Users.
4. **Escalations & Fallback:** If primary approvers are missing, the system aggressively falls back to predefined default users/roles, automatically enabling/deactivating logs dynamically based on the step's parallel approval mode.

---

## 🛠 Tech Stack

- **Frontend:** Nuxt 3, Vue 3 Composition API, Tailwind CSS, real-time fetching via `useLibraryBooks` composable
- **Backend:** Frappe Framework, Python 3, MariaDB (utilizing advanced ORM Document classes and controller logic)
- **APIs:** Secure `@frappe.whitelist()` Python controllers mapped directly to Vue states.

---

## 🚀 Future Roadmap & Suggested Improvements

Here is a list of features you can implement next to elevate Maxedu further:

### For the Library Management Module:
* **[Hardware] Barcode / RFID Integration:** Add a Barcode Scanner listener on the Nuxt frontend so staff can issue/return books simply by scanning the book and the student ID card.
* **[Payments] Automated Fine Collection:** Integrate Stripe or Razorpay endpoints to let students pay overdue fines directly from the digital tracking portal without giving staff cash.
* **[Media] Digital E-Library (DRM PDFs):** Connect your existing `pdf-service` to host protected eBooks that expire after the loan period.
* **[Engagement] Gamification Badges:** Award digital badges to students (e.g., "Top Reader of the Month", "Sci-Fi Enthusiast") based on backend statistics logic.

### For the Approval Desk Engine:
* **[UI] Unified Pending Inbox:** Create an "Inbox" view on the frontend that consolidates *all* pending Approval Logs for the logged-in user in a single cohesive Kanban board.
* **[Alerts] Real-Time Sockets & Push Notifications:** Enable Frappe's native `Socket.io` connection with Vue so approvers get an immediate browser alert the second a new application step lands in their queue.
* **[Logic] SLA Timers & Auto-Escalation:** Write a Frappe Scheduled Job (Cron) that evaluates Pending approval logs. If an approval has sat for > 48 hours, automatically send a reminder email or escalate the status to the `fallback_user`.

### General Infrastructure:
* **[Mobile] Native Wrappers:** Use Capacitor.js to wrap the Nuxt frontend, creating native iOS & Android applications with native push-notifications.
* **[Academics] Expansion Modules:** Develop parallel Frappe modules for **Attendance**, **Assignments**, and **Exams**, leveraging your existing Approval Desk infrastructure.