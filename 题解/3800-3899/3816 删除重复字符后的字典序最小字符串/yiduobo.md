---
title: "3816. 删除重复字符后的字典序最小字符串"
aliases: ["yiduobo的每日leetcode 3816.删除重复字符后的字典序最小字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/greedy", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/四-最小字典序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1997065725546891060"
zhihu_id: "1997065725546891060"
zhihu_title: "yiduobo的每日leetcode 3816.删除重复字符后的字典序最小字符串"
question_id: "3816"
question: "删除重复字符后的字典序最小字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-string-after-deleting-duplicate-characters/"
difficulty: "Hard"
rating: 2377
created: "2026-01-23T01:50:36+08:00"
updated: "2026-01-23T01:50:39+08:00"
upvotes: 1
comments: 0
---

# 3816. 删除重复字符后的字典序最小字符串

> **[yiduobo的每日leetcode 3816.删除重复字符后的字典序最小字符串](https://zhuanlan.zhihu.com/p/1997065725546891060) · 知乎 · 2026-01-23 · 赞同 1**
> 力扣：[3816. 删除重复字符后的字典序最小字符串](https://leetcode.cn/problems/lexicographically-smallest-string-after-deleting-duplicate-characters/) · Hard · 灵茶山艾府：[单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3816.删除重复字符后的字典序最小字符串

<https://leetcode.cn/problems/lexicographically-smallest-string-after-deleting-duplicate-characters/description/>

题目给出一个字符串s，由小写英文字母组成。

现在可以执行以下操作任意次（可以为零次），每次操作中，需要选择s剩余字母中至少出现两次的任意一个字母并删掉其中的一个。

问通过以上操作可能得到的字典序最小的字符串是什么。

对于字典序最小相关的问题，一种直观的思路是先从'a'开始考虑。

对于本题，就是考虑s中首个'a'左侧的字符应该如何处理。直观来看，应该删掉首个'a'左侧所有出现至少两次的字符，但是很快就能找到反例，例如'bcab'这个字符串，如果将第一个'b'删去，由于'c'落单无法删除，最终得到的答案为'cab'，实际上是不如删掉最后一个'b'得到的'bca'的。

回头审视之前的做法，可以发现由于落单字符的存在，并不能无脑执行删除。再考虑之前首个'b'被删除的原因，是因为后续存在一个'a'，但是中间夹了一个落单的'c'，导致'a'并不能被推到首位上来，反而让'c'取代了'b'。也就是说，删除某个字符除了应该满足非落单的条件之外，还需要满足的一点是其与字典序更小的字符是相邻的，否则删除当前字符并不会使得答案更优。

基于上面的结论，就可以利用一个栈来实现这个删除操作，即每一步都只对比当前字符与栈顶字符的大小，来确定是否删掉栈顶的字符。

具体来说，先对s进行一趟遍历，统计每种字符出现的次数，接下来再对s进行一趟遍历，使用栈记录剩下的字符。对于当前遍历到的字符c，若栈非空，且栈顶字符大于c，同时栈顶字符出现次数大于1，那么就弹出栈顶字符，重复此过程直到栈为空，或者栈顶字符小于等于c，或者栈顶字符落单为止。接下来将c加入到栈中，然后继续向后遍历即可。

为了使得字典序最小，在保证前缀最小的前提下，还需要使得字符串最短，因此在遍历完成后，还需要清理掉字符串最后重复出现的字符。具体来说，就是不断检测当前栈顶字符出现次数是否大于1次，若满足，则将其从栈中弹出。处理完成后，栈中剩下字符形成的字符串即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def lexSmallestAfterDeletion(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        cnt = {}
        for c in s:
            cnt[c] = cnt.get(c, 0) + 1
        
        stack = []
        for c in s:
            while stack and c < stack[-1] and cnt[stack[-1]] > 1:
                cnt[stack.pop()] -= 1
            stack.append(c)
        
        while stack and cnt[stack[-1]] > 1:
            cnt[stack.pop()] -= 1
        
        return ''.join(stack)
```
