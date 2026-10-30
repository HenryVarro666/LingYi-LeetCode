---
title: "LCP 52. 二叉搜索树染色"
aliases: ["yiduobo的每日leetcode LCP52.二叉搜索树染色"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/577668416"
zhihu_id: "577668416"
zhihu_title: "yiduobo的每日leetcode LCP52.二叉搜索树染色"
question_id: "LCP 52"
question: "二叉搜索树染色"
created: "2022-10-27T03:31:01+08:00"
updated: "2022-10-27T03:31:01+08:00"
upvotes: 0
comments: 0
---

# LCP 52. 二叉搜索树染色

> **[yiduobo的每日leetcode LCP52.二叉搜索树染色](https://zhuanlan.zhihu.com/p/577668416) · 知乎 · 2022-10-27 · 赞同 0**
> 力扣：LCP 52. 二叉搜索树染色

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP52.二叉搜索树染色

[力扣](https://leetcode.cn/problems/QO5KpG/)

题目给出一颗二叉搜索树以及若干区间染色的操作，问最终树上红色节点的数量。虽然给出的是二叉搜索树，实际上可以认为是给出了一个数组以及若干区间染色操作，问最终数组中红色下标的数量。

如果把最终的求解红色下标的数量视为遍历数组，求当前下标是否为红色，那么就变成了一个非常典型的区间更新、单点求解的问题，可以使用线段树来求解。不过在这里区间的下标非常大，因此需要先将其离散化之后映射到0到n - 1，然后再使用线段树求解。

具体来说，首先可以将树上的值收集起来，得到数组num_list。接下来遍历num_list，将其中的num_list[index]映射到index，这样一来树上的值就都归到0到n - 1之间了。接下来，对于区间修改的两个端点x和y，若x > num_list[-1]或y \< num_list[0]，此时的区间[x, y]与树中的节点没有交集，因此不会产生任何影响，可以直接跳过，否则的话就应该将x映射到p，y映射到q，这里的p和q分别来自最小的大于等于x的数num_list[p]以及最大的小于等于y的数num_list[q]。这样也很好理解，因为[x, y]影响到的恰好就是树中值大于等于num_list[p]且小于等于num_list[q]的数，又因为num_list[p]和num_list[q]的映射值分别为p和q，因此可以将x映射到p，y映射到q。

可以发现，在这里对于某个值，其作为区间左边界和右边界的映射规则有细微区别，因此需要两个映射数组left_mapping和right_mapping来分别记录这个数的两种映射关系。其中left_mapping表示右边界，即映射时向左找最近的映射值，而right_mapping则表示左边界，即映射时向右找最近的映射值。

对于left_mapping和right_mapping的求解，则可以将所有的x和y也加入到num_list中，去重排序后得到sorted_mixed_num_list，接下来正反两趟遍历，利用前一个或后一个数来更新当前的left_mapping或right_mapping。

得到映射关系后，剩下的就是常规的区间更新的线段树操作了。与常规的线段树有所区别，区间更新时不会立即更新到每个叶子节点，而是到刚好与待更新区间重叠的某个节点就停止向下更新，同时使用一个标记记录当前节点表示的区间被整个更新过，后续可能需要向下继续更新。

那么对于一个更新操作(now, i, j, color)：

1、如上，如果当前now管辖的区间边界now.left \= i，且now.right \= j，那么就将now.color更新为color，同时置now的标签now.flag为true，然后停止向下更新

2、否则的话若now.color以及等于color，那么此时就无须执行更新操作，直接返回

3、否则的话

3-1）若now.flag为True，说明之前now管辖的区间被整个更新过，且由于情况2不成立，说明now.color并不等于当前要更新的color，于是将now.flag下放，将now的左右孩子的color更新为now.color，同时将左右孩子的flag置为true，然后将now.flag置为false

3-2）无论now.flag如何，都需要继续向下更新，此时遵照常规线段树的更新方式，通过now.left和now.right计算出中点mid，然后根据i、j以及mid的大小关系决定更新哪些子树。更新完成后，若左右子树的color相同，那么就置now.color为这个相同的color，否则置now.color为0，表示当前子树中的颜色是混合的

而对于查询操作，则按照常规的查询方式自顶向下查询就行了。不过需要注意的是，若某个节点now.color不为0，那么就无须继续往下查询，直接返回now.color即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution(object):
    def getNumber(self, root, ops):
        """
        :type root: Optional[TreeNode]
        :type ops: List[List[int]]
        :rtype: int
        """

        num_list = []

        def dfs(now):
            if now.left:
                dfs(now.left)
            num_list.append(now.val)
            if now.right:
                dfs(now.right)

        dfs(root)

        left_mapping = {}
        right_mapping = {}
        p = 0
        for index, num in enumerate(num_list):
            left_mapping[num] = right_mapping[num] = index
        
        mixed_num_set = set(num_list)
        for _, x, y in ops:
            mixed_num_set.add(x)
            mixed_num_set.add(y)

        sorted_mixed_num_list = sorted(list(mixed_num_set))
        for index in range(len(sorted_mixed_num_list)):
            now = sorted_mixed_num_list[index]
            if now not in left_mapping:
                if index == 0:
                    left_mapping[now] = -1
                else:
                    left_mapping[now] = left_mapping[sorted_mixed_num_list[index - 1]]
        
        for index in range(len(sorted_mixed_num_list) - 1, -1, -1):
            now = sorted_mixed_num_list[index]
            if now not in right_mapping:
                if index == len(sorted_mixed_num_list) - 1:
                    right_mapping[now] = n
                else:
                    right_mapping[now] = right_mapping[sorted_mixed_num_list[index + 1]]
        
        n = len(num_list)
        f = [0] * (n * 4)
        flag = [False] * (n * 4)

        def insert(now, left, right, i, j, f, color):
            if left == i and right == j:
                f[now] = color
                flag[now] = True
                return

            if f[now] == color:
                return
            
            if flag[now]:
                f[now + now + 1] = f[now + now + 2] = f[now]
                flag[now + now + 1] = flag[now + now + 2] = True
                flag[now] = False

            mid = (left + right) >> 1
            if j <= mid:
                insert(now + now + 1, left, mid, i, j, f, color)
            elif i > mid:
                insert(now + now + 2, mid + 1, right, i, j, f, color)
            else:
                insert(now + now + 1, left, mid, i, mid, f, color)
                insert(now + now + 2, mid + 1, right, mid + 1, j, f, color)
            
            if f[now + now + 1] == f[now + now + 2]:
                f[now] = f[now + now + 1]
            else:
                f[now] = 0
        
        def get(now, left, right, f, pos):
            if f[now] != 0 or left == right:
                return f[now]
            
            mid = (left + right) >> 1
            if pos <= mid:
                return get(now + now + 1, left, mid, f, pos)
            else:
                return get(now + now + 2, mid + 1, right, f, pos)

        for type, x, y in ops:
            if right_mapping[x] == n or left_mapping[y] == -1:
                continue

            mapped_x = right_mapping[x]
            mapped_y = left_mapping[y]

            insert(0, 0, n - 1, mapped_x, mapped_y, f, 2 - type)

        res = 0
        for index in range(n):
            if get(0, 0, n - 1, f, index) == 1:
                res += 1

        return res
```
