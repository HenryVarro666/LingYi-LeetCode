---
title: "3590. 第K小的路径异或和"
aliases: ["yiduobo的每日leetcode 3590.第K小的路径异或和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/binary-indexed-tree", "leetcode/ordered-set", "leetcode/sorting", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/八-树状数组和线段树", "题单/常用数据结构/十一-根号算法", "题单/常用数据结构/专题-离线算法", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1939489676860823544"
zhihu_id: "1939489676860823544"
zhihu_title: "yiduobo的每日leetcode 3590.第K小的路径异或和"
question_id: "3590"
question: "第 K 小的路径异或和"
problem_url: "https://leetcode.cn/problems/kth-smallest-path-xor-sum/"
difficulty: "Hard"
rating: 2646
created: "2025-08-15T02:11:52+08:00"
updated: "2025-08-15T02:11:53+08:00"
upvotes: 1
comments: 0
---

# 3590. 第K小的路径异或和

> **[yiduobo的每日leetcode 3590.第K小的路径异或和](https://zhuanlan.zhihu.com/p/1939489676860823544) · 知乎 · 2025-08-15 · 赞同 1**
> 力扣：[3590. 第 K 小的路径异或和](https://leetcode.cn/problems/kth-smallest-path-xor-sum/) · Hard · 灵茶山艾府：[三种方法：启发式合并 + 有序集合 / DFS 时间戳 + 莫队 + 树状数组 / 分块](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3590.第K小的路径异或和

[3590. 第 K 小的路径异或和 - 力扣（LeetCode）](https://leetcode.cn/problems/kth-smallest-path-xor-sum/)

题目给定一颗以节点0为根节点的无向树，其中有n个节点，按照0到n - 1编号，n最大可达50000。每个节点index有一个整数值vals[index]，vals[index]的大小不超过10^5，同时index的父节点为par[index]。

定义从根节点0到节点u的路径异或和为从根节点到节点u的路径上所有节点index的vals[index]的按位异或，包括节点u。

另外给出一个二维整数数组queries，其长度不超过50000。其中的queries\[index\] \= \[u\[index\], k\[index\]\]，表示询问以u\[index\]为根的子树的所有节点中，第k\[index\]小的不同路径异或和。如果不同异或和少于k\[index\]，则查询的结果为-1。

首先，对于树中某个节点now，从根节点到now的路径异或和，可以通过根节点到now的父节点fa的路径异或和，再异或上vals[now]得到。另一方面，对于这类询问子数中所有节点相关的问题，通常可以通过dfs序将其转化为区间问题。基于以上两点，就可以先从根节点开始进行一趟dfs，一边计算从根节点到每个节点的路径异或和并使用一个数组xor按照dfs的顺序记录下这些异或和，同时对于每个节点now，分别记录首次到达now时数组xor的长度，以及遍历完now的所有孩子回溯到now时xor的长度，这中间的部分就是以now为根节点的子树中中所有孩子节点对应的异或和。这样一来，问题就转化为了如何求解静态的区间中不重复的第k小值。

对于这个问题，我一开始没注意到要找的是不重复的第k小值，所以选择了可持久化线段树来求解，不过后来注意到了这里的不重复，这也就意味着需要动用到嵌套树这种我从没写过的东西，于是转而改成使用莫队算法来求解。

莫队算法指的是对于多个离线的区间查询问题：

1、如果这些区间的规模n和查询次数m的规模接近

2、如果可以高效地（例如O(1)或者O(logn)，在这里记为O(t)）从区间[x, y]的答案扩展到区间[x - 1, y]、[x + 1, y]、[x, y - 1]、[x, y + 1]的答案

那么就可以通过规划这些区间的求解顺序，利用类似滑动窗口的处理方法，在O((n + m) \* sqrt(n) \* t)的时间内求出所有的查询。

具体实现的思路其实也非常直观，先将所有查询按区间左边界，以大小b \= sqrt(n)分配到不同的块中，其中左边界为x的区间将分配到第x / b个块中。接下来，将所有区间按照所在块数为第一关键字，右边界为第二关键字从小到大进行排序。

对于排序后的区间，先暴力求出第一个区间的结果，然后记nowx和nowy分别为第一个区间的起点和终点，接下来对于后续的所有区间，设当前区间的边界为[x, y]，此时就按照每次一步的距离，将nowx和nowy移动到x和y，同时在这个过程中更新区间信息。移动完成后，再求解当前区间的结果，然后继续移动至下一个区间即可。

接下来考察这个处理方法的时间复杂度，在这里分别考虑nowx移动的次数以及nowy移动的次数。

首先，由于块的大小b \= sqrt(n)，因此块的数量n / b也等于sqrt(n)，也就是说块数的规模也是b。

接下来对于nowx，不妨设其移动的目标为x，那么当nowx和x处于同一个块中时，移动的总次数不超过b次，因为块的大小最大为b。而如果nowx和x不在同一个块中，这种情况最多会出现b - 1次，由于块数作为第一关键字参与了排序，因此这b - 1次移动是单调且互不重叠的，累加起来的总距离最多为n，也就是从0移动到n - 1。

这样一来，m组询问中nowx的移动次数就是m \* b + n，时间复杂度为O(m \* sqrt(n))

然后对于nowy，在这里改成以块为整体进行考虑。对于每个块中的y，其最多覆盖0到n - 1，因此单个块中nowy的移动次数最多为n次。另一方面，对于块间的移动，一共会执行b - 1次，每次移动的次数同样最多为n次。

这样一来，b个块中nowy的移动次数就是b \* n + (b - 1) \* n，时间复杂度为O(n \* sqrt(n))

综合以上两点，移动的总次数就是O((m + n) \* sqrt(n))。

到了这一步，问题就变成了如何高效地更新区间信息，同时对于已经移动到位的区间，如何求解其中不重复的第k小值。对于这个问题，则可以使用哈希表配合树状数组进行求解。

具体来说，使用哈希表freq记录当前区间内每种异或值出现的次数，同时使用值域树状数组f记录区间中出现过的元素，那么对于单次移动：

1、当nowx需要通过加1向x移动时，说明原始区间的左边界向后收紧了，此时xor\[nowx\]被移出了区间，因此在这里需要将freq\[xor\[nowx\]\]减去1。若此时的freq\[xor\[nowx\]\]等于0，说明区间中没有xor\[nowx\]了，此时则应该从xor\[nowx\]开始向后迭代，将f中对应位置的元素都减去1，表示对于所有大于等于xor\[nowx\]的元素，因为此次xor\[nowx\]的移除，区间中小于该元素的数目减少了1。

2、当nowx需要通过减一向x移动时，说明原始区间的左边界向前扩展了，此时xor\[nowx - 1\]被加入到区间，因此在这里需要将freq\[xor\[nowx - 1\]\]加上1。若此时的freq\[xor\[nowx - 1\]\]等于1，说明区间中刚好有一个xor\[nowx - 1\]，此时则应该从xor\[nowx - 1\]开始向后迭代，将f中对应位置的元素都加上1。

3、当nowy需要通过加1向y移动时，说明原始区间的右边界向后扩展了，此时xor\[nowy + 1\]被加入到区间，因此在这里需要将freq\[xor\[nowx + 1\]\]加上1。同样的，若此时的freq\[xor\[nowx + 1\]\]等于1，则应该从xor\[nowx + 1\]开始向后迭代，将f中对应位置的元素都加上1。

4、当nowy需要通过减1向y移动时，说明原始区间的右边界向前收缩了，此时xor\[nowy\]被移出了区间，因此在这里需要将freq\[xor\[nowy\]\]减去1，然后从xor\[nowy\]开始向后迭代，将f中对应位置的元素都减去1。

当nowx和nowy都移动到位后，树状数组中就记录了子数组中所有元素的值，接下来就可以利用二分法求出其中第k小的元素。

由于题目中vals的取值范围不超过100000，因此所有的异或值必然在0到131071之间，其中131071是131072减去1，也就是大于100000，且二进制表示中全为1的最小值。

另一方面，由于使用了值域树状数组，而树状数组的有效下标从1开始，因此异或值在加入其中时需要进行加1的修正，所以在这里二分的上下界就应该是1和131072。

接下来对于二分到的mid，通过树状数组计算1到mid之间有多少个元素，也就是从mid开始向下迭代，累加对应的f值。若这些元素的总数大于等于k，那么就修正二分上界为mid，否则修正二分下界为mid + 1。在具体实现上，为了处理区间内元素数量不够的情况，可以将二分上界调整到131073，若最终的二分结果为131073，则说明此次查询对应的结果为-1。

这样一来，就可以在O((m + n) \* sqrt(n) \* logV \* logV)的复杂度内计算出所有查询的答案了，其中V是使用的定值131072。值得一提的是，在这里如果先将所有的异或值排序后进行离散化的话，后面树状数组和二分的复杂度还可以进一步降低成logn \* logn，我在这里偷懒，就没有加这一步优化了。

最后附上python代码：

```python
class Solution(object):
    def kthSmallest(self, par, vals, queries):
        """
        :type par: List[int]
        :type vals: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(par)
        g = [[] for _ in range(n)]
        for index, fa in enumerate(par[1:], 1):
            g[fa].append(index)

        start = [None] * n
        end = [None] * n
        xor = []

        def dfs(now, x):
            x ^= vals[now]
            start[now] = len(xor)
            xor.append(x)

            for nxt in g[now]:
                dfs(nxt, x)
            
            end[now] = len(xor) - 1
        

        dfs(0, 0)

        q = [[start[v], end[v], k, index] for index, (v, k) in enumerate(queries)]
        res = [-1] * len(q)

        b = int(n ** 0.5)
        if b == 0:
            b += 1

        q.sort(key=lambda d:(d[0] // b, d[1]))
        f = [0] * 131073

        def add(x, delta):
            while x <= 131072:
                f[x] += delta
                x += x & -x
        
        def get(k):
            left = 1
            right = 131073
            while left < right:
                mid = (left + right) // 2
                x = mid
                cnt = 0
                while x > 0:
                    cnt += f[x]
                    x -= x & -x

                if cnt >= k:
                    right = mid
                else:
                    left = mid + 1
            
            if left == 131073:
                return -1
            return left - 1

        freq = {}

        for v in range(q[0][0], q[0][1] + 1):
            freq[xor[v] + 1] = freq.get(xor[v] + 1, 0) + 1
            if freq[xor[v] + 1] == 1:
                add(xor[v] + 1, 1)
        res[q[0][3]] = get(q[0][2])
        nowx, nowy = q[0][0], q[0][1]

        for x, y, k, index in q[1:]:
            while nowx > x:
                nowx -= 1
                freq[xor[nowx] + 1] = freq.get(xor[nowx] + 1, 0) + 1
                if freq[xor[nowx] + 1] == 1:
                    add(xor[nowx] + 1, 1)

            while nowx < x:
                freq[xor[nowx] + 1] = freq.get(xor[nowx] + 1, 0) - 1
                if freq[xor[nowx] + 1] == 0:
                    add(xor[nowx] + 1, -1)
                nowx += 1
            
            while nowy > y:
                freq[xor[nowy] + 1] = freq.get(xor[nowy] + 1, 0) - 1
                if freq[xor[nowy] + 1] == 0:
                    add(xor[nowy] + 1, -1)
                nowy -= 1

            while nowy < y:
                nowy += 1
                freq[xor[nowy] + 1] = freq.get(xor[nowy] + 1, 0) + 1
                if freq[xor[nowy] + 1] == 1:
                    add(xor[nowy] + 1, 1)

            res[index] = get(k)
        
        return res
```
