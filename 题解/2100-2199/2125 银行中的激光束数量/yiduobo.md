---
title: "2125. 银行中的激光束数量"
aliases: ["yiduobo的每日leetcode 2125.银行中的激光束数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/combinatorics"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/525662351"
zhihu_id: "525662351"
zhihu_title: "yiduobo的每日leetcode 2125.银行中的激光束数量"
question_id: "2125"
question: "银行中的激光束数量"
problem_url: "https://leetcode.cn/problems/number-of-laser-beams-in-a-bank/"
difficulty: "Medium"
created: "2022-06-07T23:34:01+08:00"
updated: "2022-06-07T23:34:01+08:00"
upvotes: 0
comments: 0
---

# 2125. 银行中的激光束数量

> **[yiduobo的每日leetcode 2125.银行中的激光束数量](https://zhuanlan.zhihu.com/p/525662351) · 知乎 · 2022-06-07 · 赞同 0**
> 力扣：[2125. 银行中的激光束数量](https://leetcode.cn/problems/number-of-laser-beams-in-a-bank/) · Medium · 灵茶山艾府：[阅读理解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2125.银行中的激光束数量

[力扣](https://leetcode.cn/problems/number-of-laser-beams-in-a-bank/)

根据题目的描述，对于没有激光设备的行来说，激光束与这些行完全没有关联，而对于有激光设备的行来说，必须是两行之间不存在其他有激光设备的行，这两行之间才会产生激光束。激光束的计算方法也很简单，就是这两行激光设备的乘积。

那么可以使用一个变量last记录上一个有激光设备的行中激光设备的数量，初始化为0。接下来从上往下遍历每一行，统计当前行中激光设备的数量now。若now等于0，那么直接跳过本行，否则本行将与上一个有激光设备的行形成last \* now束激光，将这个值加入到答案中，并将last更新为now即可。

最后附上python代码：

```python
class Solution(object):
    def numberOfBeams(self, bank):
        """
        :type bank: List[str]
        :rtype: int
        """

        last = 0
        res = 0
        for line in bank:
            now = 0
            for char in line:
                if char == '1':
                    now += 1
            if now > 0:
                res += last * now
                last = now
        
        return res
```
