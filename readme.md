# Project 2: Internal Operations API

## Role Matrix (Access Control)

| Role | Read (Customers/Tickets/Orders) | Create Tickets | Create Customers & Orders |
| :--- | :---: | :---: | :---: |
| **`viewer`** | ✅ | ❌ | ❌ |
| **`support_agent`** | ✅ | ✅ | ❌ |
| **`billing_admin`** | ✅ | ✅ | ✅ |

---

## Portfolio Presentation Note
> **Production SaaS Deployment Case Study:**
> This Internal Operations API represents the primary workload deployed and containerized in **Phase 4 (Cloud Infrastructure & Provisioning)**.
