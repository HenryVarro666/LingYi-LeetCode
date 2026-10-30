---
title: "860. 柠檬水找零"
aliases: ["yiduobo的每日leetcode 860.柠檬水找零"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/349806448"
zhihu_id: "349806448"
zhihu_title: "yiduobo的每日leetcode 860.柠檬水找零"
question_id: "860"
question: "柠檬水找零"
problem_url: "https://leetcode.cn/problems/lemonade-change/"
difficulty: "Easy"
created: "2021-02-07T11:55:28+08:00"
updated: "2021-02-07T11:55:28+08:00"
upvotes: 0
comments: 0
---

# 860. 柠檬水找零

> **[yiduobo的每日leetcode 860.柠檬水找零](https://zhuanlan.zhihu.com/p/349806448) · 知乎 · 2021-02-07 · 赞同 0**
> 力扣：[860. 柠檬水找零](https://leetcode.cn/problems/lemonade-change/) · Easy · 灵茶山艾府：[分类讨论+简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

860.柠檬水找零

[力扣](https://leetcode-cn.com/problems/lemonade-change/)

由于这里的面值只有5、10、20三种，因此只需要考虑对10块和20块找零。

对于10块而言，只有找零5块这一种选择。

对于20块而言，可以明确的是在任何情况下，手握两张5块都是比只有一张10块更好的选择，因此应该首先尝试找零10+5的组合，如果不行再尝试5+5+5的组合。

具体实现时，可以通过两个变量分别统计当前手上5块和10块的数量，然后按上面总结的规则进行找零。当某一时刻无法找零时则返回false，否则返回true。

最后附上python代码：

```python
class Solution(object):
    def lemonadeChange(self, bills):
        """
        :type bills: List[int]
        :rtype: bool
        """

        cnt5 = cnt10 = 0
        for bill in bills:
            if bill == 5:
                cnt5 += 1
            elif bill == 10:
                if cnt5 == 0:
                    return False
                cnt5 -= 1
                cnt10 += 1
            else:
                if cnt10 > 0 and cnt5 > 0:
                    cnt10 -= 1
                    cnt5 -= 1
                elif cnt5 >= 3:
                    cnt5 -= 3
                else:
                    return False
        
        return True
```
