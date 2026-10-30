---
title: "771. 宝石与石头"
aliases: ["yiduobo的每日leetcode 771.宝石与石头"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339774889"
zhihu_id: "339774889"
zhihu_title: "yiduobo的每日leetcode 771.宝石与石头"
question_id: "771"
question: "宝石与石头"
problem_url: "https://leetcode.cn/problems/jewels-and-stones/"
difficulty: "Easy"
created: "2020-12-26T19:41:29+08:00"
updated: "2020-12-26T19:41:29+08:00"
upvotes: 0
comments: 0
---

# 771. 宝石与石头

> **[yiduobo的每日leetcode 771.宝石与石头](https://zhuanlan.zhihu.com/p/339774889) · 知乎 · 2020-12-26 · 赞同 0**
> 力扣：[771. 宝石与石头](https://leetcode.cn/problems/jewels-and-stones/) · Easy · 灵茶山艾府：[本题最优解！线性时间+常数空间（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

771.宝石与石头

[力扣](https://leetcode-cn.com/problems/jewels-and-stones/)

比较基础的题目，使用哈希表统计J中出现的所有字符，然后遍历S，若当前字符在哈希表中则将答案加一即可。

最后附上python代码：

```python
class Solution(object):
    def numJewelsInStones(self, J, S):
        """
        :type J: str
        :type S: str
        :rtype: int
        """

        j_set = set()
        for char in J:
            j_set.add(char)
        
        res = 0
        for char in S:
            if char in j_set:
                res += 1
        
        return res
```
