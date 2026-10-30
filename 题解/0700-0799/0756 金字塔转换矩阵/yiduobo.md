---
title: "756. 金字塔转换矩阵"
aliases: ["yiduobo的每日leetcode 756.金字塔转换矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/hash-table", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/338322605"
zhihu_id: "338322605"
zhihu_title: "yiduobo的每日leetcode 756.金字塔转换矩阵"
question_id: "756"
question: "金字塔转换矩阵"
problem_url: "https://leetcode.cn/problems/pyramid-transition-matrix/"
difficulty: "Medium"
rating: 1990
created: "2020-12-20T23:18:35+08:00"
updated: "2020-12-20T23:18:35+08:00"
upvotes: 0
comments: 0
---

# 756. 金字塔转换矩阵

> **[yiduobo的每日leetcode 756.金字塔转换矩阵](https://zhuanlan.zhihu.com/p/338322605) · 知乎 · 2020-12-20 · 赞同 0**
> 力扣：[756. 金字塔转换矩阵](https://leetcode.cn/problems/pyramid-transition-matrix/) · Medium · 灵茶山艾府：[【图解】回溯 + vis 优化 + 位运算优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

756.金字塔转换矩阵

[力扣](https://leetcode-cn.com/problems/pyramid-transition-matrix/)

从当前层的最左侧开始往右遍历，枚举所有可能形成的下一层的结果，然后递归求解下一层。

第一层bottom的长度最多为8，那么第二层的最大长度就是7，而第二层枚举到的答案必然是互不相同的，于是可以从第三层开始记忆化搜索，即记录所有长度为6的候选集是否可以形成金字塔，那么最多有8^6总共262144种状态，其中还有很多是不可能达到的状态。

我在这里没有做记忆化，直接偷懒用了python的哈希表，直接用字符串做key，效率也没有什么问题。

有两个小的优化：

1、若当前新加入的字符char不是下一层的最后一个字符，那么char必须出现在allowed中某个字符串的首位。

2、若当前新加入的字符char不是下一层的第一个字符，那么char以及char的前一个字符必须是allowed中某个字符串的前两位。

最后附上python代码：

```python
class Solution(object):
    def pyramidTransition(self, bottom, allowed):
        """
        :type bottom: str
        :type allowed: List[str]
        :rtype: bool
        """

        allowed_dict = {}
        for pyr in allowed:
            a = pyr[0]
            b = pyr[1]
            c = pyr[2]
            if a not in allowed_dict:
                allowed_dict[a] = {}
            if b not in allowed_dict[a]:
                allowed_dict[a][b] = []
            allowed_dict[a][b].append(c)

        checked_set = set()
        return self.dfs(0, bottom, allowed_dict, [], checked_set)

    def dfs(self, pos, bottom, allowed_dict, now, checked_set):
        n = len(bottom)
        if n == 1:
            return True

        if pos == n - 1:
            new_bottom = ''.join(now)
            if new_bottom not in checked_set:
                if self.dfs(0, new_bottom, allowed_dict, [], checked_set):
                    return True
                checked_set.add(new_bottom)
            return False

        a = bottom[pos]
        b = bottom[pos + 1]
        if a not in allowed_dict or b not in allowed_dict[a]:
            return False
        
        for char in allowed_dict[a][b]:
            if pos > 0 and char not in allowed_dict[now[-1]]:
                continue
            if pos < n - 2 and char not in allowed_dict:
                continue

            now.append(char)
            if self.dfs(pos + 1, bottom, allowed_dict, now, checked_set):
                return True
            now.pop()
        
        return False
```
