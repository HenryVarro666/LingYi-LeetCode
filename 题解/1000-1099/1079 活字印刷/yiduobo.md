---
title: "1079. 活字印刷"
aliases: ["yiduobo的每日leetcode 1079.活字印刷"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "leetcode/counting", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/372798491"
zhihu_id: "372798491"
zhihu_title: "yiduobo的每日leetcode 1079.活字印刷"
question_id: "1079"
question: "活字印刷"
problem_url: "https://leetcode.cn/problems/letter-tile-possibilities/"
difficulty: "Medium"
rating: 1741
created: "2021-05-16T22:17:59+08:00"
updated: "2021-05-16T22:17:59+08:00"
upvotes: 0
comments: 0
---

# 1079. 活字印刷

> **[yiduobo的每日leetcode 1079.活字印刷](https://zhuanlan.zhihu.com/p/372798491) · 知乎 · 2021-05-16 · 赞同 0**
> 力扣：[1079. 活字印刷](https://leetcode.cn/problems/letter-tile-possibilities/) · Medium · 灵茶山艾府：[O(n^2) 计数 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1079.活字印刷

[力扣](https://leetcode-cn.com/problems/letter-tile-possibilities/)

本题应该可以利用组合数学解决，可以想到的是使用母函数来做，直接排列组合不知道行不行。不过这里的tiles长度小于等于7，因此我选择的是直接暴力dfs。

按正常dfs的流程，每一轮选择一个还未被选择的tile，然后继续进行dfs，最多执行len(tiles)轮截止。为了避免重复，同一轮选择的tile不应该重复，因此可以先将tile排序，然后在枚举时若当前的tile[index]与tile[index - 1]一样，那么就跳过tile[index]。

最后附上python代码：

```python
class Solution(object):
    def numTilePossibilities(self, tiles):
        """
        :type tiles: str
        :rtype: int
        """

        self.res = 0
        char_list = sorted(list(tiles))
        used = [False] * len(char_list)
        self.dfs(0, char_list, used)
        return self.res - 1
    
    def dfs(self, level, char_list, used):
        self.res += 1
        if level == len(char_list):
            return

        last = ''
        for index, char in enumerate(char_list):
            if char != last and not used[index]:
                used[index] = True
                last = char
                self.dfs(level + 1, char_list, used)
                used[index] = False
```
