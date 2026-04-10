---
markdown-sharing:
  uri: 288031e6-b2a6-46b6-8257-9db24e1a384d
---
# A brief history of the evolution of AI Coding: from conversation to engineering

> Rapid science popularization for production and research teams | 2026-03

---

## Why does the production and research team need to pay attention to this topic?

Between 2024 and 2026, AI-assisted coding undergoes several paradigm shifts. Every leap is not just about "better tools", but a fundamental change in the collaboration model between humans and AI - what input product managers need to provide, what infrastructure needs to be built for R&D, and what risks QA needs to pay attention to are all changing accordingly.

Understanding this line of evolution can help teams avoid detours when "using AI to improve efficiency" and focus their energy on areas that truly generate leverage.

---

## 1. Vibe Coding: Write code by feeling (2024)

**Core Features**: Open the AI dialog box, describe what you want in natural language, AI generates code, and you copy-paste it into the project.```
"帮我写一个用户登录页面，用 React + Tailwind"
→ AI 输出一段代码
→ 开发者粘贴、跑起来、手动调整
```This stage is like "the fast typing partner in pair programming" - it can produce code snippets quickly, but:

- **No project context**: AI does not know your project structure, technology stack conventions, and existing components
- **No quality assurance**: Whether the generated code can run, whether the style is consistent, and whether there are any security issues all depend on human inspection.
- **Non-reproducible**: For the same question, you may get completely different answers if you change the dialogue window.

**Applicable scenarios**: Prototype verification, learning new technologies, and writing one-time scripts.

**Limitations**: Once the project scale exceeds a few hundred lines, the efficiency of Vibe Coding drops sharply - AI repeatedly writes code that is inconsistent with the existing code style and duplicates existing modules, and humans have to spend more time repairing it.

---

## 2. Prompt Engineering: Learn to ask questions (2024-2025)

**Core Features**: People found that the output quality of AI is highly dependent on the input quality, so they began to systematically study "how to ask".

Key practices include:

- **Character**: Tell the AI that it is "a senior React developer"
- **Few-shot examples**: Show the AI several expected input and output samples
- **Chain-of-Thought**: Require AI to analyze first before taking action
- **Structured output**: Specify output formats such as JSON Schema and Markdown templates```
你是一名资深后端工程师。请基于以下 API 契约，生成 Go 的 handler 代码。
要求：使用 gin 框架、标准错误处理、单元测试。
契约：[粘贴 OpenAPI 片段]
```**Progress**: The output quality has improved significantly, and a "repeatable methodology" has begun.

**Limitations**: The amount of information that Prompt can carry is limited. For real projects, "how to ask" is far less important than "what the AI ​​can see."

---

## 3. Context Engineering: Let AI see the correct information (2025)

**Core features**: People realize that **model capabilities are not the bottleneck, but the context fed to the model is**. Shift from "how to ask" to "what to let AI see."

Significant practices at this stage:

- **AGENTS.md/Rules**: Place the project-level instruction file in the warehouse to let AI automatically load project conventions
- **RAG (Retrieval Enhanced Generation)**: Dynamically retrieve relevant code and documents to feed the model based on the current task
- **Knowledge base construction**: Structured organization of architecture documents, API contracts, and business rules for AI consumption on demand
- **Long context window**: The model context changes from 4K→128K→1M tokens, allowing you to "see" more content```
[自动注入] 项目技术栈：Go + gin + PostgreSQL
[自动注入] 编码规范：error wrapping、structured logging
[自动注入] 相关模块代码：user/service.go, user/repository.go
[用户指令] 在 user 模块新增"修改密码"功能
```**Progress**: AI is starting to write code that "looks like code already in the project" rather than generic examples.

**Limitations**: Even if the AI ​​sees the right information, it may still make wrong decisions - because there is no one to constrain the boundaries of its behavior, and there is no mechanism to verify its output.

---

## 4. Spec-Driven Development: Specification Driven (2025)

**Core Features**: What is given to AI is no longer "one sentence requirements", but **structured specification documents** - PRD, design documents, API contracts, acceptance standards, forming a complete input chain.

Core philosophy:

- **Spec as Code**: Requirements documents are included in version control, reviewed, and traceable like code.
- **Double-tier SSOT**: project-level knowledge (architecture, contract) + requirement-level Spec Pack (closed-loop product from PRD to release)
- **Phase-based promotion**: Requirements clarification → Solution design → Implementation plan → Coding execution → Test verification, each stage has clear input/output/access control
- **AI participates in the whole process**: not only writing code, but also participating in demand analysis, solution design, and test case generation```
[R1 需求澄清] raw.md → solution.md
[R2 PRD 编写] solution.md → prd.md（含 AC）
[D1 技术调研] prd.md + 项目知识库 → research.md
[D2 方案设计] research.md → design.md（含 Impact Analysis）
[I1 实施计划] design.md → plan.md（任务清单）
[I2 编码执行] plan.md → 代码实现 + 测试
```**Progress**: AI changes from "code snippet generator" to "SDLC full process participant". The output can be traced, reviewed and accepted.

**Limitations**: All process constraints and access control are implemented by "telling AI what to do" - essentially suggestions, not enforcement. Models may skip steps, guess paths, and combine multiple stages at once.

---

## 5. Harness Engineering: Harness Engineering (2026)

**Core Proposition**: **The model is not the bottleneck, the system surrounding the model is. **

Harness (driving framework) refers to the entire control system wrapped around the AI Agent - not to change the model, but to change the environment in which the model runs.

> LangChain only changed the Harness (without changing the model) and the Terminal Bench ranking jumped from Top 30 to Top 5.

### Four pillars

| Pillars | Core Issues | Typical Means |
|------|---------|---------|
| **Inform** | What can the Agent see? | Warehouse i.e. SSOT, dynamic context mapping, progressive disclosure |
| **Constrain** | What can Agent do? | Architectural boundaries, tool whitelist, Router/Worker separation |
| **Verify** | Did the Agent do it right? | Self-verification loop, CI gate, Pre-completion Checklist |
| **Correct** | What should I do if the Agent makes a mistake? | Loop Detection, self-healing, experience return |

The key difference is that the constraints in all previous stages are "telling the AI what to do" (Prompt level), while Harness Engineering requires "enforcement at the code and system levels" (mechanical enforcement).```
# 之前：Prompt 级约束
"你必须先执行 spec-context，获取 FEATURE_DIR 后才能读写文件"
→ AI 可能在压力下跳过

# 现在：Harness 级约束
spec-context 脚本自动执行 → 返回 FEATURE_DIR → 校验脚本验证产物结构
→ 不通过则流程物理阻断，AI 无法继续
```### Relationship with previous stages

Harness Engineering is not a negation of the previous stages, but a culmination of:

| Stages of evolution | Position in Harness |
|---------|-------------------|
| Prompt Engineering | Part of the Inform pillar (how instructions are organized) |
| Context Engineering | The core of the Inform pillar (how to organize context) |
| Spec-Driven Development | Inform + Constrain Pillar (Structured Input + Stage Gate Control) |
| **Harness Engineering** | **Complete closed loop of four pillars (Inform + Constrain + Verify + Correct)** |

---

## 6. See the evolution in one picture```
可靠性 ↑
  │
  │                                          ┌─────────────────┐
  │                                          │   Harness Eng.  │
  │                                          │  机械强制+自验证  │
  │                                    ┌─────┤  +反馈回路+纠偏  │
  │                                    │ SDD │                 │
  │                              ┌─────┤Spec │                 │
  │                              │Ctx  │驱动  │                 │
  │                        ┌─────┤Eng. │开发  │                 │
  │                        │Prompt│上下文│     │                 │
  │                  ┌─────┤Eng. │工程  │     │                 │
  │                  │Vibe │提示词│     │     │                 │
  │                  │Coding│工程  │     │     │                 │
  └──────────────────┴─────┴─────┴─────┴─────┴─────────────────→ 时间
                    2024   2024   2025   2025        2026
                           -2025
```Each layer wraps and enhances the previous layer, rather than replacing it.

---

## 7. Practical inspiration for the production and research team

### Product Manager/Business Analyst

| Evolution Stage | What You Need to Do |
|---------|----------------|
| Vibe Coding | Speak the requirements verbally and wait for development to deliver |
| SDD stage | Write clear acceptance criteria (AC), business rules, and impact analysis |
| Harness stage | Participate in knowledge base construction - the PRD/AC you write is the input of the Agent, and the quality directly determines the quality of the AI output |

### R&D Engineer

| Evolution Stage | What You Need to Do |
|---------|----------------|
| Vibe Coding | Ask AI → Paste code → Manual adjustment |
| Context Eng. | Maintain AGENTS.md and code specification files to let AI understand the project |
| Harness stage | Build constraint infrastructure (verification scripts, CI access control, product structure inspection) to allow AI to work within the "safety fence" |

### QA/Testing

| Evolution Stage | What You Need to Do |
|---------|----------------|
| Vibe Coding | Test the code generated by AI (no different from that written by humans) |
| SDD stage | Generate test cases based on Spec to ensure AC traceability |
| Harness stage | Participate in the construction of Verify pillars - define the standards for "AI is done right" and design self-verification rules |

---

## 8. Common misunderstandings

**Myth 1: "We can just go to Harness Engineering"**

Each stage is the basis for the next stage. If the team does not even have structured Spec input (SDD stage), doing Harness directly will only get "carefully constrained garbage input → carefully verified garbage output".

**Myth 2: "This is a matter of R&D and has nothing to do with the product"**

The AI Agent's output quality limit depends on the input quality. The PRD is vaguely written, the AC is missing, and the business rules are passed on verbally - no amount of Harness can save it.

**Myth 3: "With AI, there is no need for Review"**

Quite the opposite. AI can produce a lot of code quickly, but "wrong code produced quickly" is more harmful than "wrong code written slowly". Harness Engineering’s Verify pillar exists for exactly that reason: **Trust but verify**.

**Myth 4: "Harness is fixed"**

A good Harness should be "Rippable" - as the model's capabilities improve, certain abilities that previously required Harness constraints can be gradually removed. Over-constraints introduce unnecessary complexity and cost.

---

## Summary

The evolution of AI Coding is essentially a path from "human adaptation to AI" to "system control of AI":

1. **Vibe Coding**: People adapt to AI output
2. **Prompt Engineering**: People learn how to better ask AI questions
3. **Context Engineering**: Human AI organizes better input information
4. **Spec-Driven Development**: Establishing a structured workflow for artificial intelligence
5. **Harness Engineering**: Establishing a mechanically forced control system using artificial intelligence

Every step is reducing reliance on "AI self-discipline" and increasing the proportion of "system guarantee". **The more mature the team, the less it relies on the intelligence of the model itself, and the more it relies on the engineering system surrounding the model. **

This is why we are promoting the AI SDLC project knowledge base - it is not just a "bundle of documents", but Harness Engineering's implementation practice in the SDLC field: using structured knowledge to inform the Agent, using stage access control to constrain the Agent, using product verification to verify the Agent, and using feedback loops to correct the Agent.

---

*Basic Services Department 2026-03*