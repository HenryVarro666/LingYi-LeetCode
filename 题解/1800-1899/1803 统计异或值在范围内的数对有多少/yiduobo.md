---
title: "1803. 统计异或值在范围内的数对有多少"
aliases: ["yiduobo的每日leetcode 1803.统计异或值在范围内的数对有多少"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "题单/常用数据结构", "题单/位运算", "题单/常用数据结构/六-字典树-trie", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/464204732"
zhihu_id: "464204732"
zhihu_title: "yiduobo的每日leetcode 1803.统计异或值在范围内的数对有多少"
question_id: "1803"
question: "统计异或值在范围内的数对有多少"
problem_url: "https://leetcode.cn/problems/count-pairs-with-xor-in-a-range/"
difficulty: "Hard"
rating: 2479
created: "2022-02-05T23:31:46+08:00"
updated: "2022-02-05T23:31:47+08:00"
upvotes: 0
comments: 0
---

# 1803. 统计异或值在范围内的数对有多少

> **[yiduobo的每日leetcode 1803.统计异或值在范围内的数对有多少](https://zhuanlan.zhihu.com/p/464204732) · 知乎 · 2022-02-05 · 赞同 0**
> 力扣：[1803. 统计异或值在范围内的数对有多少](https://leetcode.cn/problems/count-pairs-with-xor-in-a-range/) · Hard · 灵茶山艾府：[不会字典树？只用哈希表也能做！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1803.统计异或值在范围内的数对有多少

[力扣](https://leetcode-cn.com/problems/count-pairs-with-xor-in-a-range/)

题目的数据规模并不算小，因此直接使用O(n^2)的朴素算法两两枚举数对肯定是行不通的。题目要求的是异或值在某个区间[low, high]内的数对数量，那么一个经典的转化就是分别求出异或值在[0, high]之间的数对数量，以及异或值在[0, low - 1]内的数对数量，然后用前者减去后者就是最终答案。

现在问题转化成了如何求解异或值在[0, limit]之间的数对数量，对于这个问题，需要从异或这个操作上再进行一些挖掘。由于异或是一种位运算，在这里也很自然想到用位的方式来看待问题。注意到2^15 \= 32768 > 20000，也就是说nums、high、low以及这些数字的异或结果都可以用15位的二进制数来表示。

对于limit，首先求出其二进制表示，那么一组合法的数对异或结果就必然满足下面两种情况之一：

1、异或结果的前k位与limit的前k位相同，且异或结果的第k + 1位为0，limit的k + 1位为1。这里的k可以为0

2、异或结果与limit完全一致

可以发现，实际上情况2可以认为是情况1的某种特例，即k等于15这种情况。

由于每一位上只能是0或者1，这也就有了一种办法，即遍历nums中的数，检测当前的数now与之前遍历过的数之间合法的数对有多少。在这里当然不是逐个枚举之前遍历过的数然后判断，而是从高位开始逐位计算。令index从14开始向下枚举到0，对于当前的位index，设当前数对应的位为binary_now[index]，limit对应的位为limit[index]，就可以计算的得出same \= binary_now[index] ^ limit[index]，other \= 1 ^ same。

这里same和other的含义就是对于当前数之前遍历过的数，若其index这一位为same，那么其与now异或结果的index这一位就与limit一样，否则就与limit不同。

当limit的index这一位为1时，index这一位为other的这些数与now异或结果在index上就会小于limit。此时只要能够保证index之前的位中other对应的这些数与now异或结果与limit一致，就能得出other这些数与now异或的结果小于limit了。而说到保持一致，恰好就是same对应的数。

也就是说，对于一个数而言，其最高的14位到index + 1这一位的二进制表示都是same，而index这一位为other，且limit在index这一位为1，就说明这个数与now异或结果小于limit。反过来，若limit在index这一位为0，那么就说明这个数与now异或结果大于limit。

无论是哪种情况，对于这个数而言都无需再考察index后续的位了，而对于前缀的运用，很自然想到使用trie树来进行优化。trie树中的每个节点只有0或1这两条边，除此之外还需要使用一个变量cnt记录有多少个数拥有当前的前缀，这样一来，就无须逐个遍历，而是直接通过前缀对应节点的cnt就可以知道有多少个数满足上面的条件了。

需要特别注意的是，上面这个做法在遍历完成后并没有处理情况2中，异或结果与limit完全一致这种情况。不过此时trie树应该恰好遍历到全是same的这个节点，那么这个节点对应的cnt就是异或结果与limit完全一致的数对数目，直接用这个cnt更新答案即可。

于是现在的做法就变成了一趟遍历，对于每个数，先在trie树中检测有多少个数与其组成的数对满足题目要求，同时更新答案，然后再将当前这个数加入到trie树中。

另外，在计算前对nums进行排序也是一种极速的trick。虽然无法从时间复杂度层级上优化，但是由于是从高位开始向下计算的，那么在排序后，可能可以让部分较小的数在高位上就直接被淘汰掉，从而减少最终的计算次数。

最后附上python代码：

```python
class Node(object):

    def __init__(self):
        self.sons = [None, None]
        self.cnt = 0

class Solution(object):
    def countPairs(self, nums, low, high):
        """
        :type nums: List[int]
        :type low: int
        :type high: int
        :rtype: int
        """

        pow2 = [1]
        for index in range(14):
            pow2.append(pow2[-1] + pow2[-1])

        low -= 1
        binary_low = [0] * 15
        binary_high = [0] * 15 
        for index in range(14, -1, -1):
            if low >= pow2[index]:
                binary_low[index] = 1
                low -= pow2[index]
            if high >= pow2[index]:
                binary_high[index] = 1
                high -= pow2[index]

        root = Node()
        res = 0
        nums = sorted(nums)
        for num in nums:
            binary_now = [0] * 15
            for index in range(14, -1, -1):
                if num >= pow2[index]:
                    binary_now[index] = 1
                    num -= pow2[index]
            
            p_low = root
            p_high = root
            for index in range(14, -1, -1):
                if p_high and p_high.cnt > 0:
                    same_son = binary_high[index] ^ binary_now[index]
                    other_son = 1 ^ same_son
                    if binary_high[index] == 1 and p_high.sons[other_son]:
                        res += p_high.sons[other_son].cnt
                    p_high = p_high.sons[same_son]

                if p_low and p_low.cnt > 0:
                    same_son = binary_low[index] ^ binary_now[index]
                    other_son = 1 ^ same_son
                    if binary_low[index] == 1 and p_low.sons[other_son]:
                        res -= p_low.sons[other_son].cnt
                    p_low = p_low.sons[same_son]
            
            if p_high:
                res += p_high.cnt
            if p_low:
                res -= p_low.cnt

            tree = root
            for index in range(14, -1, -1):
                tree.cnt += 1
                if tree.sons[binary_now[index]] is None:
                    tree.sons[binary_now[index]] = Node()
                tree = tree.sons[binary_now[index]]

            tree.cnt += 1

        return res
```
