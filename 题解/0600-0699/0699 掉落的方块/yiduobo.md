---
title: "699. 掉落的方块"
aliases: ["yiduobo的每日leetcode 699.掉落的方块"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/316523832"
zhihu_id: "316523832"
zhihu_title: "yiduobo的每日leetcode 699.掉落的方块"
question_id: "699"
question: "掉落的方块"
problem_url: "https://leetcode.cn/problems/falling-squares/"
created: "2020-11-28T00:35:52+08:00"
updated: "2020-11-28T00:35:52+08:00"
upvotes: 0
comments: 0
---

# 699. 掉落的方块

> **[yiduobo的每日leetcode 699.掉落的方块](https://zhuanlan.zhihu.com/p/316523832) · 知乎 · 2020-11-28 · 赞同 0**
> 力扣：[699. 掉落的方块](https://leetcode.cn/problems/falling-squares/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

699.掉落的方块

[力扣](https://leetcode-cn.com/problems/falling-squares/)

首先，由于下落的正方形的方块，因此可以通过其起点left和高度height计算出其终点right。那么对于一个下落的方块，其必然是落在left到right这一段中最高的方块上面，因此我们可以将这个问题转化一下，将其视为给出高度height以及区间[left, right]，找到区间中最大的数max，然后将区间[left, right]中的所有数置为max + height。

到了这里，问题就转化为了动态区间最大值的问题，最经典的做法就是线段树。不过注意到这里区间的取值范围在1到10^8之间，无法直接使用线段树。由于这里我们只关心高度，并不关心区间的宽度，例如[1-100]，[200-10000]这两个区间与[1-2]，[3-4]在这里并没有本质区别。因此我们首先需要对区间的左右位置进行离散化，具体做法就是对所有区间的左右坐标从小到大进行排序，然后将每个具体的坐标值映射到这个序上。这样一来，由于最多只有1000个区间，因此所有的区间坐标都可以收缩到1到2000之间，为后续使用线段树打好了基础。

---

接下来简单介绍一下线段树这种数据结构。具体来说就是对于树中的任意节点，其都管辖着一段区间[l, r]。若l \= r，那么该节点是叶子节点，表示原始区间上位置l的这个点；若l \< r，那么该节点记录的则是区间l到r这一段中节点的最大值，同时该节点有两个孩子节点，分别管理l到(l + r) / 2以及(l + r) / 2 + 1到r这两个子区间。其中根节点管辖的是整个区间[0, max_r - 1]。

区间[l, r]的最大值就是区间[l, (l + r) / 2]的最大值以及区间[(l + r) / 2, r]的最大值中较大的那个，这意味着节点p的值p.val就等于max(p.left.val，p.right.val)，而叶子节点的值就等于其对应的点的值。

在更新区间值的时候，如果我们更新区间中每一个节点的值，那么时间复杂度反而达到了nlogn，还不如朴素的算法，因此可以使用一个小trick。

具体来说就是对于需要更新的区间[i, j]，若其刚好与当前节点表示的区间[l, r]完全一致，那么我们就设置一个全覆盖标记，表示当前节点p表示区间[l , r]中的的所有值都被更新成了p.val，同时我们不再继续往下更新节点。这样一来就可以节省一些更新的成本。当然，这样做的话每次更新的时候需要检测这个标记以免出现问题，需要根据这个标记及时下放之前的更新结果。

若l \= i且r \= j，那么更新的区间完全重叠，直接置p.val \= val，同时置p.flag \= true然后返回，此次更新完成；若不满足上面的条件，那么就会稍微复杂一些：

1、若此时p.flag \= true，那么我们需要先将之前更新的值下放，即先使用p.val递归更新p.left以及p.right，然后置p.flag为false

2、使用新值val更新p.val。需要注意的是，这里有一个隐藏条件：若之前区间中最大值p.val所在的位置pos在这一次操作中需要被更新，那么这里的新值val必然是在p.val的基础上累加了最新的这个方块的高度，即val > p.val；若p.val对应的pos没有被更新，那么老的p.val依然有可能成为p所管辖区间的最大值。因此，这里的更新就是p.val \= max(p.val, val)

3、步骤2完成后，设mid \= (l + r) / 2，若j \<\= mid，说明需要更新的区间[i, j]位于p.left管辖的区间[l, mid]之内，那么此时使用新值val应该递归更新p.left；若i > mid，则是使用新值val递归更新p.right；若都不满足，那么就需要将[i, j]通过mid截为两段，然后使用新值val分别递归更新p.left以及p.right

4、步骤3完成后，若p.left.val \= p.right.val，且p.left.flag和p.right.flag都为true，说明p.left管辖区间内所有的值与p.right管辖区间内所有的值都一样，因此我们可以置p.flag为true。当然，p.value已经也必然等于p.left.val，不过已经在之前的步骤2完成了更新。

除了上面的更新操作之外，还有查询操作：

1、若需要查询的区间[i, j]与当前p管辖的区间[l, r]完全一致，那么直接返回p.val

2、若p.flag\=true，说明区间内所有的值完全一致，那么直接返回p.val

3、设mid \= (l + r) / 2，若j \<\= mid，说明需要查询的区间[i, j]位于p.left管辖的区间[l, mid]之内，那么此时应该递归查询p.left；若i > mid，则是递归查询p.right；若都不满足，则分别查询使用p.left中的[i, mid]以及p.right中的[mid + 1, j]，然后取较大值

---

那么到了这里，就有了一种做法：

1、计算每个区间的左右边界，排序后将左右边界进行离散化

2、按原始顺序依次遍历每个区间离散化之后的边界[left, right]以及其对应的height，通过线段树查询[left, right]中的最大值max，然后将max+height更新到区间[left, right]中

3、查询线段树中的最大值，并将其加入到答案中

对于线段树的实现，可以使用树节点类来做，也可以使用类似堆的数组下标的做法来做。这两种是经典的自顶向下的实现，当然也有高效的自底向上的实现方法，例如zkw线段树。在这里就不再展开了。

最后附上python代码：

```python
class Solution(object):
    def fallingSquares(self, positions):
        """
        :type positions: List[List[int]]
        :rtype: List[int]
        """

        pos_set = set()
        for start, height in positions:
            end = start + height - 1
            pos_set.add(start)
            pos_set.add(end)

        pos_dict = {}
        for index, pos in enumerate(sorted(list(pos_set))):
            pos_dict[pos] = index

        pos_list = []
        for start, height in positions:
            end = start + height - 1
            pos_list.append([pos_dict[start], pos_dict[end], height])

        max_r = 1
        level = 0
        while max_r < len(pos_set):
            level += 1
            max_r += max_r

        f = [0] * (max_r + max_r - 1)
        same_flag = [True] * (max_r + max_r - 1)
        res = []
        for start, end, height in pos_list:
            now_height = self.get(0, 0, max_r - 1, start, end, f, same_flag)
            self.put(0, 0, max_r - 1, start, end, f, same_flag, now_height + height)
            res.append(self.get(0, 0, max_r - 1, 0, max_r - 1, f, same_flag))

        return res

    def get(self, pos, l, r, i, j, f, same_flag):
        if l == i and j == r:
            return f[pos]

        if same_flag[pos]:
            return f[pos]
        
        mid = (l + r) >> 1
        if j <= mid:
            return self.get(pos + pos + 1, l, mid, i, j, f, same_flag)
        elif i > mid:
            return self.get(pos + pos + 2, mid + 1, r, i, j, f, same_flag)
        else:
            return max(self.get(pos + pos + 1, l, mid, i, mid, f, same_flag), self.get(pos + pos + 2, mid + 1, r, mid + 1, j, f, same_flag))
    
    def put(self, pos, l, r, i, j, f, same_flag, val):
        if l == i and j == r:
            f[pos] = val
            same_flag[pos] = True
            return
        
        mid = (l + r) >> 1
        if same_flag[pos]:
            self.put(pos + pos + 1, l, mid, l, mid, f, same_flag, f[pos])
            self.put(pos + pos + 2, mid + 1, r, mid + 1, r, f,same_flag, f[pos])
            same_flag[pos] = False

        f[pos] = max(val, f[pos])

        if j <= mid:
            self.put(pos + pos + 1, l, mid, i, j, f, same_flag, val)
        elif i > mid:
            self.put(pos + pos + 2, mid + 1, r, i, j, f, same_flag, val)
        else:
            self.put(pos + pos + 1, l, mid, i, mid, f, same_flag, val)
            self.put(pos + pos + 2, mid + 1, r, mid + 1, j, f, same_flag, val)
        
        if f[pos + pos + 1] == f[pos + pos + 2] and same_flag[pos + pos + 1] and same_flag[pos + pos + 2]:
            same_flag[pos] = True
```
