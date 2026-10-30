---
title: "93. 复原IP地址"
aliases: ["yiduobo的每日leetcode 93.复原IP地址"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/backtracking", "leetcode/enumeration", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/136821330"
zhihu_id: "136821330"
zhihu_title: "yiduobo的每日leetcode 93.复原IP地址"
question_id: "93"
question: "复原 IP 地址"
problem_url: "https://leetcode.cn/problems/restore-ip-addresses/"
difficulty: "Medium"
created: "2020-04-27T23:35:06+08:00"
updated: "2020-04-27T23:35:06+08:00"
upvotes: 0
comments: 0
---

# 93. 复原IP地址

> **[yiduobo的每日leetcode 93.复原IP地址](https://zhuanlan.zhihu.com/p/136821330) · 知乎 · 2020-04-27 · 赞同 0**
> 力扣：[93. 复原 IP 地址](https://leetcode.cn/problems/restore-ip-addresses/) · Medium · 灵茶山艾府：[两种方法：三重循环 / 回溯+剪枝（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

93.复原IP地址<https://leetcode-cn.com/problems/restore-ip-addresses/>

搜索回溯的题目。

每次尝试截取1至3位作为这个部分的值，然后继续考虑剩余的s。截取时需要判断位数为两位或三位时不能以0开头，以及位数为三位时是否小于等于255。

当处理完四轮之后，若剩余s正好也为空，说明找到了一种可行的分割方案。另外，若剩余的s长度不足，或者剩余的s过长，都可以提前return加快效率。

最后附上python代码：

```python
class Solution(object):
    def restoreIpAddresses(self, s):
        """
        :type s: str
        :rtype: List[str]
        """

        res = []
        self.dfs(4, s, [], res)
        return ['.'.join(x) for x in res]

    def dfs(self, level, s, now, res):
        if level == 0:
            if len(s) == 0:
                res.append(now[:])
            return
        if 3 * level < len(s):
            return
        if level > len(s):
            return
        
        now.append(s[0])
        self.dfs(level - 1, s[1:], now, res)
        now.pop()
        if s[0] != '0' and len(s) >= 2:
            now.append(s[0 : 2])
            self.dfs(level - 1, s[2:], now, res)
            now.pop()
            if len(s) >= 3 and int(s[0 : 3]) <= 255:
                now.append(s[0 : 3])
                self.dfs(level - 1, s[3:], now, res)
                now.pop()
```
