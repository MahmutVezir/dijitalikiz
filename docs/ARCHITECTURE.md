# Research Architecture

## Purpose

This repository is the experimental infrastructure for:

**LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi**

The scientific target is unchanged: determine whether explicit Cross-Component Dependency Graph (CCDG) representation improves LLM root-cause diagnosis compared with the frozen Standard Context condition.

## Runtime architecture

```
GitHub
  |
  +-- source code / protocol / test suite
  |
  +-- GitHub Actions
          |
          v
       Kaggle GPU
          |
          v
 Hugging Face checkpoint
          |
          v
         LLM
       /     \
Standard    CCDG
Context     Context
       \     /
        Evaluation
            |
      Case-level result
            |
   Exact McNemar analysis
```

## Components

- **GitHub:** source control, research protocol, manifests, tests, reproducibility evidence.
- **Python:** experiment runner, context construction, output parsing, deterministic evaluation and statistical analysis.
- **Kaggle:** GPU execution environment for the frozen pilot/benchmark.
- **Hugging Face:** model/checkpoint distribution.
- **LLM:** experimental system under evaluation.
- **pytest/GitHub Actions:** software and protocol regression checks.

## Explicitly out of scope

- Supabase as a database/backend.
- Vercel as a deployment/runtime platform.
- Next.js/React frontend.
- PostgreSQL application database.
- Authentication.
- A production dashboard.

These services are not required by the research question and would add infrastructure without improving the primary experimental comparison.

## Important data distinction

A case may legitimately contain technology names such as Vercel or Supabase because those technologies can be part of the software system being diagnosed. Such case records are research data and must **not** be deleted merely because the corresponding services are not used by this repository.

## Scientific invariants

The following must not be changed merely to simplify infrastructure:

1. Standard vs CCDG is the primary experimental contrast.
2. Ground truth remains hidden from model context.
3. Model checkpoint/revision remains frozen.
4. Generation parameters and seeds remain frozen for the declared pilot.
5. The primary analysis unit remains the software case, not an individual seed.
6. The declared case-level majority rule remains unchanged.
7. The primary inferential test remains the exact two-sided McNemar test.
8. No observed pilot result may be used to retrofit the protocol.
9. No result may be fabricated, simulated, or inferred from code readiness.

## Repository cleanup policy

Legacy research material may be archived only after dependency checks. Binary archives and historical snapshots are not part of the active runtime. They should be removed only when their contents are preserved elsewhere or demonstrably unnecessary.

The active experiment remains protocol-ready and experiment-pending until real inference data and the confirmatory benchmark are completed.
