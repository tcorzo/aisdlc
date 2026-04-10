---
title: Spec initialization command design and implementation (create spec working branch and directory)
status: draft
audience: [PM, BA, DEV]
principles_ref: design/aisdlc.md
---
## 0. Background and target (aligned`design/aisdlc.md`)

This solution is used to implement the **Spec initialization command**: automatically create the spec working branch and directory structure, ensuring that the "dual-layer SSOT + Spec as Code" principle in the AI SDLC specification is followed.

### 0.1 Core Objectives

Through automated processes, quickly create standardized requirements working branches and directory structures to ensure:

- **Naming Consistency**: Unified numbering and naming rules
- **Structural Integrity**: Standard directory structure, compliant with AI SDLC specifications
- **Traceability**: original requirements remain in`requirements/raw.md`in
- **Automatic context identification**: Automatically identify the requirement directory through the branch name, no additional parameters are required

### 0.2 Unify output location

All output is unified to:`.aisdlc/specs/{num}-{short-name}/`(Requirement level Spec Pack root directory)

> Constraint: Spec Pack and requirements/design/implementation documents are always in the root project; even if the repository contains`git submodule`, the submodule is only used as a code workspace for the subsequent implementation phase and does not host Spec documents.

---

## 1. Why use branch form?

### 1.1 Branching as a context identification mechanism

**Core design concept**: Use Git branches as **context identifier** for Spec-level requirements to achieve "zero parameter" context acquisition.

#### 1.1.1 Problem background

In the AI SDLC process, each requirement has an independent Spec Pack, which contains documents for multiple stages (requirements, design, implementation, etc.). When executing spec-level auxiliary commands (such as requirements analysis, solution design, code implementation, etc.), you need to know clearly:

- **Which requirement is currently being processed? **
- **Where is the Spec Pack directory for this requirement? **
- **How to automatically load the contextual information of this requirement? **

#### 1.1.2 Advantages of branch design

**1. Automatic context recognition**

- Git branch name`{num}-{short-name}`Maps directly to the Spec directory`.aisdlc/specs/{num}-{short-name}/`- pass`git branch --show-current`You can get the current branch name
- No need for users to manually specify requirement IDs or directory paths

**2. Workspace Isolation**

- Work on each requirement in an independent branch to avoid documents and codes with different requirements from interfering with each other
- Comply with Git Flow best practices for easy code review and merge management
- Supports parallel development of multiple requirements without conflicting with each other
- If the subsequent implementation involves submodules, the sub-repository should in principle use the Spec branch with the same name as the root project, but these sub-repository branches are not`spec-init`Stage batch creation

**3. Version control and traceability**

- The commit history of the branch completely records the evolution of requirements
- Document changes at each stage have independent submission records
- Facilitates rollback and troubleshooting

**4. Progressive disclosure support**

- When the Agent detects that it is currently in a certain spec branch, it automatically loads the Spec Pack for that requirement.
- No need to specify the requirements context repeatedly in every conversation
- conform to`design/aisdlc.md`"Progressive Disclosure" Principle in

#### 1.1.3 Context acquisition process```
用户执行 spec 级辅助命令
    ↓
检测当前 Git 分支名称（如：001-user-auth）
    ↓
解析分支名称，提取编号和短名称
    ↓
自动定位 Spec 目录：.aisdlc/specs/001-user-auth/
    ↓
加载该需求的上下文信息（requirements/*、design/* 等）
    ↓
执行命令，无需用户额外提供需求信息
```### 1.2 Branch naming convention

**Format**:`{num}-{short-name}`

- **`{num}`**: three-digit number (such as`001`、`002`), used to uniquely identify and sort
- **`{short-name}`**: A short name of 2-4 words (kebab-case), describing the required core functions

**Example**:
-`001-user-auth`: User authentication requirements
-`002-payment-integration`: Payment integration requirements
-`003-analytics-dashboard`: Analyze dashboard requirements

---

## 2. Function Overview

This command is used to automate the creation of the spec working branch and directory structure:

- Analyze the original requirements, extract keywords and generate a short name of 2-4 words (kebab-case)
- From remote branches, local branches and`.aisdlc/specs`Find the highest number in a directory
- Create new branch`{num}-{short-name}`- Create a complete spec directory structure
- Write original requirements`requirements/raw.md`, and delete the original file (if any)

---

## 3. Execution process

### 3.1 Step 0: Preflight

Before executing the main process, perform the following pre-checks:

- Confirm that you are currently in the Git repository root directory
- Check`.aisdlc/specs`Whether the directory exists (create it if it does not exist)
- Verify that the Git repository status is normal

**Purpose**: Ensure that the environment is ready to avoid failure of subsequent operations.

### 3.2 Step 1: Parse the input

**Input source**:
- **File Path**: If the input contains a file path and the file exists, read the file content as the original requirement
- **Original requirement text**: If the input is not a file path, it will be processed directly as the original requirement text.
- **Empty Input**: If the input is empty, prompt the user to enter the original requirement

**Output**: Original requirement text content

### 3.3 Step 1.5: Determine the requirements file path

In order to avoid encoding problems in Chinese content when passing parameters, the file path is uniformly used to pass the required content:

- **If the original requirement comes from a file**: use the original file path directly
- **If the original requirement is text input**: Create a temporary file to save the requirement content (UTF-8 with BOM encoding), use the temporary file path

**Output**:
- Requirement file path (original file path or temporary file path)
- Whether it is a mark of temporary files (for subsequent cleanup)

### 3.4 Step 2: Generate short name

Use AI to analyze the original requirement content and generate a short name:

**Generation Rules**:
- Analyze function descriptions and extract the most meaningful keywords
- Create short names of 2-4 words
- Prefer the "verb-noun" format (e.g.`add-user-auth`、`fix-payment-bug`)
- Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
- Convert to kebab-case (lowercase, hyphen between words)

**Generate Example**:
- "I want to add user authentication" →`user-auth`
- "Implement OAuth2 integration for the API" → `oauth2-api-integration`
- "Create a dashboard for analytics" → `analytics-dashboard`
- "Fix payment processing timeout bug" → `fix-payment-timeout`**Output**: short name (kebab-case format, 2-4 words)

### 3.5 Step 3: Call the PowerShell script to execute the complete process

Call a PowerShell script`skills/spec-init/scripts/spec-create-branch.ps1`of`Main`function, passing the following parameters:

- **`ShortName`** (required): short name generated in step 2
- **`SourceFilePath`**(Required): Requirements file path determined in step 1.5
- **`Title`**(optional): Title of the requirement

The script performs the following operations in sequence:

#### 3.5.1 Find the maximum number

Find the maximum number from three sources:
- **remote branch**: execute`git fetch --all --prune`Get all remote branches that match`{num}-{short-name}`Format
- **Local branch**: Matches in the local branch`{num}-{short-name}`Format
- **`.aisdlc/specs`Directory**: matches in the directory`{num}-{short-name}`Format

Find the maximum number N, using N+1 as the new number (formatted as three digits, e.g.`001`、`002`).

**Number search rules**:
- Branch format:`{num}-{short-name}`,in`{num}`is 1-3 digits
- Directory format:`.aisdlc/specs/{num}-{short-name}/`- Use regular expressions to match and extract numbers

#### 3.5.2 Create branch

- Execute`git checkout -b {num}-{short-name}`Create and switch branches
- Verify that the branch is created successfully
- If the branch already exists, throw an error and stop execution

#### 3.5.3 Create directory structure

- Create`.aisdlc/specs/{num}-{short-name}/`Home directory
- Create the following subdirectories:
  -`requirements/`
  - `design/`
  - `implementation/`
  - `verification/`
  - `release/`- If the directory already exists, throw an error and stop execution

#### 3.5.4 Write original requirements

- Read original requirement content from file (UTF-8 with BOM encoding)
- write content`requirements/raw.md`(UTF-8 with BOM encoding)

#### 3.5.5 Delete original files

- Delete source files (original or temporary files)

**Script return value**: A hash table containing the following information
-`number`: Number in three-digit format
-`shortName`:short name
-`branchName`:Full branch name
-`specDir`:Spec directory path
-`title`:title (if provided)

---

## 4. Automatic context recognition mechanism

### 4.1 Branch to directory mapping

**Mapping Rules**: Branch Name`{num}-{short-name}`→ directory path`.aisdlc/specs/{num}-{short-name}/`**Example**:
- branch`001-user-auth`→ Table of Contents`.aisdlc/specs/001-user-auth/`- branch`002-payment-integration`→ Table of Contents`.aisdlc/specs/002-payment-integration/`### 4.2 Context acquisition of subsequent commands

When executing spec-level auxiliary commands (such as requirements analysis, solution design, etc.), the context is automatically obtained in the following ways:

1. **Get the current branch name**:`git branch --show-current`2. **Resolve branch names**: Extract numbers and short names
3. **Locate the Spec directory**:`.aisdlc/specs/{num}-{short-name}/`4. **Load context information**:
   - read`requirements/raw.md`(original requirement)
   - read`requirements/prd.md`(if present)
   - read`design/design.md`(if present)
   - Read other related documents

**Advantages**:
- Users do not need to manually specify requirement IDs or directory paths
- Reduce typing errors and contextual confusion
- Improve the efficiency and accuracy of command execution

### 4.3 Usage scenarios of contextual information

**Scenario 1: Requirements Analysis Command**
- automatic reading`requirements/raw.md`- Analyze based on original requirements and generate PRD, use cases and other documents
- No need for users to provide required content again

**Scenario 2: Scheme design command**
- automatic reading`requirements/prd.md`and related requirements documents
- Design and generate solutions based on needs`design/design.md`- Automatically associate requirement context

**Scenario 3: Code to implement commands**
- automatic reading`design/design.md`and requirements documentation
- Code implementation based on design plan
- Ensure implementation is consistent with requirements and design

### 4.4 Standardized process for obtaining context information

In order to ensure that all spec-level commands can correctly obtain context information, a standardized context information acquisition process needs to be established.

#### 4.4.1 Standardization requirements

**Core Principle**: Before all subsequent spec-level commands are executed, context information related to the current spec must be obtained through a script.

**Purpose**:
- Ensure that the command can accurately locate the currently required workspace
- Avoid hardcoding paths and branch names
- Unify the method of obtaining context information to improve maintainability
- Support correct execution in different environments (different developers, different machines)

#### 4.4.2 Required basic information

All spec-level commands require the following basic information:

**1. REPO_ROOT**
- **Meaning**: The root directory path of the Git repository
- **Purpose**: Used as a baseline for all relative paths to ensure that file operations are within the correct warehouse scope
- **Getting method**: Automatically detect the Git root directory of the current working directory through Git commands or scripts

**2.CURRENT_BRANCH**
- **Meaning**: Current Git branch name (format:`{num}-{short-name}`)
- **Use**:
  - as an identifier of the requirement context
  - Used to locate the corresponding Spec directory
  - Verify you are on the correct spec branch
- **Acquisition method**: Pass`git branch --show-current`Get

**3.FEATURE_DIR**
- **Meaning**: The current required Spec Pack root directory path (format:`.aisdlc/specs/{num}-{short-name}/`)
- **Use**:
  - serves as the root directory for all spec documents
  - Used to read and write documents in requirements, design, implementation and other stages
  - Ensure that file operations are performed in the correct required directory
- **Acquisition method**: Based on`CURRENT_BRANCH`Automatic build path:`{REPO_ROOT}/.aisdlc/specs/{CURRENT_BRANCH}/`**Additional note: submodule does not change the parsing rules of FEATURE_DIR**

-`.gitmodules`It is only used in the subsequent implementation phase to identify "which sub-repositories can participate in code modification"
- Even if the command is triggered from the submodule directory, it should trace back to the root project and resolve the same`FEATURE_DIR`- Do not allow separate mapping of new Spec directories based on submodule branches

#### 4.4.3 Context information acquisition process

**Standard execution process**:```
执行 spec 级命令
    ↓
调用上下文信息获取脚本/函数
    ↓
获取 REPO_ROOT（Git 仓库根目录）
    ↓
获取 CURRENT_BRANCH（当前分支名称）
    ↓
验证分支名称格式（{num}-{short-name}）
    ↓
构建 FEATURE_DIR（.aisdlc/specs/{CURRENT_BRANCH}/）
    ↓
验证 FEATURE_DIR 是否存在
    ↓
返回上下文信息（REPO_ROOT、CURRENT_BRANCH、FEATURE_DIR）
    ↓
使用上下文信息执行命令逻辑
```#### 4.4.4 Verification and error handling

**Validation Rules**:

1. **REPO_ROOT verification**
   - must exist`.git`Directory
   - must exist`.aisdlc/specs`directory (may need to be initialized if it does not exist)

2. **CURRENT_BRANCH Verification**
   - Branch names must conform to the format:`{num}-{short-name}`- The number part must be 1-3 digits
   - The short name part must be kebab-case (lowercase letters, numbers, hyphens)

3. **FEATURE_DIR Verification**
   - Directory must exist
   - The directory structure must be complete (including`requirements/`、`design/`subdirectories)

**Error handling**:

- If not currently in the Git repository: prompt the user to switch to the correct repository directory
- If the current branch does not comply with the specification: prompt the user to switch to the correct spec branch
- If FEATURE_DIR does not exist: prompt the user to execute first`spec-init`Command to create spec branch and directory

#### 4.4.5 Implementation method

**Script/Function Design**:

- Create a general context information acquisition function (such as`Get-SpecContext`)
- This function can be called by all spec-level commands
- Returns a standardized context information object (containing`REPO_ROOT`、`CURRENT_BRANCH`、`FEATURE_DIR`fields)
- If the warehouse exists`.gitmodules`, can additionally return a submodule status snapshot for the implementation phase to verify branch consistency and workspace status.

**Calling Convention**:

- All spec-level commands must first call the context information acquisition function before executing the main logic.
- If acquisition fails, the command should terminate immediately with an error
- After successful acquisition, use the returned context information for subsequent operations

#### 4.4.6 Advantages

By standardizing the context information acquisition process, we achieve:

- **Consistency**: All commands use the same way to obtain context, reducing duplicate code
- **Reliability**: A unified verification mechanism ensures that the context information is correct
- **Maintainability**: Context acquisition logic is centrally managed for easy modification and optimization
- **Extensibility**: New contextual information fields can be easily added in the future (e.g.`SPEC_NUMBER`、`SHORT_NAME`etc.)

---

## 5. Completion standards (DoD: for self-test)

- [ ] Short name has been generated, conforming to naming convention (2-4 words, kebab-case, priority verb-noun format)
- [ ] The required file path has been determined (original file path or temporary file path, UTF-8 with BOM encoding)
- [ ] The PowerShell script was called successfully, passing the correct parameters
- [ ] The source file has been automatically deleted after the script execution is completed.
- [ ] The script returns a resulting hash table containing`number`、`shortName`、`branchName`、`specDir`、`title`Field
- [ ] numbers have been correctly looked up (from three sources: remote branch, local branch, specs directory) and formatted as three digits
- [ ] Git branch`{num}-{short-name}`Created and switched successfully
- [ ] directory structure`.aisdlc/specs/{num}-{short-name}/`Created with all required subdirectories
- [ ]`requirements/raw.md`Created, contains original requirement content, encoded using UTF-8 with BOM
- [ ] The branch name and directory path are mapped correctly, and the Spec directory can be automatically located through the branch name.

---

## 6. Error handling

### 6.1 Short name conflict

If the short name already exists and the number conflicts, the user is prompted to confirm or modify the short name.

### 6.2 Git operation failed

If the Git operation fails (for example, the branch already exists), an error is displayed and execution stops.

### 6.2.1 Submodule branch creation timing

-`spec-init`Only responsible for the initialization of the Spec branch and Spec Pack directory of the root project
- If subsequent requirements will modify the submodule, the implementation plan should be`I1 -> I2`between based on`impact-analysis`Clearly identify the affected sub-warehouses
- Before entering I2, again`required`The sub-repository creates and verifies the Spec branch with the same name as the root project

### 6.3 Directory already exists

If the directory already exists, prompt the user to confirm overwriting or use a different number.

### 6.4 File reading failed

If the specified file path does not exist or cannot be read, an error will be prompted.

---

## 7. Subsequent commands (what to do next)

After the spec branch and directory are created, you can:

- Start writing requirements document: Edit`.aisdlc/specs/{num}-{short-name}/requirements/prd.md`- Conduct needs analysis: Edit`.aisdlc/specs/{num}-{short-name}/requirements/usecase.md`- Start schematic design: Edit`.aisdlc/specs/{num}-{short-name}/design/design.md`**Important**: All subsequent spec-level auxiliary commands can automatically identify the requirement context through the current branch name, without providing additional requirement information.

> Shortest path (minor requirement): Complete this command (create branches and directories) →`spec-design-solution`(Small requirements go directly to D2, based on`requirements/raw.md`) → execute

---

## 8. Operational constraints

- **Non-destructive**: Will not overwrite existing branches or directories (unless explicitly confirmed by the user)
- **Number auto-increment**: Automatically find the maximum number and increment it
- **Short name generation**: Use AI to analyze demand content and generate short names that comply with specifications
- **Unified encoding**: All file operations use UTF-8 with BOM encoding to ensure that Chinese content is processed correctly
- **Branch and directory consistency**: The branch name and directory path must be consistent to ensure that the automatic context recognition mechanism works properly.
- **The sub-warehouse does not carry Spec documents**:`.gitmodules`Submodule only participates in the implementation phase and cannot replace the root project.`.aisdlc/specs/...`---

## 9. Summary of design points

### 9.1 Branch as context identifier

- **Core Value**: Automatically identify the requirement context through branch names and achieve "zero parameter" context acquisition
- **Mapping**: branch name`{num}-{short-name}`→Spec Catalog`.aisdlc/specs/{num}-{short-name}/`- **Usage scenario**: All spec-level auxiliary commands can automatically obtain the requirement context through the current branch

### 9.2 Workspace isolation

- Work on each requirement in an independent branch to avoid mutual interference
- Supports parallel development of multiple requirements
- Comply with Git Flow best practices

### 9.3 Version Control and Traceability

- The commit history of the branch completely records the evolution of requirements
- Document changes at each stage have independent submission records
- Facilitates rollback and troubleshooting

### 9.4 Progressive Disclosure Support

- When the Agent detects that it is currently in a certain spec branch, it automatically loads the Spec Pack for that requirement.
- No need to specify the requirements context repeatedly in every conversation
- Comply with the "Progressive Disclosure" principle in the AI SDLC specification

### 9.5 Responsibility boundaries with Submodule

- The root project branch is Spec identity with`FEATURE_DIR`the only anchor point
-`.gitmodules`Provide only static facts for submodule (path/remote)
- In principle, the sub-repository uses the Spec branch with the same name as the root project, but the creation and verification occur during the implementation phase, not`spec-init`stage batch processing