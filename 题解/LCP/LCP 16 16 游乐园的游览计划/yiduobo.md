---
title: "LCP 16. 游乐园的游览计划"
aliases: ["yiduobo的每日leetcode LCP16.游乐园的游览计划"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/571671362"
zhihu_id: "571671362"
zhihu_title: "yiduobo的每日leetcode LCP16.游乐园的游览计划"
question_id: "LCP 16"
question: "游乐园的游览计划"
problem_url: "https://leetcode.cn/problems/you-le-yuan-de-you-lan-ji-hua/"
created: "2022-10-09T04:53:21+08:00"
updated: "2022-10-09T04:53:21+08:00"
upvotes: 0
comments: 0
---

# LCP 16. 游乐园的游览计划

> **[yiduobo的每日leetcode LCP16.游乐园的游览计划](https://zhuanlan.zhihu.com/p/571671362) · 知乎 · 2022-10-09 · 赞同 0**
> 力扣：[LCP 16. 游乐园的游览计划](https://leetcode.cn/problems/you-le-yuan-de-you-lan-ji-hua/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP16.游乐园的游览计划

[力扣](https://leetcode.cn/problems/you-le-yuan-de-you-lan-ji-hua/)

非常复杂的分情况讨论的问题。题目给出若干带权重的点，要求从中找出两个有边或点重叠的三角形，使得这两个三角形中出现的点权重之和最大。

直接枚举每个三角形的时间复杂度高达O(n^3)，即使使用哈希表，也需要O(n^2)的时间来枚举完所有的三角形。

再次观察题目的数据规模，发现有一点值得注意，即边的数量与点的数量是一个量级的，那么可以从这里想办法寻找突破口。

不妨设图中边的数量为M，也就意味着所有节点度的和为2M。不妨以sqrt(2M)为阈值划线，将度数小于阈值的节点归为一类，将度数大于等于阈值的节点归位另一类。

首先，对于前一类节点，这些节点的特点是边数比较少，因此在这里应该枚举这些节点所连接的边。即对于某个节点i，枚举与i相连的两条边(i, j)和(i, k)，若j与k也相连，那么就找到了(i, j, k)这样一组三角形。

这个步骤总的运算次数为d[0]^2 + d[1]^2 + ... + d[p]^2，这里的d[i]表示第i个节点的度。由于这部分节点的度都小于sqrt(2M)，那么

d[0]^2 \< d[0] \* sqrt(2M)

d[1]^2 \< d[1] \* sqrt(2M)

...

d[p]^2 \< d[p] \* sqrt(2M)

于是就有

d[0]^2 + d[1]^2 + ... + d[p]^2 \< (d[0] + d[1] + ... + d[p]) \* sqrt(2M)

又由于d[0] + d[1] + ... + d[p]必然小于等于图的总度数2M，于是这一步的时间复杂度就是O(M \* sqrt(M))

接下来，对于后一类节点，这部分节点的边数较多，但点数较少，因此单个节点的度数大于等于sqrt(2M)，因此这部分点的总数必然小于等于sqrt(2M)，否则图的总度数就超过2M了。因为点数较少，那么自然就是枚举三角形的三个点，然后判断是否两两相连。这一步的时间复杂度为O(sqrt(M)^3)，同样是O(M \* sqrt(M))

这样一来，通过划线分类，就可以在比较优良的时间复杂度内找出图中所有的三角形了。

另外，根据上面的时间复杂度还有一个隐藏的条件就是，图中三角形的数量也是M \* sqrt(M)这个量级的，因为即使两种情况下的每一次枚举都形成了三角形，那总的枚举次数就是图中三角形的次数，这个量级最多也就是M \* sqrt(M)。有了这个前提，至少在后续的分类讨论时可以对所有三角形进行简单的遍历操作而不会出现时间复杂度过高的问题。

接下来的问题是如何选择三角形。

题目给出了三种选择方法，分别是：

1、选择两个完全重叠的三角形。

对于这种情况，实际上就是选择一个三角形，那么很明显应该选择点权重和最大的那个三角形，只需将所有三角形遍历一遍就行了。

2、选择两个有一条边重叠的三角形。

对于这种情况，可以枚举所有三角形，以三角形的三条边作为哈希表的key，储存包含key这条边的点权重最大的两个三角形。接下来就只需要枚举哈希表中的key，使用点权重最大的两个三角形来更新答案。

3、选择只有一个点重叠的三角形。

这种情况稍微复杂一点，但是也只有两种子情况。不妨设重叠的点为A，包含点A的权重最大的三角形为ABC，那么B和C必然都会出现在某个最优解中。下面给出简单的证明：

若B和C都没有出现，那么使用ABC替代选择的某个三角形，最终的点权和要么更大，要么保持不变。

若B或C其中一方没有出现，那么不妨设另一方与AD组成了三角形。此时使用B和C中没有出现的那一方替换掉D，最终的点权和要么更大，要么保持不变。

由于B和C都会出现，那么就可以分成两种子情况：

3-1）ABC组成了一个三角形，而另一个三角形则是ADE。对于这种情况，需要以A作为key，记录包含A的权重最大的三角形。接下来枚举所有三角形，然后以三角形的三个点分别作为key去哈希表中寻找对应的最大的三角形，若哈希表中的三角形与当前枚举的三角形只有点A重叠，那么就用这两个三角形的点来更新答案。

3-2）ABD组成了一个三角形，ACE组成了另一个三角形。对于这种情况，实际上相当于找包含边AB的次大的三角形，以及包含边AC的次大的三角形，这里正好可以复用情况2中以边作为key的哈希表。不过需要特别注意的是，这里的ABD和ACE，要求D和E不能相同，而情况2中的哈希表中保存的包含边AB的次大的三角形的第三点可能与包含边AC的次大的三角形的第三点相同，这种情况下这两个三角形是不能使用的。于是还需要将情况2中边的哈希表扩展一下，变成储存包含key这条边的点权重最大的三个三角形，这样一来就可以避免上面所说的第三点相同的情况了。

最后附上python代码：

```python
class Solution(object):
    def maxWeight(self, edges, value):
        """
        :type edges: List[List[int]]
        :type value: List[int]
        :rtype: int
        """

        linked = {}
        for x, y in edges:
            if x not in linked:
                linked[x] = set()
            if y not in linked:
                linked[y] = set()
            linked[x].add(y)
            linked[y].add(x)
        
        n = len(linked)
        m = len(edges)
        #阈值划线
        threshold = int(sqrt(2 * m))
        triangle_set = set()

        over_set = set()
        #低度数的点构成的三角形
        for i in linked:
            if len(linked[i]) < threshold:
                for j in linked[i]:
                    for k in linked[i]:
                        if j == k or k not in linked[j]:
                            continue
                        triangle_set.add(tuple(sorted([i, j, k])))
            else:
                over_set.add(i)
        
        #高度数的点构成的三角形
        for i in over_set:
            for j in over_set:
                if i == j or j not in linked[i]:
                    continue
                for k in over_set:
                    if i == k or j == k or k not in linked[i] or k not in linked[j]:
                        continue
                    triangle_set.add(tuple(sorted([i, j, k])))
        
        def add(key, other, v, first, second, third):
            if key not in first:
                first[key] = [0, None]
            if key not in second:
                second[key] = [0, None]
            if key not in third:
                third[key] = [0, None]
            
            if v > first[key][0]:
                third[key] = second[key][:]
                second[key] = first[key][:]
                first[key][0] = v
                first[key][1] = other

            elif v > second[key][0]:
                third[key] = second[key][:]
                second[key][0] = v
                second[key][1] = other
            
            elif v > third[key][0]:
                third[key][0] = v
                third[key][1] = other

        def get(key, other, first, second, third):
            first_flag = second_flag = True
            for node in other:
                if node == first[key][1]:
                    first_flag = False
                if node == second[key][1]:
                    second_flag = False
                    third_flag = False

            if first_flag:
                return first[key]
            elif second_flag:
                return second[key]
            else:
                return third[key]

        first = {}
        second = {}
        third = {}
        max_node = {}
        res = 0
        for i, j, k in triangle_set:
            v = value[i] + value[j] + value[k]
            #情况1,
            res = max(res, v)

            #更新边为key的哈希表
            add((i, j), k, v, first, second, third)
            add((i, k), j, v, first, second, third)
            add((j, k), i, v, first, second, third)
            
            #更新点为key的哈希表
            if i not in max_node or max_node[i][0] < v:
                max_node[i] = [v, set([j, k])]
            if j not in max_node or max_node[j][0] < v:
                max_node[j] = [v, set([i, k])]
            if k not in max_node or max_node[k][0] < v:
                max_node[k] = [v, set([i, j])]

        for i, j, k in triangle_set:
            #情况2
            res = max(res, get((i, j), [k], first, second, third)[0] + value[k])
            res = max(res, get((i, k), [j], first, second, third)[0] + value[j])
            res = max(res, get((j, k), [i], first, second, third)[0] + value[i])

            #情况3-1
            if j not in max_node[i][1] and k not in max_node[i][1]:
                res = max(res, max_node[i][0] + value[j] + value[k])
            if i not in max_node[j][1] and k not in max_node[j][1]:
                res = max(res, max_node[j][0] + value[i] + value[k])
            if i not in max_node[k][1] and j not in max_node[k][1]:
                res = max(res, max_node[k][0] + value[i] + value[j])

            #情况3-2
            v1, other1 = get((i, j), [k], first, second, third)
            v2, other2 = get((i, k), [j, other1], first, second, third)
            res = max(res, v1 + v2 - value[i])
            v2, other2 = get((j, k), [i, other1], first, second, third)
            res = max(res, v1 + v2 - value[j])

            v1, other1 = get((i, k), [j], first, second, third)
            v2, other2 = get((i, j), [k, other1], first, second, third)
            res = max(res, v1 + v2 - value[i])
            v2, other2 = get((j, k), [i, other1], first, second, third)
            res = max(res, v1 + v2 - value[k])

            v1, other1 = get((j, k), [i], first, second, third)
            v2, other2 = get((i, j), [k, other1], first, second, third)
            res = max(res, v1 + v2 - value[j])
            v2, other2 = get((i, k), [j, other1], first, second, third)
            res = max(res, v1 + v2 - value[k])
        
        return res
```
