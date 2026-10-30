---
title: "4033. 有效K个不同元素子数组I"
aliases: ["yiduobo的每日leetcode 4033.有效K个不同元素子数组I"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/binary-indexed-tree", "leetcode/prefix-sum", "leetcode/random", "leetcode/sliding-window", "leetcode/randomized", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/数学算法", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/常用数据结构/八-树状数组和线段树", "题单/常用数据结构/十一-根号算法", "题单/常用数据结构/专题-离线算法", "题单/数学算法/六-随机算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2077905933565424935"
zhihu_id: "2077905933565424935"
zhihu_title: "yiduobo的每日leetcode 4033.有效K个不同元素子数组I"
question_id: "4033"
question: "有效 K 个不同元素子数组 I"
problem_url: "https://leetcode.cn/problems/valid-k-unique-subarrays-i/"
difficulty: "Hard"
rating: 2314
created: "2026-09-01T01:14:16+08:00"
updated: "2026-09-01T01:14:16+08:00"
upvotes: 1
comments: 0
---

# 4033. 有效K个不同元素子数组I

> **[yiduobo的每日leetcode 4033.有效K个不同元素子数组I](https://zhuanlan.zhihu.com/p/2077905933565424935) · 知乎 · 2026-09-01 · 赞同 1**
> 力扣：[4033. 有效 K 个不同元素子数组 I](https://leetcode.cn/problems/valid-k-unique-subarrays-i/) · Hard · 灵茶山艾府：[异或哈希 + 滑动窗口 / 树状数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4033.有效K个不同元素子数组I

<https://leetcode.cn/problems/valid-k-unique-subarrays-i/description/>

题目给出一个整数数组nums，以及一个整数k。

另外给出一个二维整数数组queries，其中queries\[index\] \= \[left\[index\], right\[index\]\]，表示left\[index\]到right\[index\]这一段子数组。

对于每个查询的子数组，这个子数组中恰好包含k个不同的数字，且这些数字出现的次数都是偶数，那么就认为这个子数组是有效的。

要求返回一个布尔数组answer，其中answer[index]表示queries[index]这个查询对应的子数组是否是有效的。

题目中对子数组有效的判别标准实际上是两个无关的部分，因此可以拆开来分别处理。

---

对于恰好包含k个不同的数字，实际上是比较好处理的。对于确定了左边界的子数组，可以利用两个滑动窗口分别找出最左侧使得子数组中至少包含k个不同数字的右边界p1，以及最左侧使得子数组中至少包含k + 1个不同数字的右边界p2，那么所有右边界在p1到p2 - 1的子数组中就都是恰好包含k个不同数字的子数组。也就是说，利用两个滑动窗口，对nums进行一趟遍历，记录每个位置作为左边界时对应的p1和p2，那么在查询[x, y]时就只需要检测y是否处于x对应的p1到p2 - 1之间即可。

---

对于每个元素的出现次数是否为偶数，就不太好处理了。

这类区间查询的问题，一个直观的思想就是将其转化为前缀问题进行处理。对于本题，则需要对每个前缀都需要想办法记录每种数字出现的奇偶情况，同时这些记录下来的东西还需要能够高效对比，这样才能高效判断区间中的每种元素出现次数是否恰好为偶数。

如果不同数字的种类比较少，例如不超过64种，那么使用二进制编码来进行压缩就是一个可行的做法：不妨设一共有m中不同的数字，那么就可以使用一个长度为m的01串来记录前缀中每种元素出现的奇偶性。对于第index种元素，若其在前缀中出现的次数为奇数，那么就将这个01串的第index位置为1，否则置为0，这样一来，这个01串对应的数字就表示了这个前缀中每种数字的奇偶情况。随着前缀右边界向后移动，每一步只需在上一步的基础上将对应位置上的元素异或1就行了。而对于查询[x, y]，则只需要检测x - 1对应的前缀值是否与y对应的前缀值完全相同就行了。

---

很可惜，本题中出现的不同数字种类数m没有限制，因此通过这种状态压缩的方式是行不通的，但是这个01串的思路本身是很优秀的，在这里可以考虑换一种方法来记录每种前缀对应的01串，要求有三点：

- 修改复杂度低
- 空间占用合理
- 可比较

由于还没有确定最终的记录方式，因此修改复杂度无从谈起，那么可以先从后两点出发来考虑。

首先是空间占用合理。如果算上空字符串，一共有n + 1个不同的前缀，因此在这里最好能将这个01串表示成一个唯一的值，相当于将其哈希掉。不过这个串的长度上限m在极限情况下就等于n，因此常规的哈希手段要么有冲突的危险，要么复杂度太高。

另一方面，本题中的可比较是相对特殊的。对于每一组查询，实际上只需要检测x - 1和y对应的哈希值是否相同。那么在这里就只需要满足，每种不同的01串，其对应的哈希值是不会冲突的就行了。

最后再回过头来看修改复杂度。由于最终只需要计算一个哈希值，因此在这里需要将每次修改以及计算哈希值的复杂度控制在O(1)或者O(logn)。直观来看，O(1)似乎不太可能，若对于O(logn)这个级别，联想到的是二分有关的算法，或者树有关的算法。

尝试后可以发现，基于树的算法是非常合适的。方便起见，可以令p表示大于等于m的最小的2的幂次，接下来可以使用类似线段树的结构，建立一颗包含2p - 1个节点的满二叉树，编号为1到2p。这样编码的好处是对于每个节点u，其父亲节点为u >> 1，左右孩子分别为u \<\< 1以及(u \<\< 1) + 1，而兄弟节点则是u^1，也就是说可以通过位运算高效定位到其亲属节点。对于这m种不同的数字，让这些数字占据最底下这一层的前m个节点，后续的节点则不表示任何具体含义，仅起到占位的作用。而对于非叶子节点，则表示其涵盖的子数对应的01串的哈希值，因此1号节点的哈希值就是整个01串的哈希值，也就是上面需要计算的东西。

接下来对于修改操作，则只需要定位到这个数字在叶子层中对应的节点，然后沿着这个节点向上进行修改，直到根节点为止，其他所有节点的哈希值则可以保持不变，理由是这条修改路径已经涵盖了整棵树中所有包含这个叶子节点的子树的根节点，而对于其他的子树，对应的01串并没有发生变化，因此可以沿用之前的哈希值。

由于这条路径的长度就是树的高度，因此这个修改操作的复杂度是O(logp \* modify)的，其中O(modify)是修改单个节点哈希值的复杂度。很明显，这里modify的复杂度最好是O(1)或者O(logn)的。

到了这里，还剩下一个问题，就是如何高效地对单个节点进行哈希编码。需要特别注意的是，对于历史上出现过的01串，其对应的哈希值必须和历史上对应的哈希值相同。

首先考虑叶子节点。叶子节点的编码比较简单，由于每个叶子节点有奇偶两种状态，因此只需占据0到2p - 1这一共2p个哈希值就行了。其中第k种数字的编码为k \<\< 1以及(k \<\< 1) + 1，这样做的好处是对于index这个叶子，可以直接通过f[index]^1来切换其奇偶性对应的哈希值。

而对于非叶子节点，则需要自底向上逐层分配哈希值。具体的做法则是通过进一步对左右孩子的哈希值进行哈希的方式来保证编码的唯一性：对于某个非叶子节点，不妨设其编号为index，那么其左右孩子的编号为index \<\< 1以及(index \<\< 1) + 1。由于f[index \<\< 1]以及f[(index \<\< 1) + 1]已经是唯一的哈希值，因此其组合形成的key \= (f[index \<\< 1], f[(index \<\< 1) + 1])也是唯一的(这里需要保证两个f值的大小顺序是小的在前大的在后)，那么就可以再使用一个哈希表node_dict，为每种key分配一个哈希值。注意上面的叶子节点占据了0到2p - 1，因此接下来需要从2p开始进行分配。自底向上从左到右逐个分配，就完成了空字符串对应的树的初始化。

接下来是修改操作，可以先定位到修改的叶子节点index，然后到根节点的路径自底向上进行修改。首先，将index这个节点在哈希值修改为f[index]^1，然后考虑逐层向上修改父亲和祖先节点。对于index，其没有被修改的另一侧兄弟节点为index ^ 1，对应的哈希值不变，依然是f[index ^ 1]。因此若f[index]较小，那么node_dict的key就是(f[index], f[index ^ 1])，否则就是(f[index ^ 1], f[index])。接下来，若这个key在node_dict中出现过，那么index的父节点的哈希值，即f[index >> 1]就应该被修改为node_dict[key]，否则就需要额外分配一个之前没用过的哈希值给node_dict[key]，并将其赋给f[index >> 1]。接下来，将index右移一位来到其父亲节点所在的位置并重复上面的修改过程，直到index移动到根节点为止。

这样一来，单个节点修改的复杂度就是O(1)，而单次修改的复杂度就是O(logp)了。

最后附上python代码：

```python
class Solution(object):
    def validSubarrays(self, nums, k, queries):
        """
        :type nums: List[int]
        :type k: int
        :type queries: List[List[int]]
        :rtype: List[bool]
        """
        
        n = len(nums)

        freq1 = {}
        freq2 = {}
        hit_k = []
        p1 = 0
        p2 = 0
        for index, v in enumerate(nums):
            if p1 < index:
                p1 = index
            while p1 < len(nums) and len(freq1) < k:
                freq1[nums[p1]] = freq1.get(nums[p1], 0) + 1
                p1 += 1
            
            if len(freq1) < k:
                hit_k.append([-1, -1])
                continue

            if p2 < index:
                p2 = index
            while p2 < len(nums) and len(freq2) < k + 1:
                freq2[nums[p2]] = freq2.get(nums[p2], 0) + 1
                p2 += 1

            hit_k.append([p1, p2 - 1])

            freq1[v] -= 1
            if freq1[v] == 0:
                freq1.pop(v)
            freq2[v] -= 1
            if freq2[v] == 0:
                freq2.pop(v)

        vid = {}
        m = 0
        for v in nums:
            if v not in vid:
                vid[v] = m
                m += 1

        p = 1
        while p < m:
            p <<= 1
        
        f = [0] * (p << 1)
        length = p
        nxt_id = p << 1
        node_dict = {}
        while length:
            for index in range(length, length << 1):
                if length < p:
                    node_dict[(f[index << 1], f[(index << 1) + 1])] = nxt_id
                    f[index] = nxt_id
                    nxt_id += 1
                else:
                    f[index] = (index - length) << 1
            length >>= 1
        
        prefix_id = [f[1]]
        for v in nums:
            index = vid[v] + p
            f[index] ^= 1
            while index > 1:
                brother = f[index ^ 1]
                if f[index] > brother:
                    key = (brother, f[index])
                else:
                    key = (f[index], brother)
                
                if key not in node_dict:
                    node_dict[key] = nxt_id
                    nxt_id += 1
                
                f[index >> 1] = node_dict[key]
                index >>= 1
            
            prefix_id.append(f[1])
        
        return [hit_k[x][0] <= y <= hit_k[x][1] and prefix_id[y + 1] == prefix_id[x] for x, y in queries]
```
