# 前端生态选型研究 2026

- 实查日期：**2026-09-05（UTC）**（第一批 §1–§15、第二批 §16–§23、第三批 §24–§34 同日实查）
- 角色：前端生态研究员（Company OS 职能员工）
- 范围：通用前端开源生态，不绑定具体产品。第一批 §1–§15 的「关系」列与「对码印的建议」段落是以一个参考项目（码印 / SoftCopyrightAgent frontend）为样本写成的历史结论，保留供对照；第二批 §16–§23 起为产品无关的通用推荐。
- 方法：全部数字为一手实查——GitHub 元数据用 `gh api repos/<owner>/<repo>`（stars / SPDX / pushed_at / archived），npm 用 registry（`https://registry.npmjs.org/<pkg>`：latest 版本、license、peerDependencies、unpackedSize）与下载 API（`https://api.npmjs.org/downloads/point/last-week/<pkg>`，统计窗口 2026-08-23 ~ 08-29）；React 19 / Tailwind v4 支持以官方文档 / changelog / peerDependencies 为据。采集脚本第一批 219 个候选、第二批 125 条（121 个新增 + 4 个对照/交叉引用），逐条记录。
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

## 第二批（§16–§23）说明

- 实查日期：**2026-09-05（UTC）**，采集脚本 `scripts/items_round2.py`，原始数据 `data/candidates-round2-2026-09-05.json`（125 条，其中 4 条为对照/交叉引用，不重复计数：Stitches、Shoelace legacy、Astro、ECharts）。周下载窗口为采集时 API 返回的 last-week。
- 本批**不绑定任何具体产品**，「推荐」列以通用场景为准，不再使用第一批的「关系」列。
- 「GitHub」列格式：stars / GitHub SPDX / 最近 push / archived。「npm」列格式：latest / 周下载 / npm license / **unpacked**（安装体积，≠ bundle 体积；bundle 体积见「体积」列 bundlephobia / pkg-size 链接，按需实时计算，本轮未逐个抓值）。
- 「R19」= React peerDependencies 声明（`—` 表示无 react peer，通常是框架无关库）；`✅` 另附官方文档证据。

---

## 16. CSS-in-JS / 零运行时 CSS / CSS 工具链

| 候选 | GitHub | npm | R19 | 体积 | 风险 / 备注 |
|---|---|---|---|---|---|
| [Panda CSS](https://github.com/chakra-ui/panda) | 6.2k / MIT / 2026-09-05 / no | `@pandacss/dev` 1.12.1 / 428k / MIT / 856k | — | [bp](https://bundlephobia.com/package/@pandacss/dev@1.12.1) | 零运行时，构建期生成原子 CSS；Chakra 团队维护 [已验证] |
| [vanilla-extract](https://github.com/vanilla-extract-css/vanilla-extract) | 10.4k / MIT / 2026-08-27 / no | `@vanilla-extract/css` 1.21.2 / 3.0M / MIT / 389k | — | [bp](https://bundlephobia.com/package/@vanilla-extract/css@1.21.2) | 零运行时、类型安全；需 bundler 插件 [已验证] |
| [StyleX](https://github.com/facebook/stylex) | 10.2k / MIT / 2026-09-05 / no | `@stylexjs/stylex` 0.19.0 / 1.9M / MIT / 334k | — | [bp](https://bundlephobia.com/package/@stylexjs/stylex@0.19.0) | Meta 出品，**仍 0.x**（最近发版 2026-06-16）；API 未承诺稳定 [已验证] |
| [Pigment CSS](https://github.com/mui/pigment-css) | 1.1k / MIT / 2026-06-06 / no | `@pigment-css/react` 0.0.31 / 32k / MIT / 862k | peer ^17‖^18‖^19 | [bp](https://bundlephobia.com/package/@pigment-css/react@0.0.31) | MUI 团队零运行时方案，**0.0.x**，近 3 个月无 push [已验证] |
| [Linaria](https://github.com/callstack/linaria) | 12.3k / MIT / 2026-08-10 / no | `@linaria/core` 8.2.0 / 594k / MIT / 25k | — | [bp](https://bundlephobia.com/package/@linaria/core@8.2.0) | 零运行时 CSS-in-JS 老牌；底层已抽为 wyw-in-js [已验证] |
| [wyw-in-js](https://github.com/Anber/wyw-in-js) | 323 / MIT / 2026-09-05 / no | `@wyw-in-js/transform` 2.5.1 / 168k / MIT / 5.5M | — | [pkg](https://pkg-size.dev/@wyw-in-js/transform) | Linaria/Pigment 共用编译核心；主要单人维护 [已验证] |
| [Emotion](https://github.com/emotion-js/emotion) | 18.0k / MIT / 2026-08-28 / no | `@emotion/react` 11.14.0 / 21.2M / MIT / 817k | peer >=16.8 | [bp](https://bundlephobia.com/package/@emotion/react@11.14.0) | 运行时方案；latest 发布于 2024-12-09，近 21 个月无新版（仓库仍有 push）[已验证] |
| [styled-components](https://github.com/styled-components/styled-components) | 41.1k / MIT / 2026-09-05 / no | 6.5.3 / 11.5M / MIT / 2.1M | peer >=16.8 | [bp](https://bundlephobia.com/package/styled-components@6.5.3) | 运行时方案；RSC 不友好（官方 [FAQ](https://styled-components.com/docs/faqs)）[已验证 npm/GitHub；RSC 说明为官方文档] |
| [Restyle](https://github.com/souporserious/restyle) | 450 / MIT / 2026-05-19 / no | `restyle` 3.4.3 / 956 / MIT / 305k | peer >=19.2.6 | [bp](https://bundlephobia.com/package/restyle@3.4.3) | RSC 友好零配置方案，社区小 [已验证] |
| [UnoCSS](https://github.com/unocss/unocss) | 18.9k / **NOASSERTION** / 2026-09-05 / no | `unocss` 66.10.0 / 478k / MIT / 18k | — | [bp](https://bundlephobia.com/package/unocss@66.10.0) | 原子 CSS 引擎，Tailwind 替代；GitHub 未识别许可证，npm 为 MIT [已验证] |
| [Tailwind Variants](https://github.com/heroui-inc/tailwind-variants) | 3.3k / MIT / 2026-08-18 / no | 3.3.1 / 3.8M / MIT / 332k | tw peer `*` | [bp](https://bundlephobia.com/package/tailwind-variants@3.3.1) | 变体组合工具，声明 tailwindcss peer `*`（TWv4 兼容由 peer 推断）[已验证] |
| [Lightning CSS](https://github.com/parcel-bundler/lightningcss) | 7.7k / **MPL-2.0** / 2026-09-05 / no | 1.33.0 / 142.4M / MPL-2.0 / 514k | — | n/a（构建工具） | Rust CSS 转换/压缩器，Tailwind v4 底层依赖之一；MPL-2.0 为文件级 copyleft，作为构建工具使用无传染 [已验证] |
| [PostCSS](https://github.com/postcss/postcss) | 29.0k / MIT / 2026-09-03 / no | 8.5.28 / 280.1M / MIT / 218k | — | n/a | 事实标准 CSS 处理管线 [已验证] |
| [Sass (dart-sass)](https://github.com/sass/dart-sass) | 4.2k / MIT / 2026-09-04 / no | `sass` 1.104.0 / 32.4M / MIT / 5.9M | — | n/a | 预处理器；仍活跃 [已验证] |
| [Open Props](https://github.com/argyleink/open-props) | 5.5k / MIT / 2026-08-11 / no | 1.7.23 / 27k / MIT / 1.3M | — | [bp](https://bundlephobia.com/package/open-props@1.7.23) | CSS 变量设计令牌集；npm 最近发版 2026-01-31 [已验证] |
| [Tokenami](https://github.com/tokenami/tokenami) | 1.0k / MIT / 2026-09-04 / no | `@tokenami/dev` 0.0.76 / 75 / MIT / 266k | — | — | **npm latest 标记 deprecated**，周下载 75 → 不建议 [已验证] |
| Stitches（对照） | 7.8k / MIT / 2025-02-10 / **archived** | `@stitches/react` 1.2.8 / 1.4M / MIT / 521k | peer >=16.3 | — | 仓库已归档，仅作对照，禁止新项目引入 [已验证] |

**一句话推荐**：新项目要零运行时且类型安全，选 **vanilla-extract**（稳定 1.x、3.0M 周下载）或 **Panda CSS**（原子化 + 主题令牌）；StyleX / Pigment 仍是 0.x，观察不采用；运行时 Emotion / styled-components 只在维护旧项目时保留；原子 CSS 若不想绑 Tailwind，UnoCSS 是唯一量级相当的替代。

---

## 17. 构建工具 / 打包器 / 编译器

| 候选 | GitHub | npm | 体积 | 风险 / 备注 |
|---|---|---|---|---|
| [Rspack](https://github.com/web-infra-dev/rspack) | 12.9k / MIT / 2026-09-05 / no | `@rspack/core` 2.2.2 / 9.0M / MIT / 1.7M | n/a | Rust 版 webpack 兼容打包器，2.x 已 GA；字节维护 [已验证] |
| [Rsbuild](https://github.com/web-infra-dev/rsbuild) | 3.4k / MIT / 2026-09-05 / no | `@rsbuild/core` 2.2.3 / 1.7M / MIT / 4.8M | n/a | Rspack 之上的开箱即用应用构建器（对标 Vite 应用层）[已验证] |
| [Rslib](https://github.com/web-infra-dev/rslib) | 1.0k / MIT / 2026-09-04 / no | `@rslib/core` 1.0.0 / 312k / MIT / 409k | n/a | 库打包器，**1.0.0 刚发布**（2026-09-03）[已验证] |
| [Turbopack](https://github.com/vercel/next.js/tree/canary/turbopack) | (next.js 仓) 142.1k / MIT / 2026-09-05 / no | 无独立 npm 包 | n/a | 源码在 `vercel/next.js/turbopack` 目录，只随 Next.js 分发，**不能独立使用** [已验证：目录存在；独立使用状态为推断] |
| [Farm](https://github.com/farm-fe/farm) | 5.6k / MIT / 2026-06-14 / no | `@farmfe/core` 1.7.11 / 6.2k / MIT / 2.6M | n/a | Rust 构建器；npm latest 2025-08-04，仓库近 3 个月无 push，**有停滞迹象**（2.0.0-beta 在 beta tag）[已验证] |
| [esbuild](https://github.com/evanw/esbuild) | 40.0k / MIT / 2026-08-09 / no | 0.28.2 / 275.2M / MIT / 147k | n/a | Go 打包/转译器；长期 0.x 但极稳定 [已验证] |
| [webpack](https://github.com/webpack/webpack) | 66.0k / MIT / 2026-09-05 / no | 5.110.3 / 56.4M / MIT / 9.8M | n/a | 仍活跃发版 [已验证] |
| [Parcel](https://github.com/parcel-bundler/parcel) | 44.0k / MIT / 2026-09-05 / no | 2.16.4 / 354k / MIT / 44k | n/a | 零配置；npm latest 2026-02-02，发版频率放缓 [已验证] |
| [Rollup](https://github.com/rollup/rollup) | 26.3k / **NOASSERTION** / 2026-09-04 / no | 4.63.1 / 124.6M / MIT / 2.9M | n/a | GitHub 未识别许可证，npm MIT；Vite 生产构建底层 [已验证] |
| [tsdown](https://github.com/rolldown/tsdown) | 4.3k / MIT / 2026-09-03 / no | 0.23.0 / 5.7M / MIT / 182k | n/a | 基于 Rolldown 的库打包器，VoidZero 系；0.x [已验证] |
| [tsup](https://github.com/egoist/tsup) | 11.3k / MIT / 2026-07-20 / no | 8.5.1 / 8.5M / MIT / 390k | n/a | npm latest 2025-11-12；官方 README 已推荐迁到 tsdown（[README](https://github.com/egoist/tsup)）[已验证 npm/GitHub；README 建议为页面证据] |
| [SWC](https://github.com/swc-project/swc) | 34.2k / Apache-2.0 / 2026-09-05 / no | `@swc/core` 1.16.2 / 43.0M / Apache-2.0 / 134k | n/a | Rust 转译器，Next.js 默认 [已验证] |
| [Babel](https://github.com/babel/babel) | 44.0k / MIT / 2026-09-04 / no | `@babel/core` 8.0.1 / 181.3M / MIT / 545k | n/a | **8.0 已发布**（latest 8.0.1，2026-06-17）[已验证] |
| [Mako](https://github.com/umijs/mako) | 2.5k / MIT / 2026-09-04 / no | `@umijs/mako` 0.11.15 / 79k / MIT / 103k | n/a | 蚂蚁 Rust 打包器，npm latest 2025-11-06 [已验证] |
| [Bun](https://github.com/oven-sh/bun) | 95.9k / **NOASSERTION** / 2026-09-05 / no | `bun` 1.4.2 / 3.5M / MIT / 20k | n/a | 运行时+打包器；[LICENSE.md](https://github.com/oven-sh/bun/blob/main/LICENSE.md) 声明 Bun 本身 MIT、静态链接 JavaScriptCore 为 LGPL-2 [已验证] |
| [Vite Plus](https://github.com/voidzero-dev/vite-plus) | 5.7k / MIT / 2026-09-05 / no | `vite-plus` 0.3.0 / 1.1M / MIT / 2.1M | n/a | VoidZero 统一工具链（Vite/Vitest/Oxlint/tsdown 入口），**0.x** [已验证] |
| [unplugin](https://github.com/unjs/unplugin) | 3.6k / MIT / 2026-07-31 / no | 3.3.0 / 60.7M / MIT / 80k | n/a | 跨 bundler 插件抽象层 [已验证] |

（Vite / Vitest / Oxlint 已在 §14，不重复。）

**一句话推荐**：应用构建默认 **Vite**（§14）；需 webpack 生态兼容或超大仓，选 **Rspack/Rsbuild**（2.x GA、MIT）；库打包 **tsdown**（tsup 官方指向的后继）或刚 1.0 的 **Rslib**；Farm 与 Mako 停滞/小众不选；Turbopack 只能随 Next.js 使用。

---

## 18. 包管理 / monorepo / 发布与运行时管理

| 候选 | GitHub | npm | 风险 / 备注 |
|---|---|---|---|
| [pnpm](https://github.com/pnpm/pnpm) | 36.4k / MIT / 2026-09-05 / no | 12.3.4 / 177.6M / MIT / 3.9M | 12.x；默认 workspace 支持 [已验证] |
| [npm CLI](https://github.com/npm/cli) | 10.1k / **NOASSERTION** / 2026-09-03 / no | `npm` 12.0.2 / 15.6M / **Artistic-2.0** / 12.4M | Artistic-2.0（OSI 认可），仅工具使用无影响 [已验证] |
| [Yarn Berry](https://github.com/yarnpkg/berry) | 8.1k / BSD-2-Clause / 2026-08-04 / no | `@yarnpkg/cli` 4.18.0 / 75k / BSD-2-Clause / 21k | npm 下载低因多经 corepack 分发 [已验证；分发路径为推断] |
| [Turborepo](https://github.com/vercel/turborepo) | 31.1k / MIT / 2026-09-05 / no | `turbo` 2.10.12 / 23.5M / MIT / 58k | 任务编排 + 远程缓存（远程缓存可自托管）[已验证] |
| [Nx](https://github.com/nrwl/nx) | 29.3k / MIT / 2026-09-05 / no | `nx` 23.2.0 / 10.6M / MIT / 18.3M | 核心 MIT；Nx Cloud 为商业服务（[定价](https://nx.dev/pricing)）[已验证；商业边界为官网页面] |
| [Lerna](https://github.com/lerna/lerna) | 36.1k / MIT / 2026-09-03 / no | 10.0.1 / 1.9M / MIT / 609k | 已由 Nx 团队维护，10.x [已验证] |
| [moon](https://github.com/moonrepo/moon) | 4.1k / MIT / 2026-09-04 / no | `@moonrepo/cli` 2.5.4 / 266k / MIT / 8k | Rust 任务系统，多语言 [已验证] |
| [Changesets](https://github.com/changesets/changesets) | 12.4k / MIT / 2026-09-04 / no | `@changesets/cli` 3.0.2 / 4.7M / MIT / 88k | 版本与 changelog 管理事实标准；3.x [已验证] |
| [syncpack](https://github.com/JamieMason/syncpack) | 2.1k / MIT / 2026-08-09 / no | 15.3.3 / 2.5M / MIT / 69k | monorepo 依赖版本对齐 [已验证] |
| [Verdaccio](https://github.com/verdaccio/verdaccio) | 17.9k / MIT / 2026-09-05 / no | 6.10.2 / 668k / MIT / 1.1M | 私有 npm registry [已验证] |
| [corepack](https://github.com/nodejs/corepack) | 3.8k / MIT / 2026-09-04 / no | 0.36.0 / 5.2M / MIT / 607k | Node 官方包管理器版本钉定 [已验证] |
| [publint](https://github.com/publint/publint) | 1.3k / MIT / 2026-09-02 / no | 0.3.24 / 1.3M / MIT / 117k | 发包前 package.json/exports 校验 [已验证] |
| [are-the-types-wrong](https://github.com/arethetypeswrong/arethetypeswrong.github.io) | 1.6k / MIT / 2026-07-09 / no | `@arethetypeswrong/cli` 0.18.5 / 630k / MIT / 59k | 类型导出校验 [已验证] |
| [Deno](https://github.com/denoland/deno) | 108.4k / MIT / 2026-09-04 / no | — | 运行时；npm 无主包 [已验证] |
| [Volta](https://github.com/volta-cli/volta) | 13.1k / **NOASSERTION** / **2025-11-15** / no | — | 近 10 个月无 push，**停滞** [已验证] |
| [fnm](https://github.com/Schniz/fnm) | 26.8k / **GPL-3.0** / 2026-07-24 / no | — | Node 版本管理器，GPL-3.0 仅影响修改分发工具本身 [已验证] |

**一句话推荐**：**pnpm + Turborepo + Changesets** 是当前最低摩擦的 monorepo 组合（全 MIT、下载量领先）；需要代码生成/插件体系再上 Nx（核心 MIT，Cloud 收费）；发库前加 **publint + are-the-types-wrong**；Node 版本管理用 fnm 或 corepack，Volta 已停滞。

---

## 19. Web Components 与框架对照

| 候选 | GitHub | npm | R19 | 风险 / 备注 |
|---|---|---|---|---|
| [Lit](https://github.com/lit/lit) | 21.8k / BSD-3-Clause / 2026-09-03 / no | `lit` 3.3.3 / 7.4M / BSD-3-Clause / 106k | — | Google；npm latest 2026-05-14 [已验证] |
| `@lit/react` | (同 lit 仓) | 1.0.8 / 3.7M / BSD-3-Clause / 149k | — | 将 WC 包装为 React 组件；npm 2025-07-11 [已验证 npm] |
| [Stencil](https://github.com/stenciljs/core) | 13.1k / **NOASSERTION** / 2026-09-05 / no | `@stencil/core` 4.44.2 / 1.4M / MIT / 23.1M | — | Ionic 团队 WC 编译器；GitHub 未识别许可证 [已验证] |
| [Web Awesome](https://github.com/shoelace-style/webawesome) | 1.3k / MIT / 2026-09-03 / no | `@awesome.me/webawesome` 3.12.0 / 2.3M / MIT / 16.3M | — | Shoelace 后继；**有 Pro 付费层**（GitHub 描述"Upgrade to Pro"）[已验证] |
| Shoelace（legacy，对照） | 13.8k / MIT / 2026-05-14 / **archived** | `@shoelace-style/shoelace` 2.20.1 / 144k / MIT / 8.4M | — | 仓库归档，已迁 Web Awesome [已验证] |
| [FAST](https://github.com/microsoft/fast) | 9.7k / **NOASSERTION** / 2026-09-03 / no | `@microsoft/fast-element` 3.0.2 / 261k / MIT / 3.3M | — | 微软 WC 基础库 [已验证] |
| [Preact](https://github.com/preactjs/preact) | 38.9k / MIT / 2026-09-05 / no | 10.29.8 / 31.8M / MIT / 1.6M | n/a | 3 kB React 替代 [已验证] |
| [Solid](https://github.com/solidjs/solid) | 36.0k / MIT / 2026-09-05 / no | `solid-js` 1.9.15 / 4.0M / MIT / 1.1M | n/a | 细粒度响应式 [已验证] |
| [Svelte](https://github.com/sveltejs/svelte) | 88.0k / MIT / 2026-09-05 / no | 5.57.0 / 5.8M / MIT / 2.9M | n/a | Svelte 5 runes [已验证] |
| [Vue](https://github.com/vuejs/core) | 54.3k / MIT / 2026-09-05 / no | 3.5.42 / 15.6M / MIT / 2.5M | n/a | [已验证] |
| [Qwik](https://github.com/QwikDev/qwik) | 22.1k / MIT / 2026-09-04 / no | `@builder.io/qwik` 1.20.0 / 48k / MIT / 20.5M | n/a | 下载量最低的一线框架 [已验证] |
| [Angular](https://github.com/angular/angular) | 101.0k / MIT / 2026-09-04 / no | `@angular/core` 22.1.5 / 6.0M / MIT / 7.0M | n/a | [已验证] |
| [HTMX](https://github.com/bigskysoftware/htmx) | 49.4k / **NOASSERTION** / 2026-09-04 / no | `htmx.org` 2.0.10 / 253k / **0BSD** / 884k | n/a | 0BSD 为无条件许可 [已验证] |
| [Alpine.js](https://github.com/alpinejs/alpine) | 31.9k / MIT / 2026-09-04 / no | 3.17.1 / 737k / MIT / 689k | n/a | [已验证] |
| Astro（对照，见 §12） | 62.3k / **NOASSERTION** / 2026-09-05 / no | 7.3.1 / 5.1M / MIT / 3.0M | n/a | 仅更新数据：latest 已到 7.3.1 [已验证] |

**一句话推荐**：跨框架共享组件用 **Lit**（BSD-3，配 `@lit/react` 接入 React）；现成 WC 组件库只剩 Web Awesome（注意 Pro 功能墙，Shoelace 已归档）；框架层 React 之外，Svelte 5 / Vue 3.5 / Solid 均健康，Qwik 采用度最低。

---

## 20. 3D / Canvas / 游戏 / 白板

| 候选 | GitHub | npm | R19 | 体积 | 风险 / 备注 |
|---|---|---|---|---|---|
| [three.js](https://github.com/mrdoob/three.js) | 115.2k / MIT / 2026-09-05 / no | `three` 0.185.1 / 15.2M / MIT / 23.2M | — | [bp](https://bundlephobia.com/package/three@0.185.1) | 月度发版，永久 0.x [已验证] |
| [React Three Fiber](https://github.com/pmndrs/react-three-fiber) | 32.1k / MIT / 2026-09-04 / no | `@react-three/fiber` 9.7.0 / 5.1M / MIT / 2.2M | peer `>=19 <19.3` ✅ | [bp](https://bundlephobia.com/package/@react-three/fiber@9.7.0) | v9 仅 React 19（[v9 迁移](https://r3f.docs.pmnd.rs/tutorials/v9-migration-guide)）[已验证] |
| [drei](https://github.com/pmndrs/drei) | 9.8k / MIT / 2026-09-05 / no | `@react-three/drei` 10.7.8 / 3.9M / MIT / 1.8M | peer ^19 | [bp](https://bundlephobia.com/package/@react-three/drei@10.7.8) | R3F 助手集 [已验证] |
| [Babylon.js](https://github.com/BabylonJS/Babylon.js) | 26.0k / Apache-2.0 / 2026-09-04 / no | `@babylonjs/core` 9.25.0 / 339k / Apache-2.0 / 70.2M | — | [pkg](https://pkg-size.dev/@babylonjs/core) | 微软；全功能引擎 [已验证] |
| [PixiJS](https://github.com/pixijs/pixijs) | 48.1k / MIT / 2026-09-04 / no | `pixi.js` 8.20.1 / 1.1M / MIT / 74.3M | — | [bp](https://bundlephobia.com/package/pixi.js@8.20.1) | 2D WebGL/WebGPU [已验证] |
| [@pixi/react](https://github.com/pixijs/pixi-react) | 2.9k / MIT / **2026-01-16** / no | 8.0.5 / 87k / MIT / 10.5M | peer >=19 | [bp](https://bundlephobia.com/package/@pixi/react@8.0.5) | 近 8 个月无 push，npm 2025-12-01 [已验证] |
| [Konva](https://github.com/konvajs/konva) | 14.8k / **NOASSERTION** / 2026-09-04 / no | 10.3.3 / 2.8M / MIT / 1.5M | — | [bp](https://bundlephobia.com/package/konva@10.3.3) | 2D Canvas 场景图 [已验证] |
| [react-konva](https://github.com/konvajs/react-konva) | 6.4k / MIT / 2026-09-04 / no | 19.2.6 / 2.2M / MIT / 77k | peer ^19.2 ✅ | [bp](https://bundlephobia.com/package/react-konva@19.2.6) | 版本号跟随 React 主版本 [已验证] |
| [Fabric.js](https://github.com/fabricjs/fabric.js) | 31.4k / MIT / 2026-08-18 / no | `fabric` 7.4.0 / 960k / MIT / 22.2M | — | [bp](https://bundlephobia.com/package/fabric@7.4.0) | 图形编辑器常用 [已验证] |
| [Phaser](https://github.com/phaserjs/phaser) | 40.3k / MIT / 2026-08-21 / no | 4.2.1 / 346k / MIT / 112.5M | — | [pkg](https://pkg-size.dev/phaser) | 2D 游戏引擎，v4 [已验证] |
| [p5.js](https://github.com/processing/p5.js) | 23.9k / **LGPL-2.1** / 2026-09-03 / no | `p5` 2.3.2 / 220k / LGPL-2.1 / 17.4M | — | [pkg](https://pkg-size.dev/p5) | LGPL：打包进产品时需保证可替换/动态链接义务，商用前请法务确认 [已验证] |
| [Theatre.js](https://github.com/theatre-js/theatre) | 12.7k / Apache-2.0 / **2024-08-14** / no | `@theatre/core` 0.7.2 / 17k / Apache-2.0 / 903k | — | — | **2 年无 push，停滞** [已验证] |
| [OGL](https://github.com/oframe/ogl) | 4.6k / **NONE** / 2025-04-13 / no | `ogl` 1.0.11 / 618k / Unlicense / 423k | — | [bp](https://bundlephobia.com/package/ogl@1.0.11) | 小型 WebGL 库；GitHub 无许可证识别、npm Unlicense；近 17 个月无 push [已验证] |
| [Rough.js](https://github.com/rough-stuff/rough) | 21.2k / MIT / **2024-07-28** / no | `roughjs` 4.6.6 / 14.1M / MIT / 170k | — | [bp](https://bundlephobia.com/package/roughjs@4.6.6) | 手绘风；2 年无 push，但被 Excalidraw 依赖故下载高 [已验证；依赖关系为推断] |
| [tsParticles](https://github.com/tsparticles/tsparticles) | 9.0k / MIT / 2026-09-02 / no | `@tsparticles/react` 4.4.0 / 237k / MIT / 4k | peer >=16.8 | [bp](https://bundlephobia.com/package/@tsparticles/react@4.4.0) | 粒子背景 [已验证] |
| [Spline react](https://github.com/splinetool/react-spline) | 1.4k / MIT / 2026-03-13 / no | `@splinetool/react-spline` 4.1.0 / 164k / **npm 未声明 license** / 27k | peer `*` | — | 依赖 Spline 商业设计工具导出；npm 包缺 license 字段 [已验证] |
| [Excalidraw](https://github.com/excalidraw/excalidraw) | 131.2k / MIT / 2026-09-04 / no | `@excalidraw/excalidraw` 0.18.1 / 508k / MIT / 46.8M | peer ^17‖^18‖^19 | [pkg](https://pkg-size.dev/@excalidraw/excalidraw) | 可嵌入白板，MIT [已验证] |
| [tldraw](https://github.com/tldraw/tldraw) | 50.1k / **NOASSERTION** / 2026-09-04 / no | 5.4.0 / 369k / **SEE LICENSE IN LICENSE.md** / 14.9M | peer ^18.2‖^19.2.1 | — | **非开源许可**：[LICENSE.md](https://github.com/tldraw/tldraw/blob/main/LICENSE.md) 禁止生产环境使用，需 License Key / 商业授权 [已验证] |

**一句话推荐**：3D 走 **three.js + R3F v9（仅 React 19）+ drei**；2D Canvas 交互用 **Konva + react-konva**（react-konva 已随 React 19.2）；白板嵌入选 **Excalidraw（MIT）**，tldraw 是"源码可见但生产需付费"的许可，不能当开源用；p5.js 为 LGPL、Theatre.js/Rough.js/OGL 已停滞，谨慎。

---

## 21. 地图 / GIS

| 候选 | GitHub | npm | R19 | 风险 / 备注 |
|---|---|---|---|---|
| [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js) | 11.5k / **NOASSERTION** / 2026-09-05 / no | `maplibre-gl` 6.7.0 / 4.5M / BSD-3-Clause / 19.8M | — | Mapbox GL v1 的开源分支；[LICENSE.txt](https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt) 为 BSD-3 [已验证] |
| [react-map-gl](https://github.com/visgl/react-map-gl) | 8.5k / **NOASSERTION** / 2026-09-03 / no | 8.1.3 / 2.1M / MIT / 481k | peer >=16.3 | vis.gl（OpenJS 基金会）维护，支持 MapLibre/Mapbox 双后端 [已验证] |
| Mapbox GL JS（对照） | 12.4k / **NOASSERTION** / 2026-09-04 / no | `mapbox-gl` 3.30.0 / 4.1M / **SEE LICENSE IN LICENSE.txt** / 65.4M | — | **非开源**：[LICENSE.txt](https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt) 仅限配合 Mapbox 付费产品使用 [已验证] |
| [Leaflet](https://github.com/Leaflet/Leaflet) | 45.6k / BSD-2-Clause / 2026-09-05 / no | `leaflet` 1.9.4 / 6.9M / BSD-2-Clause / 3.7M | — | latest 1.9.4 发布于 **2023-05-18**；2.0.0-alpha.1 在 alpha tag，仓库活跃 [已验证] |
| [react-leaflet](https://github.com/PaulLeCam/react-leaflet) | 5.6k / **NOASSERTION** / 2025-12-31 / no | 5.0.0 / 3.6M / **Hippocratic-2.1** / 49k | peer ^19 | **Hippocratic 2.1 非 OSI 开源许可**（含伦理使用限制，[LICENSE.md](https://github.com/PaulLeCam/react-leaflet/blob/master/LICENSE.md)）；单人维护，npm 2024-12-14 [已验证] |
| [OpenLayers](https://github.com/openlayers/openlayers) | 12.6k / BSD-2-Clause / 2026-09-05 / no | `ol` 10.10.0 / 786k / BSD-2-Clause / 12.3M | — | 全功能 GIS 库 [已验证] |
| [deck.gl](https://github.com/visgl/deck.gl) | 14.6k / MIT / 2026-09-05 / no | 9.3.11 / 275k / MIT / 5.2M | peer >=16.3 | 大数据地理可视化，叠加 MapLibre [已验证] |
| [CesiumJS](https://github.com/CesiumGS/cesium) | 15.7k / Apache-2.0 / 2026-09-04 / no | `cesium` 1.145.0 / 298k / Apache-2.0 / 79.4M | — | 3D 地球；Cesium ion 为商业服务 [已验证；商业边界为推断] |
| [Turf.js](https://github.com/Turfjs/turf) | 10.5k / MIT / 2026-08-31 / no | `@turf/turf` 7.4.0 / 1.4M / MIT / 604k | — | 地理空间计算 [已验证] |
| [PMTiles](https://github.com/protomaps/PMTiles) | 3.0k / **NOASSERTION** / 2026-08-19 / no | `pmtiles` 4.5.0 / 808k / BSD-3-Clause / 380k | — | 单文件瓦片格式，配 MapLibre 自托管底图 [已验证] |
| [AntV L7](https://github.com/antvis/L7) | 4.1k / MIT / 2026-07-30 / no | `@antv/l7` 2.29.1 / 36k / MIT / 1.5M | — | 蚂蚁地理可视化，中文文档 [已验证] |
| ECharts 地图（见 §5） | — | — | — | 仅交叉引用 [不重复采集] |

**一句话推荐**：Web 地图默认 **MapLibre GL JS + react-map-gl + PMTiles**（全部宽松许可、可自托管、无 token）；Mapbox GL JS v2+ 不是开源许可；Leaflet 本体健康但 react-leaflet 为 Hippocratic 许可且单人维护，React 项目慎用；大数据叠加用 deck.gl，3D 地球用 CesiumJS。

---

## 22. 实时协作 / CRDT / 实时通信 / 同步引擎

| 候选 | GitHub | npm | R19 | 风险 / 备注 |
|---|---|---|---|---|
| [Yjs](https://github.com/yjs/yjs) | 22.8k / **NOASSERTION** / 2026-09-05 / no | 13.6.32 / 8.6M / MIT / 2.3M | — | CRDT 事实标准；Tiptap/BlockNote 协作层 [已验证] |
| [y-websocket](https://github.com/yjs/y-websocket) | 710 / MIT / 2026-08-06 / no | 3.1.0 / 731k / MIT / 94k | — | 官方最简 provider [已验证] |
| [Hocuspocus](https://github.com/ueberdosis/hocuspocus) | 2.6k / MIT / 2026-09-02 / no | `@hocuspocus/server` 4.6.0 / 711k / MIT / 906k | — | Tiptap 团队 Yjs 服务端，MIT（Tiptap Cloud 为付费）[已验证] |
| [Automerge](https://github.com/automerge/automerge) | 6.6k / MIT / 2026-09-04 / no | `@automerge/automerge` 3.4.1 / 48k / MIT / 46.5M | — | Rust+Wasm CRDT，unpacked 46.5M [已验证] |
| [Loro](https://github.com/loro-dev/loro) | 6.1k / MIT / 2026-09-05 / no | `loro-crdt` 1.15.1 / 157k / MIT / 19.4M | — | 高性能 CRDT，1.x [已验证] |
| [Liveblocks](https://github.com/liveblocks/liveblocks) | 4.7k / **NOASSERTION** / 2026-09-04 / no | `@liveblocks/client` 3.24.1 / 408k / Apache-2.0 / 15k | — | SDK 开源，**服务端为 SaaS**（[定价](https://liveblocks.io/pricing)：Free / $25 / $500 月）[已验证] |
| [PartyServer](https://github.com/cloudflare/partykit) | 1.3k / ISC / 2026-08-03 / no | `partyserver` 0.5.10 / 1.7M / ISC / 143k | — | 绑定 Cloudflare Durable Objects [已验证] |
| [Socket.IO](https://github.com/socketio/socket.io) | 63.2k / MIT / 2026-09-04 / no | `socket.io-client` 4.8.3 / 14.5M / MIT / 1.4M | — | client latest 2025-12-23 [已验证] |
| [Zero](https://github.com/rocicorp/mono) | 3.4k / Apache-2.0 / 2026-09-05 / no | `@rocicorp/zero` 1.9.0 / 122k / Apache-2.0 / 8.6M | — | Rocicorp 同步引擎，需自托管 zero-cache [已验证] |
| [Electric SQL](https://github.com/electric-sql/electric) | 10.4k / Apache-2.0 / 2026-09-02 / no | `@electric-sql/client` 1.5.27 / 1.3M / Apache-2.0 / 2.4M | — | Postgres 部分复制同步 [已验证] |
| [Convex](https://github.com/get-convex/convex-js) | 365 / Apache-2.0 / 2026-09-05 / no | `convex` 1.45.0 / 1.3M / Apache-2.0 / 31.4M | peer ^18‖^19 | 客户端开源，后端为托管服务（有自托管版）[已验证；自托管为官网说明，未实测] |
| [Supabase JS](https://github.com/supabase/supabase-js) | 4.6k / MIT / 2026-09-04 / no | `@supabase/supabase-js` 2.115.0 / 25.0M / MIT / 638k | — | Realtime 通道随 SDK [已验证] |
| [Jazz](https://github.com/garden-co/jazz) | 184 / **NOASSERTION** / 2026-09-05 / no | `jazz-tools` 0.20.19 / 3.8k / MIT / 12.8M | peer `*` | 0.x、社区极小 [已验证] |

**一句话推荐**：自控协作基础设施选 **Yjs + Hocuspocus**（全 MIT，与 §8 Tiptap/BlockNote 天然对接）；想省运维选 **Liveblocks**（SDK Apache-2.0 但服务收费）；需要"数据库级"同步而非文档协作，看 Electric SQL / Zero（均 Apache-2.0，需自托管服务端）；Automerge/Loro 适合非文档型 CRDT 场景。

---

## 23. 本地优先 / 浏览器存储 / WASM 数据库

| 候选 | GitHub | npm | R19 | 风险 / 备注 |
|---|---|---|---|---|
| [TinyBase](https://github.com/tinyplex/tinybase) | 5.2k / MIT / 2026-09-03 / no | 9.7.0 / 14k / MIT / 16.0M | peer ^19.2.8 ✅ | 响应式本地数据存储，React 19 peer 明确 [已验证] |
| [Dexie.js](https://github.com/dexie/Dexie.js) | 14.6k / Apache-2.0 / 2026-08-28 / no | `dexie` 4.4.5 / 2.3M / Apache-2.0 / 3.2M | — | IndexedDB 封装事实标准；Dexie Cloud 为付费同步 [已验证] |
| `dexie-react-hooks` | (同 Dexie 仓) | 4.4.0 / 488k / Apache-2.0 / 154k | peer >=16 | `useLiveQuery` [已验证 npm] |
| [PGlite](https://github.com/electric-sql/pglite) | 16.0k / Apache-2.0 / 2026-08-26 / no | `@electric-sql/pglite` 0.5.8 / **15.3M** / Apache-2.0 / 25.4M | — | 浏览器 Postgres（Wasm），0.x；周下载 15.3M 为 API 返回值 [已验证] |
| [RxDB](https://github.com/pubkey/rxdb) | 23.4k / Apache-2.0 / 2026-09-04 / no | 17.5.0 / 73k / Apache-2.0 / 11.5M | peer `*` | 核心 Apache-2.0，**部分插件为付费 Premium**（[官网](https://rxdb.info/premium/)）[已验证；付费边界为官网页面] |
| [idb](https://github.com/jakearchibald/idb) | 7.4k / ISC / **2025-05-07** / no | 8.0.3 / 24.7M / ISC / 83k | — | IndexedDB Promise 封装；16 个月无更新，但功能完备 [已验证] |
| [idb-keyval](https://github.com/jakearchibald/idb-keyval) | 3.2k / **NOASSERTION** / 2026-07-08 / no | 6.3.0 / 8.7M / Apache-2.0 / 56k | — | 极简 KV [已验证] |
| [localForage](https://github.com/localForage/localForage) | 25.8k / Apache-2.0 / **2024-07-30** / no | 1.10.0 / 8.8M / Apache-2.0 / 468k | — | npm latest **2021-08-18**，停滞 [已验证] |
| [sql.js](https://github.com/sql-js/sql.js) | 13.7k / **NOASSERTION** / 2026-08-14 / no | 1.14.2 / 2.5M / MIT / 24.2M | — | SQLite 编译到 Wasm（内存型）[已验证] |
| [wa-sqlite](https://github.com/rhashimoto/wa-sqlite) | 1.4k / MIT / 2026-08-28 / no | 1.0.0 / 12k / **npm 未声明 license** / 2.2M | — | npm latest 2024-01-05；GitHub MIT [已验证] |
| [SQLite Wasm (官方)](https://github.com/sqlite/sqlite-wasm) | 1.1k / **NONE** / 2026-07-13 / no | `@sqlite.org/sqlite-wasm` 3.53.0-build1 / 796k / Apache-2.0 / 2.8M | — | SQLite 官方 OPFS 持久化；GitHub 无许可证识别（SQLite 本体为公有领域）[已验证；公有领域为 SQLite 官网] |
| [PowerSync](https://github.com/powersync-ja/powersync-js) | 720 / Apache-2.0 / 2026-09-04 / no | `@powersync/web` 2.3.0 / 85k / Apache-2.0 / 10.3M | — | SDK 开源，同步服务有云/自托管 [已验证；服务形态为推断] |
| [InstantDB](https://github.com/instantdb/instant) | 10.5k / Apache-2.0 / 2026-09-05 / no | `@instantdb/react` 1.0.67 / 173k / Apache-2.0 / 728k | peer >=16 | 客户端 Apache-2.0，后端托管 [已验证] |
| [Triplit](https://github.com/aspen-cloud/triplit) | 3.1k / **AGPL-3.0** / **2026-01-19** / no | `@triplit/client` 1.0.50 / 146k / AGPL-3.0-only / 811k | — | **AGPL** 且近 8 个月无 push，npm 2025-07-31 [已验证] |
| [Evolu](https://github.com/evoluhq/evolu) | 1.9k / MIT / 2026-09-03 / no | `@evolu/react` 11.0.2 / 279 / MIT / 25k | peer >=19 | 端到端加密本地优先，采用度极低 [已验证] |
| [unstorage](https://github.com/unjs/unstorage) | 2.6k / MIT / 2026-09-05 / no | 1.17.5 / 24.8M / MIT / 354k | — | 统一 KV 抽象（浏览器/Node/云）[已验证] |
| [Legend-State](https://github.com/LegendApp/legend-state) | 4.2k / MIT / 2026-08-11 / no | `@legendapp/state` 2.1.15 / 97k / MIT / 993k | peer >=16.8 | latest 2.x 停在 2024-08-30，3.0 长期 beta [已验证] |

**一句话推荐**：浏览器结构化存储默认 **Dexie 4 + dexie-react-hooks**（Apache-2.0、最成熟）；轻量 KV 用 idb-keyval；需要 SQL 选 **SQLite Wasm 官方（OPFS）** 或 PGlite（Postgres 语法，仍 0.x）；带云同步的方案（RxDB Premium、Dexie Cloud、PowerSync、InstantDB）都存在商业边界，Triplit 为 AGPL 且停滞，不选。

---

## 第二批风险清单（GitHub SPDX ≠ npm license 或非宽松许可）

| 候选 | GitHub SPDX | npm license | 判断 |
|---|---|---|---|
| tldraw | NOASSERTION | SEE LICENSE IN LICENSE.md | **非开源**，生产需商业授权 |
| Mapbox GL JS | NOASSERTION | SEE LICENSE IN LICENSE.txt | **非开源**，绑定 Mapbox 付费产品 |
| react-leaflet | NOASSERTION | Hippocratic-2.1 | 非 OSI 许可（伦理条款） |
| Triplit | AGPL-3.0 | AGPL-3.0-only | 网络 copyleft |
| p5.js | LGPL-2.1 | LGPL-2.1 | 弱 copyleft，嵌入需注意 |
| Lightning CSS | MPL-2.0 | MPL-2.0 | 文件级 copyleft，构建工具无影响 |
| fnm | GPL-3.0 | — | 仅 CLI 工具，无影响 |
| npm CLI | NOASSERTION | Artistic-2.0 | OSI 认可，仅工具 |
| HTMX | NOASSERTION | 0BSD | 宽松 |
| OGL | NONE | Unlicense | 公有领域式，但项目停滞 |
| Spline react / wa-sqlite | MIT | （npm 未声明） | 需以仓库 LICENSE 为准 |
| UnoCSS / Rollup / Bun / Stencil / FAST / Astro / Konva / MapLibre / react-map-gl / PMTiles / Yjs / Liveblocks / Jazz / idb-keyval / sql.js | NOASSERTION | MIT / BSD-3 / Apache-2.0 | GitHub 未识别许可证文件，npm 为宽松许可，实质无风险 |
| Volta | NOASSERTION | — | 无 npm 包；仓库停滞 |
| @lit/react、dexie-react-hooks、SQLite Wasm | （无独立仓 / NONE） | BSD-3 / Apache-2.0 / Apache-2.0 | 按 npm license 采信 |

**archived**：Stitches、Shoelace（legacy）。**npm deprecated**：Tokenami。**停滞（≥8 个月无 push）**：Theatre.js、Rough.js、localForage、OGL、Volta、Triplit、@pixi/react。**商业功能墙**：Web Awesome Pro、Nx Cloud、Liveblocks、RxDB Premium、Dexie Cloud、Convex/InstantDB 托管后端。


---

# 第三批（§24–§34）：认证 / 支付 / AI 前端 / 微前端 / 监控 / 可视化搭建 / 服务端渲图 / 工具函数 / 媒体 / 通知 / 命令面板

- 实查日期：**2026-09-05（UTC）**，279 条（含 10 条指向前文章节的交叉引用行，数据文件 `data/candidates-round3-2026-09-05.json`）。
- 表格列：★ = GitHub stars；GitHub SPDX 为 GitHub API 识别结果（`NOASSERTION`/`NONE` = 未识别，需看 npm license 或仓库 LICENSE）；周下载来自 `api.npmjs.org` last-week；React peer 原文摘自 npm `peerDependencies`；备注中的「最新发布」= npm latest 版本发布日期早于 2024-09-01（≥2 年无发版）。
- 所有行均为 **[已验证]**（API 返回值）；「一句话推荐」中的取舍判断为研究员结论。

## 24. 认证 UI / 认证 SDK

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| Better Auth | [better-auth/better-auth](https://github.com/better-auth/better-auth) | 29.8k | MIT | 2026-09-05 | [better-auth](https://www.npmjs.com/package/better-auth) | 1.7.2 | 7.5M | MIT | ^18.0.0 \|\| ^19.0.0 |  |
| Auth.js (NextAuth) | [nextauthjs/next-auth](https://github.com/nextauthjs/next-auth) | 28.4k | ISC | 2026-07-22 | [next-auth](https://www.npmjs.com/package/next-auth) | 4.24.15 | 6.0M | ISC | ^17.0.2 \|\| ^18 \|\| ^19 |  |
| Clerk React (SDK) | [clerk/javascript](https://github.com/clerk/javascript) | 1.8k | MIT | 2026-09-05 | [@clerk/react](https://www.npmjs.com/package/@clerk/react) | 6.15.1 | 2.1M | MIT | ^18.0.0 \|\| ~19.0.3 \|\| ~19.1.4 \|\| ~19.2.3 \|\| ~19.3.0-0 |  |
| Supabase Auth UI React | [supabase-community/auth-ui](https://github.com/supabase-community/auth-ui) | 544 | MIT | 2025-10-23 | [@supabase/auth-ui-react](https://www.npmjs.com/package/@supabase/auth-ui-react) | 0.4.7 | 135.0k | - | - | **archived**；最新发布 2024-01-04 |
| Lucia (guide) | [lucia-auth/lucia](https://github.com/lucia-auth/lucia) | 10.4k | MIT | 2026-08-08 | - | - | - | - | - |  |
| @oslojs/crypto (oslo 后继) | [oslo-project/crypto](https://github.com/oslo-project/crypto) | 80 | MIT | 2024-10-24 | [@oslojs/crypto](https://www.npmjs.com/package/@oslojs/crypto) | 1.0.1 | 1.5M | MIT | - | **npm deprecated** |
| Arctic (OAuth 2) | [pilcrowonpaper/arctic](https://github.com/pilcrowonpaper/arctic) | 1.7k | MIT | 2026-08-08 | [arctic](https://www.npmjs.com/package/arctic) | 3.7.0 | 971.1k | MIT | - | **npm deprecated** |
| jose (JWT) | [panva/jose](https://github.com/panva/jose) | 7.8k | MIT | 2026-09-05 | [jose](https://www.npmjs.com/package/jose) | 6.2.12 | 128.0M | MIT | - |  |
| oidc-client-ts | [authts/oidc-client-ts](https://github.com/authts/oidc-client-ts) | 1.9k | Apache-2.0 | 2026-09-01 | [oidc-client-ts](https://www.npmjs.com/package/oidc-client-ts) | 3.5.0 | 2.6M | Apache-2.0 | - |  |
| react-oidc-context | [authts/react-oidc-context](https://github.com/authts/react-oidc-context) | 1.0k | MIT | 2026-06-12 | [react-oidc-context](https://www.npmjs.com/package/react-oidc-context) | 3.3.1 | 791.1k | MIT | >=16.14.0 |  |
| Keycloak JS | [keycloak/keycloak](https://github.com/keycloak/keycloak) | 36.6k | Apache-2.0 | 2026-09-05 | [keycloak-js](https://www.npmjs.com/package/keycloak-js) | 26.2.4 | 1.1M | Apache-2.0 | - |  |
| Firebase UI Web | [firebase/firebaseui-web](https://github.com/firebase/firebaseui-web) | 4.9k | Apache-2.0 | 2026-09-03 | [firebaseui](https://www.npmjs.com/package/firebaseui) | 6.1.0 | 55.8k | Apache-2.0 | - | 最新发布 2023-08-02 |
| Ory Elements | [ory/elements](https://github.com/ory/elements) | 187 | Apache-2.0 | 2026-07-31 | [@ory/elements-react](https://www.npmjs.com/package/@ory/elements-react) | 1.2.1 | 15.9k | Apache License 2.0 | ^18.0.0 \|\| ^19.0.0 \|\| ^19.0.0-0 |  |
| SimpleWebAuthn (browser) | [MasterKale/SimpleWebAuthn](https://github.com/MasterKale/SimpleWebAuthn) | 2.3k | MIT | 2026-09-05 | [@simplewebauthn/browser](https://www.npmjs.com/package/@simplewebauthn/browser) | 14.0.0 | 4.1M | MIT | - |  |
| Auth0 SPA JS | [auth0/auth0-spa-js](https://github.com/auth0/auth0-spa-js) | 1.0k | MIT | 2026-09-05 | [@auth0/auth0-spa-js](https://www.npmjs.com/package/@auth0/auth0-spa-js) | 2.24.1 | 2.4M | MIT | - |  |
| Logto React | [logto-io/js](https://github.com/logto-io/js) | 96 | MIT | 2026-09-02 | [@logto/react](https://www.npmjs.com/package/@logto/react) | 4.0.14 | 34.0k | MIT | >=16.8.0 |  |
| Hanko Elements | [teamhanko/hanko](https://github.com/teamhanko/hanko) | 9.0k | NOASSERTION | 2026-09-03 | [@teamhanko/hanko-elements](https://www.npmjs.com/package/@teamhanko/hanko-elements) | 3.0.0 | 7.2k | MIT | - |  |
| Zitadel React | [zitadel/zitadel-react](https://github.com/zitadel/zitadel-react) | 22 | NOASSERTION | 2026-08-19 | [@zitadel/react](https://www.npmjs.com/package/@zitadel/react) | 1.1.1 | 12.4k | MIT | - |  |

**一句话推荐**：自托管认证选 **Better Auth**（MIT，React 18/19 peer，周下载 7.5M，push 当日）；Next.js 存量项目用 Auth.js；纯协议层用 **jose**（JWT，128M/周）+ oidc-client-ts / react-oidc-context；Passkey 用 SimpleWebAuthn。**不选**：Supabase Auth UI（archived，2024-01 停更）、oslo/Arctic（npm 已 deprecated）、Firebase UI（latest 2023-08）。Clerk/Auth0/Logto/Hanko/Zitadel/Ory SDK 均开源，但绑定各自托管服务（商业边界为推断）。Lucia 已转为「教程」形式，无 npm 包。

## 25. 支付 UI / 支付 SDK

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| Stripe React | [stripe/react-stripe-js](https://github.com/stripe/react-stripe-js) | 2.0k | MIT | 2026-09-03 | [@stripe/react-stripe-js](https://www.npmjs.com/package/@stripe/react-stripe-js) | 6.9.0 | 8.9M | MIT | >=16.8.0 <20.0.0 |  |
| stripe-js | [stripe/stripe-js](https://github.com/stripe/stripe-js) | 752 | MIT | 2026-09-05 | [@stripe/stripe-js](https://www.npmjs.com/package/@stripe/stripe-js) | 9.15.0 | 12.3M | MIT | - |  |
| PayPal React | [paypal/paypal-js](https://github.com/paypal/paypal-js) | 338 | Apache-2.0 | 2026-09-03 | [@paypal/react-paypal-js](https://www.npmjs.com/package/@paypal/react-paypal-js) | 10.4.0 | 434.8k | Apache-2.0 | ^16.8.0 \|\| ^17 \|\| ^18 \|\| ^19 |  |
| Paddle JS | [PaddleHQ/paddle-js-wrapper](https://github.com/PaddleHQ/paddle-js-wrapper) | 74 | Apache-2.0 | 2026-08-25 | [@paddle/paddle-js](https://www.npmjs.com/package/@paddle/paddle-js) | 1.6.5 | 171.6k | Apache-2.0 | - |  |
| LemonSqueezy JS | [lmsqueezy/lemonsqueezy.js](https://github.com/lmsqueezy/lemonsqueezy.js) | 535 | MIT | 2024-11-05 | [@lemonsqueezy/lemonsqueezy.js](https://www.npmjs.com/package/@lemonsqueezy/lemonsqueezy.js) | 4.0.0 | 110.5k | MIT | - |  |
| Polar | [polarsource/polar](https://github.com/polarsource/polar) | 10.2k | Apache-2.0 | 2026-09-05 | [@polar-sh/sdk](https://www.npmjs.com/package/@polar-sh/sdk) | 0.49.0 | 266.9k | MIT | - |  |
| Braintree Web Drop-in | [braintree/braintree-web-drop-in](https://github.com/braintree/braintree-web-drop-in) | 203 | MIT | 2026-06-17 | [braintree-web-drop-in](https://www.npmjs.com/package/braintree-web-drop-in) | 1.47.0 | 202.4k | MIT | - |  |
| Adyen Web | [Adyen/adyen-web](https://github.com/Adyen/adyen-web) | 254 | MIT | 2026-09-05 | [@adyen/adyen-web](https://www.npmjs.com/package/@adyen/adyen-web) | 6.44.0 | 562.8k | MIT | - |  |
| react-credit-cards-2 | [amarofashion/react-credit-cards](https://github.com/amarofashion/react-credit-cards) | 2.6k | MIT | 2024-01-19 | [react-credit-cards-2](https://www.npmjs.com/package/react-credit-cards-2) | 1.2.0 | 25.5k | MIT | ^16.8.0 \|\| ^17.0.0 \|\| ^18.0.0 \|\| ^19.0.0 |  |
| card-validator | [braintree/card-validator](https://github.com/braintree/card-validator) | 938 | MIT | 2026-06-20 | [card-validator](https://www.npmjs.com/package/card-validator) | 10.0.4 | 1.4M | MIT | - |  |
| Autumn (billing) | [useautumn/autumn](https://github.com/useautumn/autumn) | 2.7k | Apache-2.0 | 2026-09-05 | [autumn-js](https://www.npmjs.com/package/autumn-js) | 1.3.0 | 145.1k | MIT | ^18.0.0 \|\| ^19.0.0 |  |
| Creem | [armitage-labs/creem-sdk](https://github.com/armitage-labs/creem-sdk) | 27 | NONE | 2026-03-26 | [creem](https://www.npmjs.com/package/creem) | 1.6.2 | 35.7k | MIT | - | **archived** |

**一句话推荐**：Stripe 官方 **@stripe/react-stripe-js**（MIT，peer 覆盖到 React 19，8.9M/周）是唯一成熟的 React 支付 UI；PayPal 用官方 `@paypal/react-paypal-js`（Apache-2.0，仓库已并入 paypal/paypal-js）；MoR 类（Paddle/LemonSqueezy/Polar/Creem/Autumn）SDK 开源但均绑定付费服务。**注意**：LemonSqueezy JS 自 2024-11 无更新；Creem 仓库已 archived；react-credit-cards-2 仓库 2024-01 后无 push。所有支付库均为服务端配套 SDK，无「纯前端」免费替代。

## 26. AI 前端（对话 UI / 推理 / SDK / 流式）

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| Vercel AI SDK | [vercel/ai](https://github.com/vercel/ai) | 26.6k | NOASSERTION | 2026-09-05 | [ai](https://www.npmjs.com/package/ai) | 7.0.93 | 23.6M | Apache-2.0 | - |  |
| @ai-sdk/react | [vercel/ai](https://github.com/vercel/ai) | 26.6k | NOASSERTION | 2026-09-05 | [@ai-sdk/react](https://www.npmjs.com/package/@ai-sdk/react) | 4.0.96 | 8.2M | Apache-2.0 | ^18 \|\| ~19.0.1 \|\| ~19.1.2 \|\| ^19.2.1 |  |
| assistant-ui | [assistant-ui/assistant-ui](https://github.com/assistant-ui/assistant-ui) | 12.0k | MIT | 2026-09-05 | [@assistant-ui/react](https://www.npmjs.com/package/@assistant-ui/react) | 0.15.18 | 1.7M | MIT | ^18 \|\| ^19 |  |
| CopilotKit | [CopilotKit/CopilotKit](https://github.com/CopilotKit/CopilotKit) | 37.2k | MIT | 2026-09-05 | [@copilotkit/react-core](https://www.npmjs.com/package/@copilotkit/react-core) | 1.70.1 | 452.7k | MIT | ^18 \|\| ^19 \|\| ^19.0.0-rc |  |
| LangChain.js | [langchain-ai/langchainjs](https://github.com/langchain-ai/langchainjs) | 18.2k | MIT | 2026-09-04 | [langchain](https://www.npmjs.com/package/langchain) | 1.5.10 | 3.0M | MIT | - |  |
| LlamaIndex.TS | [run-llama/LlamaIndexTS](https://github.com/run-llama/LlamaIndexTS) | 3.1k | MIT | 2026-03-11 | [llamaindex](https://www.npmjs.com/package/llamaindex) | 0.12.1 | 125.3k | MIT | - | **archived** |
| Transformers.js | [huggingface/transformers.js](https://github.com/huggingface/transformers.js) | 16.3k | Apache-2.0 | 2026-09-04 | [@huggingface/transformers](https://www.npmjs.com/package/@huggingface/transformers) | 4.2.0 | 2.8M | Apache-2.0 | - |  |
| WebLLM | [mlc-ai/web-llm](https://github.com/mlc-ai/web-llm) | 19.0k | Apache-2.0 | 2026-09-03 | [@mlc-ai/web-llm](https://www.npmjs.com/package/@mlc-ai/web-llm) | 0.2.84 | 78.9k | Apache-2.0 | - |  |
| ONNX Runtime Web | [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) | 21.8k | MIT | 2026-09-05 | [onnxruntime-web](https://www.npmjs.com/package/onnxruntime-web) | 1.29.0 | 4.3M | MIT | - |  |
| TensorFlow.js | [tensorflow/tfjs](https://github.com/tensorflow/tfjs) | 19.1k | Apache-2.0 | 2026-06-23 | [@tensorflow/tfjs](https://www.npmjs.com/package/@tensorflow/tfjs) | 4.22.0 | 527.2k | Apache-2.0 | - |  |
| MediaPipe Tasks Vision | [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) | 36.9k | Apache-2.0 | 2026-09-05 | [@mediapipe/tasks-vision](https://www.npmjs.com/package/@mediapipe/tasks-vision) | 1.0.1 | 4.6M | Apache-2.0 | - |  |
| Deep Chat | [OvidijusParsiunas/deep-chat](https://github.com/OvidijusParsiunas/deep-chat) | 3.7k | MIT | 2026-09-02 | [deep-chat-react](https://www.npmjs.com/package/deep-chat-react) | 2.5.1 | 9.1k | MIT | >=16.8.0 |  |
| NLUX | [nlkitai/nlux](https://github.com/nlkitai/nlux) | 1.4k | NOASSERTION | 2025-11-25 | [@nlux/react](https://www.npmjs.com/package/@nlux/react) | 2.17.1 | 6.3k | MPL-2.0 | ^18 | 最新发布 2024-08-15 |
| LobeHub UI | [lobehub/lobe-ui](https://github.com/lobehub/lobe-ui) | 2.2k | MIT | 2026-09-05 | [@lobehub/ui](https://www.npmjs.com/package/@lobehub/ui) | 5.40.0 | 426.5k | MIT | ^19.0.0 |  |
| Ant Design X | [ant-design/x](https://github.com/ant-design/x) | 4.8k | NONE | 2026-09-01 | [@ant-design/x](https://www.npmjs.com/package/@ant-design/x) | 2.9.0 | 102.5k | MIT | >=18.0.0 |  |
| Chatbot UI (Mckay) | [mckaywrigley/chatbot-ui](https://github.com/mckaywrigley/chatbot-ui) | 33.3k | MIT | 2024-08-03 | - | - | - | - | - |  |
| Vercel AI Elements | [vercel/ai-elements](https://github.com/vercel/ai-elements) | 2.4k | NOASSERTION | 2026-09-01 | [ai-elements](https://www.npmjs.com/package/ai-elements) | 1.9.0 | 89.5k | Apache-2.0 | - |  |
| ai-sdk-ui (shadcn ai) | [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | 123.1k | MIT | 2026-09-04 | [shadcn](https://www.npmjs.com/package/shadcn) | 4.21.0 | 8.7M | MIT | - |  |
| OpenAI Node | [openai/openai-node](https://github.com/openai/openai-node) | 11.2k | Apache-2.0 | 2026-09-05 | [openai](https://www.npmjs.com/package/openai) | 7.10.0 | 39.0M | Apache-2.0 | - |  |
| Anthropic SDK TS | [anthropics/anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript) | 2.1k | MIT | 2026-09-04 | [@anthropic-ai/sdk](https://www.npmjs.com/package/@anthropic-ai/sdk) | 0.124.0 | 38.0M | MIT | - |  |
| eventsource-parser | [rexxars/eventsource-parser](https://github.com/rexxars/eventsource-parser) | 498 | MIT | 2026-08-20 | [eventsource-parser](https://www.npmjs.com/package/eventsource-parser) | 4.1.0 | 67.2M | MIT | - |  |
| @microsoft/fetch-event-source | [Azure/fetch-event-source](https://github.com/Azure/fetch-event-source) | 2.9k | MIT | 2026-02-28 | [@microsoft/fetch-event-source](https://www.npmjs.com/package/@microsoft/fetch-event-source) | 2.0.1 | 3.4M | MIT | - | 最新发布 2021-04-25 |
| Mastra | [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | 27.7k | NOASSERTION | 2026-09-05 | [@mastra/core](https://www.npmjs.com/package/@mastra/core) | 1.64.0 | 1.6M | Apache-2.0 | - |  |
| Streamdown (见 §8) | - | - | - | - | - | - | - | - | - |  |

**一句话推荐**：应用层用 **Vercel AI SDK `ai` + `@ai-sdk/react`**（npm Apache-2.0，GitHub SPDX 显示 NOASSERTION，23.6M/周）配 **assistant-ui**（MIT，React 18/19）或 shadcn 官方 `ai-elements`；需 Copilot 侧栏/Agent 交互选 CopilotKit（MIT）；浏览器端推理用 Transformers.js（Apache-2.0）或 WebLLM；流式解析用 eventsource-parser（67M/周）。**注意**：LlamaIndex.TS 仓库已 archived；NLUX 为 MPL-2.0 且 2024-08 后无发版；`@microsoft/fetch-event-source` 最新发布 2021-04；Chatbot UI 是应用模板非库，2024-08 后无 push。LobeHub UI peer 仅 `^19.0.0`。

## 27. 微前端

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| Module Federation (core) | [module-federation/core](https://github.com/module-federation/core) | 2.6k | MIT | 2026-09-05 | [@module-federation/enhanced](https://www.npmjs.com/package/@module-federation/enhanced) | 2.9.0 | 4.4M | MIT | - |  |
| @originjs/vite-plugin-federation | [originjs/vite-plugin-federation](https://github.com/originjs/vite-plugin-federation) | 3.0k | NOASSERTION | 2025-05-17 | [@originjs/vite-plugin-federation](https://www.npmjs.com/package/@originjs/vite-plugin-federation) | 1.4.1 | 264.4k | MulanPSL-2.0 | - |  |
| single-spa | [single-spa/single-spa](https://github.com/single-spa/single-spa) | 13.9k | NOASSERTION | 2026-02-28 | [single-spa](https://www.npmjs.com/package/single-spa) | 6.0.3 | 441.2k | MIT | - |  |
| qiankun (蚂蚁) | [umijs/qiankun](https://github.com/umijs/qiankun) | 16.7k | MIT | 2026-08-30 | [qiankun](https://www.npmjs.com/package/qiankun) | 2.10.16 | 67.4k | MIT | - | 最新发布 2023-11-15 |
| Garfish (字节) | [web-infra-dev/garfish](https://github.com/web-infra-dev/garfish) | 2.9k | NOASSERTION | 2026-09-04 | [garfish](https://www.npmjs.com/package/garfish) | 1.19.12 | 1.3k | MIT | - |  |
| wujie 无界 (腾讯) | [Tencent/wujie](https://github.com/Tencent/wujie) | 5.0k | NOASSERTION | 2026-06-16 | [wujie](https://www.npmjs.com/package/wujie) | 2.1.0 | 5.6k | MIT | - |  |
| micro-app (京东) | [jd-opensource/micro-app](https://github.com/jd-opensource/micro-app) | 6.3k | MIT | 2026-06-25 | [@micro-zoe/micro-app](https://www.npmjs.com/package/@micro-zoe/micro-app) | 1.0.0-rc.32 | 3.9k | MIT | - |  |
| Piral | [smapiot/piral](https://github.com/smapiot/piral) | 1.9k | MIT | 2026-09-03 | [piral](https://www.npmjs.com/package/piral) | 1.12.3 | 4.8k | MIT | - |  |
| Bit | [teambit/bit](https://github.com/teambit/bit) | 18.5k | NOASSERTION | 2026-09-05 | [@teambit/bit](https://www.npmjs.com/package/@teambit/bit) | 2.2.37 | 9.4k | Apache-2.0 | - |  |
| import-maps polyfill (es-module-shims) | [guybedford/es-module-shims](https://github.com/guybedford/es-module-shims) | 1.7k | MIT | 2026-08-17 | [es-module-shims](https://www.npmjs.com/package/es-module-shims) | 2.8.4 | 229.6k | MIT | - |  |
| Native Federation (Angular Architects) | [angular-architects/module-federation-plugin](https://github.com/angular-architects/module-federation-plugin) | 852 | MIT | 2026-08-07 | [@angular-architects/native-federation](https://www.npmjs.com/package/@angular-architects/native-federation) | 22.1.2 | 91.2k | MIT | - |  |
| zoid (PayPal) | [krakenjs/zoid](https://github.com/krakenjs/zoid) | 2.1k | Apache-2.0 | 2026-08-03 | [zoid](https://www.npmjs.com/package/zoid) | 9.0.86 | 85.7k | - | - | 最新发布 2022-01-12 |

**一句话推荐**：新项目优先 **Module Federation 2.0（`@module-federation/enhanced`）**，MIT，Rspack/webpack/Vite 均有官方插件（4.4M/周）；框架无关路由编排用 single-spa；国内方案中 **wujie（腾讯，2026-06 仍发版）** 与 micro-app（京东，1.0.0-rc）活跃，**qiankun latest 停在 2023-11**（仓库仍有 push）。**注意**：`@originjs/vite-plugin-federation` 为 **MulanPSL-2.0**（木兰宽松许可证，OSI 认可）且 2025-04 后无发版；zoid 最新发布 2022-01；Bit 是平台产品，SDK Apache-2.0。

## 28. 性能监控 / 错误追踪 / 分析 / 会话回放

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| web-vitals | [GoogleChrome/web-vitals](https://github.com/GoogleChrome/web-vitals) | 8.6k | Apache-2.0 | 2026-08-26 | [web-vitals](https://www.npmjs.com/package/web-vitals) | 6.2.1 | 38.9M | Apache-2.0 | - |  |
| Sentry Browser | [getsentry/sentry-javascript](https://github.com/getsentry/sentry-javascript) | 8.7k | MIT | 2026-09-04 | [@sentry/browser](https://www.npmjs.com/package/@sentry/browser) | 10.73.0 | 32.4M | MIT | - |  |
| @sentry/react | [getsentry/sentry-javascript](https://github.com/getsentry/sentry-javascript) | 8.7k | MIT | 2026-09-04 | [@sentry/react](https://www.npmjs.com/package/@sentry/react) | 10.73.0 | 24.4M | MIT | ^16.14.0 \|\| 17.x \|\| 18.x \|\| 19.x |  |
| OpenTelemetry Web | [open-telemetry/opentelemetry-js](https://github.com/open-telemetry/opentelemetry-js) | 3.5k | Apache-2.0 | 2026-09-04 | [@opentelemetry/sdk-trace-web](https://www.npmjs.com/package/@opentelemetry/sdk-trace-web) | 2.11.0 | 7.6M | Apache-2.0 | - |  |
| Grafana Faro | [grafana/faro-web-sdk](https://github.com/grafana/faro-web-sdk) | 1.1k | Apache-2.0 | 2026-09-05 | [@grafana/faro-web-sdk](https://www.npmjs.com/package/@grafana/faro-web-sdk) | 2.11.0 | 977.5k | Apache-2.0 | - |  |
| PostHog JS | [PostHog/posthog-js](https://github.com/PostHog/posthog-js) | 601 | NOASSERTION | 2026-09-05 | [posthog-js](https://www.npmjs.com/package/posthog-js) | 1.427.2 | 12.7M | (Apache-2.0 AND MIT) | >=16.8.0 |  |
| Plausible tracker | [plausible/plausible-tracker](https://github.com/plausible/plausible-tracker) | 287 | MIT | 2025-08-12 | [plausible-tracker](https://www.npmjs.com/package/plausible-tracker) | 0.3.9 | 66.7k | MIT | - | **archived**；**npm deprecated**；最新发布 2024-05-27 |
| Umami | [umami-software/umami](https://github.com/umami-software/umami) | 38.6k | MIT | 2026-09-05 | - | - | - | - | - |  |
| rrweb (会话回放) | [rrweb-io/rrweb](https://github.com/rrweb-io/rrweb) | 20.1k | MIT | 2026-09-04 | [rrweb](https://www.npmjs.com/package/rrweb) | 2.1.1 | 2.7M | MIT | - |  |
| OpenReplay tracker | [openreplay/openreplay](https://github.com/openreplay/openreplay) | 12.7k | NOASSERTION | 2026-09-04 | [@openreplay/tracker](https://www.npmjs.com/package/@openreplay/tracker) | 18.1.5 | 249.3k | MIT | - |  |
| Highlight.run | [highlight/highlight](https://github.com/highlight/highlight) | 9.4k | NOASSERTION | 2026-08-20 | [highlight.run](https://www.npmjs.com/package/highlight.run) | 10.7.2 | 184.5k | Apache-2.0 | - |  |
| Lighthouse | [GoogleChrome/lighthouse](https://github.com/GoogleChrome/lighthouse) | 30.7k | Apache-2.0 | 2026-09-04 | [lighthouse](https://www.npmjs.com/package/lighthouse) | 13.4.1 | 4.4M | Apache-2.0 | - |  |
| unlighthouse | [harlan-zw/unlighthouse](https://github.com/harlan-zw/unlighthouse) | 4.8k | MIT | 2026-08-14 | [unlighthouse](https://www.npmjs.com/package/unlighthouse) | 0.18.0 | 41.7k | MIT | - |  |
| perfume.js | [Zizzamia/perfume.js](https://github.com/Zizzamia/perfume.js) | 3.2k | MIT | 2025-10-25 | [perfume.js](https://www.npmjs.com/package/perfume.js) | 9.4.0 | 33.7k | MIT | - | 最新发布 2024-03-22 |
| Partytown | [QwikDev/partytown](https://github.com/QwikDev/partytown) | 13.8k | MIT | 2026-08-25 | [@qwik.dev/partytown](https://www.npmjs.com/package/@qwik.dev/partytown) | 0.14.3 | 170.7k | MIT | - |  |
| why-did-you-render | [welldone-software/why-did-you-render](https://github.com/welldone-software/why-did-you-render) | 12.5k | MIT | 2026-04-15 | [@welldone-software/why-did-you-render](https://www.npmjs.com/package/@welldone-software/why-did-you-render) | 10.0.1 | 835.5k | MIT | ^19 |  |
| React Scan | [aidenybai/react-scan](https://github.com/aidenybai/react-scan) | 21.8k | MIT | 2026-08-16 | [react-scan](https://www.npmjs.com/package/react-scan) | 0.5.7 | 1.0M | MIT | ^16.8.0 \|\| ^17.0.0 \|\| ^18.0.0 \|\| ^19.0.0 |  |
| Million.js | [aidenybai/million](https://github.com/aidenybai/million) | 17.7k | MIT | 2026-05-20 | [million](https://www.npmjs.com/package/million) | 3.1.11 | 32.5k | MIT | - | 最新发布 2024-06-04 |
| Vercel Analytics | [vercel/analytics](https://github.com/vercel/analytics) | 515 | MIT | 2026-08-26 | [@vercel/analytics](https://www.npmjs.com/package/@vercel/analytics) | 2.0.1 | 6.0M | MIT | ^18 \|\| ^19 \|\| ^19.0.0-rc |  |
| Vercel Speed Insights | [vercel/speed-insights](https://github.com/vercel/speed-insights) | 114 | MIT | 2026-07-08 | [@vercel/speed-insights](https://www.npmjs.com/package/@vercel/speed-insights) | 2.0.0 | 4.0M | Apache-2.0 | ^18 \|\| ^19 \|\| ^19.0.0-rc |  |
| Bugsnag JS | [bugsnag/bugsnag-js](https://github.com/bugsnag/bugsnag-js) | 894 | MIT | 2026-09-02 | [@bugsnag/js](https://www.npmjs.com/package/@bugsnag/js) | 8.10.0 | 1.2M | MIT | - |  |
| GlitchTip / Sentry compat | - | - | - | - | - | - | - | - | - |  |

**一句话推荐**：Core Web Vitals 采集用 **web-vitals**（Apache-2.0，38.9M/周）；错误追踪 **@sentry/react**（MIT SDK；Sentry 服务端为 FSL-1.1 许可，[LICENSE](https://github.com/getsentry/sentry/blob/master/LICENSE.md)，自托管需注意）；厂商中立走 OpenTelemetry Web / Grafana Faro（Apache-2.0）；产品分析 PostHog JS（npm `Apache-2.0 AND MIT`）或自托管 Umami（MIT，无前端 npm 包）；会话回放底层 **rrweb**（MIT）。开发期性能用 React Scan（MIT，1.0M/周）。**注意**：Plausible tracker archived + deprecated（官方改用 script 引入）；perfume.js、Million.js 2024 年后无发版；Highlight.run / OpenReplay / Bugsnag SDK 开源但依赖各自后端；Vercel Analytics/Speed Insights 仅 Vercel 平台。

## 29. 可视化搭建 / 页面编辑器 / 低代码 / 节点图 / 布局

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| Puck | [puckeditor/puck](https://github.com/puckeditor/puck) | 13.3k | MIT | 2026-09-04 | [@puckeditor/core](https://www.npmjs.com/package/@puckeditor/core) | 0.23.0 | 177.2k | MIT | ^18.0.0 \|\| ^19.0.0 |  |
| craft.js | [prevwong/craft.js](https://github.com/prevwong/craft.js) | 8.7k | MIT | 2025-02-14 | [@craftjs/core](https://www.npmjs.com/package/@craftjs/core) | 0.2.12 | 68.9k | MIT | ^16.8.0 \|\| ^17 \|\| ^18 \|\| ^19 |  |
| GrapesJS | [GrapesJS/grapesjs](https://github.com/GrapesJS/grapesjs) | 26.2k | NOASSERTION | 2026-08-26 | [grapesjs](https://www.npmjs.com/package/grapesjs) | 0.23.6 | 347.5k | BSD-3-Clause | - |  |
| Builder.io SDK React | [BuilderIO/builder](https://github.com/BuilderIO/builder) | 8.8k | MIT | 2026-09-04 | [@builder.io/react](https://www.npmjs.com/package/@builder.io/react) | 9.4.4 | 85.1k | MIT | >=16.8.0 \|\| ^19.0.0-rc |  |
| Plasmic | [plasmicapp/plasmic](https://github.com/plasmicapp/plasmic) | 7.0k | MIT | 2026-09-04 | [@plasmicapp/loader-react](https://www.npmjs.com/package/@plasmicapp/loader-react) | 2.0.22 | 10.8k | MIT | >=18.0.0 |  |
| Webstudio | [webstudio-is/webstudio](https://github.com/webstudio-is/webstudio) | 8.9k | AGPL-3.0 | 2026-09-05 | - | - | - | - | - |  |
| react-email | [resend/react-email](https://github.com/resend/react-email) | 19.7k | MIT | 2026-09-03 | [@react-email/components](https://www.npmjs.com/package/@react-email/components) | 1.0.12 | 5.7M | MIT | ^18.0 \|\| ^19.0 \|\| ^19.0.0-rc | **npm deprecated** |
| MJML | [mjmlio/mjml](https://github.com/mjmlio/mjml) | 18.2k | MIT | 2026-09-03 | [mjml](https://www.npmjs.com/package/mjml) | 5.4.0 | 2.0M | MIT | - |  |
| Unlayer (react-email-editor) | [unlayer/react-email-editor](https://github.com/unlayer/react-email-editor) | 5.2k | MIT | 2026-09-03 | [react-email-editor](https://www.npmjs.com/package/react-email-editor) | 2.1.2 | 256.5k | MIT | >=16.8 |  |
| Easy Email | [zalify/easy-email](https://github.com/zalify/easy-email) | 3.0k | MIT | 2026-08-13 | [easy-email-editor](https://www.npmjs.com/package/easy-email-editor) | 4.17.1 | 18.5k | MIT | ^18.2.0 |  |
| Form.io React | [formio/react](https://github.com/formio/react) | 370 | MIT | 2026-07-09 | [@formio/react](https://www.npmjs.com/package/@formio/react) | 6.2.1 | 26.7k | MIT | >=17 |  |
| SurveyJS (form library) | [surveyjs/survey-library](https://github.com/surveyjs/survey-library) | 4.9k | MIT | 2026-09-05 | [survey-react-ui](https://www.npmjs.com/package/survey-react-ui) | 3.0.3 | 242.6k | MIT | ^16.5.0 \|\| ^17.0.1 \|\| ^18.1.0 \|\| ^19.0.0 |  |
| react-jsonschema-form | [rjsf-team/react-jsonschema-form](https://github.com/rjsf-team/react-jsonschema-form) | 15.9k | Apache-2.0 | 2026-09-04 | [@rjsf/core](https://www.npmjs.com/package/@rjsf/core) | 6.8.0 | 1.2M | Apache-2.0 | >=18 |  |
| Formily (阿里) | [alibaba/formily](https://github.com/alibaba/formily) | 12.6k | MIT | 2025-06-21 | [@formily/react](https://www.npmjs.com/package/@formily/react) | 2.3.7 | 38.6k | MIT | >=16.8.0 |  |
| amis (百度) | [baidu/amis](https://github.com/baidu/amis) | 18.9k | Apache-2.0 | 2026-03-18 | [amis](https://www.npmjs.com/package/amis) | 6.13.0 | 4.9k | Apache-2.0 | >=16.8.6 |  |
| LowCodeEngine (阿里) | [alibaba/lowcode-engine](https://github.com/alibaba/lowcode-engine) | 15.9k | MIT | 2025-03-10 | [@alilc/lowcode-engine](https://www.npmjs.com/package/@alilc/lowcode-engine) | 1.3.4 | 478 | MIT | - |  |
| Tmagic Editor (腾讯) | [Tencent/tmagic-editor](https://github.com/Tencent/tmagic-editor) | 4.9k | NOASSERTION | 2026-09-04 | [@tmagic/editor](https://www.npmjs.com/package/@tmagic/editor) | 1.7.13 | 659 | Apache-2.0 | - |  |
| React Flow (xyflow) | [xyflow/xyflow](https://github.com/xyflow/xyflow) | 38.3k | MIT | 2026-09-05 | [@xyflow/react](https://www.npmjs.com/package/@xyflow/react) | 12.11.6 | 11.2M | MIT | >=17 |  |
| Rete.js | [retejs/rete](https://github.com/retejs/rete) | 12.2k | MIT | 2026-07-24 | [rete](https://www.npmjs.com/package/rete) | 2.0.6 | 94.7k | MIT | - |  |
| LogicFlow (滴滴) | [didi/LogicFlow](https://github.com/didi/LogicFlow) | 11.7k | Apache-2.0 | 2026-07-30 | [@logicflow/core](https://www.npmjs.com/package/@logicflow/core) | 2.2.5 | 17.2k | Apache-2.0 | - |  |
| AntV X6 | [antvis/X6](https://github.com/antvis/X6) | 6.7k | MIT | 2026-08-11 | [@antv/x6](https://www.npmjs.com/package/@antv/x6) | 3.1.8 | 100.1k | MIT | - |  |
| JointJS | [clientIO/joint](https://github.com/clientIO/joint) | 5.4k | MPL-2.0 | 2026-09-04 | [@joint/core](https://www.npmjs.com/package/@joint/core) | 4.3.3 | 47.4k | MPL-2.0 | - |  |
| react-grid-layout | [react-grid-layout/react-grid-layout](https://github.com/react-grid-layout/react-grid-layout) | 22.4k | MIT | 2026-08-31 | [react-grid-layout](https://www.npmjs.com/package/react-grid-layout) | 2.2.4 | 3.9M | MIT | >= 16.3.0 |  |
| Gridstack | [gridstack/gridstack.js](https://github.com/gridstack/gridstack.js) | 9.1k | MIT | 2026-09-04 | [gridstack](https://www.npmjs.com/package/gridstack) | 13.2.0 | 625.6k | MIT | - |  |
| react-mosaic | [nomcopter/react-mosaic](https://github.com/nomcopter/react-mosaic) | 4.8k | NOASSERTION | 2026-08-06 | [react-mosaic-component](https://www.npmjs.com/package/react-mosaic-component) | 7.0.0 | 78.2k | Apache-2.0 | 16 - 19 |  |
| dockview | [mathuo/dockview](https://github.com/mathuo/dockview) | 3.4k | NOASSERTION | 2026-09-04 | [dockview](https://www.npmjs.com/package/dockview) | 8.2.0 | 238.0k | MIT | - |  |

**一句话推荐**：React 可视化页面编辑器选 **Puck**（MIT，13.3k★，包名已迁至 `@puckeditor/core`，旧包 `@measured/puck` 已 deprecated）；craft.js 停在 0.2.x 且 2025-02 后无 push；HTML 拖拽建站用 GrapesJS（BSD-3）。邮件模板 **react-email**（MIT；注意 `@react-email/components` 最新版 1.0.12 被标 deprecated，需确认官方包名迁移）或 MJML。JSON Schema 表单用 **react-jsonschema-form**（Apache-2.0，1.2M/周）；国内低代码（amis / LowCodeEngine / Formily / Tmagic）活跃度普遍下降（LowCodeEngine 周下载 478、Formily 2025-05 后无发版）。节点图 **React Flow**（MIT，11.2M/周）；仪表盘布局 **react-grid-layout**（MIT）或 Gridstack；IDE 式面板 dockview。**注意**：Webstudio 为 **AGPL-3.0**（无 npm 库）；JointJS 为 **MPL-2.0**（JointJS+ 为商业版）；Builder.io / Plasmic SDK 开源但绑定托管服务。

## 30. 服务端 / Node 端渲图（OG 图、截图、PDF、Canvas）

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| Satori (Vercel) | [vercel/satori](https://github.com/vercel/satori) | 13.9k | MPL-2.0 | 2026-08-24 | [satori](https://www.npmjs.com/package/satori) | 0.33.4 | 3.4M | MPL-2.0 | - |  |
| @vercel/og | [vercel/next.js](https://github.com/vercel/next.js) | 142.1k | MIT | 2026-09-05 | [@vercel/og](https://www.npmjs.com/package/@vercel/og) | 1.0.2 | 1.9M | MPL-2.0 | - |  |
| resvg-js | [thx/resvg-js](https://github.com/thx/resvg-js) | 2.0k | MPL-2.0 | 2026-06-30 | [@resvg/resvg-js](https://www.npmjs.com/package/@resvg/resvg-js) | 2.6.2 | 2.6M | MPL-2.0 | - | 最新发布 2024-03-26 |
| sharp | [lovell/sharp](https://github.com/lovell/sharp) | 32.6k | Apache-2.0 | 2026-09-05 | [sharp](https://www.npmjs.com/package/sharp) | 0.35.4 | 93.9M | Apache-2.0 | - |  |
| jimp | [jimp-dev/jimp](https://github.com/jimp-dev/jimp) | 14.7k | MIT | 2026-04-07 | [jimp](https://www.npmjs.com/package/jimp) | 1.6.1 | 3.5M | MIT | - |  |
| @napi-rs/canvas | [Brooooooklyn/canvas](https://github.com/Brooooooklyn/canvas) | 2.3k | MIT | 2026-09-04 | [@napi-rs/canvas](https://www.npmjs.com/package/@napi-rs/canvas) | 1.0.8 | 22.1M | MIT | - |  |
| node-canvas | [Automattic/node-canvas](https://github.com/Automattic/node-canvas) | 10.7k | NONE | 2026-08-24 | [canvas](https://www.npmjs.com/package/canvas) | 3.2.3 | 8.1M | MIT | - |  |
| skia-canvas | [samizdatco/skia-canvas](https://github.com/samizdatco/skia-canvas) | 2.6k | MIT | 2026-08-28 | [skia-canvas](https://www.npmjs.com/package/skia-canvas) | 3.0.8 | 177.9k | MIT | - |  |
| Puppeteer | [puppeteer/puppeteer](https://github.com/puppeteer/puppeteer) | 95.5k | Apache-2.0 | 2026-09-05 | [puppeteer](https://www.npmjs.com/package/puppeteer) | 25.10.0 | 11.9M | Apache-2.0 | - |  |
| Playwright (截图, 见 §14) | - | - | - | - | - | - | - | - | - |  |
| html-to-image | [bubkoo/html-to-image](https://github.com/bubkoo/html-to-image) | 7.2k | MIT | 2026-05-28 | [html-to-image](https://www.npmjs.com/package/html-to-image) | 1.11.13 | 6.5M | MIT | - |  |
| modern-screenshot | [qq15725/modern-screenshot](https://github.com/qq15725/modern-screenshot) | 2.1k | MIT | 2026-04-16 | [modern-screenshot](https://www.npmjs.com/package/modern-screenshot) | 4.7.0 | 2.5M | MIT | - |  |
| dom-to-image-more | [1904labs/dom-to-image-more](https://github.com/1904labs/dom-to-image-more) | 680 | NOASSERTION | 2026-08-10 | [dom-to-image-more](https://www.npmjs.com/package/dom-to-image-more) | 3.10.2 | 291.3k | MIT | - |  |
| takumi (Rust satori) | [kane50613/takumi](https://github.com/kane50613/takumi) | 2.9k | Apache-2.0 | 2026-09-05 | [@takumi-rs/core](https://www.npmjs.com/package/@takumi-rs/core) | 2.13.6 | 352.9k | (MIT OR Apache-2.0) | - |  |
| og-image (workers-og) | [kvnang/workers-og](https://github.com/kvnang/workers-og) | 356 | MIT | 2025-06-12 | [workers-og](https://www.npmjs.com/package/workers-og) | 0.0.27 | 77.9k | - | - |  |
| pdfmake | [bpampuch/pdfmake](https://github.com/bpampuch/pdfmake) | 12.3k | NOASSERTION | 2026-06-12 | [pdfmake](https://www.npmjs.com/package/pdfmake) | 0.3.11 | 2.6M | MIT | - |  |
| jsPDF | [parallax/jsPDF](https://github.com/parallax/jsPDF) | 31.3k | MIT | 2026-09-03 | [jspdf](https://www.npmjs.com/package/jspdf) | 4.2.1 | 15.2M | MIT | - |  |
| Gotenberg | [gotenberg/gotenberg](https://github.com/gotenberg/gotenberg) | 13.0k | MIT | 2026-09-05 | - | - | - | - | - |  |

**一句话推荐**：OG 图生成 **Satori**（Vercel，**MPL-2.0**，3.4M/周）+ **resvg-js**（MPL-2.0，但 latest 停在 2024-03）；Next.js 直接用 `@vercel/og`（npm MPL-2.0，含 Satori）；Rust 实现的 **takumi**（MIT/Apache 双许可，2026-09 活跃）是 Satori 的宽松许可替代。位图处理 **sharp**（Apache-2.0，93.9M/周）；Node Canvas 首选 **@napi-rs/canvas**（MIT，22.1M/周，预编译无 node-gyp）。浏览器端 DOM 截图用 **modern-screenshot** 或 html-to-image（均 MIT）；前端 PDF 生成 **jsPDF**（MIT，15.2M/周）或 pdfmake；服务端 HTML→PDF 用 Puppeteer/Playwright 或 Gotenberg（MIT，Docker 服务）。MPL-2.0 为文件级 copyleft，作为依赖使用不影响业务代码闭源，但修改其源码文件需开源。

## 31. HTTP 客户端 / 工具函数 / 数据处理

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| ky (见 §0) | [sindresorhus/ky](https://github.com/sindresorhus/ky) | 17.1k | MIT | 2026-09-02 | [ky](https://www.npmjs.com/package/ky) | 2.1.0 | 7.4M | MIT | - |  |
| ofetch | [unjs/ofetch](https://github.com/unjs/ofetch) | 5.4k | MIT | 2026-09-03 | [ofetch](https://www.npmjs.com/package/ofetch) | 1.5.1 | 27.2M | MIT | - |  |
| wretch | [elbywan/wretch](https://github.com/elbywan/wretch) | 5.2k | MIT | 2026-06-19 | [wretch](https://www.npmjs.com/package/wretch) | 3.0.9 | 282.2k | MIT | - |  |
| up-fetch | [L-Blondy/up-fetch](https://github.com/L-Blondy/up-fetch) | 1.4k | MIT | 2026-09-01 | [up-fetch](https://www.npmjs.com/package/up-fetch) | 2.6.1 | 28.3k | MIT | - |  |
| better-fetch | [Bekacru/better-fetch](https://github.com/Bekacru/better-fetch) | 1.0k | MIT | 2026-09-05 | [@better-fetch/fetch](https://www.npmjs.com/package/@better-fetch/fetch) | 1.3.1 | 7.5M | MIT | - |  |
| es-toolkit | [toss/es-toolkit](https://github.com/toss/es-toolkit) | 11.3k | MIT | 2026-09-03 | [es-toolkit](https://www.npmjs.com/package/es-toolkit) | 1.52.0 | 46.1M | MIT | - |  |
| lodash | [lodash/lodash](https://github.com/lodash/lodash) | 61.3k | NOASSERTION | 2026-07-03 | [lodash](https://www.npmjs.com/package/lodash) | 4.18.1 | 173.7M | MIT | - |  |
| lodash-es | - | - | - | - | [lodash-es](https://www.npmjs.com/package/lodash-es) | 4.18.1 | 46.5M | MIT | - |  |
| Radash | [sodiray/radash](https://github.com/sodiray/radash) | 4.8k | MIT | 2025-06-18 | [radash](https://www.npmjs.com/package/radash) | 12.1.1 | 2.1M | MIT | - |  |
| remeda | [remeda/remeda](https://github.com/remeda/remeda) | 5.4k | MIT | 2026-09-03 | [remeda](https://www.npmjs.com/package/remeda) | 2.45.0 | 10.3M | MIT | - |  |
| Ramda | [ramda/ramda](https://github.com/ramda/ramda) | 24.1k | MIT | 2026-07-26 | [ramda](https://www.npmjs.com/package/ramda) | 0.32.0 | 14.3M | MIT | - |  |
| Effect | [Effect-TS/effect](https://github.com/Effect-TS/effect) | 15.9k | MIT | 2026-09-05 | [effect](https://www.npmjs.com/package/effect) | 3.22.1 | 33.6M | MIT | - |  |
| neverthrow | [supermacro/neverthrow](https://github.com/supermacro/neverthrow) | 7.7k | MIT | 2026-02-14 | [neverthrow](https://www.npmjs.com/package/neverthrow) | 8.2.0 | 2.7M | MIT | - |  |
| ts-pattern | [gvergnaud/ts-pattern](https://github.com/gvergnaud/ts-pattern) | 15.1k | MIT | 2026-09-03 | [ts-pattern](https://www.npmjs.com/package/ts-pattern) | 5.9.0 | 6.7M | MIT | - |  |
| type-fest | [sindresorhus/type-fest](https://github.com/sindresorhus/type-fest) | 17.4k | CC0-1.0 | 2026-09-02 | [type-fest](https://www.npmjs.com/package/type-fest) | 5.9.0 | 385.6M | (MIT OR CC0-1.0) | - |  |
| immer | [immerjs/immer](https://github.com/immerjs/immer) | 29.0k | MIT | 2026-09-05 | [immer](https://www.npmjs.com/package/immer) | 11.1.18 | 59.9M | MIT | - |  |
| mutative | [unadlib/mutative](https://github.com/unadlib/mutative) | 2.0k | MIT | 2026-08-13 | [mutative](https://www.npmjs.com/package/mutative) | 1.3.0 | 1.1M | MIT | - |  |
| nanoid | [ai/nanoid](https://github.com/ai/nanoid) | 27.0k | MIT | 2026-09-01 | [nanoid](https://www.npmjs.com/package/nanoid) | 6.0.1 | 241.9M | MIT | - |  |
| uuid | [uuidjs/uuid](https://github.com/uuidjs/uuid) | 15.3k | MIT | 2026-08-18 | [uuid](https://www.npmjs.com/package/uuid) | 14.0.2 | 294.9M | MIT | - |  |
| ulid | [ulid/javascript](https://github.com/ulid/javascript) | 3.4k | MIT | 2026-02-27 | [ulid](https://www.npmjs.com/package/ulid) | 3.0.2 | 10.8M | MIT | - |  |
| p-limit | [sindresorhus/p-limit](https://github.com/sindresorhus/p-limit) | 2.9k | MIT | 2026-08-31 | [p-limit](https://www.npmjs.com/package/p-limit) | 7.3.2 | 333.1M | MIT | - |  |
| p-queue | [sindresorhus/p-queue](https://github.com/sindresorhus/p-queue) | 4.3k | MIT | 2026-07-22 | [p-queue](https://www.npmjs.com/package/p-queue) | 9.3.3 | 35.5M | MIT | - |  |
| p-retry | [sindresorhus/p-retry](https://github.com/sindresorhus/p-retry) | 1.0k | MIT | 2026-09-01 | [p-retry](https://www.npmjs.com/package/p-retry) | 8.0.1 | 51.6M | MIT | - |  |
| superjson | [flightcontrolhq/superjson](https://github.com/flightcontrolhq/superjson) | 5.3k | MIT | 2026-06-18 | [superjson](https://www.npmjs.com/package/superjson) | 2.2.6 | 10.2M | MIT | - |  |
| devalue | [Rich-Harris/devalue](https://github.com/Rich-Harris/devalue) | 2.8k | MIT | 2026-09-04 | [devalue](https://www.npmjs.com/package/devalue) | 5.9.2 | 12.7M | MIT | - |  |
| fast-deep-equal | [epoberezkin/fast-deep-equal](https://github.com/epoberezkin/fast-deep-equal) | 2.0k | MIT | 2023-10-05 | [fast-deep-equal](https://www.npmjs.com/package/fast-deep-equal) | 3.1.3 | 205.1M | MIT | - | 最新发布 2020-06-08 |
| dequal | [lukeed/dequal](https://github.com/lukeed/dequal) | 1.5k | MIT | 2026-04-10 | [dequal](https://www.npmjs.com/package/dequal) | 2.0.3 | 91.0M | MIT | - | 最新发布 2022-07-11 |
| big.js | [MikeMcl/big.js](https://github.com/MikeMcl/big.js) | 5.2k | MIT | 2025-04-22 | [big.js](https://www.npmjs.com/package/big.js) | 7.0.1 | 35.5M | MIT | - |  |
| decimal.js | [MikeMcl/decimal.js](https://github.com/MikeMcl/decimal.js) | 7.3k | MIT | 2026-08-30 | [decimal.js](https://www.npmjs.com/package/decimal.js) | 10.6.0 | 85.0M | MIT | - |  |
| dinero.js | [dinerojs/dinero.js](https://github.com/dinerojs/dinero.js) | 6.8k | MIT | 2026-09-05 | [dinero.js](https://www.npmjs.com/package/dinero.js) | 2.0.2 | 560.5k | MIT | - |  |
| currency.js | [scurker/currency.js](https://github.com/scurker/currency.js) | 3.4k | MIT | 2026-09-04 | [currency.js](https://www.npmjs.com/package/currency.js) | 2.0.4 | 808.9k | MIT | - | 最新发布 2021-05-19 |
| fuse.js | [krisk/Fuse](https://github.com/krisk/Fuse) | 20.5k | Apache-2.0 | 2026-08-09 | [fuse.js](https://www.npmjs.com/package/fuse.js) | 7.5.0 | 13.9M | Apache-2.0 | - |  |
| minisearch | [lucaong/minisearch](https://github.com/lucaong/minisearch) | 6.1k | MIT | 2025-09-16 | [minisearch](https://www.npmjs.com/package/minisearch) | 7.2.0 | 2.6M | MIT | - |  |
| Orama | [oramasearch/orama](https://github.com/oramasearch/orama) | 10.5k | NOASSERTION | 2026-08-04 | [@orama/orama](https://www.npmjs.com/package/@orama/orama) | 3.1.18 | 1.3M | Apache-2.0 | - |  |
| FlexSearch | [nextapps-de/flexsearch](https://github.com/nextapps-de/flexsearch) | 13.8k | Apache-2.0 | 2026-06-28 | [flexsearch](https://www.npmjs.com/package/flexsearch) | 0.8.212 | 1.4M | Apache-2.0 | - |  |
| match-sorter | [kentcdodds/match-sorter](https://github.com/kentcdodds/match-sorter) | 4.1k | MIT | 2026-05-13 | [match-sorter](https://www.npmjs.com/package/match-sorter) | 8.3.0 | 3.6M | MIT | - |  |
| comlink | [GoogleChromeLabs/comlink](https://github.com/GoogleChromeLabs/comlink) | 12.8k | Apache-2.0 | 2026-09-05 | [comlink](https://www.npmjs.com/package/comlink) | 4.4.2 | 2.7M | Apache-2.0 | - |  |
| mitt | [developit/mitt](https://github.com/developit/mitt) | 11.9k | MIT | 2024-08-14 | [mitt](https://www.npmjs.com/package/mitt) | 3.0.1 | 31.5M | MIT | - | 最新发布 2023-07-04 |
| nanoevents | [ai/nanoevents](https://github.com/ai/nanoevents) | 1.6k | MIT | 2026-07-22 | [nanoevents](https://www.npmjs.com/package/nanoevents) | 10.0.0 | 1.2M | MIT | - |  |
| eventemitter3 | [primus/eventemitter3](https://github.com/primus/eventemitter3) | 3.5k | MIT | 2026-01-19 | [eventemitter3](https://www.npmjs.com/package/eventemitter3) | 5.0.4 | 158.7M | MIT | - |  |
| query-string | [sindresorhus/query-string](https://github.com/sindresorhus/query-string) | 6.9k | MIT | 2026-09-01 | [query-string](https://www.npmjs.com/package/query-string) | 9.5.1 | 25.3M | MIT | - |  |
| qs | [ljharb/qs](https://github.com/ljharb/qs) | 8.9k | BSD-3-Clause | 2026-08-31 | [qs](https://www.npmjs.com/package/qs) | 6.16.0 | 183.3M | BSD-3-Clause | - |  |
| js-cookie | [js-cookie/js-cookie](https://github.com/js-cookie/js-cookie) | 22.6k | MIT | 2026-08-10 | [js-cookie](https://www.npmjs.com/package/js-cookie) | 3.0.8 | 30.5M | MIT | - |  |
| copy-to-clipboard | [sudodoki/copy-to-clipboard](https://github.com/sudodoki/copy-to-clipboard) | 1.4k | MIT | 2026-08-05 | [copy-to-clipboard](https://www.npmjs.com/package/copy-to-clipboard) | 4.0.2 | 11.9M | MIT | - |  |
| validator.js | [validatorjs/validator.js](https://github.com/validatorjs/validator.js) | 23.7k | MIT | 2026-08-15 | [validator](https://www.npmjs.com/package/validator) | 13.15.35 | 26.5M | MIT | - |  |
| libphonenumber-js | [catamphetamine/libphonenumber-js](https://github.com/catamphetamine/libphonenumber-js) | 3.0k | MIT | 2026-06-18 | [libphonenumber-js](https://www.npmjs.com/package/libphonenumber-js) | 1.13.12 | 26.9M | MIT | - |  |
| DOMPurify | [cure53/DOMPurify](https://github.com/cure53/DOMPurify) | 17.4k | Apache-2.0 | 2026-09-05 | [dompurify](https://www.npmjs.com/package/dompurify) | 3.4.14 | 64.3M | (MPL-2.0 OR Apache-2.0) | - |  |
| sanitize-html | [apostrophecms/sanitize-html](https://github.com/apostrophecms/sanitize-html) | 4.1k | MIT | 2026-02-26 | [sanitize-html](https://www.npmjs.com/package/sanitize-html) | 2.17.7 | 10.3M | MIT | - | **archived** |
| he (HTML entities) | [mathiasbynens/he](https://github.com/mathiasbynens/he) | 3.6k | MIT | 2021-12-29 | [he](https://www.npmjs.com/package/he) | 1.2.0 | 44.7M | MIT | - | 最新发布 2018-09-23 |
| marked | [markedjs/marked](https://github.com/markedjs/marked) | 37.1k | NOASSERTION | 2026-09-05 | [marked](https://www.npmjs.com/package/marked) | 18.0.11 | 73.3M | MIT | - |  |
| markdown-it | [markdown-it/markdown-it](https://github.com/markdown-it/markdown-it) | 21.9k | MIT | 2026-08-27 | [markdown-it](https://www.npmjs.com/package/markdown-it) | 15.0.1 | 30.9M | MIT | - |  |
| Papa Parse (CSV) | [mholt/PapaParse](https://github.com/mholt/PapaParse) | 13.6k | MIT | 2026-09-01 | [papaparse](https://www.npmjs.com/package/papaparse) | 5.7.0 | 15.5M | MIT | - |  |
| SheetJS (xlsx CE) | [SheetJS/sheetjs](https://github.com/SheetJS/sheetjs) | 36.3k | Apache-2.0 | 2024-04-18 | [xlsx](https://www.npmjs.com/package/xlsx) | 0.18.5 | 12.6M | Apache-2.0 | - | 最新发布 2022-03-24 |
| ExcelJS | [exceljs/exceljs](https://github.com/exceljs/exceljs) | 15.5k | MIT | 2025-01-21 | [exceljs](https://www.npmjs.com/package/exceljs) | 4.4.0 | 14.2M | MIT | - | 最新发布 2023-10-19 |
| yaml | [eemeli/yaml](https://github.com/eemeli/yaml) | 1.7k | ISC | 2026-08-01 | [yaml](https://www.npmjs.com/package/yaml) | 2.9.0 | 202.4M | ISC | - |  |
| chroma.js | [gka/chroma.js](https://github.com/gka/chroma.js) | 10.6k | NOASSERTION | 2026-06-01 | [chroma-js](https://www.npmjs.com/package/chroma-js) | 3.2.0 | 3.5M | (BSD-3-Clause AND Apache-2.0) | - |  |
| colord | [omgovich/colord](https://github.com/omgovich/colord) | 1.9k | MIT | 2026-09-01 | [colord](https://www.npmjs.com/package/colord) | 2.10.0 | 20.7M | MIT | - |  |
| culori | [Evercoder/culori](https://github.com/Evercoder/culori) | 1.2k | MIT | 2026-07-02 | [culori](https://www.npmjs.com/package/culori) | 4.0.2 | 1.9M | MIT | - |  |
| pretty-bytes | [sindresorhus/pretty-bytes](https://github.com/sindresorhus/pretty-bytes) | 1.3k | MIT | 2026-09-03 | [pretty-bytes](https://www.npmjs.com/package/pretty-bytes) | 7.1.3 | 32.2M | MIT | - |  |
| filesize | [avoidwork/filesize.js](https://github.com/avoidwork/filesize.js) | 1.7k | BSD-3-Clause | 2026-09-03 | [filesize](https://www.npmjs.com/package/filesize) | 11.0.23 | 16.2M | BSD-3-Clause | - |  |
| hotkeys-js | [jaywcjlove/hotkeys-js](https://github.com/jaywcjlove/hotkeys-js) | 7.1k | MIT | 2026-08-28 | [hotkeys-js](https://www.npmjs.com/package/hotkeys-js) | 4.0.7 | 1.4M | MIT | - |  |
| tinykeys | [jamiebuilds/tinykeys](https://github.com/jamiebuilds/tinykeys) | 4.1k | MIT | 2026-05-26 | [tinykeys](https://www.npmjs.com/package/tinykeys) | 4.0.0 | 310.7k | MIT | - |  |
| react-hotkeys-hook | [JohannesKlauss/react-hotkeys-hook](https://github.com/JohannesKlauss/react-hotkeys-hook) | 3.5k | MIT | 2026-09-03 | [react-hotkeys-hook](https://www.npmjs.com/package/react-hotkeys-hook) | 5.3.3 | 4.4M | MIT | >=16.8.0 |  |
| idb (见 §23) | - | - | - | - | - | - | - | - | - |  |

**一句话推荐**：HTTP 用 **ky**（MIT，fetch 封装，7.4M/周）或 ofetch（unjs，27.2M/周）；工具函数 **es-toolkit**（MIT，46.1M/周，lodash 兼容层）替代 lodash（lodash 4.18 于 2026-04 恢复发版，GitHub SPDX NOASSERTION、npm MIT）；不可变更新 immer（59.9M/周）；类型工具 type-fest（npm `MIT OR CC0-1.0`）；ID 用 nanoid / uuid；并发控制 p-limit / p-queue；模式匹配 ts-pattern；大数 decimal.js / big.js；货币 dinero.js（currency.js 2021 后无发版）；客户端搜索 **fuse.js**（Apache-2.0）或 minisearch/Orama；HTML 消毒 **DOMPurify**（npm `MPL-2.0 OR Apache-2.0`，可选 Apache）；sanitize-html 仓库已 archived；Markdown 解析 marked / markdown-it；CSV Papa Parse；xlsx 用 **ExcelJS**（MIT，但 2023-10 后无发版）——SheetJS 社区版 `xlsx` npm 停在 0.18.5（2022-03），新版仅从 cdn.sheetjs.com 分发；YAML 用 `yaml`（ISC）；颜色 colord / culori / chroma.js（npm `BSD-3 AND Apache-2.0`）；快捷键 react-hotkeys-hook / tinykeys / hotkeys-js。**长期无发版但仍被大量依赖**（功能已稳定）：fast-deep-equal（2020）、dequal（2022）、he（2018）、mitt（2023）。

## 32. 图片 / 媒体 / 视频 / 音频 / 扫码

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| react-image-crop | [DominicTobias/react-image-crop](https://github.com/DominicTobias/react-image-crop) | 4.1k | ISC | 2026-06-21 | [react-image-crop](https://www.npmjs.com/package/react-image-crop) | 11.1.2 | 2.5M | ISC | >=16.13.1 |  |
| react-easy-crop | [ValentinH/react-easy-crop](https://github.com/ValentinH/react-easy-crop) | 2.8k | MIT | 2026-09-05 | [react-easy-crop](https://www.npmjs.com/package/react-easy-crop) | 6.2.3 | 3.4M | MIT | >=16.4.0 |  |
| Cropper.js | [fengyuanchen/cropperjs](https://github.com/fengyuanchen/cropperjs) | 13.9k | MIT | 2026-09-05 | [cropperjs](https://www.npmjs.com/package/cropperjs) | 2.2.0 | 1.7M | MIT | - |  |
| react-advanced-cropper | [advanced-cropper/react-advanced-cropper](https://github.com/advanced-cropper/react-advanced-cropper) | 885 | NOASSERTION | 2026-07-25 | [react-advanced-cropper](https://www.npmjs.com/package/react-advanced-cropper) | 0.20.1 | 174.1k | MIT | >=16.8.0 |  |
| browser-image-compression | [Donaldcwl/browser-image-compression](https://github.com/Donaldcwl/browser-image-compression) | 1.7k | MIT | 2024-03-08 | [browser-image-compression](https://www.npmjs.com/package/browser-image-compression) | 2.0.2 | 1.5M | MIT | - | 最新发布 2023-03-06 |
| compressorjs | [fengyuanchen/compressorjs](https://github.com/fengyuanchen/compressorjs) | 5.8k | MIT | 2026-08-29 | [compressorjs](https://www.npmjs.com/package/compressorjs) | 1.3.0 | 452.6k | MIT | - |  |
| Squoosh (libs) | [GoogleChromeLabs/squoosh](https://github.com/GoogleChromeLabs/squoosh) | 25.8k | Apache-2.0 | 2026-09-04 | - | - | - | - | - |  |
| @jsquash/webp | [jamsinclair/jSquash](https://github.com/jamsinclair/jSquash) | 722 | Apache-2.0 | 2026-01-05 | [@jsquash/webp](https://www.npmjs.com/package/@jsquash/webp) | 1.5.0 | 209.6k | Apache-2.0 | - |  |
| exifr | [MikeKovarik/exifr](https://github.com/MikeKovarik/exifr) | 1.2k | MIT | 2024-03-29 | [exifr](https://www.npmjs.com/package/exifr) | 7.1.3 | 2.0M | MIT | - | 最新发布 2021-08-05 |
| heic2any | [alexcorvi/heic2any](https://github.com/alexcorvi/heic2any) | 883 | MIT | 2024-04-11 | [heic2any](https://www.npmjs.com/package/heic2any) | 0.0.4 | 1.2M | MIT | - | 最新发布 2023-03-29 |
| yet-another-react-lightbox | [igordanchenko/yet-another-react-lightbox](https://github.com/igordanchenko/yet-another-react-lightbox) | 1.3k | MIT | 2026-09-01 | [yet-another-react-lightbox](https://www.npmjs.com/package/yet-another-react-lightbox) | 3.32.2 | 554.4k | MIT | ^16.8.0 \|\| ^17 \|\| ^18 \|\| ^19 |  |
| PhotoSwipe | [dimsemenov/PhotoSwipe](https://github.com/dimsemenov/PhotoSwipe) | 25.2k | MIT | 2025-12-04 | [photoswipe](https://www.npmjs.com/package/photoswipe) | 5.4.4 | 545.3k | MIT | - | 最新发布 2024-05-24 |
| react-photo-album | [igordanchenko/react-photo-album](https://github.com/igordanchenko/react-photo-album) | 783 | MIT | 2026-08-31 | [react-photo-album](https://www.npmjs.com/package/react-photo-album) | 3.6.1 | 112.7k | MIT | ^18 \|\| ^19 |  |
| react-zoom-pan-pinch | [BetterTyped/react-zoom-pan-pinch](https://github.com/BetterTyped/react-zoom-pan-pinch) | 1.9k | MIT | 2026-09-04 | [react-zoom-pan-pinch](https://www.npmjs.com/package/react-zoom-pan-pinch) | 4.2.0 | 2.5M | MIT | * |  |
| Swiper | [nolimits4web/swiper](https://github.com/nolimits4web/swiper) | 41.9k | MIT | 2026-09-02 | [swiper](https://www.npmjs.com/package/swiper) | 14.2.0 | 4.3M | MIT | - |  |
| Embla (见 §0) | - | - | - | - | - | - | - | - | - |  |
| Keen Slider | [rcbyr/keen-slider](https://github.com/rcbyr/keen-slider) | 5.0k | MIT | 2026-01-22 | [keen-slider](https://www.npmjs.com/package/keen-slider) | 6.8.6 | 232.3k | MIT | - | 最新发布 2023-07-05 |
| unpic (响应式图片) | [ascorbic/unpic-img](https://github.com/ascorbic/unpic-img) | 2.1k | NONE | 2026-09-03 | [@unpic/react](https://www.npmjs.com/package/@unpic/react) | 1.0.2 | 1.3M | MIT | ^17.0.0 \|\| ^18.0.0 \|\| ^19.0.0 |  |
| vite-imagetools | [JonasKruckenberg/imagetools](https://github.com/JonasKruckenberg/imagetools) | 1.1k | MIT | 2026-09-05 | [vite-imagetools](https://www.npmjs.com/package/vite-imagetools) | 12.0.1 | 280.1k | MIT | - |  |
| Video.js | [videojs/video.js](https://github.com/videojs/video.js) | 39.9k | NOASSERTION | 2026-08-03 | [video.js](https://www.npmjs.com/package/video.js) | 8.24.0 | 1.1M | Apache-2.0 | - |  |
| Plyr | [sampotts/plyr](https://github.com/sampotts/plyr) | 30.0k | MIT | 2026-08-23 | [plyr](https://www.npmjs.com/package/plyr) | 3.8.4 | 407.1k | MIT | - |  |
| Vidstack | [vidstack/player](https://github.com/vidstack/player) | 3.7k | MIT | 2026-08-21 | [@vidstack/react](https://www.npmjs.com/package/@vidstack/react) | 0.6.15 | 301.9k | MIT | ^18.0.0 | 最新发布 2024-04-19 |
| react-player | [cookpete/react-player](https://github.com/cookpete/react-player) | 10.3k | MIT | 2025-11-13 | [react-player](https://www.npmjs.com/package/react-player) | 3.4.0 | 2.4M | MIT | ^17.0.2 \|\| ^18 \|\| ^19 |  |
| hls.js | [video-dev/hls.js](https://github.com/video-dev/hls.js) | 16.9k | NOASSERTION | 2026-09-04 | [hls.js](https://www.npmjs.com/package/hls.js) | 1.7.2 | 8.6M | Apache-2.0 | - |  |
| dash.js | [Dash-Industry-Forum/dash.js](https://github.com/Dash-Industry-Forum/dash.js) | 5.5k | NOASSERTION | 2026-09-01 | [dashjs](https://www.npmjs.com/package/dashjs) | 5.2.1 | 992.0k | BSD-3-Clause | - |  |
| Shaka Player | [shaka-project/shaka-player](https://github.com/shaka-project/shaka-player) | 8.2k | Apache-2.0 | 2026-09-04 | [shaka-player](https://www.npmjs.com/package/shaka-player) | 5.2.9 | 327.3k | Apache-2.0 | - |  |
| Howler.js | [goldfire/howler.js](https://github.com/goldfire/howler.js) | 25.3k | MIT | 2025-11-23 | [howler](https://www.npmjs.com/package/howler) | 2.2.4 | 967.0k | MIT | - | 最新发布 2023-09-19 |
| Tone.js | [Tonejs/Tone.js](https://github.com/Tonejs/Tone.js) | 14.7k | MIT | 2026-09-03 | [tone](https://www.npmjs.com/package/tone) | 15.1.22 | 227.4k | MIT | - |  |
| wavesurfer.js | [katspaugh/wavesurfer.js](https://github.com/katspaugh/wavesurfer.js) | 10.4k | BSD-3-Clause | 2026-09-03 | [wavesurfer.js](https://www.npmjs.com/package/wavesurfer.js) | 7.12.11 | 1.3M | BSD-3-Clause | - |  |
| Peaks.js (BBC) | [bbc/peaks.js](https://github.com/bbc/peaks.js) | 3.4k | LGPL-3.0 | 2025-11-08 | [peaks.js](https://www.npmjs.com/package/peaks.js) | 4.0.0 | 10.1k | LGPL-3.0 | - |  |
| ffmpeg.wasm | [ffmpegwasm/ffmpeg.wasm](https://github.com/ffmpegwasm/ffmpeg.wasm) | 17.8k | MIT | 2026-02-01 | [@ffmpeg/ffmpeg](https://www.npmjs.com/package/@ffmpeg/ffmpeg) | 0.12.15 | 709.5k | MIT | - |  |
| mediabunny | [Vanilagy/mediabunny](https://github.com/Vanilagy/mediabunny) | 7.1k | MPL-2.0 | 2026-09-04 | [mediabunny](https://www.npmjs.com/package/mediabunny) | 1.55.7 | 2.7M | MPL-2.0 | - |  |
| Remotion | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | 58.4k | NOASSERTION | 2026-09-05 | [remotion](https://www.npmjs.com/package/remotion) | 4.0.521 | 1.7M | SEE LICENSE IN LICENSE.md | >=16.8.0 |  |
| react-webcam | [mozmorris/react-webcam](https://github.com/mozmorris/react-webcam) | 1.8k | MIT | 2026-03-10 | [react-webcam](https://www.npmjs.com/package/react-webcam) | 7.2.0 | 480.0k | MIT | >=16.2.0 | 最新发布 2023-10-25 |
| html5-qrcode | [mebjas/html5-qrcode](https://github.com/mebjas/html5-qrcode) | 6.2k | Apache-2.0 | 2025-12-01 | [html5-qrcode](https://www.npmjs.com/package/html5-qrcode) | 2.3.8 | 1.5M | Apache-2.0 | - | 最新发布 2023-04-15 |
| zxing-wasm | [Sec-ant/zxing-wasm](https://github.com/Sec-ant/zxing-wasm) | 265 | MIT | 2026-09-01 | [zxing-wasm](https://www.npmjs.com/package/zxing-wasm) | 3.1.3 | 1.9M | MIT | - |  |
| qr-scanner | [nimiq/qr-scanner](https://github.com/nimiq/qr-scanner) | 2.9k | MIT | 2024-03-30 | [qr-scanner](https://www.npmjs.com/package/qr-scanner) | 1.4.2 | 271.2k | MIT | - | 最新发布 2022-11-23 |
| react-pdf-highlighter (见 §10) | - | - | - | - | - | - | - | - | - |  |
| Motion Canvas | [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | 19.1k | MIT | 2026-07-02 | [@motion-canvas/core](https://www.npmjs.com/package/@motion-canvas/core) | 3.17.2 | 2.4k | MIT | - |  |
| Lottie (见 §4) | - | - | - | - | - | - | - | - | - |  |

**一句话推荐**：图片裁剪 **react-easy-crop**（MIT，3.4M/周，2026-07 发版）或 Cropper.js 2；客户端压缩 compressorjs（2026-04 发版；browser-image-compression 2023 后无发版）；WebP/AVIF 编解码 `@jsquash/*`（Squoosh 内核，Apache-2.0）；灯箱 **yet-another-react-lightbox**（MIT，peer 到 React 19）；轮播 Swiper（MIT，4.3M/周）或 §0 的 Embla；响应式图片 unpic。视频播放：HLS 用 **hls.js**（npm Apache-2.0，8.6M/周）、DASH 用 dash.js（BSD-3）或 Shaka Player（Apache-2.0）；播放器 UI **Video.js**（Apache-2.0）、Plyr（MIT）、react-player（MIT，v3 支持 React 19）；Vidstack 停在 0.6.x（2024-04）。音频 wavesurfer.js（BSD-3）、Tone.js（MIT）、Howler（MIT，2023 后无发版）。浏览器端转码 ffmpeg.wasm（MIT）或 **mediabunny**（**MPL-2.0**，2.7M/周，活跃）。扫码 **zxing-wasm**（MIT，2026-08 发版）；html5-qrcode / qr-scanner 均 2023 年前停更。**注意**：**Remotion 为自定义许可**（个人/小团队免费，公司需 Company License，[LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)）；Peaks.js 为 **LGPL-3.0**。

## 33. 通知 / Toast / 反馈 / 产品导览 / 浮层

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| sonner (见 §0) | [emilkowalski/sonner](https://github.com/emilkowalski/sonner) | 12.9k | MIT | 2026-08-10 | [sonner](https://www.npmjs.com/package/sonner) | 2.0.8 | 50.5M | MIT | ^18.0.0 \|\| ^19.0.0 \|\| ^19.0.0-rc |  |
| react-hot-toast (见 §0) | [timolins/react-hot-toast](https://github.com/timolins/react-hot-toast) | 11.0k | MIT | 2025-08-16 | [react-hot-toast](https://www.npmjs.com/package/react-hot-toast) | 2.6.0 | 3.9M | MIT | >=16 |  |
| react-toastify | [fkhadra/react-toastify](https://github.com/fkhadra/react-toastify) | 13.4k | MIT | 2026-04-19 | [react-toastify](https://www.npmjs.com/package/react-toastify) | 11.1.0 | 4.1M | MIT | ^18 \|\| ^19 |  |
| notistack | [iamhosseindhv/notistack](https://github.com/iamhosseindhv/notistack) | 4.1k | NOASSERTION | 2026-03-31 | [notistack](https://www.npmjs.com/package/notistack) | 3.0.2 | 1.8M | MIT | ^17.0.0 \|\| ^18.0.0 \|\| ^19.0.0 |  |
| Notyf | [caroso1222/notyf](https://github.com/caroso1222/notyf) | 2.9k | MIT | 2023-01-07 | [notyf](https://www.npmjs.com/package/notyf) | 3.10.0 | 48.5k | MIT | - | 最新发布 2021-06-08 |
| Toastify JS | [apvarun/toastify-js](https://github.com/apvarun/toastify-js) | 2.5k | MIT | 2024-08-19 | [toastify-js](https://www.npmjs.com/package/toastify-js) | 1.12.0 | 141.6k | MIT | - | 最新发布 2022-07-21 |
| Notiflix | [notiflix/Notiflix](https://github.com/notiflix/Notiflix) | 690 | MIT | 2025-10-14 | [notiflix](https://www.npmjs.com/package/notiflix) | 3.2.8 | 9.4k | MIT | - |  |
| SweetAlert2 | [sweetalert2/sweetalert2](https://github.com/sweetalert2/sweetalert2) | 18.1k | MIT | 2026-07-20 | [sweetalert2](https://www.npmjs.com/package/sweetalert2) | 11.26.25 | 1.1M | MIT | - |  |
| Push.js (Web Push) | [Nickersoft/push.js](https://github.com/Nickersoft/push.js) | 8.7k | MIT | 2023-12-15 | [push.js](https://www.npmjs.com/package/push.js) | 1.0.12 | 34.1k | MIT | - | **archived**；最新发布 2019-07-22 |
| NProgress | [rstacruz/nprogress](https://github.com/rstacruz/nprogress) | 26.4k | MIT | 2022-06-04 | [nprogress](https://www.npmjs.com/package/nprogress) | 0.2.0 | 4.0M | MIT | - | 最新发布 2015-05-13 |
| react-top-loading-bar | [klendi/react-top-loading-bar](https://github.com/klendi/react-top-loading-bar) | 749 | MIT | 2026-07-20 | [react-top-loading-bar](https://www.npmjs.com/package/react-top-loading-bar) | 3.0.2 | 292.6k | MIT | ^16 \|\| ^17 \|\| ^18 \|\| ^19 |  |
| Novu (in-app inbox) | [novuhq/novu](https://github.com/novuhq/novu) | 39.8k | NOASSERTION | 2026-09-04 | [@novu/react](https://www.npmjs.com/package/@novu/react) | 3.19.1 | 176.6k | ISC | ^18.0.0 \|\| ^19.0.0 \|\| ^19.0.0-0 |  |
| Knock React | [knocklabs/javascript](https://github.com/knocklabs/javascript) | 31 | MIT | 2026-09-04 | [@knocklabs/react](https://www.npmjs.com/package/@knocklabs/react) | 0.13.2 | 425.4k | MIT | ^17.0.0 \|\| ^18.0.0 \|\| ^19.0.0 |  |
| react-loading-skeleton | [dvtng/react-loading-skeleton](https://github.com/dvtng/react-loading-skeleton) | 4.2k | MIT | 2026-03-05 | [react-loading-skeleton](https://www.npmjs.com/package/react-loading-skeleton) | 3.5.0 | 1.5M | MIT | >=16.8.0 |  |
| react-spinners | [davidhu2000/react-spinners](https://github.com/davidhu2000/react-spinners) | 3.4k | MIT | 2026-09-02 | [react-spinners](https://www.npmjs.com/package/react-spinners) | 0.17.0 | 786.3k | MIT | ^16.0.0 \|\| ^17.0.0 \|\| ^18.0.0 \|\| ^19.0.0 |  |
| canvas-confetti | [catdad/canvas-confetti](https://github.com/catdad/canvas-confetti) | 12.7k | ISC | 2025-10-25 | [canvas-confetti](https://www.npmjs.com/package/canvas-confetti) | 1.9.4 | 8.4M | ISC | - |  |
| react-confetti | [alampros/react-confetti](https://github.com/alampros/react-confetti) | 1.7k | MIT | 2026-01-21 | [react-confetti](https://www.npmjs.com/package/react-confetti) | 6.4.0 | 2.5M | MIT | ^16.3.0 \|\| ^17.0.1 \|\| ^18.0.0 \|\| ^19.0.0 |  |
| Shepherd (产品导览) | [shepherd-pro/shepherd](https://github.com/shepherd-pro/shepherd) | 13.8k | NOASSERTION | 2026-09-03 | [shepherd.js](https://www.npmjs.com/package/shepherd.js) | 15.3.0 | 309.5k | AGPL-3.0 | - |  |
| driver.js | [kamranahmedse/driver.js](https://github.com/kamranahmedse/driver.js) | 26.7k | MIT | 2026-07-18 | [driver.js](https://www.npmjs.com/package/driver.js) | 1.8.0 | 2.0M | MIT | - |  |
| intro.js | [usablica/intro.js](https://github.com/usablica/intro.js) | 23.5k | NOASSERTION | 2026-08-07 | [intro.js](https://www.npmjs.com/package/intro.js) | 8.5.0 | 209.3k | AGPL-3.0 | - |  |
| react-joyride | [gilbarbara/react-joyride](https://github.com/gilbarbara/react-joyride) | 7.9k | MIT | 2026-07-09 | [react-joyride](https://www.npmjs.com/package/react-joyride) | 3.2.0 | 1.4M | MIT | 16.8 - 19 |  |
| Onborda (Next/Tailwind) | [uixmat/onborda](https://github.com/uixmat/onborda) | 1.4k | NONE | 2026-06-08 | [onborda](https://www.npmjs.com/package/onborda) | 1.2.5 | 46.1k | MIT | >=18 |  |
| NextStepjs | [enszrlu/NextStep](https://github.com/enszrlu/NextStep) | 1.0k | MIT | 2026-07-20 | [nextstepjs](https://www.npmjs.com/package/nextstepjs) | 2.3.0 | 60.7k | MIT | >=18 |  |
| react-tooltip | [ReactTooltip/react-tooltip](https://github.com/ReactTooltip/react-tooltip) | 3.8k | MIT | 2026-06-15 | [react-tooltip](https://www.npmjs.com/package/react-tooltip) | 6.0.8 | 2.2M | MIT | >=16.14.0 |  |
| Tippy.js | [atomiks/tippyjs](https://github.com/atomiks/tippyjs) | 12.2k | MIT | 2024-05-27 | [tippy.js](https://www.npmjs.com/package/tippy.js) | 6.3.7 | 6.8M | MIT | - | **archived**；最新发布 2021-11-10 |
| Floating UI | [floating-ui/floating-ui](https://github.com/floating-ui/floating-ui) | 32.7k | MIT | 2026-08-26 | [@floating-ui/react](https://www.npmjs.com/package/@floating-ui/react) | 0.27.20 | 23.3M | MIT | >=17.0.0 |  |

**一句话推荐**：Toast 用 **sonner**（MIT，50.5M/周，shadcn 默认）；MUI 栈用 notistack；非 React 用 SweetAlert2（MIT，1.1M/周）。浮层定位 **Floating UI**（MIT，23.3M/周，Radix/shadcn 底层）；Tippy.js 仓库已 archived（同一作者主导 Floating UI）。产品导览选 **driver.js**（MIT，2.0M/周）或 react-joyride（MIT，peer `16.8 - 19`）；**Shepherd 与 intro.js 均为 AGPL-3.0 + 商业双许可**（[Shepherd README](https://github.com/shepherd-pro/shepherd)、[intro.js license](https://github.com/usablica/intro.js/blob/master/license.md)），商业项目慎用。骨架屏 react-loading-skeleton；彩带 canvas-confetti（ISC，8.4M/周）。应用内通知中心 Novu（`@novu/react` ISC）/ Knock 均为托管服务 SDK。**停更**：NProgress latest 2015、Notyf 2021、Toastify JS 2022、Push.js archived。

## 34. 命令面板 / 搜索 UI / 选择器 / 快捷键

| 候选 | GitHub | ★ | GitHub SPDX | 最近推送 | npm 包 | 最新版 | 周下载 | npm license | React peer | 备注 |
|---|---|---:|---|---|---|---|---:|---|---|---|
| cmdk (见 §0) | [pacocoursey/cmdk](https://github.com/pacocoursey/cmdk) | 12.9k | MIT | 2025-10-29 | [cmdk](https://www.npmjs.com/package/cmdk) | 1.1.1 | 44.0M | MIT | ^18 \|\| ^19 \|\| ^19.0.0-rc |  |
| kbar | [timc1/kbar](https://github.com/timc1/kbar) | 5.2k | MIT | 2026-08-10 | [kbar](https://www.npmjs.com/package/kbar) | 1.0.0 | 314.7k | MIT | ^17.0.0 \|\| ^18.0.0 \|\| ^19.0.0 |  |
| react-cmdk | [albingroen/react-cmdk](https://github.com/albingroen/react-cmdk) | 1.2k | MIT | 2024-06-19 | [react-cmdk](https://www.npmjs.com/package/react-cmdk) | 1.3.9 | 93.0k | MIT | ^16.x \|\| ^17.x \|\| ^18.x | 最新发布 2023-04-18 |
| ninja-keys | [ssleptsov/ninja-keys](https://github.com/ssleptsov/ninja-keys) | 1.7k | MIT | 2024-07-14 | [ninja-keys](https://www.npmjs.com/package/ninja-keys) | 1.2.2 | 29.7k | MIT | - | 最新发布 2022-07-01 |
| command-score | [superhuman/command-score](https://github.com/superhuman/command-score) | 138 | MIT | 2023-01-25 | [command-score](https://www.npmjs.com/package/command-score) | 0.1.2 | 246.2k | MIT | - | **archived**；最新发布 2016-06-10 |
| Pagefind | [Pagefind/pagefind](https://github.com/Pagefind/pagefind) | 5.4k | MIT | 2026-09-05 | [pagefind](https://www.npmjs.com/package/pagefind) | 1.5.2 | 1.6M | MIT | - |  |
| DocSearch (Algolia) | [algolia/docsearch](https://github.com/algolia/docsearch) | 4.4k | MIT | 2026-09-05 | [@docsearch/react](https://www.npmjs.com/package/@docsearch/react) | 5.0.5 | 2.5M | MIT | >= 16.8.0 < 20.0.0 |  |
| Algolia autocomplete | [algolia/autocomplete](https://github.com/algolia/autocomplete) | 5.3k | MIT | 2026-09-04 | [@algolia/autocomplete-js](https://www.npmjs.com/package/@algolia/autocomplete-js) | 1.19.9 | 220.2k | MIT | - |  |
| InstantSearch React | [algolia/instantsearch](https://github.com/algolia/instantsearch) | 4.1k | MIT | 2026-09-04 | [react-instantsearch](https://www.npmjs.com/package/react-instantsearch) | 7.49.0 | 520.8k | MIT | >= 16.8.0 < 20 |  |
| Typesense InstantSearch adapter | [typesense/typesense-instantsearch-adapter](https://github.com/typesense/typesense-instantsearch-adapter) | 525 | MIT | 2026-07-08 | [typesense-instantsearch-adapter](https://www.npmjs.com/package/typesense-instantsearch-adapter) | 3.0.2 | 156.1k | Apache-2.0 | - |  |
| Meilisearch JS | [meilisearch/meilisearch-js](https://github.com/meilisearch/meilisearch-js) | 869 | MIT | 2026-09-01 | [meilisearch](https://www.npmjs.com/package/meilisearch) | 0.60.0 | 563.9k | MIT | - |  |
| react-select | [JedWatson/react-select](https://github.com/JedWatson/react-select) | 28.0k | MIT | 2026-07-16 | [react-select](https://www.npmjs.com/package/react-select) | 5.10.2 | 9.7M | MIT | ^16.8.0 \|\| ^17.0.0 \|\| ^18.0.0 \|\| ^19.0.0 |  |
| downshift | [downshift-js/downshift](https://github.com/downshift-js/downshift) | 12.3k | MIT | 2026-06-30 | [downshift](https://www.npmjs.com/package/downshift) | 9.4.0 | 4.7M | MIT | >=16.12.0 |  |
| react-mentions (仓库已删除) | - | - | - | - | [react-mentions](https://www.npmjs.com/package/react-mentions) | 4.4.10 | 790.2k | BSD-3-Clause | >=16.8.3 | **npm deprecated**；最新发布 2023-06-30 |
| Tribute.js (@mention) | [zurb/tribute](https://github.com/zurb/tribute) | 2.1k | MIT | 2025-01-30 | [tributejs](https://www.npmjs.com/package/tributejs) | 5.1.3 | 169.5k | MIT | - | 最新发布 2020-03-25 |
| Mousetrap | [ccampbell/mousetrap](https://github.com/ccampbell/mousetrap) | 11.8k | Apache-2.0 | 2023-03-15 | [mousetrap](https://www.npmjs.com/package/mousetrap) | 1.6.5 | 1.0M | Apache-2.0 WITH LLVM-exception | - | 最新发布 2020-01-23 |
| Fuse.js (见 §31) | - | - | - | - | - | - | - | - | - |  |

**一句话推荐**：命令面板 **cmdk**（MIT，44.0M/周，shadcn `<Command>` 底层）；kbar（MIT，1.0.0 于 2026-08 发布）为带 UI 的替代；react-cmdk / ninja-keys 均 2022–2023 后停更；command-score archived。静态站搜索 **Pagefind**（MIT）；文档站 DocSearch（Algolia 免费计划限公开技术文档，[申请条件](https://docsearch.algolia.com/docs/who-can-apply)）；自托管搜索客户端 Meilisearch JS（MIT）/ Typesense adapter（Apache-2.0）。选择器 **react-select**（MIT，9.7M/周，peer 到 React 19）或无头 downshift（MIT）。**注意**：react-mentions 的 GitHub 仓库（signavio）已删除且 npm 标记 deprecated（790k/周仍在用），@提及需求建议用 Tiptap/Lexical 的 mention 扩展或 Tribute.js（MIT，2020 后无发版）；Mousetrap npm license 为 `Apache-2.0 WITH LLVM-exception`，2020 后无发版，快捷键改用 §31 的 tinykeys / react-hotkeys-hook。

---

## 第三批风险清单（非宽松许可 / 自定义许可 / archived / deprecated）

| 候选 | GitHub SPDX | npm license | 判断 |
|---|---|---|---|
| Remotion | NOASSERTION | SEE LICENSE IN LICENSE.md | **自定义许可**：个人与小公司免费，其他公司需 Company License |
| Shepherd | NOASSERTION | AGPL-3.0 | AGPL + 商业双许可 |
| intro.js | NOASSERTION | AGPL-3.0 | AGPL + 商业许可（v2.0 起） |
| Webstudio | AGPL-3.0 | — | 应用产品，无库包 |
| Satori / @vercel/og / resvg-js / mediabunny / JointJS | MPL-2.0（@vercel/og 仓为 next.js MIT） | MPL-2.0 | 文件级 copyleft，作依赖使用无影响 |
| NLUX | NOASSERTION | MPL-2.0 | 同上，且 2024-08 后停更 |
| Peaks.js | LGPL-3.0 | LGPL-3.0 | 弱 copyleft |
| DOMPurify | Apache-2.0 | (MPL-2.0 OR Apache-2.0) | 可选 Apache，无风险 |
| @originjs/vite-plugin-federation | NOASSERTION | MulanPSL-2.0 | 木兰宽松许可证（OSI 认可） |
| type-fest | CC0-1.0 | (MIT OR CC0-1.0) | 宽松 |
| chroma.js | NOASSERTION | (BSD-3-Clause AND Apache-2.0) | 宽松 |
| PostHog JS | NOASSERTION | (Apache-2.0 AND MIT) | 宽松 |
| Mousetrap | Apache-2.0 | Apache-2.0 WITH LLVM-exception | 宽松 |
| zoid / workers-og / Supabase Auth UI | Apache-2.0 / MIT / MIT | （npm 未声明） | 以仓库 LICENSE 为准 |
| Vercel AI SDK、ai-elements、Mastra、Hanko、Zitadel、single-spa、Garfish、wujie、Bit、OpenReplay、Highlight、GrapesJS、Tmagic、react-mosaic、dockview、dom-to-image-more、pdfmake、lodash、Orama、marked、react-advanced-cropper、Video.js、hls.js、dash.js、notistack、Novu | NOASSERTION | MIT / Apache-2.0 / BSD-3 / ISC | GitHub 未识别许可证文件，npm 为宽松许可 |
| Creem、Ant Design X、node-canvas、unpic、Onborda | NONE | MIT | 同上 |

**archived**：Supabase Auth UI、Creem、LlamaIndex.TS、Plausible tracker、sanitize-html、Push.js、Tippy.js、command-score。**npm deprecated**：oslo → @oslojs/*（后者亦被标 deprecated）、arctic、plausible-tracker、`@measured/puck` → `@puckeditor/core`、`@react-email/components` 1.0.12、react-mentions；`@clerk/clerk-react` → `@clerk/react`。**仓库删除**：signavio/react-mentions。**服务绑定 SDK（开源但需付费后端）**：Clerk、Auth0、Logto、Hanko、Zitadel、Ory、Stripe、PayPal、Paddle、LemonSqueezy、Polar、Creem、Autumn、Adyen、Braintree、Liveblocks（§22）、Builder.io、Plasmic、Unlayer、Novu、Knock、Highlight、OpenReplay、Bugsnag、Vercel Analytics/Speed Insights、DocSearch、Algolia InstantSearch。

## 附录 A. 本轮新增的重大上游变化（老板需知）

1. **React Router v8**（2026-06-17）删除 `react-router-dom` 包，我们 102 处 import 需迁到 `react-router`。证据：[changelog v8.0.0](https://reactrouter.com/changelog)、npm `react-router-dom` dist-tags latest=7.18.3。
2. **TanStack Table v9**（latest 9.2.4）API 变化：`useReactTable`→`useTable`、显式 `features`。证据：[迁移指南](https://tanstack.com/table/latest/docs/framework/react/guide/migrating)。
3. **Vitest 5.0.0**（2026-09-03）发布。证据：[release](https://github.com/vitest-dev/vitest/releases/tag/v5.0.0)。
4. **CodeMirror 全部仓库迁出 GitHub**（2026-04-15 归档），源码在 code.haverbeke.berlin，npm 持续发布。证据：`gh api repos/codemirror/dev` archived=true；[README](https://github.com/codemirror/dev)。
5. **Base UI 包名变更**：`@base-ui-components/react` → `@base-ui/react`（npm deprecated 提示）。证据：[releases](https://base-ui.com/react/overview/releases)。
6. **Origin UI → coss（AGPL-3.0）**：`origin-space/originui` 已重定向到 `cosscom/coss`。证据：[LICENSE](https://github.com/cosscom/coss/blob/main/LICENSE)。
7. **dnd-kit 新代 `@dnd-kit/react` 0.5.0**（2026-09-05 发布，React 19），旧 `@dnd-kit/core` 自 2024-12 无发布。

第二批（§16–§23）新增：

8. **tsup 官方宣布不再积极维护**，README 指向 tsdown（[README](https://github.com/egoist/tsup)、[迁移指南](https://tsdown.dev/guide/migrate-from-tsup)）；tsdown 0.23.0，Rslib 1.0.0（2026-09-03）。
9. **Babel 8.0 已发布**（`@babel/core` latest 8.0.1，2026-06-17）。
10. **tldraw 许可证为非开源自定义许可**，生产环境需 License Key（[LICENSE.md](https://github.com/tldraw/tldraw/blob/main/LICENSE.md)）；白板嵌入选 Excalidraw（MIT）。
11. **Shoelace 仓库已归档**，后继 Web Awesome 3.x 含 Pro 付费层。
12. **React Three Fiber v9 仅支持 React 19**（peer `>=19 <19.3`）。
13. **Leaflet 2.0.0-alpha.1** 已在 npm alpha tag，latest 仍为 2023 年的 1.9.4；react-leaflet 5 采用 Hippocratic-2.1 许可。

## 附录 B. 数据来源与复现

- GitHub：`gh api repos/<owner>/<repo> --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at,archived:.archived}'`
- npm 元数据：`https://registry.npmjs.org/<pkg>`（`dist-tags.latest`、`versions[latest].license/peerDependencies/dist.unpackedSize`、`time`）
- npm 周下载：`https://api.npmjs.org/downloads/point/last-week/<pkg>`（窗口 2026-08-23 ~ 2026-08-29）
- 复现：`python3 scripts/collect.py scripts/items_round1.py data/candidates-2026-09-05.json`（第一批）/ `python3 scripts/collect.py scripts/items_round2.py data/candidates-round2-2026-09-05.json`（第二批）/ `python3 scripts/collect.py scripts/items_round3.py data/candidates-round3-2026-09-05.json`（第三批，279 条），然后 `scripts/downloads.py <json>` 补周下载、`scripts/summarize.py <json> <txt>` 出逐行摘要。
- 未在本文表格中单独列出但已采集的对照项（均 MIT/ISC，供追问）：sonner 2.0.8、cva 0.7.1、tailwind-merge 3.6.0、clsx 2.1.1、vaul 1.1.2、cmdk 1.1.1、react-resizable-panels 4.12.3、embla-carousel-react 8.6.0、input-otp 1.5.0、next-themes 0.4.6、qrcode.react 4.2.0、mermaid 11.17.2、@number-flow/react 0.6.2、react-error-boundary 6.1.5、usehooks-ts 3.1.1、ky 2.1.0、axios 1.20.0、react-use 17.6.1（Unlicense）、pdf-lib 1.17.1（npm 最后发布 2021-11-06）、html2canvas 1.4.1（2022-01-22）。

## 附录 C. 全部链接索引

### 官方文档 / 兼容性 / 许可证证据
- tsup README（停止维护声明）：https://github.com/egoist/tsup
- tsdown 从 tsup 迁移：https://tsdown.dev/guide/migrate-from-tsup
- React Three Fiber v9 迁移：https://r3f.docs.pmnd.rs/tutorials/v9-migration-guide
- styled-components FAQ（RSC）：https://styled-components.com/docs/faqs
- tldraw LICENSE：https://github.com/tldraw/tldraw/blob/main/LICENSE.md
- Mapbox GL JS LICENSE：https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt
- MapLibre LICENSE（BSD-3）：https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt
- react-leaflet LICENSE（Hippocratic-2.1）：https://github.com/PaulLeCam/react-leaflet/blob/master/LICENSE.md
- Bun LICENSE：https://github.com/oven-sh/bun/blob/main/LICENSE.md
- Lightning CSS LICENSE（MPL-2.0）：https://github.com/parcel-bundler/lightningcss/blob/master/LICENSE
- Triplit LICENSE（AGPL-3.0）：https://github.com/aspen-cloud/triplit/blob/main/LICENSE
- Liveblocks 定价：https://liveblocks.io/pricing
- Nx 定价（Nx Cloud）：https://nx.dev/pricing
- RxDB Premium：https://rxdb.info/premium/
- Turbopack 源码目录：https://github.com/vercel/next.js/tree/canary/turbopack
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
