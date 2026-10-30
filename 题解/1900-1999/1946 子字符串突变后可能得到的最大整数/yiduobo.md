---
title: "1946. 子字符串突变后可能得到的最大整数"
aliases: ["yiduobo的每日leetcode 1946.子字符串突变后可能得到的最大整数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/491167505"
zhihu_id: "491167505"
zhihu_title: "yiduobo的每日leetcode 1946.子字符串突变后可能得到的最大整数"
question_id: "1946"
question: "子字符串突变后可能得到的最大整数"
problem_url: "https://leetcode.cn/problems/largest-number-after-mutating-substring/"
difficulty: "Medium"
rating: 1445
created: "2022-04-01T00:54:33+08:00"
updated: "2022-04-01T00:54:34+08:00"
upvotes: 0
comments: 0
---

# 1946. 子字符串突变后可能得到的最大整数

> **[yiduobo的每日leetcode 1946.子字符串突变后可能得到的最大整数](https://zhuanlan.zhihu.com/p/491167505) · 知乎 · 2022-04-01 · 赞同 0**
> 力扣：[1946. 子字符串突变后可能得到的最大整数](https://leetcode.cn/problems/largest-number-after-mutating-substring/) · Medium · 灵茶山艾府：[Go 贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1946.子字符串突变后可能得到的最大整数

[力扣](https://leetcode-cn.com/problems/largest-number-after-mutating-substring/)

由于只能替换一个子字符串，因此必然是选择高位上有收益的地方进行替换，于是可以从高位开始向低位一趟遍历，找到替换的起点。

接下来从替换的起点开始执行替换。若当前位置上替换的收益不为负，那么就执行替换，然后继续向后考虑。重复此过程直到替换没有收益了，或者替换完了整个字符串后缀。

最后附上python代码：

```python
class Solution(object):
    def maximumNumber(self, num, change):
        """
        :type num: str
        :type change: List[int]
        :rtype: str
        """

        flag = False
        num_list = []
        for index, char in enumerate(num):
            if change[ord(char) - 48] > ord(char) - 48:
                flag = True
                num_list.append(change[ord(char) - 48])
            else:
                if change[ord(char) - 48] < ord(char) - 48 and flag:
                    return ''.join([str(x) for x in num_list]) + num[index:]
                
                num_list.append(ord(char) - 48)
        
        return ''.join([str(x) for x in num_list])
```
