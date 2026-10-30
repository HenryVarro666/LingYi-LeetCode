---
title: "799. 香槟塔"
aliases: ["yiduobo的每日leetcode 799.香槟塔"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/342664627"
zhihu_id: "342664627"
zhihu_title: "yiduobo的每日leetcode 799.香槟塔"
question_id: "799"
question: "香槟塔"
problem_url: "https://leetcode.cn/problems/champagne-tower/"
difficulty: "Medium"
created: "2021-01-07T21:10:13+08:00"
updated: "2021-01-07T21:10:13+08:00"
upvotes: 1
comments: 0
---

# 799. 香槟塔

> **[yiduobo的每日leetcode 799.香槟塔](https://zhuanlan.zhihu.com/p/342664627) · 知乎 · 2021-01-07 · 赞同 1**
> 力扣：[799. 香槟塔](https://leetcode.cn/problems/champagne-tower/) · Medium · 灵茶山艾府：[BFS 模拟 + 优化（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

799.香槟塔

[力扣](https://leetcode-cn.com/problems/champagne-tower/)

乍一看感觉可以直接使用二项式定理来做，但是需要注意的是，这里每一层的杯子的进度是不一样的，例如样例中第三层中间的杯子就比两侧的杯子先满，从而使得第四层中间的两个杯子将比两侧的两个杯子先注入香槟，因此无法直接套用二项式定理。

没有想出组合数学相关的做法，只能老老实实逐层递推。令f[i][j]表示第i行第j个杯子最终的香槟量，初始化f[0][0] \= poured，其他f值均为0。接下来从0开始往下递推，遍历当前层的每个杯子，那么对于f[i][j]，若f[i][j] \<\= 1，那么f[i][j]未满，将不会向下溢出流量，否则设delta \= f[i][j] - 1，那么delta将均分到f[i + 1][j]以及f[i + 1][j + 1]当中，即

f[i + 1][j] +\= delta / 2

f[i + 1][j + 1] +\= delta / 2

当处理到询问的行列时停止继续递推。若对应杯子中的量大于1，那么答案为1，否则就是杯子中的量。

注意到这里状态转移只涉及到前一行，那么可以使用01滚动数组来节省空间。

最后附上python代码：

```python
class Solution(object):
    def champagneTower(self, poured, query_row, query_glass):
        """
        :type poured: int
        :type query_row: int
        :type query_glass: int
        :rtype: float
        """
        
        f = [[float(poured)], []]
        flag = 1
        for i in range(1, query_row + 1):
            f[flag] = [0.0] * (i + 1)
            for j, c in enumerate(f[1 - flag]):
                if c > 1:
                    delta = c - 1
                    f[flag][j] += delta / 2.0
                    f[flag][j + 1] += delta / 2.0
            flag ^= 1
            

        res = f[query_row & 1][query_glass]
        if res > 1:
            return 1.0
        return res
```
