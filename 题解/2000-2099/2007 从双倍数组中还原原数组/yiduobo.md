---
title: "2007. 从双倍数组中还原原数组"
aliases: ["yiduobo的每日leetcode 2007.从双倍数组中还原原数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/queue", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/503290928"
zhihu_id: "503290928"
zhihu_title: "yiduobo的每日leetcode 2007.从双倍数组中还原原数组"
question_id: "2007"
question: "从双倍数组中还原原数组"
problem_url: "https://leetcode.cn/problems/find-original-array-from-doubled-array/"
difficulty: "Medium"
created: "2022-04-22T19:58:31+08:00"
updated: "2022-04-22T19:58:31+08:00"
upvotes: 0
comments: 0
---

# 2007. 从双倍数组中还原原数组

> **[yiduobo的每日leetcode 2007.从双倍数组中还原原数组](https://zhuanlan.zhihu.com/p/503290928) · 知乎 · 2022-04-22 · 赞同 0**
> 力扣：[2007. 从双倍数组中还原原数组](https://leetcode.cn/problems/find-original-array-from-doubled-array/) · Medium · 灵茶山艾府：[三种方法：从 O(nlogn) 到 O(n)（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2007.从双倍数组中还原原数组

[力扣](https://leetcode-cn.com/problems/find-original-array-from-doubled-array/)

由于数组中的数都大于等于0，因此如果原数组存在的话，那么双倍数组中的最小值必然来自于原数组。设这个最小值为x，那么就可以从双倍数组中剔除x和2x，然后继续这个过程直到找不到对应的2x或者还原了原数组。

当然，在这里如果直接暴力找的话，时间复杂度是O(n^2)的，必须想办法进行优化。可以发现，随着每次寻找，最小值x是在逐渐增大的，同时2x也是在逐渐增大的，那么就可以想将双倍数组进行排序，然后一趟遍历，并使用一个遍历p记录当前2x对应的下标，p的初始值为1。

对于当前遍历到的index，若其还没有从双倍数组中剔除，那么：

1、若此时的p小于等于index，那么就将p移动到index + 1，因为2x必然是出现在x后面的

2、接下来从p开始向后寻找，直到找到2x或者p到达双倍数组的末尾。

若找到了2x，那么就将index和p从数组中剔除。在这里可以利用一个set表示哪些位置上的数还没有被剔除而不需要真的删去某个数。除此之外，还需要将x加入到答案中。

若没有找到2x，说明无解，直接返回空数组即可。

对于上述的过程，index将遍历每个位置一次，p最多也只会遍历每个位置一次，因此整体的时间复杂度就是O(n)。再加上一开始排序的复杂度，所以总的时间复杂度就是O(nlogn)。

最后附上python代码：

```python
class Solution(object):
    def findOriginalArray(self, changed):
        """
        :type changed: List[int]
        :rtype: List[int]
        """

        changed = sorted(changed)

        used = set()

        res = []
        p = 1
        for index in range(len(changed)):
            if index not in used:
                if p <= index:
                    p = index + 1
                while p < len(changed) and changed[p] != changed[index] + changed[index]:
                    p += 1
                if p == len(changed):
                    return []
                
                used.add(index)
                used.add(p)
                res.append(changed[index])

                p += 1
                
        
        return res
```
