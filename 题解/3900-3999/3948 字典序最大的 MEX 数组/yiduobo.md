---
title: "3948. 字典序最大的MEX数组"
aliases: ["yiduobo的每日leetcode 3948.字典序最大的MEX数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/queue", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2044530332536402099"
zhihu_id: "2044530332536402099"
zhihu_title: "yiduobo的每日leetcode 3948.字典序最大的MEX数组"
question_id: "3948"
question: "字典序最大的 MEX 数组"
problem_url: "https://leetcode.cn/problems/lexicographically-maximum-mex-array/"
difficulty: "Hard"
rating: 2122
created: "2026-05-31T21:40:57+08:00"
updated: "2026-05-31T21:40:57+08:00"
upvotes: 2
comments: 0
---

# 3948. 字典序最大的MEX数组

> **[yiduobo的每日leetcode 3948.字典序最大的MEX数组](https://zhuanlan.zhihu.com/p/2044530332536402099) · 知乎 · 2026-05-31 · 赞同 2**
> 力扣：[3948. 字典序最大的 MEX 数组](https://leetcode.cn/problems/lexicographically-maximum-mex-array/) · Hard · 灵茶山艾府：[分组循环（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3948.字典序最大的MEX数组

<https://leetcode.cn/problems/lexicographically-maximum-mex-array/description/>

题目给出一个整数数组nums。

现在要求通过不断执行以下操作构造一个数组result，直到nums为空：

- 选择一个在1到len(nums)之间的整数k，计算nums前k个元素的MEX
- 将MEX添加到result末尾，然后将nums的前k个元素移除

问最终可能获得的字典序最大的result是什么。

数组的MEX指的是数组中不包含的最小非负整数。

题目要求得到的result字典序尽量大，那么每一轮操作，都应该让当前的nums[:k]能得到的MEX尽量大，同时这个k在MEX相同时应该尽量的小。

为了达成这个目的，就可以先对nums进行一趟遍历，使用一个哈希表pos记录每种元素v出现的所有位置，其中pos[v]表示v在nums中的所有下标，为了方便操作，我在这里让这些下标按照降序排列。

接下来，开始进行逐段划分，一开始的段起点now为0，同时使用一个变量nxt记录下一段的起点。

对于当前段，让MEX从0开始不断向上尝试，若now以及其右侧存在至少一个等于MEX的元素，那么就说明MEX可以变得更大，此时就应该将now右侧首次出现的MEX包含在当前这一段里面，然后让MEX加上1然后继续检测，直到now的右侧不存在对应的MEX为止。

具体来说，在这里就应该将pos[MEX]中所有小于now的下标位置弹出，若最终剩下的pos[MEX]非空，说明now或者其右侧存在至少一个MEX，此时使用这个MEX的下标加1更新nxt，然后将MEX加上1然后继续尝试；若剩下的pos[MEX]为空，说明这一段的MEX已经确定了，此时应该将其加入到result中，然后将now移动到nxt并进行下一段划分，直到now来到数组末尾为止。

值得一提的是，以上过程看上去是复杂的循环嵌套，但是基于MEX的特性，每一轮成功的检测都至少会消耗掉nums中的一个元素，也就是now至少会向后推进一位，即MEX的枚举次数不会超过now向后推进的次数。另一方面，对于pos[MEX]中处于当前now左侧的下标被弹出的操作，由于每个下标也至多被弹出一次。综合起来，整个处理过程的时间复杂度依然是O(n)。

最后附上python代码：

```python
class Solution(object):
    def maximumMEX(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        pos = {}
        for index, v in enumerate(nums):
            if v not in pos:
                pos[v] = []
            pos[v].append(index)
        
        for v in pos:
            pos[v].reverse()

        res = []
        now = 0
        while now < len(nums):
            mex = 0
            nxt = now + 1
            while True:
                while mex in pos and pos[mex][-1] < now:
                    pos[mex].pop()
                    if not pos[mex]:
                        pos.pop(mex)
                
                if mex not in pos:
                    break
                
                nxt = max(nxt, pos[mex][-1] + 1)
                mex += 1

            res.append(mex)
            now = nxt
        
        return res
```
