---
title: "2659. 将数组清空"
aliases: ["yiduobo的每日leetcode 2659.将数组清空"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648259147"
zhihu_id: "648259147"
zhihu_title: "yiduobo的每日leetcode 2659.将数组清空"
question_id: "2659"
question: "将数组清空"
problem_url: "https://leetcode.cn/problems/make-array-empty/"
difficulty: "Hard"
rating: 2282
created: "2023-08-06T04:31:12+08:00"
updated: "2023-08-06T04:31:12+08:00"
upvotes: 0
comments: 0
---

# 2659. 将数组清空

> **[yiduobo的每日leetcode 2659.将数组清空](https://zhuanlan.zhihu.com/p/648259147) · 知乎 · 2023-08-06 · 赞同 0**
> 力扣：[2659. 将数组清空](https://leetcode.cn/problems/make-array-empty/) · Hard · 灵茶山艾府：[两种思路：树状数组模拟/挖掘性质（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2659.将数组清空

[力扣](https://leetcode.cn/problems/make-array-empty/)

题目中移动数组的操作使得处理起来不是太方便，不过数组是按顺序移动的，那么不妨换一个视角，从移动数组直到合适的数来到数组头部，改成不断向后循环移动数组头部指针直到来到待删除的下一个数。

改成移动指针后，移动的方式就有两种可能。

第一种是目标位置在当前指针位置的后方，此时只需正常向后移动即可。期间经过的数字个数就是当前位置下标到目标位置下标之间尚存的数字个数。

第二种则是目标位置在当前指针前方，此时需要先将当前指针移动到数组末尾，然后在从数组头部开始将指针移动到目标位置。期间经过的数字个数就是当前位置下标到数组末尾下标之间尚存的数字个数，再加上从数组头部下标开始到目标位置下标之间尚存的数字个数。

如果当某个下标数字还存在时将数组值视为1，不存在时将数组值视为0，那么问题就转化成了一个动态的区间和问题。由于数组下标在十万以内，因此可以使用树状数组，将区间和问题转为前缀和问题。

到了这里，就得到了一种可行的处理方法。

首先初始化树状数组，将每一位上都加上1。接下来按从小到大的顺序将数组排序，需要注意排序时需要保留原始的数组下标。再接下来初始化头部指针下标为0，然后遍历排序后的数组，那么当前遍历到的数所处的原始下标就是头部指针的目标下标。

若目标下标在当前头部指针后方，那么就使用这两个位置的前缀和之差更新答案。需要注意的是，这里的前缀和之差实际上多计算了一次移动的消耗，但是删除数字正好需要一次操作，因此在这里减1加1就省略掉了。

若目标下标在当前头部指针前方，那么就先使用数组最后一位的前缀和与当前头部指针位置的前缀和之差，再加上目标位置的前缀和更新答案。

无论是哪种情况，都需要将目标下标这一位加上-1，表示删去该位置上的数，然后将头部指针下标移动到这个目标下标并继续向后遍历，直到遍历完所有数字为止。

最后附上python代码：

```python
class Solution(object):
    def countOperationsToEmptyArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        f = [0] * (n + 1)

        def add(x, delta):
            while x <= n:
                f[x] += delta
                x += x & -x

        def get(x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s

        for index in range(1, n + 1):
            add(index, 1)
        
        now = 0
        res = 0
        for index, _ in sorted(enumerate(nums), key=lambda d:d[1]):
            index += 1
            if now < index:
                res += get(index) - get(now)
            else:
                res += get(n) - get(now) + get(index)

            add(index, -1)
            now = index
        
        return res
```
