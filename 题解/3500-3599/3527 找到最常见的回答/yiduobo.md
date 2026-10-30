---
title: "3527. 找到最常见的回答"
aliases: ["yiduobo的每日leetcode 3527.找到最常见的回答"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1904683830830400164"
zhihu_id: "1904683830830400164"
zhihu_title: "yiduobo的每日leetcode 3527.找到最常见的回答"
question_id: "3527"
question: "找到最常见的回答"
problem_url: "https://leetcode.cn/problems/find-the-most-common-response/"
difficulty: "Medium"
created: "2025-05-12T22:59:48+08:00"
updated: "2025-05-12T22:59:48+08:00"
upvotes: 0
comments: 0
---

# 3527. 找到最常见的回答

> **[yiduobo的每日leetcode 3527.找到最常见的回答](https://zhuanlan.zhihu.com/p/1904683830830400164) · 知乎 · 2025-05-12 · 赞同 0**
> 力扣：[3527. 找到最常见的回答](https://leetcode.cn/problems/find-the-most-common-response/) · Medium · 灵茶山艾府：[哈希表统计（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3527.找到最常见的回答

[3527. 找到最常见的回答 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-most-common-response/description/)

题目给出一个二维字符串数组responses，其中每个responses[index]是一个字符串数组，表示第index天调查的回答结果。其中responses以及每个responses[index]的长度都不超过1000，每个回答的长度不超过10。

现在要求返回每个responses[index]中的回答去重后，所有天数中最常见的回答。若多个回答出现的频率相同，取其中字典序最小的那个。

题目的数据规模不大，可以直接遍历每天的回答，先使用集合去重，然后使用哈希表统计每天去重后的回答出现的次数。遍历完成后，再遍历哈希表中的所有回答，取其中出现次数最多且字典序最小的那个即可。

最后附上python代码：

```python
class Solution(object):
    def findCommonResponse(self, responses):
        """
        :type responses: List[List[str]]
        :rtype: str
        """
        
        cnt = {}
        for resp in responses:
            resp_set = set(resp)
            for s in resp_set:
                cnt[s] = cnt.get(s, 0) + 1
        
        res = None
        for s in cnt:
            if res is None or cnt[s] > cnt[res] or (cnt[s] == cnt[res] and s < res):
                res = s
        return res
```
