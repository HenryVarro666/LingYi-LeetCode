---
name: lc-video
description: 把 LeetCode 题解（灵茶山艾府 / yiduobo / 用户自己的代码）做成逐行可视化的中文讲解动画视频，或为某个算法分类做概念讲解视频。用户说“给 xx 题做个动画/视频”“把这题的题解做成视频”“按 hot100 批量出视频”时使用。
---

# LeetCode 题解动画视频（lc-video）

把一份题解变成 1–3 分钟的 1080p 讲解视频，固定结构：

**① 题意 → ② 大神原文的核心思路 → ③ 逐步动画（代码行高亮 + 数据结构可视化 + 变量面板 + 字幕）→ ④ 复杂度和易错点**

引擎在 `~/Documents/Leetcode/tools/lc_video/`（Obsidian 库 `Leetcode` 的 `tools/lc_video`）。它会**真正执行**配置里的代码并逐行追踪变量，所以动画和代码一定对得上。每道题只需写一个配置文件。**开工前先完整读 `tools/lc_video/README.md`**——配置格式、所有视图类型、字幕模板、卡片字段和质量清单都在里面；参考配置看 `configs/ling/0011.py`。

## 素材在哪
- 灵茶山艾府：`灵茶山艾府题解/solutions/NNNN 题名 · 标题.md`（含题目描述 callout、多种写法；callout 行首的 `> ` 要去掉）
- yiduobo：`yiduobo题解/solutions/NNNN 题名 · yiduobo.md`（知乎文章，推导 + Python 2 风格代码）
- Hot100 分类：`灵茶山艾府题解/题单/LeetCode 热题 100/*.md`，已整理成 `tools/lc_video/hot100.json`
- 用户自己的代码：Leetcode 根目录下的 `NNN.py` 等

## 运行环境
- 需要 Python ≥ 3.10、`pillow`、`pygments`、`ffmpeg`、Noto Sans CJK 字体（引擎默认读 `/usr/share/fonts/opentype/noto/`）。
- 云端会话 + 已连接电脑：电脑上的 Linux 工作区（device_bash）已具备全部依赖，`~/mnt/Leetcode/tools/lc_video` 就是引擎目录。注意 device_bash 单次调用最长 180 秒、后台进程不会保留：一次调用只渲染 4–5 个视频（`python hot100.py render DEST --jobs 5 --budget 5 --only <列表>` 会并行开 5 个后停止派新任务，约 90–110 秒）。
- 也可以把引擎复制到云端容器里渲染（`python batch.py --jobs 1`，输出在 `out/`），再用 device_commit_files 按 `hot100.py paths` 给出的路径写回 Leetcode 文件夹。
- 从云端同步改动到电脑：把 `tools/lc_video` 打成**带时间戳文件名**的 tgz（同名文件可能拿到旧副本），commit 到 `Leetcode/output/_lcvideo_tmp/`，再在 device_bash 里 `tar xzf ... --overwrite`（连接的文件夹默认不允许删除文件，不加 `--overwrite` 会报 File exists）。

## 流程（每道题）
1. **读题解**：确定要讲哪位作者的哪种写法（灵神多写法时选主推写法；yiduobo 用他文章里的代码和推导）。摘出原文里最关键的一句话做 quote。
2. **写配置** `configs/<ling|yiduobo|mine>/NNNN.py`：
   - `code` 逐字照搬作者代码，只做 Python 3 最小修改（yiduobo：`/`→`//`、`xrange`→`range`、删 docstring 等，并在 summary 注明）；行尾注释保留（会自动变成字幕）。
   - `call` 用题目示例或更小的输入（数组 ≤ 10、网格 ≤ 4×5、树 ≤ 9 节点），`expect` 必填。链表 `L([...])`/`result_fn=list_vals`，树 `Tr([...])`/`result_fn=tree_list`，设计题用多行 `call`。
   - `views` 选能表达算法核心状态的视图：数组/柱状图 + 指针 + 窗口、哈希表、栈/队列/堆、网格/DP 表、链表、树、调用栈、区间、公式行，兜底用 `custom`。
   - `captions` 给关键行写讲“为什么”的模板（`{表达式}`、`B.变量` 取执行前的值、`ret` 取返回值）；其余行自动生成。
   - `cards`：one_liner、complexity、problem、quote（作者原文）、idea（2–3 条）、summary（复杂度 + 易错点 + 同类题）。全中文短句，\`code\` 和 ==强调== 标记可用。
3. **检查**：`python make.py CFG --steps`（不报错、expect 通过、关键行都有“为什么”、预估 60–180 秒）→ `python make.py CFG --preview a,b` 抽 2 帧用 Read 看图，确认视图不重叠、指针和颜色在表达核心状态。
4. **渲染**：`python make.py CFG out.mp4`，或批量 `python hot100.py render <Leetcode>/hot100动画 --jobs 3`。
5. **归档**：Hot100 题放 `hot100动画/<NN 分类>/<NNNN 题名> · <作者>.mp4`（`hot100.py paths` 打印目标路径），然后 `python hot100.py index <Leetcode>/hot100动画` 重建 `00 Hot100 动画索引.md`。非 Hot100 题：面试经典150/热题173/字节30天/List.md 里的题配置放 `configs/ling2|yiduobo2/`，用 `python sets.py render|index <Leetcode>/题单动画` 渲染和建索引（category 从 20 个分类里选，tags 写所属题单）；其他零散题放 `视频/<NNNN 题名> · <作者>.mp4`。

## 分类概念视频
配置放 `configs/concept/NN_分类名.py`：`num=None, author='概念讲解', kind='concept'`，`code` 是这一类的通用模板套在极小例子上（双指针→有序两数之和，滑动窗口→不定长窗口模板，二分→开区间 lower_bound，DP→爬楼梯从记忆化到递推……）；卡片用 `problem_heading='什么时候用？'`、`before=[概念卡]`、`idea_heading='两位作者怎么说'`、`summary_heading='本类 Hot100 题目 & 学习顺序'`。

## 质量要求
- 两位作者同一题要体现各自的思路和原文，不要写成一样的文案。
- 字幕不能一屏全是“执行 xxx”：比较/移动/更新答案这些关键行必须解释原因。
- 不要修改引擎去适配单题；引擎不够用时用 `custom` 视图。确实需要改引擎时，改完要对 `configs/` 下全部配置跑一遍 `--steps` 回归（不少配置用了有状态字幕、`tracer._origin` 布局等技巧，依赖“字幕按步骤顺序各求值一次”）。
- 想对比两位作者时，先看 `Python刷题函数/两位大神差异对照.md` 里该题的对照行。
- 做完告诉用户视频在哪个文件夹、时长，以及索引是否已更新。
