# 批量生成流水线

把 `题解/` 里两位作者的全部题解做成动画视频。单个视频怎么配置见上一级的 [README.md](../README.md)。

| 文件 | 作用 |
|---|---|
| `manifest.py` | 扫描两位作者的题解，按刷题路径排序（labuladong 路线图 → 灵神核心路线 → 灵神 12 个题单 → 其余按题号），生成 `../all.json` |
| `briefs.py` | 给每道题生成一份精简简报（题面 + 灵神 Python 代码 + yiduobo 推导和代码），给写配置的代理读 |
| `AGENT_TASK3.md` | 写配置的代理的任务说明（配置规范、检查方法、什么时候跳过） |
| `../allsets.py` | `next`（下一批待做题号）、`check`（逐个 `--steps` 校验，可隔离失败配置）、`render`（渲染缺失的视频）、`status` |
| `../repo.py` | 仓库命名规则：`题解/<区间>/<NNNN 题名>/<NNNN 题名> · <作者>.mp4` |
| `organize.py` | 从 Obsidian 库生成/刷新仓库：题解 md、图片、已有视频、每题 README、刷题路径、索引、根 README |
| `pack.py` / `lock.py` | 云端 ↔ Mac 同步打包；定时任务的运行锁 |
| `AUTOPILOT.md` | 定时任务每次运行的操作手册 |

配置目录：`configs/ling`、`configs/yiduobo`（Hot100）、`configs/ling2`、`configs/yiduobo2`（面试 150 / 热题 173 / 字节高频）、`configs/ling_all`、`configs/yiduobo_all`（其余全部）、`configs/concept`（分类概念）。
`configs/skipped/` 记录做不了的题和原因（题意不明 / 无代码 / 无法演示），`configs/failed/` 是没通过检查、等待修复的配置。

```bash
python allsets.py status ..                  # 进度
python allsets.py next 48                    # 下一批题号
python allsets.py check all-new              # 校验全部新配置
python allsets.py render .. --jobs 4         # 渲染缺失的视频到 ../题解/...
python pipeline/organize.py <Leetcode 库> ..  # 刷新仓库里的 README / 刷题路径 / 索引
```
