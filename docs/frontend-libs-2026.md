# 前端生态选型研究 2026（码印 / CodeStamp 前端）

- 实查日期：**2026-09-05（UTC）**
- 角色：前端生态研究员（Company OS 职能员工）
- 对象仓库：wookat/SoftCopyrightAgent `frontend/`
- 方法：全部数字为一手实查——GitHub 元数据用 `gh api repos/<owner>/<repo>`（stars / SPDX / pushed_at / archived），npm 用 registry（`https://registry.npmjs.org/<pkg>`：latest 版本、license、peerDependencies、unpackedSize）与下载 API（`https://api.npmjs.org/downloads/point/last-week/<pkg>`，统计窗口 2026-08-23 ~ 08-29）；React 19 / Tailwind v4 支持以官方文档 / changelog / peerDependencies 为据。采集脚本共 219 个候选，逐条记录。
- 标注约定：**[已验证]** = 本轮直接查到 API/页面/命令输出；**[推测]** = 由证据推断，未独立核实。表格中 `—` = 无对应 npm 包或未查到。
- 字段说明：
  - 「GitHub」= stars / GitHub SPDX（`NOASSERTION` 表示 GitHub 无法识别许可证文件，需看 npm license 或仓库 LICENSE） / 最近 push / archived。
  - 「npm」= latest 版本 / 周下载 / **unpacked size**（npm 安装体积，**不是**浏览器 bundle 体积；bundle 体积请点各行「体积」列的 bundlephobia 链接，该站按需实时计算，本轮未逐个抓取数值）。
  - 「R19 / TWv4」= 是否支持 React 19 / Tailwind CSS v4：`✅` 有官方文档或 peer 声明；`peer` 仅由 peerDependencies 推断；`n/a` 与该项无关（非 React 组件 / 非 Tailwind 插件）。
  - 「关系」= 相对码印现有栈：**已在用 / 可直接补用 / 需替换现有 / 不适用**。

---

## 0. 总结论：四象限（保留 / 补用 / 替换 / 不用）

### 保留（已在用，继续，按需小版本升级）

| 库 | 现用 → 最新 | 结论 |
|---|---|---|
| React 19 / TypeScript 7 / Vite 8 / pnpm 11 | `react ^19.0.0`→19.2.8；`vite ^8.1.5`→8.2.2 | 主流、最新，保留 |
| Tailwind CSS v4 + `@tailwindcss/vite` | 4.3.3 = latest | 保留 |
| shadcn/ui 模式（Radix 原语 + CVA + tailwind-merge） | `shadcn` CLI 4.21.0；Radix 1.6.7 | 保留。shadcn 现已官方支持 Radix / Base UI / React Aria 三种原语（见 §1），**不必换原语** |
| lucide-react | 1.26.0 → 1.41.0 | 保留，117 处 import；ISC 许可 |
| sonner | 2.0.7 → 2.0.8 | 保留 |
| TanStack Query 5 | ^5.101.4 → 5.102.8 | 保留 |
| react-markdown + remark-gfm、shiki | 10.1.0 / 4.0.1 / 4.3.1→4.4.3 | 保留 |
| Vitest / Testing Library / Playwright | Vitest 4.1.10（latest 已是 **5.0.0**，2026-09-03 发布） | 保留；Vitest 5 升级放入后续技术债，不急 |

### 补用（现有栈缺口，可直接加，均 MIT/ISC/Apache-2.0）

| 缺口 | 首选 | 备选 | 理由（详见对应章节） |
|---|---|---|---|
| 表单 + 校验 | **react-hook-form 7.87 + zod 4.5 + @hookform/resolvers** | TanStack Form + valibot | shadcn `<Form>` 官方基于 RHF+zod；周下载 58.7M / 274.7M |
| 动效 | **motion 13.2**（framer-motion 同源） | `tw-animate-css`（shadcn 默认 CSS 动画） | MIT、R19 peer；GSAP 许可证特殊不选 |
| 图表 | **recharts 3.10**（shadcn charts 官方封装） | ECharts 6（中文重图表场景） | MIT、R19 peer；Tremor 停滞（最后 push 2025-10-10） |
| 长列表虚拟化 | **@tanstack/react-virtual 3.14** | react-window 2.3 | 与 TanStack Table 同族 |
| 日期 | **date-fns 4.4** + react-day-picker 10（shadcn Calendar） | dayjs | tree-shakable、shadcn 默认 |
| 上传 / 拖拽 | **react-dropzone 20** + `@dnd-kit/react`（0.5，注意仍 0.x） | pragmatic-drag-and-drop | 现有 pdf-preview 用 iframe，暂不需 pdf.js |
| PDF 内嵌预览升级（可选） | react-pdf 10（pdf.js 6） | EmbedPDF | 仅在 iframe 兜底不满足移动端时 |
| SEO head 管理（预渲染已有） | **@unhead/react 3.4**（要求 React ≥19.2.4） | react-helmet-async 3 | react-helmet 原版 2020 后无 npm 发布，**不用** |
| a11y 自动检查 | **@axe-core/playwright 4.13**（MPL-2.0，仅 devDependency） | eslint-plugin-jsx-a11y | WCAG AA 验收硬指标 |
| 工程 | **oxlint 1.81**（仓库当前无 lint）、Knip 6、size-limit 13、rollup-plugin-visualizer 7 | Biome 2 | 都是 devDependency，零运行时 |
| 中文字体 | **思源黑体 / Noto Sans CJK（OFL-1.1）**，配 cn-font-split 分包 | 霞鹜文楷（OFL-1.1，标题装饰用） | MiSans / HarmonyOS Sans / 阿里普惠体为厂商自定义许可，见 §15 |
| 客户端状态（若需） | **zustand 5** | jotai 2 | 当前 TanStack Query 已覆盖服务端状态，仅 UI 状态需要时再加 |

### 替换（现有依赖出现上游重大变化，需要有计划迁移）

| 现有 | 变化（已验证） | 建议 |
|---|---|---|
| `react-router-dom ^7.18.1`（102 处 import） | **React Router v8（2026-06-17）已删除 `react-router-dom` 包**，v8 要求 React ≥19.2.7、Vite 7+、ESM-only；`react-router-dom` latest 停在 7.18.3 | **不急**：v7 仍维护（7.18.3 于 2026-08-28 发布）。建议在 v7 内先把 import 改为 `react-router` / `react-router/dom`（v7 已支持），之后升 v8 只是改版本号 |
| `@tanstack/react-table 8.21.3` | **TanStack Table v9（9.2.4）**：`useReactTable`→`useTable`、必须显式声明 `features`、ESM-only、按需 tree-shaking（官方称起步 5 kB） | **不急**：v8 仍在 npm；v9 提供 `@tanstack/react-table/legacy` 的 `useLegacyTable` 过渡。列入技术债，等 shadcn data-table 文档同步 v9 后再迁 |
| `@base-ui-components/react`（若有人建议引入） | 该包已在 npm 标记 deprecated：「Package was renamed to `@base-ui/react`」 | 如引入 Base UI，一律用 `@base-ui/react`（1.8.0） |

### 不用（本轮明确不建议引入）

| 库 | 原因（已验证） |
|---|---|
| GSAP | 许可证非 OSI（npm license 字段：「Standard 'no charge' license」），条款含竞争限制且声明可修改；动效需求 motion 足够 |
| coss ui（原 Origin UI） | 仓库 `cosscom/coss` GitHub SPDX = **AGPL-3.0**（仅 `apps/origin/`、`apps/ui/` 保留 MIT 的 legacy 文件）；SaaS 场景 AGPL 风险高 |
| Tremor | 最近 push 2025-10-10、npm 最后发布 2025-01-13、peer `react ^18.0.0`，与 React 19 不匹配 |
| Ant Design / Arco / TDesign / Semi / Mantine / Chakra / MUI 等整套组件库 | 与 shadcn+Tailwind v4 token 体系并行会双份样式系统；antd unpacked 48.9 MB、TDesign 53.7 MB、Semi 61 MB |
| IconPark（字节） | GitHub **archived = true**，npm 最后发布 2022-07-04 |
| react-helmet（nfl 原版） | npm 最后发布 2020-06-08，最近 push 2023-07-18 |
| Monaco Editor | unpacked 97.9 MB，产品无代码编辑需求（只有高亮，shiki 已覆盖） |
| jszip | license `(MIT OR GPL-3.0-or-later)` 双许可可选 MIT，但 npm 最后发布 2022-08-02；如需 zip 优先看 fflate/服务端打包 |
| Next.js / Remix / TanStack Start | 我们是 SPA + 预渲染脚本（`scripts/prerender.mjs`），元框架迁移收益低于成本 |
| Aceternity UI | 官网组件免费但 Pro 收费（pricing 页），且无可核验的官方开源仓库（`manuarora700/aceternity-ui` 不存在，npm `aceternity-ui` 最后发布 2024-07-22）|

---

## 1. 组件库 / UI 库

| 候选 | GitHub（★ / SPDX / push / archived） | npm（版本 / 周下载 / unpacked） | 体积 | R19 | TWv4 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|---|
| [shadcn/ui](https://github.com/shadcn-ui/ui) | 123.1k / MIT / 2026-09-04 / 否 | `shadcn` 4.21.0 / 8.7M / 839 kB（CLI） | n/a（源码复制） | ✅ [Vite 安装文档](https://ui.shadcn.com/docs/installation/vite) | ✅ [Tailwind v4 文档](https://ui.shadcn.com/docs/tailwind-v4) | **已在用** | [changelog](https://ui.shadcn.com/docs/changelog)：已支持 Radix / Base UI / React Aria 三种原语 × 8 种风格；无许可证风险 |
| [Radix UI Primitives](https://github.com/radix-ui/primitives) | 19.2k / MIT / 2026-08-08 / 否 | `radix-ui` 1.6.7 / 12.8M / 106 kB | [bundlephobia](https://bundlephobia.com/package/radix-ui) | ✅ peer `^19.0` | n/a | **已在用**（7 个 `@radix-ui/react-*`） | 发布节奏放缓（最近 npm 2026-07-24），但仍维护；WorkOS 出资 |
| [Base UI](https://github.com/mui/base-ui) | 10.8k / MIT / 2026-09-05 / 否 | `@base-ui/react` 1.8.0 / 11.2M / — | [bundlephobia](https://bundlephobia.com/package/@base-ui/react) | ✅ peer `^17‖^18‖^19` | n/a | 可直接补用（shadcn 已官方支持） | [1.0 stable 2025-12-11](https://base-ui.com/react/overview/releases)；旧包名 `@base-ui-components/react` 已 deprecated |
| [React Aria Components](https://github.com/adobe/react-spectrum) | 15.8k / Apache-2.0 / 2026-09-05 / 否 | 1.21.1 / 4.0M / 6.6 MB | [bundlephobia](https://bundlephobia.com/package/react-aria-components) | ✅ peer `^19.0.0-rc.1` | n/a | 可直接补用 | a11y 最强，体积最大；Adobe 维护 |
| [Headless UI](https://github.com/tailwindlabs/headlessui) | 28.7k / MIT / 2026-04-13 / 否 | `@headlessui/react` 2.2.10 / 7.2M / 1.0 MB | [bundlephobia](https://bundlephobia.com/package/@headlessui/react) | ✅ peer `^19` | n/a | 不适用（与 Radix 重叠） | Tailwind Labs 维护，但 2026 年更新少（最近 push 4 月） |
| [Ark UI](https://github.com/chakra-ui/ark) | 5.4k / MIT / 2026-09-05 / 否 | `@ark-ui/react` 5.39.1 / 1.1M / 3.3 MB | [bundlephobia](https://bundlephobia.com/package/@ark-ui/react) | peer `>=18` | n/a | 不适用（重叠） | Zag.js 状态机，跨框架 |
| [Mantine](https://github.com/mantinedev/mantine) | 31.7k / MIT / 2026-09-01 / 否 | `@mantine/core` 9.6.0 / 2.6M / 9.2 MB | [bundlephobia](https://bundlephobia.com/package/@mantine/core) | ✅ peer `^19.2.0` | ✗（自带 CSS 变量体系） | 不适用（双样式系统） | 需替换全部 token；不选 |
| [Chakra UI](https://github.com/chakra-ui/chakra-ui) | 40.6k / MIT / 2026-09-05 / 否 | `@chakra-ui/react` 3.37.0 / 1.8M / 2.7 MB | [bundlephobia](https://bundlephobia.com/package/@chakra-ui/react) | peer `>=18` | ✗（Panda/Emotion 体系） | 不适用 | 同上 |
| [HeroUI](https://github.com/heroui-inc/heroui)（原 NextUI） | 30.6k / Apache-2.0（GitHub）· npm MIT / 2026-09-04 / 否 | `@heroui/react` 3.2.4 / 536k / 812 kB | [bundlephobia](https://bundlephobia.com/package/@heroui/react) | ✅ peer `>=19.0.0` | ✅ peer `tailwindcss >=4.0.0` | 不适用（整套组件库，风格与 shadcn 冲突） | v3 底层是 React Aria；GitHub 与 npm 许可证字段不一致，需以仓库 LICENSE 为准 |
| [daisyUI](https://github.com/saadeghi/daisyui) | 42.3k / MIT / 2026-09-03 / 否 | 5.7.28 / 984k / 2.8 MB | [bundlephobia](https://bundlephobia.com/package/daisyui) | n/a（纯 CSS） | ✅ [v5 升级文档](https://daisyui.com/docs/upgrade/) | 不适用（class 语义与 shadcn 冲突） | — |
| [Ant Design](https://github.com/ant-design/ant-design) | 99.4k / MIT / 2026-09-05 / 否 | `antd` 6.6.2 / 3.8M / **48.9 MB** | [bundlephobia](https://bundlephobia.com/package/antd) | ✅ [React 19 兼容文档](https://ant.design/docs/react/v5-for-19) | ✗（CSS-in-JS） | 不适用 | 中文后台首选但与我们 token 体系冲突 |
| [Arco Design](https://github.com/arco-design/arco-design) | 5.7k / MIT / 2026-08-24 / 否 | `@arco-design/web-react` 2.66.16 / 57.9k / 17.2 MB | [bundlephobia](https://bundlephobia.com/package/@arco-design/web-react) | peer `>=16` | ✗ | 不适用 | 周下载低 |
| [TDesign React](https://github.com/Tencent/tdesign-react) | 964 / MIT / 2026-09-04 / 否 | `tdesign-react` 1.18.3 / 45.5k / 53.7 MB | [bundlephobia](https://bundlephobia.com/package/tdesign-react) | peer `>=16.13.1` | ✗ | 不适用 | 星数/下载低 |
| [Semi Design](https://github.com/DouyinFE/semi-design) | 10.3k / NOASSERTION（LICENSE 文件为 MIT）/ 2026-09-01 / 否 | `@douyinfe/semi-ui` 2.103.0 / 26.3k / 61.0 MB | [bundlephobia](https://bundlephobia.com/package/@douyinfe/semi-ui) | peer `>=16` | ✗ | 不适用 | — |
| [MUI Material](https://github.com/mui/material-ui) | 99.0k / MIT / 2026-09-04 / 否 | `@mui/material` 9.4.0 / 10.4M / 5.7 MB | [bundlephobia](https://bundlephobia.com/package/@mui/material) | ✅ peer `^19.0.0` | ✗（Emotion） | 不适用 | — |

**对码印的建议**：保留 shadcn/ui + Radix 现状。shadcn 官方已把 Base UI（MUI 团队，1.0 stable）与 React Aria 列为一等原语，因此「换原语」不再是迁移决策而是逐组件选择；只有 Radix 某组件出现 a11y/维护问题时，才用 `shadcn add` 以 Base UI 版本替换该组件。整套组件库（antd/Mantine/HeroUI 等）一律不引入，避免与 `tokens.css` 104 个变量的 token 体系并行。

---

## 2. shadcn 生态补件

| 候选 | GitHub | npm | R19 | TWv4 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [Magic UI](https://github.com/magicuidesign/magicui) | 22.2k / MIT / 2026-09-05 / 否 | 无同名 npm（registry 复制模式，`magicui` 404） | ✅ | ✅ [Tailwind v4 文档](https://magicui.design/docs/tailwind-v4)：「supports Tailwind v4 and React 19 by default」 | 可直接补用（营销页动效块） | 依赖 `motion`；Pro 模板收费但基础组件 MIT |
| [Kibo UI](https://github.com/haydenbleasel/kibo) | 3.9k / MIT / 2026-05-04 / 否 | `kibo-ui` CLI 1.1.5 / 907 / 4 kB | ✅（React ≥18） | ✅（要求 shadcn CSS Variables 模式） | 可直接补用（Dropzone、Gantt、Kanban 等复合件） | [Setup 文档](https://www.kibo-ui.com/docs/setup)；更新频率中等（最近 push 5 月） |
| [Motion Primitives](https://github.com/ibelick/motion-primitives) | 6.2k / MIT / 2026-03-19 / 否 | `motion-primitives` 0.1.0 / 3.1k / 20 kB | ✅（motion 12+） | ✅ | 可直接补用 | [文档](https://motion-primitives.com/docs)；更新慢（最近 push 3 月） |
| [Untitled UI React](https://github.com/untitleduico/react) | 1.9k / MIT / 2026-09-02 / 否 | `untitledui` CLI 0.1.64 / 8.9k / 271 kB | ✅（React 19.1+，React Aria） | ✅ | 可直接补用 | [官网](https://www.untitledui.com/react)、[LICENSE=MIT](https://github.com/untitleduico/react/blob/main/LICENSE)；Figma 完整版收费 |
| [coss ui（原 Origin UI）](https://github.com/cosscom/coss) | 10.5k / **AGPL-3.0** / 2026-09-05 / 否 | 无 | ✅ | ✅ | **不用** | [README](https://github.com/cosscom/coss)：Origin UI 为 legacy snapshot；[LICENSE](https://github.com/cosscom/coss/blob/main/LICENSE) AGPLv3，仅 `apps/origin/`、`apps/ui/` 内的旧文件 MIT；`origin-space/originui` 已 302 到同一仓库 |
| [Aceternity UI](https://ui.aceternity.com/) | 无官方开源仓库可核验 | `aceternity-ui` 0.2.2 / 2.6k / 最后发布 2024-07-22 | 未核验 | 未核验 | **不用** | [pricing](https://ui.aceternity.com/pricing) Pro 收费；免费组件按页面复制，许可不透明 |
| [cult-ui](https://github.com/nolly-studio/cult-ui) | 6.1k / MIT / 2026-07-22 / 否 | 无（复制模式） | ✅ | ✅ | 可直接补用（少量营销动效） | [文档](https://www.cult-ui.com/docs)；Pro 收费 |
| [tweakcn](https://github.com/jnsahaj/tweakcn) | 10.3k / Apache-2.0 / 2026-09-03 / 否 | 在线工具 | n/a | ✅ | 可直接补用（主题生成器，产出 CSS 变量） | 可用于校对 `tokens.css` 对比度 |
| [awesome-shadcn-ui](https://github.com/birobirobiro/awesome-shadcn-ui) | 20.4k / MIT / 2026-09-01 / 否 | 目录 | n/a | n/a | 索引 | 每项需单独核许可证 |
| [Tremor（blocks）](https://github.com/tremorlabs/tremor) | 3.6k / Apache-2.0 / **2025-10-10** / 否 | `@tremor/react` 3.18.7 / 388k / 最后发布 2025-01-13；peer `react ^18.0.0` | ✗ | ✗（v3 仍 Tailwind v3 配置） | **不用** | 维护停滞证据：11 个月无 push、20 个月无发布 |

**对码印的建议**：营销页动效块优先 Magic UI（MIT、明确 R19+TWv4），复合业务件（Dropzone/Kanban）看 Kibo UI；两者都是源码复制进 `components/`，引入时逐文件保留许可证头。coss/Origin UI 一律不复制——即使单个组件文件是 MIT，也要人工确认文件级 license，运营成本高于价值。Tremor 明确停滞，图表走 §5 的 shadcn charts。

---

## 3. 图标库

| 候选 | GitHub | npm | 体积 | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [lucide](https://github.com/lucide-icons/lucide) | 24.4k / NOASSERTION（npm **ISC**）/ 2026-09-04 / 否 | `lucide-react` 1.41.0 / **97.8M** / 32 MB（全量，tree-shake 后按用量） | [bundlephobia](https://bundlephobia.com/package/lucide-react) | ✅ peer `^19.0.0` | **已在用**（117 处 import；现 1.26.0） | 无风险；建议升到 1.41.0 |
| [Phosphor](https://github.com/phosphor-icons/react) | 1.7k / MIT / 2026-01-06 / 否 | `@phosphor-icons/react` 2.1.10 / 3.4M / 33 MB | [bundlephobia](https://bundlephobia.com/package/@phosphor-icons/react) | peer `>=16.8` | 不适用（风格混用） | 6 种 weight；更新较慢 |
| [Tabler Icons](https://github.com/tabler/tabler-icons) | 21.6k / MIT / 2026-09-03 / 否 | `@tabler/icons-react` 3.46.0 / 3.1M / 66 MB | [bundlephobia](https://bundlephobia.com/package/@tabler/icons-react) | peer `>=16` | 可直接补用（lucide 缺图时） | 与 lucide 同为 24px 线性，风格接近 |
| [Heroicons](https://github.com/tailwindlabs/heroicons) | 23.8k / MIT / 2026-05-12 / 否 | `@heroicons/react` 2.2.0 / 4.1M / 3.7 MB | [bundlephobia](https://bundlephobia.com/package/@heroicons/react) | ✅ peer `^19.0.0-rc` | 不适用 | npm 最后发布 2024-11-18 |
| [Radix Icons](https://github.com/radix-ui/icons) | 2.7k / MIT / 2026-04-02 / 否 | `@radix-ui/react-icons` 1.3.2 / 5.5M / 3.4 MB | [bundlephobia](https://bundlephobia.com/package/@radix-ui/react-icons) | ✅ peer `^19.0.0` | 不适用 | 15px 网格，与 lucide 24px 不一致 |
| [Iconify](https://github.com/iconify/iconify) | 6.3k / MIT / 2026-09-05 / 否 | `@iconify/react` 6.0.2 / 1.0M / 211 kB | [bundlephobia](https://bundlephobia.com/package/@iconify/react) | peer `>=16` | 可直接补用（一次性用到冷门图标集） | 默认运行时从 API 拉 SVG，需离线打包（`@iconify/tailwind4` 或 unplugin-icons）才不依赖第三方网络 |
| [Remix Icon](https://github.com/Remix-Design/RemixIcon) | 8.3k / NOASSERTION / 2026-04-28 / 否 | `@remixicon/react` 4.9.0 / 828k / 5.1 MB；license 「**Remix Icon License 1.0**」 | [bundlephobia](https://bundlephobia.com/package/@remixicon/react) | peer `>=18.2.0` | 不适用 | 非 SPDX 标准许可证，需法务看条款 |
| [IconPark（字节）](https://github.com/bytedance/IconPark) | 9.1k / Apache-2.0 / 2023-02-24 / **archived=true** | `@icon-park/react` 1.4.2 / 21.6k / 最后发布 2022-07-04 | — | peer `>=16.9` | **不用** | 已归档 |
| [Hugeicons](https://github.com/hugeicons/hugeicons-react) | 52 / MIT / 2026-06-15 / 否 | `@hugeicons/react` 1.1.10 / 886k；免费集 `@hugeicons/core-free-icons` 4.3.0 MIT | [bundlephobia](https://bundlephobia.com/package/@hugeicons/react) | peer `>=16` | 不适用 | 免费 4k+ 图标，Pro 收费（功能墙） |
| [react-icons](https://github.com/react-icons/react-icons) | 12.6k / NOASSERTION（npm MIT）/ 2026-08-12 / 否 | 5.7.0 / 8.8M / **88 MB** | [bundlephobia](https://bundlephobia.com/package/react-icons) | peer `*` | 不适用 | 聚合包，各子集许可证不同（含 CC-BY） |

**对码印的建议**：保留 lucide-react 单一图标源（一致的 24px 线性风格 = a11y 与品牌一致性）。补图顺序：先 lucide 新版（1.41 比现用 1.26 多 15 个小版本的图标），再 Tabler（风格相近、MIT）；品牌 logo 类走 `components/brand`。不引入 Remix Icon（非标准许可）、IconPark（归档）、react-icons（许可证混杂）。

---

## 4. 动效

| 候选 | GitHub | npm | 体积 | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [Motion](https://github.com/motiondivision/motion)（framer-motion） | 33.5k / MIT / 2026-09-02 / 否 | `motion` 13.2.0 / 20.0M（`framer-motion` 别名 45.7M）/ 718 kB | [bundlephobia](https://bundlephobia.com/package/motion) | ✅ peer `^19.0.0` | **可直接补用（首选）** | Magic UI / Motion Primitives 均依赖它；MIT |
| [react-spring](https://github.com/pmndrs/react-spring) | 29.1k / MIT / 2026-09-04 / 否 | `@react-spring/web` 10.1.2 / 5.5M / 56 kB | [bundlephobia](https://bundlephobia.com/package/@react-spring/web) | ✅ peer `^19.0.0` | 可直接补用（物理动效） | 与 motion 二选一即可 |
| [AutoAnimate](https://github.com/formkit/auto-animate) | 13.9k / MIT / 2026-07-10 / 否 | `@formkit/auto-animate` 0.10.0 / 1.5M / 59 kB | [bundlephobia](https://bundlephobia.com/package/@formkit/auto-animate) | ✅（框架无关） | 可直接补用（列表增删过渡，一行代码） | 0.x 版本号 |
| [GSAP](https://github.com/greensock/GSAP) | 28.3k / GitHub SPDX **NONE** / 2026-04-13 / 否 | `gsap` 3.15.0 / 4.8M / 6.3 MB；npm license 字段「Standard 'no charge' license」 | [bundlephobia](https://bundlephobia.com/package/gsap) | n/a | **不用** | [官方许可页](https://gsap.com/licensing/)：商业免费但非 OSI 许可，含「不得用于与 Webflow 竞争的产品」限制、保留修改权 |
| [Lottie（lottie-web）](https://github.com/airbnb/lottie-web) | 32.1k / MIT / 2025-09-01 / 否 | `lottie-web` 5.13.0 / 7.7M / 25 MB | [bundlephobia](https://bundlephobia.com/package/lottie-web) | n/a | 不适用（暂无设计师动画资产） | 核心库 1 年无 push |
| [dotLottie React](https://github.com/LottieFiles/dotlottie-web) | 866 / MIT / 2026-09-02 / 否 | `@lottiefiles/dotlottie-react` 0.19.16 / 1.3M / 527 kB | [bundlephobia](https://bundlephobia.com/package/@lottiefiles/dotlottie-react) | ✅ peer `^19` | 备选（如未来有 Lottie 资产） | WASM 渲染，比 lottie-web 小 |
| [tw-animate-css](https://github.com/Wombosvideo/tw-animate-css) | 797 / MIT / 2026-02-28 / 否 | 1.4.0 / **37.4M** / 47 kB | [bundlephobia](https://bundlephobia.com/package/tw-animate-css) | n/a | 可直接补用（shadcn 新项目默认） | [shadcn Tailwind v4 文档](https://ui.shadcn.com/docs/tailwind-v4)：2025-03-19 起 `tailwindcss-animate` 已弃用，改为 `tw-animate-css` |
| [react-transition-group](https://github.com/reactjs/react-transition-group) | 10.2k / BSD-3-Clause / 2026-03-05 / 否 | 4.4.5 / 56.5M / 244 kB | — | peer `>=16.6` | 不适用 | npm 最后发布 2022-08-01 |

**对码印的建议**：`tw-animate-css`（纯 CSS，shadcn v4 默认）覆盖 dialog/sheet 等进出场；营销页首屏与数字滚动用 `motion`（配合 `@number-flow/react` 0.6，MIT）。控制台工作区限制动效（`prefers-reduced-motion` 必须尊重，WCAG 2.3.3）。GSAP 不引入：许可证不是 OSI 开源许可且保留单方修改权。

---

## 5. 图表 / 可视化

| 候选 | GitHub | npm | 体积 | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [Recharts](https://github.com/recharts/recharts) | 27.5k / MIT / 2026-09-04 / 否 | 3.10.1 / **57.3M** / 7.5 MB | [bundlephobia](https://bundlephobia.com/package/recharts) | ✅ peer `^19.0.0` | **可直接补用（首选）** | [shadcn charts](https://ui.shadcn.com/docs/components/chart) 官方封装、走 CSS 变量主题 |
| [Nivo](https://github.com/plouc/nivo) | 14.1k / MIT / 2026-07-21 / 否 | `@nivo/core` 0.99.0 / 1.7M / 254 kB | [bundlephobia](https://bundlephobia.com/package/@nivo/core) | ✅ peer `^19.0` | 备选 | 0.x；npm 最后发布 2025-05-23 |
| [visx](https://github.com/airbnb/visx) | 21.0k / MIT / 2026-06-22 / 否 | `@visx/visx` 4.0.0 / 96.5k / 12 kB（元包） | [bundlephobia](https://bundlephobia.com/package/@visx/xychart) | ✅ peer `^19.0.0` | 不适用（低阶，开发成本高） | — |
| [Tremor](https://github.com/tremorlabs/tremor) | 3.6k / Apache-2.0 / **2025-10-10** / 否 | `@tremor/react` 3.18.7 / 388k；peer `react ^18.0.0` | — | ✗ | **不用** | 停滞（见 §2） |
| [ECharts](https://github.com/apache/echarts) | 67.2k / Apache-2.0 / 2026-09-04 / 否 | `echarts` 6.1.0 / 5.1M / 60 MB（按需 import 可降） | [bundlephobia](https://bundlephobia.com/package/echarts) | n/a（用 [echarts-for-react](https://github.com/hustcc/echarts-for-react) 3.0.6，peer `>=16`） | 备选（复杂中文报表/地图） | 体积大，主题需手工映射 token |
| [Chart.js](https://github.com/chartjs/Chart.js) | 67.7k / MIT / 2026-05-27 / 否 | 4.5.1 / 12.9M / 6.2 MB；[react-chartjs-2](https://github.com/reactchartjs/react-chartjs-2) 5.3.1 peer `^19.0.0` | [bundlephobia](https://bundlephobia.com/package/chart.js) | ✅ | 备选 | Canvas 渲染，a11y 需自行补 aria |
| [D3](https://github.com/d3/d3) | 113.6k / ISC / 2026-05-28 / 否 | 7.9.0 / 20.0M / 871 kB | [bundlephobia](https://bundlephobia.com/package/d3) | n/a | 不适用（底层） | npm 最后发布 2024-03-12 |
| [Observable Plot](https://github.com/observablehq/plot) | 5.4k / ISC / 2026-09-01 / 否 | `@observablehq/plot` 0.6.17 / 611k / 1.5 MB | [bundlephobia](https://bundlephobia.com/package/@observablehq/plot) | n/a | 不适用 | 0.x |
| [AntV G2](https://github.com/antvis/G2) | 12.6k / MIT / 2026-09-03 / 否 | `@antv/g2` 5.4.8 / 364k / 8.8 MB | [bundlephobia](https://bundlephobia.com/package/@antv/g2) | n/a | 不适用 | 中文文档好，但非 React 原生 |

**对码印的建议**：控制台「用量/额度/生成统计」类图表直接 `shadcn add chart`（Recharts 3 + CSS 变量），与 `tokens.css` 天然对接、SVG 可读屏。ECharts 仅在需要中文地图/大数据量时按需 import。Tremor 不用。

---

## 6. 表单 / 校验

| 候选 | GitHub | npm | 体积 | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [react-hook-form](https://github.com/react-hook-form/react-hook-form) | 44.8k / MIT / 2026-09-04 / 否 | 7.87.0 / **58.7M** / 1.2 MB | [bundlephobia](https://bundlephobia.com/package/react-hook-form) | ✅ peer `^19` | **可直接补用（首选）** | [shadcn Form](https://ui.shadcn.com/docs/components/form) 官方基于 RHF |
| [@hookform/resolvers](https://github.com/react-hook-form/resolvers) | 2.3k / MIT / 2026-08-17 / 否 | 5.9.1 / 49.0M / 1.2 MB | [bundlephobia](https://bundlephobia.com/package/@hookform/resolvers) | n/a | 可直接补用 | 支持 zod/valibot/arktype/Standard Schema |
| [TanStack Form](https://github.com/TanStack/form) | 6.7k / MIT / 2026-09-05 / 否 | `@tanstack/react-form` 1.33.5 / 2.9M / 567 kB | [bundlephobia](https://bundlephobia.com/package/@tanstack/react-form) | ✅ peer `^19.0.0` | 备选（与 Query/Table 同族） | 生态（shadcn 示例）少于 RHF |
| [zod](https://github.com/colinhacks/zod) | 43.8k / MIT / 2026-09-04 / 否 | 4.5.4 / **274.7M** / 5.8 MB（含 `zod/mini`） | [bundlephobia](https://bundlephobia.com/package/zod) | n/a | **可直接补用（首选）** | 可复用 `openapi-typescript` 生成的类型做 `z.infer` 对齐 |
| [valibot](https://github.com/fabian-hiller/valibot) | 9.0k / MIT / 2026-09-05 / 否 | 1.4.2 / 18.5M / 1.8 MB | [bundlephobia](https://bundlephobia.com/package/valibot) | n/a | 备选（体积敏感） | 模块化、tree-shake 好 |
| [arktype](https://github.com/arktypeio/arktype) | 7.9k / MIT / 2026-07-07 / 否 | 2.2.3 / 2.0M / 337 kB | [bundlephobia](https://bundlephobia.com/package/arktype) | n/a | 不适用 | 语法学习成本 |
| [Standard Schema](https://github.com/standard-schema/standard-schema) | 3.6k / MIT / 2026-08-28 / 否 | `@standard-schema/spec` 1.1.0 / 109.7M / 23 kB | — | n/a | 规范（自动受益） | zod/valibot/arktype/TanStack Form 均实现 |
| [Formik](https://github.com/jaredpalmer/formik) | 34.3k / Apache-2.0 / 2025-11-10 / 否 | 2.4.9 / 4.6M / 585 kB | [bundlephobia](https://bundlephobia.com/package/formik) | peer `>=16.8` | **不用** | 更新慢（近 10 个月无 push） |
| [yup](https://github.com/jquense/yup) | 23.7k / MIT / 2026-09-05 / 否 | 1.7.1 / 12.5M / 270 kB | [bundlephobia](https://bundlephobia.com/package/yup) | n/a | 不适用 | zod 更贴合 TS |

**对码印的建议**：注册/登录/软著信息填报表单统一 `react-hook-form + zod + @hookform/resolvers`，通过 `shadcn add form` 引入 `<Form>` 封装（自动 `aria-describedby`/`aria-invalid`，满足 WCAG 3.3.1）。zod schema 与后端 `openapi.json` 字段对齐，后续可用 `zod/mini` 控体积。

---

## 7. 表格 / 虚拟列表

| 候选 | GitHub | npm | 体积 | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [TanStack Table](https://github.com/TanStack/table) | 28.4k / MIT / 2026-08-31 / 否 | `@tanstack/react-table` **9.2.4** / 20.0M / 135 kB；peer `>=18` | [bundlephobia](https://bundlephobia.com/package/@tanstack/react-table) | ✅ | **已在用（8.21.3）→ 需计划升级 v9** | [v9 迁移指南](https://tanstack.com/table/latest/docs/framework/react/guide/migrating)：`useReactTable`→`useTable`、显式 `features`、ESM-only、`useLegacyTable` 过渡 |
| [TanStack Virtual](https://github.com/TanStack/virtual) | 7.1k / MIT / 2026-08-26 / 否 | `@tanstack/react-virtual` 3.14.10 / 23.2M / 57 kB | [bundlephobia](https://bundlephobia.com/package/@tanstack/react-virtual) | ✅ peer `^19.0.0` | **可直接补用（首选）** | 与 Table 同族 |
| [react-window](https://github.com/bvaughn/react-window) | 17.2k / MIT / 2026-09-05 / 否 | 2.3.1 / 6.9M / 217 kB | [bundlephobia](https://bundlephobia.com/package/react-window) | ✅ peer `^19.0.0` | 备选 | v2 API 重写 |
| [react-virtuoso](https://github.com/petyosi/react-virtuoso) | 6.4k / GitHub NONE（npm MIT）/ 2026-09-05 / 否 | 4.18.13 / 3.5M / 244 kB | [bundlephobia](https://bundlephobia.com/package/react-virtuoso) | peer `>= 19` | 备选（变高行/聊天流） | — |
| [AG Grid Community](https://github.com/ag-grid/ag-grid) | 15.6k / NOASSERTION（[LICENSE.txt](https://github.com/ag-grid/ag-grid/blob/latest/LICENSE.txt)：community MIT、enterprise 商业）/ 2026-09-05 / 否 | `ag-grid-react` 36.1.0 / 2.4M / 834 kB | [bundlephobia](https://bundlephobia.com/package/ag-grid-community) | ✅ peer `^19.0.0` | 不适用（当前无 Excel 级需求） | 商业化陷阱：分组/透视/Excel 导出等在 enterprise |
| [MUI X DataGrid](https://github.com/mui/mui-x) | 5.8k / NONE（npm MIT，Pro/Premium 商业）/ 2026-09-04 / 否 | `@mui/x-data-grid` 9.13.0 / 3.2M / 5.3 MB | — | ✅ | 不适用 | 依赖 MUI 样式体系；功能墙同 AG Grid |
| [Glide Data Grid](https://github.com/glideapps/glide-data-grid) | 5.3k / MIT / 2026-01-21 / 否 | 6.0.3 / 317k / 3.7 MB；peer `^16.12‖17‖18` | — | ✗（peer 未含 19） | 不适用 | npm 最后发布 2024-02-03 |
| [react-data-grid](https://github.com/adazzle/react-data-grid) | 7.7k / NOASSERTION（npm MIT）/ 2026-09-05 / 否 | 7.0.0-beta.61 / 597k / 373 kB；peer `^19.2` | — | ✅ | 不适用 | 长期 beta |

**对码印的建议**：任务列表/材料列表继续 TanStack Table；v9 升级作为独立技术债（改动集中在 `useTable({ features })`，markup 不变，可先用 `useLegacyTable` 平滑）。列表超过约 200 行（历史任务）加 `@tanstack/react-virtual`。AG Grid/MUI X 的免费版功能墙明确，不引入。

## 8. 编辑器 / 富文本 / Markdown / 代码

| 候选 | GitHub | npm | 体积 | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [react-markdown](https://github.com/remarkjs/react-markdown) | 15.9k / MIT / 2026-09-01 / 否 | 10.1.0 / 33.7M / 53 kB | [bundlephobia](https://bundlephobia.com/package/react-markdown) | ✅ peer `>=18` | **已在用** | 无风险 |
| [remark-gfm](https://github.com/remarkjs/remark-gfm) | 1.2k / MIT / 2025-02-10 / 否 | 4.0.1 / 39.3M / 22 kB | [bundlephobia](https://bundlephobia.com/package/remark-gfm) | n/a | **已在用** | 稳定期，更新少属正常（unified 生态） |
| [shiki](https://github.com/shikijs/shiki) | 13.8k / MIT / 2026-08-10 / 否 | 4.4.3 / 23.7M / 603 kB | [bundlephobia](https://bundlephobia.com/package/shiki) | n/a | **已在用**（^4.3.1） | 语法/主题按需加载控体积 |
| [Streamdown（Vercel）](https://github.com/vercel/streamdown) | 5.6k / Apache-2.0 / 2026-09-02 / 否 | 2.6.0 / 6.5M / 111 kB | [bundlephobia](https://bundlephobia.com/package/streamdown) | ✅ peer `^19.0.0` | 可直接补用（AI 流式 Markdown 渲染，未闭合代码块/表格容错） | 内置 shiki + Tailwind 样式；与 react-markdown 二选一用于 SSE 生成预览 |
| [MDX](https://github.com/mdx-js/mdx) | 19.8k / MIT / 2026-09-02 / 否 | `@mdx-js/react` 3.1.1 / 21.0M / 14 kB | — | peer `>=16` | 不适用（指南页已用 Markdown 数据源） | — |
| [Tiptap](https://github.com/ueberdosis/tiptap) | 38.3k / MIT / 2026-09-04 / 否 | `@tiptap/react` 3.31.3 / 14.9M / 567 kB | [bundlephobia](https://bundlephobia.com/package/@tiptap/react) | ✅ peer `^19.0.0` | 备选（若做「章节在线编辑」） | [pricing](https://tiptap.dev/pricing)：编辑器 MIT 免费，协作/AI/DOCX 导入导出为云付费（$49/月起）——功能墙 |
| [Lexical](https://github.com/facebook/lexical) | 23.8k / MIT / 2026-09-04 / 否 | 0.50.0 / 5.1M / 3.5 MB | [bundlephobia](https://bundlephobia.com/package/lexical) | ✅（`@lexical/react`） | 备选 | 0.x，API 仍变动 |
| [Plate](https://github.com/udecode/plate) | 16.6k / NOASSERTION（npm MIT）/ 2026-09-04 / 否 | `platejs` 53.3.11 / 505k / 3.6 kB（元包） | — | peer `>=18` | 备选（shadcn 风格富文本） | 基于 Slate；组件走 shadcn registry |
| [BlockNote](https://github.com/TypeCellOS/BlockNote) | 10.2k / NOASSERTION（npm **MPL-2.0**）/ 2026-09-05 / 否 | `@blocknote/react` 0.54.0 / 546k / 23 MB | — | ✅ peer `^19.0` | 不适用 | MPL-2.0 + 部分 Pro 组件商业授权 |
| [Milkdown](https://github.com/Milkdown/milkdown) | 11.9k / MIT / 2026-09-04 / 否 | `@milkdown/kit` 7.22.1 / 353k / 122 kB | [bundlephobia](https://bundlephobia.com/package/@milkdown/kit) | n/a | 不适用 | Markdown WYSIWYG，生态小 |
| [CodeMirror 6](https://github.com/codemirror/dev) | 7.8k / GitHub **archived=true**（2026-04-15）/ npm MIT | `@codemirror/view` 6.43.11 / 14.8M / 1.3 MB；npm 最后发布 **2026-09-03** | [bundlephobia](https://bundlephobia.com/package/@codemirror/view) | n/a（[@uiw/react-codemirror](https://github.com/uiwjs/react-codemirror) 4.25.11 peer `>=17`） | 备选（若需可编辑代码框） | **仓库已迁出 GitHub**：README 注明「moved to https://code.haverbeke.berlin/codemirror/dev」，npm `repository.url` 同步指向该地址；项目活跃，只是不在 GitHub |
| [Monaco Editor](https://github.com/microsoft/monaco-editor) | 46.7k / MIT / 2026-09-03 / 否 | 0.56.0 / 8.9M / **97.9 MB** | [bundlephobia](https://bundlephobia.com/package/monaco-editor) | n/a（[@monaco-editor/react](https://github.com/suren-atoyan/monaco-react) 4.7.0 peer `^19`） | **不用** | 体积不适合首屏 |
| [@uiw/react-md-editor](https://github.com/uiwjs/react-md-editor) | 2.9k / MIT / 2026-08-21 / 否 | 4.1.2 / 797k / 4.3 MB | [bundlephobia](https://bundlephobia.com/package/@uiw/react-md-editor) | peer `>=16.8` | 备选（轻量 Markdown 编辑） | 样式需覆写以贴合 token |
| [Vditor](https://github.com/Vanessa219/vditor) | 11.3k / MIT / 2026-08-30 / 否 | 4.0.0 / 45.4k / 24 MB | — | n/a | 不适用 | 非 React 原生 |

**对码印的建议**：展示链路保留 react-markdown + remark-gfm + shiki；生成过程的 SSE 流式预览可评估 Streamdown（Apache-2.0，Vercel 维护，专为未闭合 Markdown 容错）。若产品路线图落地「章节级在线编辑」（见 `docs/research/R3-竞品与政策调研`），首选 Tiptap 开源核心（MIT），**不开通其云服务**；不用 Monaco。CodeMirror 若引入，注意 issue/源码在 code.haverbeke.berlin 而非 GitHub。

---

## 9. 日期 / 时间

| 候选 | GitHub | npm | 体积 | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [date-fns](https://github.com/date-fns/date-fns) | 36.6k / GitHub NONE（npm MIT）/ 2026-08-30 / 否 | 4.4.0 / **100.1M** / 10.9 MB（全量，按函数 tree-shake） | [bundlephobia](https://bundlephobia.com/package/date-fns) | n/a | **可直接补用（首选）** | shadcn Calendar/DatePicker 示例默认 |
| [dayjs](https://github.com/iamkun/dayjs) | 48.7k / MIT / 2026-09-01 / 否 | 1.11.23 / 70.1M / 682 kB | [bundlephobia](https://bundlephobia.com/package/dayjs) | n/a | 备选 | 2 kB 核心，插件机制；中文 locale 好 |
| [react-day-picker](https://github.com/gpbl/react-day-picker) | 6.8k / MIT / 2026-08-26 / 否 | 10.0.1 / 44.7M / 987 kB | [bundlephobia](https://bundlephobia.com/package/react-day-picker) | peer `>=16.8` | 可直接补用（shadcn Calendar 底层） | v10 刚发（2026-05-15），shadcn 文档以 v9 为主，引入时核对 |
| [temporal-polyfill](https://github.com/fullcalendar/temporal-polyfill) | 771 / GitHub NONE（npm MIT）/ 2026-08-13 / 否 | 1.0.4 / 3.5M / 1.0 MB | [bundlephobia](https://bundlephobia.com/package/temporal-polyfill) | n/a | 备选（等浏览器原生 Temporal 普及） | — |
| [@js-temporal/polyfill](https://github.com/js-temporal/temporal-polyfill) | 787 / ISC / 2026-05-14 / 否 | 0.5.1 / 2.4M / 3.0 MB | [bundlephobia](https://bundlephobia.com/package/@js-temporal/polyfill) | n/a | 不适用 | 0.x，官方参考实现偏重 |
| [Luxon](https://github.com/moment/luxon) | 16.5k / MIT / 2026-08-09 / 否 | 3.7.2 / 39.3M / 4.6 MB | [bundlephobia](https://bundlephobia.com/package/luxon) | n/a | 不适用 | — |
| [moment](https://github.com/moment/moment)（对照） | 47.9k / MIT / 2026-09-02 / 否 | 2.30.1 / 36.9M / 4.4 MB | — | n/a | **不用** | 官方已宣布维护模式，npm 最后发布 2023-12-27 |
| [@internationalized/date](https://github.com/adobe/react-spectrum) | 15.8k / Apache-2.0 / 2026-09-05 / 否 | 3.12.4 / 15.0M / 1.2 MB | [bundlephobia](https://bundlephobia.com/package/@internationalized/date) | n/a | 不适用（除非用 React Aria） | — |

**对码印的建议**：软著申请涉及「开发完成日期 / 首次发表日期」等日期字段，用 `date-fns` + `react-day-picker`（shadcn Calendar）即可；服务器时间统一 ISO 字符串，前端 `zh-CN` locale 格式化。不引入 moment/Luxon。

---

## 10. 文件上传 / 拖拽 / PDF / DOCX

| 候选 | GitHub | npm | 体积 | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [react-dropzone](https://github.com/react-dropzone/react-dropzone) | 11.0k / MIT / 2026-08-30 / 否 | 20.1.1 / 13.4M / 340 kB | [bundlephobia](https://bundlephobia.com/package/react-dropzone) | ✅ peer `>= 18` | **可直接补用（首选）** | 源码 zip 上传；Kibo UI Dropzone 即基于它 |
| [dnd-kit](https://github.com/clauderic/dnd-kit) | 17.6k / MIT / 2026-09-05 / 否 | `@dnd-kit/core` 6.3.1 / 24.9M / 1.1 MB（最后发布 2024-12-05）；新版 `@dnd-kit/react` **0.5.0** / 1.2M / 2026-09-05 发布，peer `^19.0.0` | [bundlephobia](https://bundlephobia.com/package/@dnd-kit/react) | ✅ | 可直接补用（章节排序） | 两代包并存：`core` 稳定但停更、`react` 活跃但 0.x |
| [pragmatic-drag-and-drop（Atlassian）](https://github.com/atlassian/pragmatic-drag-and-drop) | 12.7k / NOASSERTION（npm Apache-2.0）/ 2026-09-04 / 否 | 3.1.0 / 1.3M / 505 kB | [bundlephobia](https://bundlephobia.com/package/@atlaskit/pragmatic-drag-and-drop) | n/a（框架无关） | 备选 | 原生 HTML5 DnD，移动端需 adapter |
| [pdf.js](https://github.com/mozilla/pdf.js) | 53.8k / Apache-2.0 / 2026-09-04 / 否 | `pdfjs-dist` 6.3.289 / 25.3M / 34.8 MB | [bundlephobia](https://bundlephobia.com/package/pdfjs-dist) | n/a | 备选（现用 iframe 预览） | worker 需单独打包 |
| [react-pdf](https://github.com/wojtekmaj/react-pdf) | 11.2k / MIT / 2026-09-04 / 否 | 10.5.0 / 6.3M / 312 kB | [bundlephobia](https://bundlephobia.com/package/react-pdf) | ✅ peer `^19.0.0` | 备选（移动端内嵌 PDF 兜底不足时） | 依赖 pdfjs-dist |
| [EmbedPDF](https://github.com/embedpdf/embed-pdf-viewer) | 4.5k / NOASSERTION（npm MIT）/ 2026-09-01 / 否 | `@embedpdf/core` 2.15.0 / 420k / 805 kB | [bundlephobia](https://bundlephobia.com/package/@embedpdf/core) | peer `>=16.8` | 备选 | PDFium WASM，标注能力强 |
| [@react-pdf/renderer](https://github.com/diegomura/react-pdf) | 16.8k / MIT / 2026-09-03 / 否 | 4.9.0 / 5.4M / 320 kB | — | ✅ peer `^19.0.0` | 不适用（PDF 由后端 reportlab 生成） | — |
| [docx-preview](https://github.com/VolodymyrBaydalka/docxjs) | 2.1k / Apache-2.0 / 2026-07-07 / 否 | 0.4.0 / 1.5M / 975 kB | [bundlephobia](https://bundlephobia.com/package/docx-preview) | n/a | 备选（DOCX 在线预览） | 0.x，排版保真有限 |
| [mammoth.js](https://github.com/mwilliamson/mammoth.js) | 6.3k / BSD-2-Clause / 2026-08-28 / 否 | 1.12.2 / 7.8M / 2.2 MB | [bundlephobia](https://bundlephobia.com/package/mammoth) | n/a | 备选（DOCX→HTML 语义转换） | 丢失版式，适合正文预览 |
| [docx（生成）](https://github.com/dolanmiu/docx) | 5.9k / MIT / 2026-08-07 / 否 | 9.7.1 / 5.5M / 4.7 MB | — | n/a | 不适用（DOCX 由后端生成） | — |
| [Uppy](https://github.com/transloadit/uppy) | 31.0k / MIT / 2026-09-04 / 否 | `@uppy/core` 6.0.0 / 1.2M / 1.1 MB | — | n/a | 不适用（重，含云导入） | 商业 Transloadit 绑定倾向 |
| [FilePond](https://github.com/pqina/filepond) | 16.4k / MIT / 2026-08-28 / 否 | `react-filepond` 7.1.3 / 177k / 26 kB | — | peer `16 - 19` | 不适用 | 自带样式体系 |
| [jszip](https://github.com/Stuk/jszip) | 10.4k / NOASSERTION / 2026-09-05 / 否 | 3.10.1 / 43.1M；license `(MIT OR GPL-3.0-or-later)`；最后发布 2022-08-02 | — | n/a | 不用（如需前端 zip，改用服务端） | 双许可可选 MIT，但长期无发布 |
| [file-saver](https://github.com/eligrey/FileSaver.js) | 22.0k / NOASSERTION（npm MIT）/ 2023-03-01 / 否 | 2.0.5 / 7.7M；最后发布 2020-11-19 | — | n/a | 不用 | 现代浏览器 `<a download>` 即可 |

**对码印的建议**：源码上传用 react-dropzone（配 shadcn/Kibo Dropzone 样式）；PDF 预览维持 `pdf-preview.tsx` 的 iframe + 新窗口/下载兜底，只有当 390px 移动端验收确认 iframe 不可用时再引入 react-pdf（体积 +~1 MB worker）。DOCX 交付物以下载为主，如需在线预览优先 docx-preview（保留版式）。拖拽排序若要做，直接用 `@dnd-kit/react`（新代，React 19），不要再引 `@dnd-kit/core`。

---

## 11. 状态管理 / 数据层

| 候选 | GitHub | npm | 体积 | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|---|
| [TanStack Query](https://github.com/TanStack/query) | 50.3k / MIT / 2026-09-05 / 否 | `@tanstack/react-query` 5.102.8 / 65.7M / 745 kB | [bundlephobia](https://bundlephobia.com/package/@tanstack/react-query) | ✅ peer `^19` | **已在用**（119 处 import） | 无风险 |
| [Zustand](https://github.com/pmndrs/zustand) | 58.6k / MIT / 2026-08-31 / 否 | 5.0.15 / 54.5M / 95 kB | [bundlephobia](https://bundlephobia.com/package/zustand) | ✅ peer `>=18` | 可直接补用（跨页 UI 状态，如工作区布局/向导步骤） | — |
| [Jotai](https://github.com/pmndrs/jotai) | 21.3k / MIT / 2026-09-04 / 否 | 2.20.3 / 6.1M / 543 kB | [bundlephobia](https://bundlephobia.com/package/jotai) | peer `>=17` | 备选（原子粒度） | 与 zustand 二选一 |
| [Redux Toolkit](https://github.com/reduxjs/redux-toolkit) | 11.2k / MIT / 2026-09-05 / 否 | `@reduxjs/toolkit` 2.12.0 / 28.3M / 6.0 MB | [bundlephobia](https://bundlephobia.com/package/@reduxjs/toolkit) | ✅ peer `^19` | 不适用（样板重，Query 已覆盖服务端状态） | — |
| [SWR](https://github.com/vercel/swr) | 32.5k / MIT / 2026-09-02 / 否 | 2.5.1 / 16.9M / 320 kB | [bundlephobia](https://bundlephobia.com/package/swr) | ✅ peer `^19.0.0` | 不适用（与 Query 重叠） | — |
| [Valtio](https://github.com/pmndrs/valtio) | 10.2k / MIT / 2026-08-30 / 否 | 2.3.2 / 2.0M / 101 kB | [bundlephobia](https://bundlephobia.com/package/valtio) | peer `>=18` | 不适用 | — |
| [XState](https://github.com/statelyai/xstate) | 30.1k / MIT / 2026-09-04 / 否 | 5.32.6 / 5.6M / 2.3 MB | [bundlephobia](https://bundlephobia.com/package/xstate) | n/a | 备选（生成流水线多状态机可视化） | 学习成本高 |
| [nuqs](https://github.com/47ng/nuqs) | 10.8k / MIT / 2026-09-05 / 否 | 2.10.1 / 4.7M / 473 kB | [bundlephobia](https://bundlephobia.com/package/nuqs) | ✅ peer `^19.0.0-0` | 可直接补用（URL 查询参数即状态，支持 React Router 适配器） | 列表筛选/分页可分享 |
| [openapi-typescript](https://github.com/openapi-ts/openapi-typescript) | 8.4k / MIT / 2026-09-05 / 否 | 7.13.0 / 7.0M；`openapi-fetch` 0.17.0 / 8.4M / 229 kB | [bundlephobia](https://bundlephobia.com/package/openapi-fetch) | n/a | **已在用**（`generate:api` 脚本）；`openapi-fetch` 可直接补用做类型安全 fetch | `openapi-fetch` 仍 0.x |
| [orval](https://github.com/orval-labs/orval) | 6.4k / MIT / 2026-09-05 / 否 | 8.28.1 / 2.0M / 521 kB | — | n/a | 备选（直接生成 TanStack Query hooks） | 与现有 `openapi-typescript` 二选一 |

**对码印的建议**：服务端状态继续 TanStack Query；客户端跨页 UI 状态只有在 Context 不够时才加 zustand（95 kB unpacked、无样板）。列表页筛选建议 nuqs 存 URL。API 层可在 `openapi-typescript` 基础上加 `openapi-fetch`，与 `api.gen.ts` 类型零重复。

---

## 12. 路由 / 元框架

| 候选 | GitHub | npm | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|
| [React Router](https://github.com/remix-run/react-router) | 56.6k / MIT / 2026-09-02 / 否 | `react-router` **8.3.1** / 53.2M；peer `react >=19.2.7`；`react-router-dom` latest **7.18.3**（2026-08-28）/ 43.5M | ✅ | **已在用（react-router-dom ^7.18.1，102 处 import）→ 需计划迁移** | [v8.0.0 changelog（2026-06-17）](https://reactrouter.com/changelog)：删除 `react-router-dom`、要求 Node 22.22+/React 19.2.7+/Vite 7+、ESM-only；v7 仍在发版 |
| [TanStack Router](https://github.com/TanStack/router) | 15.0k / MIT / 2026-09-05 / 否 | `@tanstack/react-router` 1.170.32 / 22.1M / 1.1 MB | ✅ peer `>=19` | 需替换现有（不建议） | 类型安全路由强，但 102 处 import 迁移成本高、收益不明确 |
| [Next.js](https://github.com/vercel/next.js) | 142.1k / MIT / 2026-09-05 / 否 | 16.3.4 / 55.3M / 185 MB | ✅ | 不适用（我们 SPA + FastAPI 托管静态） | 仅对比 |
| [Remix](https://github.com/remix-run/remix) | 33.4k / MIT / 2026-09-04 / 否 | `@remix-run/react` 2.17.5 / 721k；peer `^18.0.0` | ✗ | 不适用 | 已并入 React Router v7 框架模式 |
| [TanStack Start](https://github.com/TanStack/router) | 同上 | `@tanstack/react-start` 1.168.49 / 16.5M | ✅ | 不适用 | — |
| [Astro](https://github.com/withastro/astro) | 62.3k / NOASSERTION（npm MIT）/ 2026-09-05 / 否 | 7.3.1 / 5.1M | ✅（islands） | 不适用（营销页与控制台同一 SPA） | 若未来营销页独立，是 SEO 优选 |
| [Vike](https://github.com/vikejs/vike) | 5.8k / MIT / 2026-09-03 / 否 | 0.4.266 / 93.7k | n/a | 不适用 | 0.x |
| [vite-react-ssg](https://github.com/Daydreamer-riri/vite-react-ssg) | 241 / MIT / 2026-08-03 / 否 | 0.9.2 / 47k；peer `^19.0.0` | ✅ | 不适用（已有自研 `scripts/prerender.mjs`） | 星数低 |

**对码印的建议**：不换路由。分两步：(1) 在 v7 内把 `react-router-dom` import 全部改为 `react-router`（v7 已支持，纯机械替换，可用 codemod/sed 一次完成并跑 typecheck+vitest+e2e）；(2) 择期升 v8（前提 React ≥19.2.7，当前 `react ^19.0.0` 已解析到 19.2.8，满足）。元框架一律不迁。

---

## 13. 国际化 / 无障碍 / SEO 工具

| 候选 | GitHub | npm | R19 | 关系 | 风险 / 备注 |
|---|---|---|---|---|---|
| [i18next](https://github.com/i18next/i18next) + [react-i18next](https://github.com/i18next/react-i18next) | 8.6k / MIT / 2026-09-03；10.0k / MIT / 2026-09-03 | 26.4.2 / 22.0M；17.0.13 / 15.9M | peer `>= 16.8` | 可直接补用（若需英文站） | 当前 `lang="zh-CN"` 单语，暂不需要 |
| [Lingui](https://github.com/lingui/js-lingui) | 5.9k / MIT / 2026-09-04 / 否 | `@lingui/react` 6.6.0 / 1.1M / 22 kB | ✅ peer `^19.0.0` | 备选（编译期提取，体积最小） | — |
| [react-intl（FormatJS）](https://github.com/formatjs/formatjs) | 14.7k / BSD-3-Clause / 2026-09-05 / 否 | 10.1.26 / 3.3M / 180 kB | peer `>=18` | 备选 | — |
| [Paraglide（inlang）](https://github.com/opral/inlang-paraglide-js) | 675 / MIT / 2026-08-27 / 否 | 2.25.0 / 506k | n/a | 不适用 | 生态小 |
| [react-aria](https://github.com/adobe/react-spectrum) | 15.8k / Apache-2.0 / 2026-09-05 / 否 | 3.52.1 / 8.8M / 15.6 MB | ✅ | 不适用（Radix 已提供 a11y 行为） | — |
| [axe-core](https://github.com/dequelabs/axe-core) | 7.5k / **MPL-2.0** / 2026-09-04 / 否 | 4.13.0 / 68.9M / 3.1 MB；`@axe-core/playwright` 4.13.0 / 9.6M | n/a | **可直接补用（devDependency）** | MPL-2.0 对「作为测试工具使用、不修改源码」无传染；WCAG AA 自动化检查首选 |
| [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y) | 3.6k / MIT / 2026-01-06 / 否 | 6.10.2 / 45.9M；最后发布 2024-10-26 | n/a | 备选（仓库当前无 ESLint） | 若选 oxlint，其内置 jsx-a11y 规则集可替代 |
| [pa11y](https://github.com/pa11y/pa11y) | 4.5k / **LGPL-3.0** / 2026-08-28 / 否 | 10.0.0 / 287k | n/a | 不适用（axe 已够） | CLI 工具，LGPL 不影响产品代码，但多一套依赖 |
| [@unhead/react](https://github.com/unjs/unhead) | 1.3k / MIT / 2026-09-05 / 否 | 3.4.0 / 151k / 55 kB；peer `react >=19.2.4` | ✅ | **可直接补用（首选 head 管理）** | 活跃（unjs 组织）；周下载低于 helmet-async 但 React 19 原生 |
| [react-helmet-async](https://github.com/staylor/react-helmet-async) | 2.3k / Apache-2.0 / 2026-03-03 / 否 | 3.0.0 / 4.7M / 102 kB | ✅ peer `^19.0.0` | 备选 | 单人维护 |
| [react-helmet（nfl 原版）](https://github.com/nfl/react-helmet) | 17.5k / MIT / **2023-07-18** / 否 | 6.1.0 / 3.6M；最后发布 **2020-06-08** | peer `>=16.3` | **不用** | 停滞 6 年 |

**对码印的建议**：a11y 把 `@axe-core/playwright` 接进现有 Playwright e2e（每个 golden-path 页跑一次 `AxeBuilder`，阈值 WCAG 2.1 AA），这是把「WCAG AA 验收硬指标」自动化的最低成本方案。SEO：预渲染脚本已产出静态 HTML，`<title>/<meta>` 管理若要抽象，用 `@unhead/react`（React 19.2+ 原生）。国际化暂不引入，产品当前中文单语。

---

## 14. 工程与测试

| 候选 | GitHub | npm | 关系 | 风险 / 备注 |
|---|---|---|---|---|
| [Vite](https://github.com/vitejs/vite) | 82.7k / MIT / 2026-09-05 / 否 | 8.2.2 / 176.3M | **已在用（^8.1.5）** | Vite 8 底层为 [Rolldown](https://github.com/rolldown/rolldown)（13.9k / MIT，1.2.7） |
| [Vitest](https://github.com/vitest-dev/vitest) | 17.1k / MIT / 2026-09-05 / 否 | **5.0.0**（2026-09-03）/ 99.9M | **已在用（^4.1.10）** | [v5.0.0 release](https://github.com/vitest-dev/vitest/releases/tag/v5.0.0)：破坏性变更含 `sequential` 选项移除、locator 表示改对象、inline `expect`；升级前跑全量 vitest |
| [Playwright](https://github.com/microsoft/playwright) | 95.7k / Apache-2.0 / 2026-09-04 / 否 | `@playwright/test` 1.63.0 / 58.4M | **已在用（^1.62.0）** | — |
| [Testing Library React](https://github.com/testing-library/react-testing-library) | 19.6k / MIT / 2026-08-27 / 否 | 16.3.3 / 57.1M；`@testing-library/user-event` 14.6.7 | **已在用** | — |
| [Storybook](https://github.com/storybookjs/storybook) | 91.0k / MIT / 2026-09-05 / 否 | 10.6.0 / 22.6M / 22 MB | 可直接补用（37 个 composite 组件的可视回归） | [Storybook 10 迁移](https://storybook.js.org/docs/releases/migration-guide)：ESM-only、Node 20.19+/22.12+ |
| [Ladle](https://github.com/tajo/ladle) | 3.0k / MIT / 2026-06-28 / 否 | `@ladle/react` 5.1.1 / 341k | 备选（轻量 Storybook 替代，Vite 原生） | 生态小 |
| [Biome](https://github.com/biomejs/biome) | 25.7k / MIT OR Apache-2.0 / 2026-09-05 / 否 | 2.5.12 / 14.4M | 备选（lint+format 一体） | 无 type-aware 规则（推断型） |
| [oxlint](https://github.com/oxc-project/oxc) | 22.6k / MIT / 2026-09-05 / 否 | 1.81.0 / 19.9M；`oxfmt` 0.66.0 / 11.8M | **可直接补用（首选 lint）** | 仓库当前无 lint（AGENTS.md 已说明）；oxlint 零配置、Rust 速度、含 react/jsx-a11y 规则 |
| [ESLint](https://github.com/eslint/eslint) + [typescript-eslint](https://github.com/typescript-eslint/typescript-eslint) | 27.5k / MIT；16.4k / MIT | 10.10.0 / 159.4M；8.69.0 / 87.3M | 备选 | 配置成本高于 oxlint/Biome |
| [Prettier](https://github.com/prettier/prettier) | 52.2k / MIT / 2026-09-05 / 否 | 3.9.6 / 132.4M | 备选（格式化） | 与 oxfmt/Biome 二选一 |
| [Knip](https://github.com/webpro-nl/knip) | 12.2k / ISC / 2026-09-02 / 否 | 6.34.0 / 14.3M | 可直接补用（找未用文件/依赖/导出） | 一次性清理 + CI 门禁 |
| [size-limit](https://github.com/ai/size-limit) | 6.9k / MIT / 2026-07-30 / 否 | 13.0.3 / 1.4M | 可直接补用（首屏 JS 预算门禁） | 配合现有 `scripts/check-preload.mjs` |
| [rollup-plugin-visualizer](https://github.com/btd/rollup-plugin-visualizer) | 2.4k / MIT / 2026-08-14 / 否 | 7.1.1 / 8.1M | 可直接补用（bundle 分析） | Vite 8/Rolldown 兼容性需实测 |
| [MSW](https://github.com/mswjs/msw) | 18.2k / MIT / 2026-07-24 / 否 | 2.15.0 / 21.1M | 可直接补用（vitest 里 mock `/api`） | — |
| [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) | 7.1k / Apache-2.0 / 2026-03-27 / 否 | `@lhci/cli` 0.15.1 / 1.4M | 备选（性能/a11y 分数门禁） | 公司规则 GitHub Actions 禁用，只能本地跑 |
| [vite-plugin-pwa](https://github.com/vite-pwa/vite-plugin-pwa) | 4.3k / MIT / 2026-05-05 / 否 | 1.3.0 / 4.4M | 不适用（当前无离线需求） | — |
| [Husky](https://github.com/typicode/husky) + [lint-staged](https://github.com/lint-staged/lint-staged) | 35.3k / MIT；14.7k / MIT | 9.1.7 / 36.0M；17.5.0 / 29.3M | 可直接补用（本地门禁，契合「本地验证即合并」规则） | — |
| [jsdom](https://github.com/jsdom/jsdom) / [happy-dom](https://github.com/capricorn86/happy-dom) | 21.7k / MIT；4.6k / MIT | 30.0.1 / 98.8M；20.14.0 / 15.9M | 已在用 jsdom 类环境（vitest） | happy-dom 更快但兼容性略低 |

**对码印的建议**：公司规则是「本地验证全绿即合并、Actions 禁用」，因此工程投入应放在**本地门禁**：`oxlint`（补上仓库缺失的 lint，含 a11y 规则）+ `knip`（清死代码）+ `size-limit`（首屏预算）+ `husky/lint-staged`，都是 devDependency、无运行时影响。Storybook 10 可作为 UI 设计师/UX 研究员协作载体（CHARTER 要求前端与设计协作），但优先级低于 a11y 自动化。Vitest 5 升级放到下一个技术债窗口。

---

## 15. 设计资源与字体

| 候选 | 来源 / 许可（已验证） | 关系 | 风险 / 备注 |
|---|---|---|---|
| [shadcn/ui 官方 Figma](https://ui.shadcn.com/docs/figma) | 官方文档页列出社区 Figma kit（各自许可） | 可直接补用 | 需逐个核 kit 作者许可；[tweakcn](https://github.com/jnsahaj/tweakcn)（Apache-2.0）可把 Figma token 转 CSS 变量 |
| [Untitled UI Figma](https://www.untitledui.com/) | 免费版 + 付费 Pro；React 代码 MIT（见 §2） | 备选 | 免费 Figma 组件有限（功能墙） |
| [Radix Colors](https://github.com/radix-ui/colors) | 1.7k / MIT / 2025-12-17；`@radix-ui/colors` 3.0.0 / 3.2M | 可直接补用（12 阶色板生成暗色工作区） | npm 最后发布 2023-10-02，但色板本身稳定 |
| [Geist](https://github.com/vercel/geist-font) | 3.6k / **OFL-1.1** / 2026-07-14；`geist` 1.7.2 / 2.2M | 可直接补用（拉丁/数字） | — |
| [Inter](https://github.com/rsms/inter) | 19.9k / **OFL-1.1** / 2024-11-19；`@fontsource/inter` 5.3.0 / 2.7M | 可直接补用 | 字体已稳定，仓库少更新正常 |
| [思源黑体 Source Han Sans](https://github.com/adobe-fonts/source-han-sans) | 17.2k / GitHub NOASSERTION，[LICENSE.txt](https://github.com/adobe-fonts/source-han-sans/blob/master/LICENSE.txt) = **SIL OFL 1.1** | **可直接补用（中文正文首选）** | OFL 允许随软件嵌入/再分发，禁止单独售卖、改名需去 Reserved Font Name |
| [思源宋体 Source Han Serif](https://github.com/adobe-fonts/source-han-serif) | 9.7k / 同上 OFL 1.1 | 可直接补用（文档预览衬线） | — |
| [Noto Sans CJK](https://github.com/notofonts/noto-cjk) | 4.0k / GitHub NONE（与思源同源，OFL 1.1） | 备选 | 与思源黑体字形同源 |
| [霞鹜文楷 LXGW WenKai](https://github.com/lxgw/LxgwWenKai) | 25.8k / **OFL-1.1** / 2026-08-13；`lxgw-wenkai-webfont` 1.7.0（npm 2023-02-20，MIT 打包） | 可直接补用（标题/品牌装饰） | 正文可读性弱于黑体 |
| [MiSans（小米）](https://hyperos.mi.com/font/) | 厂商自定义协议：[MiSans 字体知识产权许可协议](https://hyperos.mi.com/font-download/MiSans%E5%AD%97%E4%BD%93%E7%9F%A5%E8%AF%86%E4%BA%A7%E6%9D%83%E8%AE%B8%E5%8F%AF%E5%8D%8F%E8%AE%AE.pdf)：免版税、**可撤销**、须在软件中注明、**不得改编/二次开发、不得单独再分发** | 不适用（Web 字体子集化=改编，且可撤销） | 非 OFL |
| [HarmonyOS Sans（华为）](https://developer.huawei.com/consumer/cn/doc/design-guides/font-0000001157868583) | 厂商自定义协议（页面为 JS 渲染，本轮未抓到条款原文）**[未核验]** | 不适用 | 条款未核验前不引入 |
| [阿里巴巴普惠体](https://fonts.alibabagroup.com/) | 厂商自定义协议（页面 JS 渲染，本轮未抓到条款原文）**[未核验]** | 不适用 | 同上 |
| [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono) | 13.0k / **OFL-1.1**；`@fontsource/jetbrains-mono` 5.3.0 / 965k | 可直接补用（代码高亮等宽） | — |
| [Maple Mono](https://github.com/subframe7536/maple-font) | 28.7k / **OFL-1.1** / 2026-09-03 | 备选（中英等宽 2:1，含 CJK） | 无 fontsource 包 |
| [cn-font-split](https://github.com/KonghaYao/cn-font-split) | 1.2k / Apache-2.0 / 2026-06-12；7.4.3 | **可直接补用（中文字体分包必备）** | 思源黑体单字重 ~16 MB，必须按 unicode-range 分包 |
| [Fontsource](https://github.com/fontsource/fontsource) | 6.1k / MIT（打包脚本）；字体各自 OFL | 可直接补用（npm 自托管字体） | 避免依赖 Google Fonts 在国内的可达性 |

**对码印的建议**：中文正文 = 思源黑体（OFL-1.1）经 `cn-font-split` 分包自托管；拉丁/数字 = Geist 或 Inter（OFL-1.1）；等宽 = JetBrains Mono。三者许可证一致（OFL），可随产品分发无附加义务。MiSans/HarmonyOS Sans/阿里普惠体虽「免费商用」，但为厂商单方协议（MiSans 明确可撤销、禁改编、禁再分发），Web 子集化嵌入存在解释风险，**不用**。设计侧以 shadcn Figma kit + tweakcn 校对 `tokens.css` 对比度（WCAG AA ≥4.5:1）。

---

## 附录 A. 本轮新增的重大上游变化（老板需知）

1. **React Router v8**（2026-06-17）删除 `react-router-dom` 包，我们 102 处 import 需迁到 `react-router`。证据：[changelog v8.0.0](https://reactrouter.com/changelog)、npm `react-router-dom` dist-tags latest=7.18.3。
2. **TanStack Table v9**（latest 9.2.4）API 变化：`useReactTable`→`useTable`、显式 `features`。证据：[迁移指南](https://tanstack.com/table/latest/docs/framework/react/guide/migrating)。
3. **Vitest 5.0.0**（2026-09-03）发布。证据：[release](https://github.com/vitest-dev/vitest/releases/tag/v5.0.0)。
4. **CodeMirror 全部仓库迁出 GitHub**（2026-04-15 归档），源码在 code.haverbeke.berlin，npm 持续发布。证据：`gh api repos/codemirror/dev` archived=true；[README](https://github.com/codemirror/dev)。
5. **Base UI 包名变更**：`@base-ui-components/react` → `@base-ui/react`（npm deprecated 提示）。证据：[releases](https://base-ui.com/react/overview/releases)。
6. **Origin UI → coss（AGPL-3.0）**：`origin-space/originui` 已重定向到 `cosscom/coss`。证据：[LICENSE](https://github.com/cosscom/coss/blob/main/LICENSE)。
7. **dnd-kit 新代 `@dnd-kit/react` 0.5.0**（2026-09-05 发布，React 19），旧 `@dnd-kit/core` 自 2024-12 无发布。

## 附录 B. 数据来源与复现

- GitHub：`gh api repos/<owner>/<repo> --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at,archived:.archived}'`
- npm 元数据：`https://registry.npmjs.org/<pkg>`（`dist-tags.latest`、`versions[latest].license/peerDependencies/dist.unpackedSize`、`time`）
- npm 周下载：`https://api.npmjs.org/downloads/point/last-week/<pkg>`（窗口 2026-08-23 ~ 2026-08-29）
- 未在本文表格中单独列出但已采集的对照项（均 MIT/ISC，供追问）：sonner 2.0.8、cva 0.7.1、tailwind-merge 3.6.0、clsx 2.1.1、vaul 1.1.2、cmdk 1.1.1、react-resizable-panels 4.12.3、embla-carousel-react 8.6.0、input-otp 1.5.0、next-themes 0.4.6、qrcode.react 4.2.0、mermaid 11.17.2、@number-flow/react 0.6.2、react-error-boundary 6.1.5、usehooks-ts 3.1.1、ky 2.1.0、axios 1.20.0、react-use 17.6.1（Unlicense）、pdf-lib 1.17.1（npm 最后发布 2021-11-06）、html2canvas 1.4.1（2022-01-22）。

## 附录 C. 全部链接索引

### 官方文档 / 兼容性 / 许可证证据
- shadcn/ui Vite 安装：https://ui.shadcn.com/docs/installation/vite
- shadcn/ui Tailwind v4：https://ui.shadcn.com/docs/tailwind-v4
- shadcn/ui changelog：https://ui.shadcn.com/docs/changelog
- shadcn/ui charts：https://ui.shadcn.com/docs/components/chart
- shadcn/ui form：https://ui.shadcn.com/docs/components/form
- shadcn/ui Figma：https://ui.shadcn.com/docs/figma
- Base UI releases：https://base-ui.com/react/overview/releases
- React Router changelog：https://reactrouter.com/changelog
- TanStack Table v9 迁移：https://tanstack.com/table/latest/docs/framework/react/guide/migrating
- Vitest 5.0.0 release：https://github.com/vitest-dev/vitest/releases/tag/v5.0.0
- Vitest 迁移指南：https://vitest.dev/guide/migration
- Storybook 10 迁移：https://storybook.js.org/docs/releases/migration-guide
- Ant Design React 19 兼容：https://ant.design/docs/react/v5-for-19
- daisyUI v5 升级：https://daisyui.com/docs/upgrade/
- Magic UI Tailwind v4：https://magicui.design/docs/tailwind-v4
- Kibo UI Setup：https://www.kibo-ui.com/docs/setup
- Motion Primitives：https://motion-primitives.com/docs
- Untitled UI React：https://www.untitledui.com/react ；LICENSE：https://github.com/untitleduico/react/blob/main/LICENSE
- coss README：https://github.com/cosscom/coss ；LICENSE（AGPL-3.0）：https://github.com/cosscom/coss/blob/main/LICENSE
- Aceternity UI：https://ui.aceternity.com/ ；pricing：https://ui.aceternity.com/pricing
- cult-ui：https://www.cult-ui.com/docs
- GSAP 许可：https://gsap.com/licensing/
- Tiptap pricing：https://tiptap.dev/pricing
- AG Grid LICENSE.txt：https://github.com/ag-grid/ag-grid/blob/latest/LICENSE.txt
- CodeMirror 新地址：https://code.haverbeke.berlin/codemirror/dev
- 思源黑体 LICENSE（OFL 1.1）：https://github.com/adobe-fonts/source-han-sans/blob/master/LICENSE.txt
- MiSans 许可协议：https://hyperos.mi.com/font-download/MiSans%E5%AD%97%E4%BD%93%E7%9F%A5%E8%AF%86%E4%BA%A7%E6%9D%83%E8%AE%B8%E5%8F%AF%E5%8D%8F%E8%AE%AE.pdf
- SIL OFL 1.1：https://scripts.sil.org/OFL

### GitHub 仓库（按章节）
- §1：https://github.com/shadcn-ui/ui · https://github.com/radix-ui/primitives · https://github.com/mui/base-ui · https://github.com/adobe/react-spectrum · https://github.com/tailwindlabs/headlessui · https://github.com/chakra-ui/ark · https://github.com/mantinedev/mantine · https://github.com/chakra-ui/chakra-ui · https://github.com/heroui-inc/heroui · https://github.com/saadeghi/daisyui · https://github.com/ant-design/ant-design · https://github.com/arco-design/arco-design · https://github.com/Tencent/tdesign-react · https://github.com/DouyinFE/semi-design · https://github.com/mui/material-ui
- §2：https://github.com/magicuidesign/magicui · https://github.com/haydenbleasel/kibo · https://github.com/ibelick/motion-primitives · https://github.com/untitleduico/react · https://github.com/cosscom/coss · https://github.com/nolly-studio/cult-ui · https://github.com/jnsahaj/tweakcn · https://github.com/birobirobiro/awesome-shadcn-ui · https://github.com/tremorlabs/tremor
- §3：https://github.com/lucide-icons/lucide · https://github.com/phosphor-icons/react · https://github.com/tabler/tabler-icons · https://github.com/tailwindlabs/heroicons · https://github.com/radix-ui/icons · https://github.com/iconify/iconify · https://github.com/Remix-Design/RemixIcon · https://github.com/bytedance/IconPark · https://github.com/hugeicons/hugeicons-react · https://github.com/react-icons/react-icons
- §4：https://github.com/motiondivision/motion · https://github.com/pmndrs/react-spring · https://github.com/formkit/auto-animate · https://github.com/greensock/GSAP · https://github.com/airbnb/lottie-web · https://github.com/LottieFiles/dotlottie-web · https://github.com/Wombosvideo/tw-animate-css · https://github.com/reactjs/react-transition-group · https://github.com/barvian/number-flow
- §5：https://github.com/recharts/recharts · https://github.com/plouc/nivo · https://github.com/airbnb/visx · https://github.com/apache/echarts · https://github.com/hustcc/echarts-for-react · https://github.com/chartjs/Chart.js · https://github.com/reactchartjs/react-chartjs-2 · https://github.com/d3/d3 · https://github.com/observablehq/plot · https://github.com/antvis/G2
- §6：https://github.com/react-hook-form/react-hook-form · https://github.com/react-hook-form/resolvers · https://github.com/TanStack/form · https://github.com/colinhacks/zod · https://github.com/fabian-hiller/valibot · https://github.com/arktypeio/arktype · https://github.com/standard-schema/standard-schema · https://github.com/jaredpalmer/formik · https://github.com/jquense/yup
- §7：https://github.com/TanStack/table · https://github.com/TanStack/virtual · https://github.com/bvaughn/react-window · https://github.com/petyosi/react-virtuoso · https://github.com/ag-grid/ag-grid · https://github.com/mui/mui-x · https://github.com/glideapps/glide-data-grid · https://github.com/adazzle/react-data-grid
- §8：https://github.com/remarkjs/react-markdown · https://github.com/remarkjs/remark-gfm · https://github.com/shikijs/shiki · https://github.com/vercel/streamdown · https://github.com/mdx-js/mdx · https://github.com/ueberdosis/tiptap · https://github.com/facebook/lexical · https://github.com/udecode/plate · https://github.com/TypeCellOS/BlockNote · https://github.com/Milkdown/milkdown · https://github.com/codemirror/dev · https://github.com/uiwjs/react-codemirror · https://github.com/microsoft/monaco-editor · https://github.com/suren-atoyan/monaco-react · https://github.com/uiwjs/react-md-editor · https://github.com/Vanessa219/vditor
- §9：https://github.com/date-fns/date-fns · https://github.com/iamkun/dayjs · https://github.com/gpbl/react-day-picker · https://github.com/fullcalendar/temporal-polyfill · https://github.com/js-temporal/temporal-polyfill · https://github.com/moment/luxon · https://github.com/moment/moment
- §10：https://github.com/react-dropzone/react-dropzone · https://github.com/clauderic/dnd-kit · https://github.com/atlassian/pragmatic-drag-and-drop · https://github.com/mozilla/pdf.js · https://github.com/wojtekmaj/react-pdf · https://github.com/embedpdf/embed-pdf-viewer · https://github.com/diegomura/react-pdf · https://github.com/VolodymyrBaydalka/docxjs · https://github.com/mwilliamson/mammoth.js · https://github.com/dolanmiu/docx · https://github.com/transloadit/uppy · https://github.com/pqina/filepond · https://github.com/Stuk/jszip · https://github.com/eligrey/FileSaver.js
- §11：https://github.com/TanStack/query · https://github.com/pmndrs/zustand · https://github.com/pmndrs/jotai · https://github.com/reduxjs/redux-toolkit · https://github.com/vercel/swr · https://github.com/pmndrs/valtio · https://github.com/statelyai/xstate · https://github.com/47ng/nuqs · https://github.com/openapi-ts/openapi-typescript · https://github.com/orval-labs/orval
- §12：https://github.com/remix-run/react-router · https://github.com/TanStack/router · https://github.com/vercel/next.js · https://github.com/remix-run/remix · https://github.com/withastro/astro · https://github.com/vikejs/vike · https://github.com/Daydreamer-riri/vite-react-ssg
- §13：https://github.com/i18next/i18next · https://github.com/i18next/react-i18next · https://github.com/lingui/js-lingui · https://github.com/formatjs/formatjs · https://github.com/opral/inlang-paraglide-js · https://github.com/dequelabs/axe-core · https://github.com/jsx-eslint/eslint-plugin-jsx-a11y · https://github.com/pa11y/pa11y · https://github.com/unjs/unhead · https://github.com/staylor/react-helmet-async · https://github.com/nfl/react-helmet
- §14：https://github.com/vitejs/vite · https://github.com/rolldown/rolldown · https://github.com/vitest-dev/vitest · https://github.com/microsoft/playwright · https://github.com/testing-library/react-testing-library · https://github.com/storybookjs/storybook · https://github.com/tajo/ladle · https://github.com/biomejs/biome · https://github.com/oxc-project/oxc · https://github.com/eslint/eslint · https://github.com/typescript-eslint/typescript-eslint · https://github.com/prettier/prettier · https://github.com/webpro-nl/knip · https://github.com/ai/size-limit · https://github.com/btd/rollup-plugin-visualizer · https://github.com/mswjs/msw · https://github.com/GoogleChrome/lighthouse-ci · https://github.com/vite-pwa/vite-plugin-pwa · https://github.com/typicode/husky · https://github.com/lint-staged/lint-staged · https://github.com/jsdom/jsdom · https://github.com/capricorn86/happy-dom
- §15：https://github.com/radix-ui/colors · https://github.com/vercel/geist-font · https://github.com/rsms/inter · https://github.com/adobe-fonts/source-han-sans · https://github.com/adobe-fonts/source-han-serif · https://github.com/notofonts/noto-cjk · https://github.com/lxgw/LxgwWenKai · https://github.com/JetBrains/JetBrainsMono · https://github.com/subframe7536/maple-font · https://github.com/KonghaYao/cn-font-split · https://github.com/fontsource/fontsource

### 体积查询入口
- bundlephobia：`https://bundlephobia.com/package/<pkg>@<version>`（各表「体积」列已给出对应链接）
- pkg-size：`https://pkg-size.dev/<pkg>`

---

实查日期：2026-09-05（UTC）。本文件只做研究记录，不含代码变更。
