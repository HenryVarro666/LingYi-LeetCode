---
title: "1550. 存在连续三个奇数的数组"
aliases: ["yiduobo的每日leetcode 1550.存在连续三个奇数的数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/425678363"
zhihu_id: "425678363"
zhihu_title: "yiduobo的每日leetcode 1550.存在连续三个奇数的数组"
question_id: "1550"
question: "存在连续三个奇数的数组"
problem_url: "https://leetcode.cn/problems/three-consecutive-odds/"
difficulty: "Easy"
created: "2021-10-25T23:18:58+08:00"
updated: "2021-10-25T23:18:58+08:00"
upvotes: 0
comments: 0
---

# 1550. 存在连续三个奇数的数组

> **[yiduobo的每日leetcode 1550.存在连续三个奇数的数组](https://zhuanlan.zhihu.com/p/425678363) · 知乎 · 2021-10-25 · 赞同 0**
> 力扣：[1550. 存在连续三个奇数的数组](https://leetcode.cn/problems/three-consecutive-odds/) · Easy · 灵茶山艾府：[简单题，简单做。附思考题，欢迎挑战！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1550.存在连续三个奇数的数组

[力扣](https://leetcode-cn.com/problems/three-consecutive-odds/)

比较基础的题目。一趟扫描，记录以当前位置为结尾的连续奇数个数cnt。若当前数为奇数，那么将cnt加上1，当cnt等于3时返回true。若当前数为偶数，则将cnt置0。

若正常推出循环，说明起见cnt没有到达过3，因此返回false。

最后附上python代码：

```python
class Solution(object):
    def threeConsecutiveOdds(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """

        cnt = 0
        for num in arr:
            if num & 1:
                cnt += 1
                if cnt == 3:
                    return True
            else:
                cnt = 0
        
        return False
```
