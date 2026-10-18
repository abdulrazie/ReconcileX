# ReconcileX 🔍

> **A transaction reconciliation and discrepancy investigation engine for e-commerce payments.**

ReconcileX acts as a financial detective for online merchants. Rather than simply matching records when everything goes smoothly, it specializes in catching real-world accounting anomalies across internal store orders, payment provider gateway reports, and bank settlement statements.

---

## 📌 The Problem

In a typical e-commerce business (e.g., selling accessories in Malaysia):
1. **Store Order:** A customer places order `ORD-1001` for RM250.
2. **Payment Provider Report:** Gateway reports payment `PAY-7781` for RM250 (or may contain duplicates/missing references).
3. **Bank Settlement:** Bank deposits funds minus gateway fees, chargebacks, or timing delays.
4. **ReconcileX Investigation:** Matches records that agree, flags discrepancies (amount mismatches, duplicate payments, ghost charges, delayed settlements), and logs human-readable reason codes for auditing.

---

## 🏗️ Project Structure

```text
reconcilex/
├── .venv/                      # Python virtual environment (ignored by git)
├── .env                        # Local environment variables & secrets (ignored by git)
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Project dependencies
├── README.md                   # Project overview & documentation
├── scripts/
│   └── generate_data.py        # Synthetic dataset generator with planted anomalies
├── src/
│   └── reconcilex/
│       ├── __init__.py         # Package initialization
│       ├── db.py               # Database connections and models
│       └── reconciliation.py   # Core reconciliation and discrepancy detection logic
└── tests/
    └── test_reconciliation.py  # Automated tests for match rules and edge cases
```

---

## 🗺️ Engineering Roadmap

- [ ] **Phase 1: Database Foundation (PostgreSQL)** — Schema design, relational integrity, constraints, transactions.
- [ ] **Phase 2: Realistic Test Data Generation** — Synthetic data generator simulating clean records + 5 deliberate edge cases (duplicates, delayed settlements, fee deductions, amount mismatches, orphan records).
- [ ] **Phase 3: Core Reconciliation Engine** — Deterministic matching rules, reason-code tagging, and audit trail generation.
- [ ] **Phase 4: FastAPI Backend** — Endpoints for file ingestion, reconciliation triggers, and discrepancy investigation.
- [ ] **Phase 5: Automated Testing & Migrations** — Test suite (`pytest`) covering edge cases and database migrations with Alembic.
- [ ] **Phase 6: Portfolio & Deployment** — Docker containerization, structured logging, and CI/CD via GitHub Actions.
