# 前端产品从 0 到 1：官方资料与 AI 实践证据

> 调研范围：只读调研；未修改任何仓库。页面状态按本次实际 `web_get_contents` / `curl -L` 检查记录。英文摘录保留页面原文，不把推断写成原文事实。
>
> 核验时间：2026-09-06（环境时间）。部分站点会随时间更新；GitHub stars / pushed_at 为本次 `gh api repos/...` 返回值。

## D. 优先：用 AI 从 0 到 1 实现前端

### D1. 大厂官方资料

#### Vercel v0

- URL（已核验）：<https://v0.dev/docs>
- 原文摘录：
  > “Ship features, refine designs, update copy, and create live prototypes, all with a prompt. Deploy to production immediately, or open a pull request for review.”
  >
  > “Create high-fidelity UIs from your wireframes or mockups.”
- 对 0→1 的直接证据：v0 文档明确把 wireframe/mockup、原型、代码、部署/PR 放在同一条工作流里。

- URL（已核验）：<https://vercel.com/blog/working-with-figma-and-custom-design-systems-in-v0>
- 原文摘录：
  > “When working with existing Figma components in v0, an iterative approach is highly recommended.”
  >
  > “Start by focusing on individual components / Test and refine each one before moving on to the next / Fine-tune the smaller pieces and ensure they work well within v0’s generation process / Gradually build up to complete landing pages by piecing together the components, rather than attempting a lengthy single-piece generation all at once.”

- URL（已核验）：<https://vercel.com/blog/bridging-the-gap-between-design-and-code-with-v0>
- 原文摘录：
  > “They use v0 as a dynamic design descriptor, a way to share interactive prototypes and demonstrate feature behavior.”
  >
  > “This allows, designers and engineers collaborate in real time, refining ideas without the friction of design-to-code translation.”

#### Anthropic / Claude Code

- URL（已核验）：<https://www.anthropic.com/engineering/claude-code-best-practices>
- 原文摘录：
  > “Claude explores, plans, and implements.”
  >
  > “Give Claude a check it can run: tests, a build, a screenshot to compare.”
  >
  > “Claude does the work, runs the check, reads the result, and iterates until the check passes.”
- 关键流程摘录：
  > “Explore first, then plan, then code”
  > “Separate research and planning from implementation to avoid solving the wrong problem.”

- URL（已核验）：<https://www.anthropic.com/research/building-effective-agents>
- 原文摘录：
  > “Consistently, the most successful implementations use simple, composable patterns rather than complex frameworks.”
  >
  > “When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed.”
- 相关 0→1 启示（不冒充原文）：先用直接、可解释的工作流，只有需求确实需要时才增加 agent 复杂度。

#### GitHub Copilot / Spec-Driven Development

- URL（已核验）：<https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent>
- 原文摘录：
  > “Copilot coding agent works independently in the background to complete tasks and create pull requests.”
- 备注：本页说明 coding agent 的任务→后台实现→PR 交付方式；具体产品需求拆解仍应由项目规范约束。

- URL（已核验）：<https://github.com/github/spec-kit>
- 原文摘录（仓库描述/README）：
  > “💫 Toolkit to help you get started with Spec-Driven Development”
- gh api 实查：stars **133,669**；pushed_at **2026-09-04T11:51:20Z**；license **MIT**。
- 组织方式：仓库把 specification-first 的工具、模板和工作流作为可复用资产，而不是只提供一次性 prompt。

- URL（已核验）：<https://docs.github.com/en/copilot/tutorials/speed-up-development-work>
- 原文摘录：
  > “Create a space when you start working on a specific feature. Add the relevant code, a product specification, and any supporting materials.”
  >
  > “Copilot can help you: Summarize how the current implementation works. Suggest changes or additions based on the specification. Draft a first implementation or outline next steps. Flag missing elements or inconsistencies.”

#### Google Stitch / Firebase Studio

- URL（已核验）：<https://stitch.withgoogle.com/>
- 备注：页面可打开，但本次抓取没有得到稳定的可引用正文段落；按要求列为「未核验摘录」，不把搜索摘要当作页面原文。

- URL（已核验）：<https://firebase.google.com/docs/studio>
- 备注：页面可打开，但本次抓取未提取到可稳定复核的工作流关键句；列为「未核验摘录」。

#### Figma Make / Figma MCP

- URL（已核验）：<https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server>
- 原文摘录：
  > “The Figma MCP server helps developers explore and implement designs quickly and accurately.”
  >
  > “Get design context and code from your Figma designs, FigJam, and Make files.”
  >
  > “Gather code resources from Make files and provide them to the LLM as context. This can help as you move from prototype to production application.”

- URL（已核验）：<https://help.figma.com/hc/en-us/articles/35280968300439-Figma-MCP-collection-What-is-the-Figma-MCP-server>
- 原文摘录：
  > “Select a Figma frame and turn it into code with an agentic development tool.”
  >
  > “Gather code resources from Figma Make files and provide them to your agentic tools as context. This can help as you move from a prototype to a production-ready application.”

#### OpenAI Codex

- URL（已核验）：<https://developers.openai.com/codex/quickstart>
- 原文摘录：
  > “3. Select a project — Choose a project folder that you want Codex to work in.”
  >
  > “4. Send your first message — After choosing the project, make sure Local is selected to have Codex work on your machine and send your first message to Codex.”
  >
  > “Use Git checkpoints — Codex can modify your codebase, so consider creating Git checkpoints before and after each task so you can easily revert changes if needed.”

#### Cursor

- URL（已核验）：<https://cursor.com/docs/context/rules>
- 原文摘录：本次页面可打开，但抓取正文不稳定，未保留未经复核的句子；**未核验摘录**。
- URL（已核验）：<https://cursor.com/docs/agent/overview>
- 原文摘录：本次页面可打开，但抓取正文不稳定，未保留未经复核的句子；**未核验摘录**。

#### Lovable / bolt.new

- URL（已核验）：<https://docs.lovable.dev/>
- 备注：页面可打开；本次正文未提取到稳定的 0→1 流程句；**未核验摘录**。

- URL（已核验）：<https://support.bolt.new/>
- 备注：页面可打开；本次正文未提取到稳定的 0→1 流程句；**未核验摘录**。

#### 国内工具

- Qoder：<https://www.qoder.com/docs> —— `curl` 返回 200；本次未获得稳定正文摘录，**未核验摘录**。
- Trae：<https://www.trae.ai/docs> —— `curl` 返回 200；本次未获得稳定正文摘录，**未核验摘录**。
- 腾讯 CodeBuddy：<https://codebuddy.tencent.com/docs> —— 本次未获得稳定正文摘录，**未核验**。
- MasterGo AI：<https://mastergo.com/ai> —— 本次未获得稳定正文摘录，**未核验**。
- 即时设计 AI：<https://js.design/ai> —— 本次未获得稳定正文摘录，**未核验**。

### D2. GitHub 高星仓库：gh api 实查

> 以下数值均来自本次 `gh api repos/<owner>/<repo> --jq '{stargazers_count,pushed_at,...}'`，不是网页展示值。

| 项目 | 仓库 URL | stars | pushed_at | license | 如何组织 0→1 / 设计系统工作 |
|---|---|---:|---|---|---|
| GitHub Spec Kit | <https://github.com/github/spec-kit> | 133,669 | 2026-09-04T11:51:20Z | MIT | specification-first 工具包；先把需求/规格变成可执行的开发上下文。 |
| BMAD-METHOD | <https://github.com/bmad-code-org/BMAD-METHOD> | 52,721 | 2026-09-06T10:22:20Z | NOASSERTION | Breakthrough Method for Agile AI Driven Development；用角色、工作流和阶段化产物组织 AI 开发。 |
| Anthropic Skills | <https://github.com/anthropics/skills> | 174,792 | 2026-09-03T16:37:14Z | 未声明 | Agent Skills 仓库；前端设计 skill 位于 <https://github.com/anthropics/skills/tree/main/skills/frontend-design>。 |
| bolt.new | <https://github.com/stackblitz/bolt.new> | 16,537 | 2024-12-17T06:29:27Z | MIT | Prompt、运行、编辑、部署全栈 web app；仓库描述明确把生成和部署放在一个工具中。 |
| 21st Magic MCP | <https://github.com/21st-dev/magic-mcp> | 5,805 | 2026-09-01T23:08:51Z | ISC | 为 Cursor/Claude Code/Windsurf 提供 React/Tailwind 组件搜索、生成和发布。 |
| Figma-Context-MCP | <https://github.com/GLips/Figma-Context-MCP> | 15,784 | 2026-09-05T21:22:46Z | MIT | 把 Figma layout information 提供给 Cursor 等 AI coding agents，作为设计上下文。 |
| awesome-cursorrules | <https://github.com/PatrickJS/awesome-cursorrules> | 40,731 | 2026-05-30T18:01:29Z | CC0-1.0 | 以规则文件集合沉淀项目约束，供 Cursor 复用。 |
| awesome-vibe-coding | <https://github.com/filipecalegario/awesome-vibe-coding> | 5,224 | 2026-04-16T01:34:11Z | CC0-1.0 | curated list，聚合 AI coding / vibe coding 参考资料。 |
| shadcn/ui | <https://github.com/shadcn-ui/ui> | 123,183 | 2026-09-06T12:54:15Z | MIT | 以可复制源码、registry 和组件分发平台组织设计系统，而非黑盒运行时组件包。 |

- `awesome-claude-code`、`awesome-ai-coding`、`kirodotdev`：按用户给出的仓库名直接 `gh api` 返回 404，未猜测替代 slug，列入未核验。
- Anthropic frontend-design skill 的官方 GitHub 路径已用 `curl` 返回 200；但仓库页面正文在本次抓取中未稳定返回完整 README，未添加未经复核的流程句。

### D3. 论坛 / 社区实践帖（经验材料，不等同官方规范）

#### Hacker News

1. URL（已核验）：<https://news.ycombinator.com/item?id=47245373>
   - 原文摘录：
     > “The workflow has to be sequential: design the frontend first as pure HTML until happy with it, extract requirements from the pages, then task the backend.”
     >
     > “1. Frontend first. I direct the frontend agent to build a page as pure HTML + CSS + JS. No API calls, just demo data. I iterate until I like how it looks.”
   - 要点：作者把 UI 先做成可观察的 demo，再从 UI 提取后端接口需求，最后联调。

2. URL（已核验）：<https://news.ycombinator.com/item?id=44351335>
   - 原文摘录：
     > “In this mode the flow is then about validating the code to make sure it is my ‘image’ frequently.”
     >
     > “Frequent checkpointing and sprinkling .md files with latest understanding is very important.”
   - 要点：频繁用视觉/预期校验，配合 Git checkpoint 和持久化 markdown 上下文。

3. URL（已核验）：<https://news.ycombinator.com/item?id=46939622>
   - 原文摘录：
     > “The core flow is: PRD review with clarifying questions (optional PRD generation) / Development plan …”
   - 要点：把 PRD 澄清、开发计划和 agent 协作作为持久流程；页面正文截断处未继续引用未显示的句子。

#### V2EX / 掘金 / 知乎

4. URL（已核验）：<https://www.v2ex.com/t/1222628>
   - 原文摘录：
     > “1. 与 claude 讨论项目内容和逻辑，生成项目项目文档 prd.md”
     >
     > “2. 让 cc 根据 prd.md 生成开发计划文档 plan.md 和前端设计方案 frotend.md”
     >
     > “4. 让 gpt 或 cc 把前端代码融入到项目中，完成”
   - 要点：社区实践采用 PRD → plan/frontend design → 代码 → 集成的文档链。

5. URL（已核验）：<https://www.v2ex.com/t/1222628>
   - 原文摘录：
     > “先启动一个 agent，确定需求，生成 README 和一个 TODO，主要是项目愿景、路线的、阶段里程碑、当前阶段的任务”
     >
     > “最后多用几个 agent 检查有哪些 BUG 和未完成的功能。”
   - 要点：用 README/TODO 管理阶段和里程碑，并把多 agent 检查放到实现之后。

6. URL（已核验）：<https://juejin.cn/post/7647418615483252777>
   - 原文摘录：
     > “实战：AI 简历助手从 0 到 1——需求分析 → 技术选型 → 接口设计 → 前端实现 → 部署上线。”
   - 要点：文章明确列出需求分析、技术选型、接口、前端、部署的顺序；这是作者经验，不是平台官方标准。

7. URL（已核验）：<https://juejin.cn/post/7646396172870107151>
   - 原文摘录：
     > “今天用十分钟，从零跑到一个能叫得出名字的 AI 助手。”
     >
     > “它是一个 TypeScript 的 AI 工具包，帮你做三件事：1. 对接大模型 …”
   - 要点：偏实现型教程，证据重点是从 TypeScript 项目骨架到模型接入；页面抓取在后半段截断，未扩展引用。

8. URL（已核验）：<https://zhuanlan.zhihu.com/p/2044827861551420505>
   - 原文摘录：
     > “这套工作流的核心是可视化先行，代码自动生成。具体分为 4 个步骤：想法结构化 → 原型可视化 → 假设验证 → 代码生成。”
     >
     > “AI生成的是草稿，不是终稿”
   - 要点：先结构化想法、画原型和验证假设，再把视觉上下文交给 Codex 生成代码，并进行多轮迭代。

9. Reddit：本次针对 `r/ClaudeAI`、`r/cursor`、`r/webdev` 的限定搜索未得到可稳定打开且符合主题的帖子，未猜测链接，列入未核验。

10. V2EX 原始求助帖中的多条回复明确提醒人工介入：
    - 同一 URL：<https://www.v2ex.com/t/1222628>
    - 原文摘录：
      > “一定要耐下心先手写一个模块功能，然后让 ai 去抄，否则它自由发挥的太多了。”
    - 这条是单个回复者的经验，不应上升为通用事实；它与 Anthropic 的“提供上下文、给出可执行验证”的官方建议方向一致，但两者不是同一证据。

### D4. 共同步骤（只从上面已核验材料归纳）

1. **把目标和上下文写清楚**：用 PRD、产品规格、README/TODO、目标用户和约束作为 agent 输入。依据：GitHub Copilot Spaces、V2EX PRD/README 实践、Anthropic “Provide specific context in your prompts”。
2. **先探索和规划，再实现**：先让 agent 读代码/需求、澄清问题并生成计划，避免直接生成错误方案。依据：Anthropic “Explore first, then plan, then code”；Copilot implementation-planner/Spaces；Spec Kit。
3. **先做可观察的界面或小组件**：从 wireframe/Figma/截图或独立组件开始，优先形成可评审的视觉结果。依据：v0 文档、v0 Figma workflow、Figma MCP、HN 的 frontend-first 实践。
4. **建立设计系统上下文**：给 AI 提供现有 tokens、组件、Figma variables、代码库规则和 skill，而不是只给一句“做一个页面”。依据：Figma MCP、v0 custom design systems、shadcn/ui 设计 tokens、Anthropic `CLAUDE.md` 建议、Figma-Context-MCP。
5. **小步迭代组件到页面**：先单个组件，测试/精修后再组合成完整页面。依据：v0 “Start by focusing on individual components … Gradually build up to complete landing pages”。
6. **实现后必须自动化验证**：运行 tests/build/lint，UI 变更要截图或浏览器核验，并让 agent 读取失败输出后迭代。依据：Anthropic Claude Code best practices、OpenAI Codex Git checkpoints、HN 视觉校验实践。
7. **从 UI 反推接口并联调**：在页面/交互基本明确后提取数据和 API 需求，再接后端。依据：HN frontend-first pipeline；V2EX 中“前端先模拟、分析接口、再联调”的实践。
8. **用 Git checkpoint、持久化文档和 PR 审查收敛**：任务前后建立可回退点，维护项目记忆，必要时用 PR 让人审查。依据：Codex quickstart、HN checkpoint/markdown 实践、GitHub Copilot coding agent 的 PR 交付模型。

## A. 设计流程

### A1. Google Design Sprint

- URL（已核验）：<https://designsprintkit.withgoogle.com/methodology/overview>
- 原文摘录：
  > “The Design Sprint follows six phases: Understand, Define, Sketch, Decide, Prototype, and Validate.”
- 说明：用户清单写“五阶段”，当前官方页面实际写的是**六阶段**；未擅自改成五阶段。

### A2. Design Council Double Diamond

- 用户给出的旧路径已 `curl` 返回 404；实际核验的官方新路径：<https://www.designcouncil.org.uk/resources/the-double-diamond>
- 原文摘录：
  > “The Double Diamond is a visual representation of the design and innovation process. It’s a simple way to describe the steps taken in any design and innovation project, irrespective of methods and tools used.”
- 四阶段的官方历史页：<https://www.designcouncil.org.uk/our-resources/the-double-diamond/history-of-the-double-diamond>
- 原文摘录：
  > “It is based on four distinct phases that the team, deliberately seeking a memorable device, named Discover, Define, Develop and Deliver.”
  >
  > “The process starts by questioning the challenge and quickly leads to research to identify user needs.”

### A3. NN/g

- Design Thinking 101：<https://www.nngroup.com/articles/design-thinking/>（已核验）
  > “The design-thinking framework follows an overall flow of 1) understand, 2) explore, and 3) materialize. Within these larger buckets fall the 6 phases: empathize, define, ideate, prototype, test, and implement.”
- Wireframing（用户给出的 `/articles/wireframes/` 返回 404；替代官方页已核验）：<https://www.nngroup.com/articles/draw-wireframe-even-if-you-cant-draw/>
  > “Wireframes visualize a user path or flow, as well as page layouts, information hierarchy, and even interactions.”
  >
  > “There is a step-by-step guide to get you sketching quickly.”
- UX Research Cheat Sheet：<https://www.nngroup.com/articles/ux-research-cheat-sheet/>（已核验）
  > “Do user research at whatever stage you’re in right now.”
  >
  > “Do user research at all the stages.”
  >
  > “The important thing is not to execute a giant list of activities in rigid order, but to start somewhere and learn more and more as you go along.”

### A4. Figma Learn

- 设计系统课程总览：<https://help.figma.com/hc/en-us/articles/14552901442839-Overview-Introduction-to-design-systems>（已核验）
- 原文摘录：
  > “This course will walk you through the entire design system journey—from fundamental concepts, to building and documenting your system.”
  >
  > “Chapter 2: Build your foundations”
  >
  > “Chapter 3: Build components”
- wireframe → prototype 实例：<https://help.figma.com/hc/en-us/articles/16118297069463-Create-a-photo-gallery-prototype>（已核验）
  > “We’ve finished creating a wireframe for our gallery. Now let’s add prototyping interactions.”
- 说明：这组页面实际覆盖 wireframe、prototype、foundations、components、documentation/maintenance；未把搜索摘要当作额外事实。

### A5. Material Design 3

- Foundations：<https://m3.material.io/foundations>（已核验）
- Design tokens：<https://m3.material.io/foundations/design-tokens>（已核验；用户给的 `/overview` 也返回 200，但当前页面 canonical 内容在无 `/overview` 路径）
- 原文摘录：
  > “Design tokens are the building blocks of all UI elements. The same tokens are used in designs, tools, and code.”
  >
  > “Use design tokens instead of hardcoded values.”
  >
  > “Design tokens make it possible for a design system to have a single source of truth.”

### A6. Atomic Design

- URL（已核验）：<https://atomicdesign.bradfrost.com/chapter-2/>
- 说明：章节页可打开，但本次文本抓取未取得稳定正文摘录；**未核验摘录**。入口和章节 URL 未编造。

### A7. Refactoring UI

- URL（已核验）：<https://refactoringui.com/>
- 原文摘录：
  > “Starting from Scratch”
  >
  > “Start with a feature, not a layout”
  >
  > “Detail comes later”
- 说明：这是官网目录/摘要页原文，完整付费章节不做未经授权的全文复制。

### A8. W3C Design Tokens Community Group

- 当前社区组页面：<https://www.w3.org/community/design-tokens/>（已核验）
- 当前格式规范：<https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/>（已核验）
- 原文摘录：
  > “The Design Tokens Community Group’s goal is to provide technology upon which products and design tools can rely for sharing stylistic pieces of a design system at scale.”
  >
  > “This document describes the technical specification for a file format to exchange design tokens between different tools.”
- 用户给出的 `https://www.designtokens.org/tr/` 直接 `curl` 返回 404；使用官方社区页及其当前规范链接替代。

## B. 工程落地

### B9. shadcn/ui

- URL（已核验）：<https://ui.shadcn.com/docs/theming>
- 原文摘录：
  > “We use and recommend CSS variables for theming.”
  >
  > “This gives you semantic theme tokens like `background`, `foreground`, and `primary` that components use by default.”
  >
  > “Override those tokens in your CSS to change the look of your app without rewriting component classes.”

### B10. Tailwind CSS v4

- URL（已核验）：<https://tailwindcss.com/docs/theme>
- 原文摘录：
  > “Theme variables are special CSS variables defined using the `@theme` directive that influence which utility classes exist in your project.”
  >
  > “If you want to define your own custom design tokens, add them to your CSS file using the `@theme` directive.”

### B11. Storybook

- 用户给出的 <https://storybook.js.org/tutorials/design-systems-for-developers> 本次 `curl` 返回 404。
- 当前官方组件工作流教程：<https://storybook.js.org/tutorials/intro-to-storybook/>（已核验）
- 原文摘录：
  > “Storybook is the most popular UI component development tool for React, Vue, and Angular.”
  >
  > “Intro to Storybook teaches tried-and-true patterns for component development …”
  >
  > “Simple component / Composite component / Data / Screens / Deploy / Visual Testing”
- 说明：该页是 Storybook 官方现行教程，不把已失效的旧 URL 伪装成可用页面。

### B12. Geist 与 Radix Themes

- Geist：<https://vercel.com/geist>（已核验）
  > “Geist provides the colors, typography, materials, layout, and React components behind Vercel’s products.”
  >
  > “Foundations — Colors … Typography … Materials … Grid …”
- Radix Themes：<https://www.radix-ui.com/themes/docs/overview/getting-started>（已核验）
  > “Radix Themes is a pre-styled component library that is designed to work out of the box with minimal configuration.”
  >
  > “You are now ready to use Radix Themes components.”

### B13. W3C/WAI 设计阶段无障碍

- URL（已核验）：<https://www.w3.org/WAI/tips/designing/>
- 原文摘录：
  > “This page introduces some basic considerations to help you get started making your user interface design and visual design more accessible to people with disabilities.”
  >
  > “These tips are good practice to help you meet Web Content Accessibility Guidelines (WCAG) requirements.”

### B14. web.dev

- Learn Design：<https://web.dev/learn/design/>（已核验）
- Learn Accessibility：<https://web.dev/learn/accessibility/>（已核验）
- 说明：两个目录页均能打开；本次抓取没有稳定提取到可逐句复核的课程正文摘录，因此标记为**未核验摘录**，不编造课程句子。

## C. 开源实例：gh api 实查

### C15. Primer

- GitHub：<https://github.com/primer/design>
- gh api：stars **761**；pushed_at **2025-07-02T18:45:58Z**；license **MIT**。
- 官网：<https://primer.style/>
- 设计系统/文档入口（已核验）：<https://primer.style/product/getting-started>
- 组织说明：仓库/官网按 foundations、组件和产品使用文档组织；本次入口页正文抓取不稳定，未添加未经复核的长引文。

### C16. Shopify Polaris

- 用户给的 `https://github.com/Shopify/polaris` 实际通过 GitHub API 重定向到：<https://github.com/Shopify/polaris-react-archive>
- gh api：stars **6,170**；pushed_at **2026-08-11T07:11:56Z**；license **NOASSERTION**。
- 官网：<https://polaris.shopify.com/>（本次可访问）
- 说明：GitHub 当前仓库名已是 archive；不把历史 `shopify/polaris` slug 当成仍未重定向的事实。

### C17. Carbon

- GitHub：<https://github.com/carbon-design-system/carbon>
- gh api：stars **9,433**；pushed_at **2026-09-06T14:16:44Z**；license **Apache-2.0**。
- 官网：<https://carbondesignsystem.com/>
- 组织说明：仓库名和官网均以 Carbon design system 作为组件、设计语言和开发资源的中心；本次官网抓取正文没有稳定返回可引用的流程句，未扩展引用。

### C18. Atlassian Design System

- 官方 foundations：<https://atlassian.design/foundations>（已核验）
- 官方总览：<https://atlassian.design/get-started/about-atlassian-design-system>（已核验）
- GitHub：用户给出的 `https://github.com/atlassian/design-system` 以 `gh api` 返回 404；Atlassian 官方设计系统内容在上述 `atlassian.design` 文档站，未猜测 GitHub slug。
- 原文摘录：
  > “Foundations create engaging user experiences. These include our tokens, guidelines, and visual styles: color, spacing, typography, and more.”
  >
  > “Design tokens are the single source of truth to name and store decisions about the user interface.”

### C19. GOV.UK Design System

- GitHub：<https://github.com/alphagov/govuk-design-system>
- gh api：stars **667**；pushed_at **2026-09-04T17:19:12Z**；license **MIT**。
- 官网：<https://design-system.service.gov.uk/>
- 原文摘录（仓库说明）：
  > “One place for service teams to find styles, components and patterns for designing government services.”
- 文档/组织方式：官网把 styles、components、patterns 和服务设计内容分层；仓库 README 还把源码、构建、测试、CI、部署分开说明。

### C20. Untitled UI（开源部分）

- GitHub：<https://github.com/untitleduico/react>（已核验；这是实际公开仓库，不是用户清单中不存在的 `untitled-ui/untitled-ui`）
- gh api：stars **1,904**；pushed_at **2026-09-02T14:57:12Z**；license **MIT**。本次 `gh api` 对用户给出的旧 slug `untitled-ui/untitled-ui` 返回 404，实际公开仓库 `untitleduico/react` 返回上述数据。
- 官网：<https://www.untitledui.com/react/>
- 原文摘录（官网/仓库描述）：
  > “Untitled UI React is the world’s largest collection of open-source React components built with Tailwind CSS and React Aria.”
  >
  > “This license applies only to the components included in this open-source repository.”
- 组织说明：公开仓库是基础 React 组件集合，PRO 部分单独授权；不要把 PRO 页面/组件当成开源仓库内容。

## 未核验 / URL 修正清单

- Design Sprint：官方页面实际写 **six phases**，不是用户清单中的 five；已保留原文事实。
- Design Council 旧路径 <https://www.designcouncil.org.uk/our-resources/framework-for-innovation/design-councils-evolved-double-diamond/>：404；已换官方 <https://www.designcouncil.org.uk/resources/the-double-diamond/>。
- NN/g `/articles/wireframes/`：404；已换官方 <https://www.nngroup.com/articles/draw-wireframe-even-if-you-cant-draw/>。
- Storybook `/tutorials/design-systems-for-developers/`：404；已换官方 <https://storybook.js.org/tutorials/intro-to-storybook/>。
- Design Tokens `/tr/`：404；已换 W3C 社区组和当前报告链接。
- Google Stitch、Firebase Studio、Cursor 两个页面、Lovable、Bolt、Qoder、Trae、CodeBuddy、MasterGo、即时设计：URL 可打开或返回 200，但本次没有稳定提取可复核正文，因此只记录为**未核验摘录**。
- Reddit `r/ClaudeAI`、`r/cursor`、`r/webdev`：本次限定搜索未得到可稳定打开并符合主题的帖子，未猜测链接。
- GitHub `atlassian/design-system`、`untitled-ui/untitled-ui`、`kirodotdev`、`awesome-claude-code`、`awesome-ai-coding`：`gh api` 404；未猜测替代仓库。Untitled UI 使用实际公开仓库 <https://github.com/untitleduico/react>，其 stars / pushed_at / license 已由 `gh api` 核验。
