---
title: "3291. 形成目标字符串需要的最少字符串数I & 3292. 形成目标字符串需要的最少字符串数II"
aliases: ["yiduobo的每日leetcode 3291.形成目标字符串需要的最少字符串数I && 3292.形成目标字符串需要的最少字符串数II", "3291. 形成目标字符串需要的最少字符串数I", "3292. 形成目标字符串需要的最少字符串数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/string", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/string-matching", "leetcode/hash-function", "leetcode/hard", "leetcode/greedy", "leetcode/two-pointers", "题单/动态规划", "题单/字符串", "题单/动态规划/十一-优化-DP", "题单/字符串/二-Z-函数-后缀的前缀", "题单/字符串/四-字符串哈希", "题单/字符串/七-AC-自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/898484268"
zhihu_id: "898484268"
zhihu_title: "yiduobo的每日leetcode 3291.形成目标字符串需要的最少字符串数I && 3292.形成目标字符串需要的最少字符串数II"
question_id: ["3291", "3292"]
question: ["形成目标字符串需要的最少字符串数 I", "形成目标字符串需要的最少字符串数 II"]
problem_url: ["https://leetcode.cn/problems/minimum-number-of-valid-strings-to-form-target-i/", "https://leetcode.cn/problems/minimum-number-of-valid-strings-to-form-target-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2662
created: "2024-10-10T04:37:59+08:00"
updated: "2024-10-10T04:37:59+08:00"
upvotes: 0
comments: 0
---

# 3291. 形成目标字符串需要的最少字符串数I & 3292. 形成目标字符串需要的最少字符串数II

> **[yiduobo的每日leetcode 3291.形成目标字符串需要的最少字符串数I && 3292.形成目标字符串需要的最少字符串数II](https://zhuanlan.zhihu.com/p/898484268) · 知乎 · 2024-10-10 · 赞同 0**
> 力扣：[3291. 形成目标字符串需要的最少字符串数 I](https://leetcode.cn/problems/minimum-number-of-valid-strings-to-form-target-i/) · Medium · 灵茶山艾府：[三种方法：Z 函数 / 字符串哈希+二分 / AC 自动机（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3292. 形成目标字符串需要的最少字符串数 II](https://leetcode.cn/problems/minimum-number-of-valid-strings-to-form-target-ii/) · Hard · 灵茶山艾府：[三种方法：Z 函数 / 字符串哈希 / AC 自动机（Python/Java/C++/Go）](../3292%20形成目标字符串需要的最少字符串数%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3291.形成目标字符串需要的最少字符串数I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-valid-strings-to-form-target-i/description/)

3292.形成目标字符串需要的最少字符串数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-valid-strings-to-form-target-ii/description/)

题目给出一个字符串数组words以及一个字符串target。现在要求使用words中字符串的前缀来拼接得到target，问最少使用多少个字符串可以完成拼接。words中的字符串可以多次使用。

第二题数据规模较大，单词的总长度可以来到10^5，而target的长度高达5 \* 10^4。

遇到拼接单词问题，动态规划的算法是比较容易想到的。令f[index]表示拼接出target前index个字符所需的字符串数量，那么对于f[index]，首先有f[0] \= 0，表示拼接空串；接下来对于index > 0，有f[index] \= f[pre] + 1，这里的pre必须满足target[pre : index]是words中某个单词的前缀。

由于数据规模的原因，在这里直接暴力枚举pre的位置并去words中进行匹配显然是行不通的，必须进行优化。

首先可以明确的一点是，对于i \< j，必然有f[i] \<\= f[j]。理由是如果f[j]是通过i之前的某一点k更新过来的，即f[j] \= f[k] + 1，k \< i，那么就要求target[k : j]是words中某个单词的前缀，而对于k \< i \< j，target[k : i]也必然是这个单词的前缀，换言之f[i]也是可以通过f[k] + 1更新得到的，因此当i \< j时必然有f[i] \<\= f[j]。

根据这一点，上面的状态转移方程f[index] \= f[pre] + 1，这里的pre就应该尽量往前靠。换言之，问题到了这里就变成了找出最小的pre，满足target[pre : index]是words中某个单词的前缀。

接下来的问题就比较难处理了，一种可行的做法是计算所有单词的所有前缀的哈希值，然后按长度对这些哈希值进行分组。接下来对于f[index]，可以二分pre的位置，利用对应长度的分组的哈希表来检测target[pre : index]的哈希值是否命中，来判断是否存在某个单词的前缀与target[pre: index]相同。

上面这种处理方法在之前碰到某个类似的问题时好像写过了，所以在这里我选择的是处理多字符串匹配的常见方法trie图。

trie图是基于trie树得到的一种图类数据结构，其思路与单字符串匹配中的kmp是一样的，就是以当前节点形成的子串无法继续匹配目标串的子串时，可以尝试通过之前的匹配结果将目标串的匹配起始位置向后移动，同时将当前节点移动到可以匹配新的子串的位置。

在kmp算法中，上述过程是通过构造next数组来实现的，而在trie图中，则需要构造fail指针来完成这一步。

首先对于根节点，没有fail这一说。而对于trie树中的第一层节点，一旦匹配失败就说明出现了一个完全无法匹配的字符，此时可以将fail指向根节点。接下来对于其他的节点，不妨设当前节点是其父亲节点的x孩子，那么当匹配失败时，则可以从当前节点开始，沿着父亲节点的fail指针向上迭代，直到找到一个存在x孩子的节点为止，当前节点的fail就指向这个节点。这个过程可以理解成，通过已知的父节点的fail来找到最佳的回溯位置，保留以父亲节点结尾的子串尽量长的后缀，然后为了适配当前节点，所以还必须满足fail指向的节点也具有x孩子。

具体实现上，可以自顶向下进行bfs，对于存在的孩子按上面的描述添加fail指针，对于不存在的孩子则只需要将对应孩子的指针直接指向当前节点fail指针指向节点对应的孩子节点，这样一来会新增很多的空间消耗，但是可以省去节点因父亲的fail不存在对应的孩子节点从而必须在树中迭代而带来的复杂度。

建立好trie图之后，让target在trie图中走一圈，不妨设对于当前的target[index]，上一轮匹配到的是trie图中的now，那么在这里就应该先让now沿着target[index]对应的边走到下一个节点，若此时now走回了根节点，说明出现了无法匹配的情况，直接返回-1，否则说明以target[index]结尾的子串的后缀匹配上了trie树中now为终点的子串，匹配的长度即为now的深度length，length在建立trie树时可以提前计算好。

根据trie图中fail指针的定义，这里匹配上的一定是以target[index]为结尾且长度尽量长的单词前缀，正好符合动态规划中f数组迭代的规则，因此在这里就有f[index + 1] \= f[index + 1 - now.length] + 1。这里的加1是因为f的定义是前多少个字符，而index是从下标0开始遍历的，对应的是前index + 1个字符。

最后附上python代码：

```python
class Node(object):
    def __init__(self, prefix_length, char):
        self.prefix_length = prefix_length
        self.childs = [None] * 26
        self.fail = None
        self.char = char

class Solution(object):
    def minValidStrings(self, words, target):
        """
        :type words: List[str]
        :type target: str
        :rtype: int
        """

        root = Node(0, None)
        for w in words:
            now = root
            for index, char in enumerate(w):
                asc = ord(char) - 97
                if now.childs[asc] is None:
                    now.childs[asc] = Node(index + 1, char)
                now = now.childs[asc]
        
        q = [root]
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                for index, c in enumerate(now.childs):
                    if c is None:
                        if now == root:
                            now.childs[index] = now
                        else:
                            now.childs[index] = now.fail.childs[index]
                    else:
                        if now == root:
                            c.fail = now
                        else:
                            c.fail = now.fail.childs[index]
                        q.append(c)

            head, tail = tail, len(q)
        
        
        n = len(target)
        f = [0]
        now = root
        for index, char in enumerate(target):
            asc = ord(char) - 97
            now = now.childs[asc]
            if now == root:
                return -1
            f.append(f[index + 1 - now.prefix_length] + 1)
        
        return f[-1]
```
