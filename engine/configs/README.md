# 视频配置

每个视频对应一个配置文件（`<4 位题号>.py`，定义 `CONFIG` 字典），格式见 [../README.md](../README.md)。

| 目录 | 内容 |
|---|---|
| `ling/`、`yiduobo/` | Hot100 两位作者的视频 |
| `concept/` | Hot100 17 个分类的概念讲解 |
| `ling2/`、`yiduobo2/` | 面试经典 150 / 热题 173 / 字节高频 / List.md 里的其余题 |
| `ling_all/`、`yiduobo_all/` | 其余全部题解（灵神原文只有 Go 的，按原逻辑逐行转写为 Python，配置里有注明） |
| `skipped/` | 做不了的题和原因（`.resolved` 表示后来已经做出来了） |
| `failed/` | 曾经没通过检查的配置和错误信息（有 `.fixed` 标记的已修复） |
