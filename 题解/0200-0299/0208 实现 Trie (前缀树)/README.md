# 208. 实现 Trie (前缀树)

Medium · [力扣原题](https://leetcode.cn/problems/implement-trie-prefix-tree/)

所在刷题路径：labuladong、灵神突击、灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](0208%20实现%20Trie%20%28前缀树%29%20·%20灵茶山艾府.gif) · [mp4 文件](0208%20实现%20Trie%20%28前缀树%29%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](0208%20实现%20Trie%20%28前缀树%29%20·%20yiduobo.gif) · [mp4 文件](0208%20实现%20Trie%20%28前缀树%29%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![0208 实现 Trie (前缀树) · 灵茶山艾府](0208%20实现%20Trie%20%28前缀树%29%20·%20灵茶山艾府.gif)

### yiduobo

![0208 实现 Trie (前缀树) · yiduobo](0208%20实现%20Trie%20%28前缀树%29%20·%20yiduobo.gif)


## 题目描述

**[Trie](https://baike.baidu.com/item/字典树/9825209?fr=aladdin)**（发音类似 "try"）或者说 **前缀树** 是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补全和拼写检查。

请你实现 Trie 类：

- `Trie()` 初始化前缀树对象。

- `void insert(String word)` 向前缀树中插入字符串 `word` 。

- `boolean search(String word)` 如果字符串 `word` 在前缀树中，返回 `true`（即，在检索之前已经插入）；否则，返回 `false` 。

- `boolean startsWith(String prefix)` 如果之前已经插入的字符串 `word` 的前缀之一为 `prefix` ，返回 `true` ；否则，返回 `false` 。

**示例：**

```

输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]

解释
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // 返回 True
trie.search("app");     // 返回 False
trie.startsWith("app"); // 返回 True
trie.insert("app");
trie.search("app");     // 返回 True
```

**提示：**

- `1 <= word.length, prefix.length <= 2000`

- `word` 和 `prefix` 仅由小写英文字母组成

- `insert`、`search` 和 `startsWith` 调用次数 **总计** 不超过 `3 * 10⁴` 次

---
[↑ 返回 0200-0299](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
