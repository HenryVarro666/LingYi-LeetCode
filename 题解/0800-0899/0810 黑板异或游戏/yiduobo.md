---
title: "810. 黑板异或游戏"
aliases: ["yiduobo的每日leetcode 810.黑板异或游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343804752"
zhihu_id: "343804752"
zhihu_title: "yiduobo的每日leetcode 810.黑板异或游戏"
question_id: "810"
question: "黑板异或游戏"
problem_url: "https://leetcode.cn/problems/chalkboard-xor-game/"
created: "2021-01-12T20:01:31+08:00"
updated: "2021-01-12T20:01:31+08:00"
upvotes: 0
comments: 0
---

# 810. 黑板异或游戏

> **[yiduobo的每日leetcode 810.黑板异或游戏](https://zhuanlan.zhihu.com/p/343804752) · 知乎 · 2021-01-12 · 赞同 0**
> 力扣：[810. 黑板异或游戏](https://leetcode.cn/problems/chalkboard-xor-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

810.黑板异或游戏

[力扣](https://leetcode-cn.com/problems/chalkboard-xor-game/)

拿到题目没有什么很好的想法，于是老老实实从比较简单的情况入手开始分析：

1、当N \= 1时：

若唯一的数字为0，那么先手胜，否则后手胜

2、当N\=2时：

若两个数字异或值为0，那么先手胜

否则这两个数字不可能同时为0，那么先手只需要留下一个非0的数字，那么就转化成了N\=1的情况，因此也是先手胜

3、当N\=3时：

当三个数字异或值为0，那么先手胜

否则无论先手怎么做，都将转化成N\=2的情况，因此是后手胜

4、当N\=4时：

当四个数字异或值为0，那么先手胜

否则我们设这四个数字分别为A、B、C、D，那么若下面四种情况同时成立

B ^ C ^ D \= 0

A ^ C ^ D \= 0

A ^ B ^ D \= 0

A ^ B ^ C \= 0

先手就必败。但是注意要这里有个前提条件是A ^ B ^ C ^ D !\= 0，若我们将上面四种情况全部异或起来，那么就有

B ^ C ^ D ^ A ^ C ^ D ^ A ^ B ^ D ^ A ^ B ^ C \= 0

整理上面的式子可以得到

(A ^ B ^ C ^ D) ^ (A ^ B ^ C ^ D) ^ (A ^ B ^ C ^ D) \= 0

由于前两项异或值必然为0，那么就有

0 ^ (A ^ B ^ C ^ D) \= 0

从而可知

A ^ B ^ C ^ D \= 0

与上面的前提条件产生了矛盾

也就意味着上面四个式子不可能同时成立，于是先手必然可以有一种选择将局面转化成N \= 3的情况，也就是先手必胜了

通过上面的分析可以发现，当N为偶数时，先手必胜；当N为奇数时，若初始局面所有数异或值为0，那么先手必胜，否则后手必胜。

对于N为偶数时的证明，也可以沿用上面的证明方法，设当前所有数异或起来为S，那么如果先手必败，那么就有：

S !\= 0

S ^ X[1] \= 0

...

S ^ X[N] \= 0

将下面N个式子全部异或起来，可以得到

S ^ S ^ ... ^ S ^ (X[1] ^ X[2] ^ ... ^ X[N]) \= 0

由于这里的N为偶数，那么前N个S异或值必然为0，于是就有

X[1] ^ X[2] ^ ... ^ X[N] \= S \= 0，与S !\= 0产生了矛盾，于是先手必胜。

最后附上python代码：

```python
class Solution(object):
    def xorGame(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        s = 0
        for num in nums:
            s ^= num
        
        if s == 0:
            return True
        
        return len(nums) % 2 == 0
```
