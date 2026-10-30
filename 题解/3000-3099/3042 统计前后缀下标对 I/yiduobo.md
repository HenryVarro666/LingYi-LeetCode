---
title: "3042. 统计前后缀下标对I & 3045. 统计前后缀下标对II"
aliases: ["yiduobo的每日leetcode 3042.统计前后缀下标对I && 3045.统计前后缀下标对II", "3042. 统计前后缀下标对I", "3045. 统计前后缀下标对II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/trie", "leetcode/hard", "leetcode/string-matching", "题单/常用数据结构", "题单/字符串", "题单/常用数据结构/六-字典树-trie", "题单/字符串/二-Z-函数-后缀的前缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695945163"
zhihu_id: "695945163"
zhihu_title: "yiduobo的每日leetcode 3042.统计前后缀下标对I && 3045.统计前后缀下标对II"
question_id: ["3042", "3045"]
question: ["统计前后缀下标对 I", "统计前后缀下标对 II"]
problem_url: ["https://leetcode.cn/problems/count-prefix-and-suffix-pairs-i/", "https://leetcode.cn/problems/count-prefix-and-suffix-pairs-ii/"]
difficulty: ["Easy", "Hard"]
rating: 2328
created: "2024-05-04T23:46:48+08:00"
updated: "2024-05-04T23:46:48+08:00"
upvotes: 2
comments: 0
---

# 3042. 统计前后缀下标对I & 3045. 统计前后缀下标对II

> **[yiduobo的每日leetcode 3042.统计前后缀下标对I && 3045.统计前后缀下标对II](https://zhuanlan.zhihu.com/p/695945163) · 知乎 · 2024-05-04 · 赞同 2**
> 力扣：[3042. 统计前后缀下标对 I](https://leetcode.cn/problems/count-prefix-and-suffix-pairs-i/) · Easy · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3045. 统计前后缀下标对 II](https://leetcode.cn/problems/count-prefix-and-suffix-pairs-ii/) · Hard · 灵茶山艾府：[两种方法：Z 函数+字典树/只用字典树（Python/Java/C++/Go）](../3045%20统计前后缀下标对%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3042.统计前后缀下标对I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-prefix-and-suffix-pairs-i/description/)

3045.统计前后缀下标对II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-prefix-and-suffix-pairs-ii/description/)

题目给出一个字符串数组words，要求计算存在多少下标对i \< j满足words[i]既是words[j]的前缀，也是words[j]的后缀。

两题的题设一样，第二题的数据规模比较大，必须使用O(n)的算法。

首先对于前缀匹配问题，使用trie树就可以解决。如果不考虑字符串哈希自身的复杂度，使用哈希表应该也凑合。另一方面，对于后缀匹配的问题，则可以将两个字符串都反过来看，这样一来就又变成了前缀匹配问题。

但是需要注意的是，在这里虽然单独进行前缀匹配或者后缀匹配是可以利用trie树高效求解的，不过之后还多出了一步下标对匹配的过程。具体来说，对于某个下标i，可以通过trie树得到一个前缀匹配成功的下标集合prefix_j，以及另一个后缀匹配成功的下标集合suffix_j，但是接下来还需要检测这两个集合的交集是什么，在最坏情况下整个算法的时间复杂度就来到了O(n^2)。

一种可行的思路是既然words[i]在前缀trie树和后缀trie树中匹配的长度相同，那么不妨将二者合并，即构造trie树以及进行匹配时，使用(words[0], words[-1])，(words[1], words[-2])，...，(words[-1], words[0])这样的字符对来作为树中的节点。这样做的好处是只要匹配成功，就能保证前后缀都匹配成功，也就不需要进行集合取交集的操作，而是只需要记录trie树中每个节点的权重就行了。

于是只需从后往前遍历words，对于当前遍历到的字符串w，枚举下标index并构造字符对(w[index], w[-index - 1])，然后使用字符对来更新trie树。枚举完成后，使用trie树当前节点的权重减1来更新答案，这里减1的理由是当前节点的权重包含了w自身，因此需要减去。

最后附上python代码：

```python
class Node():
    def __init__(self):
        self.childs = {}
        self.weight = 0

class Solution(object):
    def countPrefixSuffixPairs(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        root = Node()
        res = 0
        for w in words[::-1]:
            now = root
            for index in range(len(w)):
                key = (w[index], w[-index - 1])
                if key not in now.childs:
                    now.childs[key] = Node()
                now = now.childs[key]
                now.weight += 1
            
            res += now.weight - 1
        
        return res
```
