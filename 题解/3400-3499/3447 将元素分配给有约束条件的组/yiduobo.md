---
title: "3447. 将元素分配给有约束条件的组"
aliases: ["yiduobo的每日leetcode 3447.将元素分配给有约束条件的组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1892670622175302098"
zhihu_id: "1892670622175302098"
zhihu_title: "yiduobo的每日leetcode 3447.将元素分配给有约束条件的组"
question_id: "3447"
question: "将元素分配给有约束条件的组"
problem_url: "https://leetcode.cn/problems/assign-elements-to-groups-with-constraints/"
difficulty: "Medium"
rating: 1731
created: "2025-04-07T20:45:44+08:00"
updated: "2025-04-07T20:45:44+08:00"
upvotes: 0
comments: 0
---

# 3447. 将元素分配给有约束条件的组

> **[yiduobo的每日leetcode 3447.将元素分配给有约束条件的组](https://zhuanlan.zhihu.com/p/1892670622175302098) · 知乎 · 2025-04-07 · 赞同 0**
> 力扣：[3447. 将元素分配给有约束条件的组](https://leetcode.cn/problems/assign-elements-to-groups-with-constraints/) · Medium · 灵茶山艾府：[调和级数枚举：预处理每个数能被谁整除（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3447.将元素分配给有约束条件的组

[3447. 将元素分配给有约束条件的组 - 力扣（LeetCode）](https://leetcode.cn/problems/assign-elements-to-groups-with-constraints/description/)

题目给出一个整数数组groups，其中groups[i]表示第i组的大小。另外给出一个整数数组elements。groups和elements的长度都可达10^5，同时其中的元素大小都在1到10^5之间。

现在要求按一下规则为每个组分配一个元素：

1、若groups[i]能被elements[j]整除，那么下标为j的元素可以分配给组i

2、若存在多个元素满足条件，则分配最小的下标j的元素

3、若没有符合条件的元素，则分配-1

需要注意，单个元素可以分配各多个组。

现在要求返回最后的分配方案assigned，其中assigned[i]为分配给组i的元素的下标。

题目涉及到整除，那么可以先从这一点入手分析。

对于某个v \= elements[j]，其可以被分配到所有groups[i]为v的倍数的组，也就是说，对于groups中所有值为v、2v、3v、...的元素，都可以将v分配给对应的组。另一方面，若存在某个k \< j，满足elements[k]是v的约数，那么v在这里就派不上用场了，因为所有v的倍数必然也是elements[k]的倍数，而k小于j，因此是无法分配j的。

可以发现，上面的描述与筛法是非常相似的，又由于本题中数值的取值范围在10^5之内，因此可以直接照搬筛法的处理过程。使用f[v]记录值为v的group应该分配element中的哪个下标，初始值均为-1，表示还未被分配。接下来对elements进行一趟遍历，对于当前遍历到的v \= elements[j]，若f[v]为-1，说明v还未被分配，此时应该从v开始，以v为步长进行遍历，对于所有遍历到的x，其都是v的倍数，因此可以将j分配给f[x]；反之，若f[v]不为-1，说明在此之前已经出现过v的约数，v已经派不上用场了。

计算完成后，对groups进行一趟遍历，返回其中每个元素对应的f值即可。

最后附上python代码：

```python
class Solution(object):
    def assignElements(self, groups, elements):
        """
        :type groups: List[int]
        :type elements: List[int]
        :rtype: List[int]
        """
        
        ma = max(groups)
        f = [-1] * (ma + 1)
        for index, v in enumerate(elements):
            if v <= ma and f[v] == -1:
                for x in range(v, ma + 1, v):
                    if f[x] == -1:
                        f[x] = index
        
        return [f[v] for v in groups]
```
