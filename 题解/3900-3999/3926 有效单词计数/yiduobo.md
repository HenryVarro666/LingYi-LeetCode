---
title: "3926. 有效单词计数"
aliases: ["yiduobo的每日leetcode 3926.有效单词计数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2038053356200048587"
zhihu_id: "2038053356200048587"
zhihu_title: "yiduobo的每日leetcode 3926.有效单词计数"
question_id: "3926"
question: "有效单词计数"
problem_url: "https://leetcode.cn/problems/count-valid-word-occurrences/"
difficulty: "Medium"
rating: 1608
created: "2026-05-14T00:42:31+08:00"
updated: "2026-05-14T00:42:32+08:00"
upvotes: 2
comments: 0
---

# 3926. 有效单词计数

> **[yiduobo的每日leetcode 3926.有效单词计数](https://zhuanlan.zhihu.com/p/2038053356200048587) · 知乎 · 2026-05-14 · 赞同 2**
> 力扣：[3926. 有效单词计数](https://leetcode.cn/problems/count-valid-word-occurrences/) · Medium · 灵茶山艾府：[分组循环（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3926.有效单词计数

<https://leetcode.cn/problems/count-valid-word-occurrences/description/>

题目给出一个字符串数组chunks，其中所有的子串都由小写字符以及空格、连字符组成。要求按顺序将这些字符串拼接起来，形成一个字符串s。

另外给出一个字符串数组queries。

单次定义为s的一个子串，并满足：

- 由小写英文字母组成
- 可以包含连字符，但是连字符的两侧必须都是小写英文字母
- 这个子串必须尽可能长
- 任何不是英文字母，也不是合法连字符的字符，都需要视为分隔符

要求返回一个整数数组ans，其中ans[index]表示queries[index]作为单词在s中出现的次数。

根据题目中对于单词的定义，实际上就是要求将chunks先合并成一个大的字符s，然后将非法的连字符视为空格，再进行split，并丢弃掉其中的空串，从而得到单词数组。基于这一点，就可以在合并的过程中先处理掉重复的空格以及非法的连字符，然后join起来直接split就行了。

具体来说，按顺序对chunks中所有子串进行遍历，使用一个数组记录有效字符，对于当前遍历到的字符c：

1、若c是小写字符：

此时直接将c加入到数组末尾即可

2、若c是空格或连字符：

2-1）若当前数组为空：

说明此时c将作为子串的首字符，显然c将是无用的空格或者非法的连字符，因此可以直接跳过c

2-2）若当前数组的最后一个字符为空格：

无论是两个连续的空格，还是一个空格接一个连字符，都将被视为一个分隔符，因此在这里可以无视c，保留最后这个空格就行了

2-3）若当前数组的最后一个字符为连字符：

与上面相同，无论是两个连续的连字符，还是一个连字符一个空格，都将被视为一个分隔符，因此在这里需要将数组的最后一个字符，从连字符替换成空格

2-4）若当前数组的最后一个字符为小写字母：

此时正常将c加入到数组末尾即可

遍历完成后，需要进行一次额外的判断：若数组最后一个字符为空格或者连字符，那么这个字符都是无效的，此时应该将其从数组中去除。

接下来，只需将数组join起来，形成目标字符串s，然后直接对s进行split，就得到了单词数组words。遍历其中的单词，使用哈希表记录每种单词出现的次数，最后再遍历queries，通过哈希表计算最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def countWordOccurrences(self, chunks, queries):
        """
        :type chunks: List[str]
        :type queries: List[str]
        :rtype: List[int]
        """
        
        s = []
        for ch in chunks:
            for c in ch:
                if c == '-' or c == ' ':
                    if s:
                        if s[-1] == '-':
                            s[-1] = ' '
                        elif s[-1] == ' ':
                            continue
                        else:
                            s.append(c)
                else:
                    s.append(c)
        
        if s and (s[-1] == ' ' or s[-1] == '-'):
            s.pop()
        words = ''.join(s).split()
        cnt = {}
        for w in words:
            cnt[w] = cnt.get(w, 0) + 1
        
        return [cnt.get(q, 0) for q in queries]
```
