---
markdown-sharing:
  uri: 1ffe584a-c23e-49cb-9fbb-365a2a26f3e3
---
# AI SDLC Test Verification Phase User Manual

* Installation: [Reference Document](https://markdown.fzzixun.com/d/9ad9e4f3-f0ac-40f2-ad7d-e4676a39dafe)## Who is this manual for?

This manual is intended for product managers, business analysis, design, R&D, testing, and all students involved in the closed loop from demand to delivery.  
The goal is to help you quickly understand the concepts, processes, and skill division of labor in the "test verification" phase of AI SDLC without getting bogged down in technical details.

---

## 1. First understand the three core concepts

### 1) The acceptance criteria are executable and traceable

- **Executable**: Convert AC (acceptance criteria) into step-by-step, expected, and judgeable test cases.  
- **Traceability**: Every use case can be traced back to`solution.md`or`prd.md`With AC, every failure can be located to use cases and defects.  
- Value: answer "whether it meets the acceptance criteria" and "whether it meets the delivery conditions" instead of "tested".

### 2) Separate verification products from implementation plans

- **Implementation Plan** (`implementation/plan.md`) belongs to the implementation phase: what to do, how to do it, and delivered in batches.  
- **Verification Product** (`verification/*`) belongs to the verification stage: what to test, how to test, and what are the conclusions.  
- Value: Implementation and verification perform their own duties to avoid boundary drift caused by "testing and modifying while doing".

### 3) Manual by default, structure can be migrated

- **Manual testing is performed by default** to run through the shortest closed loop, and automation is not forced to be implemented at this stage.  
- **Use case structure** remains stable (numbering, steps, expectations, traceability), which facilitates subsequent import into the use case management system or generation of automated scripts.  
- Value: First pass the verification closed loop, and then enhance automation as needed, without blocking delivery due to automation thresholds.

---

## 2. The standard process you will go through (V1–V4)

The process is advanced in modules, and each step can be independently executed, reviewed, and reflowed independently.

### V1: Test Plan

- **Function**: Freeze the "scope, strategy, environment, admission/exit criteria" of this verification.  
- **Core Output**:`verification/test-plan.md`.  
- **Corresponding skills**:`spec-test-plan`.

### V2: Test cases (Usecases)

- **Function**: Convert AC into executable steps and expected results. It is used for manual execution by default.  
- **Core Output**:`verification/usecase.md`.  
- **Corresponding skills**:`spec-test-usecase`.

### V3: Test Suites

- **Function**: Organize use cases into "executable collections" (smoke/regression/directed regression), and define execution order and blocking rules.  
- **Core Output**:`verification/suites.md`.  
- **Corresponding skills**:`spec-test-suites`.

### V4: Test execution and reporting

- **Role**: Perform verification and produce conclusive reports: whether passed, coverage, risks and defect references.  
- **Core Output**:`verification/report-{date}-{version}.md`.  
- **Corresponding skills**:`spec-test-execute`.

---

## 3. Routing principle: One "brain" makes decisions, and other skills focus on execution

During the verification phase,`spec-test`This is the main skill entrance:

- Responsible for determining "what to do next" (V1→V2→V3→V4).  
- Responsible for access control inspection (whether conditions are met to continue).  
- Responsible for automatically advancing between stages or interrupting when necessary.

Each sub-skill (such as`spec-test-plan`、`spec-test-usecase`) is Worker:

- Only responsible for the goals, products and quality thresholds of this stage.  
- Come back when you're done`spec-test`Decide on next steps.

The advantage of this is to reduce the process drift of "everyone jumps steps according to their own understanding".

---

## 4. The two most commonly used landing paths

### Path A: Shortest closed loop (suitable for simple needs)`spec-test-plan` → `spec-test-usecase` → `spec-test-execute`Applicable features:

- Mainly changes in rules/configuration/copywriting;
- The impact is small and the regression range is clear;
- The acceptance criteria can be written directly in the plan document.

Note: V3 can be merged into V2 (in`usecase.md`Directly maintain the "Package Definition" section).

### Path B: Standard closed loop (suitable for medium to complex requirements)`spec-test-plan` → `spec-test-usecase` → `spec-test-suites` → `spec-test-execute`Applicable features:

- There is obvious impact or risk of regression;
- Requires smoke blocking, directional regression and other execution arrangements;
-Multiple rounds of verification and multi-role collaboration.

---

## 5. Please adhere to the practical guidelines when using

- **Conclusion first**: The report first states "Pass/Fail/Conditional Pass", and then cites coverage, risks and defects.  
- **Clear scope**: In/Out in the test plan is clear, and`requirements/*`consistent.  
- **Unknown not pending**: The risk enters the "Risk and Verification List" (Owner/Cutoff/Signal/Action), or the "Remaining Risk/Blocking Item" in the report.  
- **Traceability**: Each use case is linked to at least 1 AC; each failure/blocking item can be located to the use case number and external defect number.  
- **Defects not placed on disk**: Defects are carried by the team's existing defect system/Issue/Work Order; only the number and link are referenced in the Spec Pack, and no new BUG files are added.

---

## 6. Skill quick check (test verification side)

-`spec-test`: Verification stage process navigation and access control routing center
-`spec-context`: Locate the current demand context (execute pre-guarantee)
-`spec-test-plan`: Generate/update test plan
-`spec-test-usecase`: Generate/update test cases
-`spec-test-suites`: Generate/update test suite
-`spec-test-execute`: Execute verification and produce test report

---

## 7. You can start like this

1. First determine whether the requirement belongs to "shortest closed loop" or "standard closed loop".  
2. use`spec-test`Enter the corresponding path; read and write`verification/*`execute before`spec-context`Get`FEATURE_DIR`.  
3. Do a minimum review after each step is completed, and do not leave key differences until later.  
4. When ambiguity occurs, the previous stage document (such as`test-plan.md`or`usecase.md`), without directly jumping to subsequent stages.

When the team runs this way for a while, you will see three obvious changes:
The acceptance criteria are clearer, failures are traceable, and delivery conclusions are more predictable.