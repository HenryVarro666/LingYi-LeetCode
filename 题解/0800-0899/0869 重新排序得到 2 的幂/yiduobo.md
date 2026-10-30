---
title: "869. 重新排序得到2的幂"
aliases: ["yiduobo的每日leetcode 869.重新排序得到2的幂"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/string", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350259852"
zhihu_id: "350259852"
zhihu_title: "yiduobo的每日leetcode 869.重新排序得到2的幂"
question_id: "869"
question: "重新排序得到 2 的幂"
problem_url: "https://leetcode.cn/problems/reordered-power-of-2/"
difficulty: "Medium"
rating: 1505
created: "2021-02-11T11:02:20+08:00"
updated: "2021-02-11T11:02:20+08:00"
upvotes: 0
comments: 0
---

# 869. 重新排序得到2的幂

> **[yiduobo的每日leetcode 869.重新排序得到2的幂](https://zhuanlan.zhihu.com/p/350259852) · 知乎 · 2021-02-11 · 赞同 0**
> 力扣：[869. 重新排序得到 2 的幂](https://leetcode.cn/problems/reordered-power-of-2/) · Medium · 灵茶山艾府：[逆向思维（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

869.重新排序得到2的幂

[力扣](https://leetcode-cn.com/problems/reordered-power-of-2/)

由于在这里可以任意交换N中各位数字，因此我们只需要判断是否存在2的幂，其各个位置上的数字构成与N的各位数字一致。于是可以先计算出N的位数L，然后枚举所有长度为L的2的幂，判断二者的数字构成是否一致即可。

最后附上python代码：

```python
class Solution(object):
    def reorderedPowerOf2(self, N):
        """
        :type N: int
        :rtype: bool
        """

        now = 1
        cnt_dict = {}
        length = 0
        while N:
            num = N % 10
            N /= 10
            length += 1
            cnt_dict[num] = cnt_dict.get(num, 0) + 1

        while len(str(now)) <= length:
            if len(str(now)) == length:
                tmp_cnt_dict = {}
                tmp = now
                while tmp:
                    num = tmp % 10
                    tmp /= 10
                    tmp_cnt_dict[num] = tmp_cnt_dict.get(num, 0) + 1
                if cnt_dict == tmp_cnt_dict:
                    return True

            now += now

        return False
```
