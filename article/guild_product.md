---
markdown-sharing:
  uri: cbc531dd-b12e-410f-a6f0-6ca66abc360f
---
# AI SDLC Product Requirements Process User Manual

* Installation: [Reference Document](https://markdown.fzzixun.com/d/9ad9e4f3-f0ac-40f2-ad7d-e4676a39dafe)## Who is this manual for?

This manual is intended for product managers, business analysis, design, R&D, testing, and all students involved in the closed loop from demand to delivery.  
The goal is to help you quickly understand the concepts, processes, and skill division of AI SDLC in the "product requirements clarification" phase without getting bogged down in technical details.

---

## 1. First understand the three core concepts

### 1) Two-tier SSOT: stable at the project level and flexible at the demand level

- **Project-level SSOT**: Precipitate long-term stable business boundaries, terminology, modules and constraints.  
- **Requirement-level SSOT (Spec Pack)**: Establish an independent space around a single requirement and focus on this goal and decision-making.  
- Value: It can not only reuse organizational knowledge, but also avoid "one requirement changing the global document".

### 2) Spec as Code: Manage requirements like code

- Each requirement has an independent branch and structured directory.  
- Each stage only produces authoritative documents for that stage.  
- All conclusions are traceable, reviewable and iterable.  
- Value: Reduce verbal synchronization loss and make cross-role collaboration more controllable.

### 3) Progressive disclosure: read on demand, converge by stages

- Not reading all the information at once.  
- Only the "minimum necessary context" is consumed in the current stage.  
- The output follows "conclusion first, supported by evidence, and verifiable".
- Value: Avoid information overload and improve decision-making speed and quality.

---

## 2. The standard process you will go through (R0-R4)

The process is advanced in modules, and each step can be independently executed, reviewed, and reflowed independently.

### R0: Spec initialization

- Function: Create an independent workspace for this requirement.  
- Result: The underlying context forming the requirements is precipitated with the original input.  
- Corresponding skills:`spec-init`.

### R1: Requirements clarification and plan formation

- Function: Turn vague requirements into reviewable solutions.  
- Core output:`solution.md`(Clear what to do, what not to do, and how to accept it).  
- Corresponding skills:`spec-product-clarify`.

### R1.5: Impact analysis (automatic enhancement after R1)

- Role: Identify affected modules, constraints and potential risks.  
- Core output:`solution.md`in`Impact Analysis`.  
- Value: Provide boundary guardrails for subsequent design and implementation.

### R2: PRD generation (optional)

- Function: Convert the plan into deliverable specifications.  
- Applicable: When the requirements are complex, the cost of cross-role collaboration is high, and the acceptance criteria need to be frozen.  
- Corresponding skills:`spec-product-prd`.

### R3: Prototype generation (optional)

- Function: Convert scenes and rules into walkable interactions and wireframe expressions.  
- Applicable: When there are obvious interactive changes or easy to produce misunderstandings.  
- Corresponding skills:`spec-product-prototype`.

### R4: Interactive Demo (optional)

- Function: "run" key interactions for higher-fidelity review.  
- Applicable: When it is necessary to quickly align experience expectations with business parties, R&D, and testing.  
- Corresponding skills:`spec-product-demo`.

---

## 3. Routing principle: One "brain" makes decisions, and other skills focus on execution.

In AI SDLC,`using-aisdlc`Is the only router (Router):

- Responsible for determining “what to do next”.  
- Responsible for access control inspection (whether conditions are met to continue).  
- Responsible for automatically advancing between stages or interrupting when necessary.  

Skills at each stage (such as`spec-product-clarify`、`spec-product-prd`) is Worker:

- Only responsible for the goals, products and quality thresholds of this stage.  
- When finished, go back to Router to decide the next step.  

The advantage of this is to reduce the process drift of "everyone jumps steps according to their own understanding".

---

## 4. The two most commonly used landing paths

### Path A: Shortest closed loop (suitable for simple needs)`spec-init` → `spec-product-clarify`(Including impact analysis) → Enter the design stage

Applicable features:

- Mainly changes in rules/configuration/copywriting;
- Interaction changes are minimal;
- The acceptance criteria can be written directly in the plan document.

### Path B: Standard closed loop (suitable for medium to complex requirements)`spec-init` → `spec-product-clarify` → `spec-product-prd`→(on demand)`spec-product-prototype`→(on demand)`spec-product-demo`→ Enter the design stage

Applicable features:

- There are significant interactions or process changes;
- Involves multi-role collaboration and review;
- Need for higher certainty in delivery and acceptance standards.

---

## 5. Please adhere to the practical guidelines when using

- **Conclusion first**: state the conclusion first, and then provide evidence and verification methods.  
- **Clear Scope**: In/Out is clear to avoid requirement creep.  
- **Unknowns are not left vacant**: Do not write "problems to be confirmed", use "hypothesis + verification list" to undertake.  
- **Closed loop within the stage**: Every step must have evaluable products, and problems should not be pushed to the next stage.  
- **Traceability**: Key conclusions can be traced back to the original requirements and previous documents.

---

## 6. Skills quick check (product demand side)

-`using-aisdlc`: Process navigation and access control routing center
-`spec-context`: Locate the current demand context (execute pre-guarantee)
-`spec-init`:Initialize Spec Pack
-`spec-product-clarify`: Clarify and generate solutions
-`spec-product-prd`: Generate PRD (optional)
-`spec-product-prototype`: Generate prototype (optional)
-`spec-product-demo`: Generate interactive demo (optional)

---

## 7. You can start like this

1. First determine whether the requirement belongs to "simple closed loop" or "standard closed loop".  
2. use`using-aisdlc`Enter the corresponding path.  
3. Do a minimum review after each step is completed, and do not leave key differences until later.  
4. When ambiguity occurs, the documents of the previous stage will be reflowed first, and subsequent stages will not be directly jumped.  

When the team runs this way for a while, you will see three obvious changes:
Requirements converge faster, there are fewer misunderstandings across roles, and reviews and deliveries are more predictable.