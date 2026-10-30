---
title: "137. 只出现一次的数字II"
aliases: ["yiduobo的每日leetcode 137.只出现一次的数字II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/graph", "leetcode/enumeration", "题单/位运算", "题单/面试经典-150-题", "题单/位运算/九-其他", "题单/面试经典-150-题/位运算"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/141889925"
zhihu_id: "141889925"
zhihu_title: "yiduobo的每日leetcode 137.只出现一次的数字II"
question_id: "137"
question: "只出现一次的数字 II"
problem_url: "https://leetcode.cn/problems/single-number-ii/"
difficulty: "Medium"
created: "2020-05-18T23:47:23+08:00"
updated: "2020-05-18T23:47:23+08:00"
upvotes: 0
comments: 0
---

# 137. 只出现一次的数字II

> **[yiduobo的每日leetcode 137.只出现一次的数字II](https://zhuanlan.zhihu.com/p/141889925) · 知乎 · 2020-05-18 · 赞同 0**
> 力扣：[137. 只出现一次的数字 II](https://leetcode.cn/problems/single-number-ii/) · Medium · 灵茶山艾府：[教你一步步推导出位运算公式！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

137.只出现一次的数字II <https://leetcode-cn.com/problems/single-number-ii/submissions/>

上一题的加强版本，需要解决出现三次的问题，异或在这里就不能再使用了。

我这在这里用的是位运算加自动机的思路。

先看位运算在这里使用，简单来说，思路就是3个相同的数，其二进制位在所有位上都应该出现了3次，于是统计所有位上1的个数，对于3取模就相当于去除了这些出现3次的数，那么剩下的就是答案。

对于样例一，可以看做二进制下的

[10]，[10]，[11]，[10]

最终第一位上总共出现了一个1，而第二位上则是出现了4个1。分别对3取模，两位上都应该有一个1，那么最终答案就是[11]，即3。

对于样例二，可以看做二进制下的

[0]，[1]，[0]，[1]，[0]，[1]，[1100011]

最终第一位上总共出现了4个1，第二位、第六位与第七位则是出现了1个1。分别对3取模，最后剩下的就是[1100011]，即99。

有了上面这个思路，那么接下来就是需要分别统计每一位上1出现的次数。

由于这里要取模，实际上可以将每一位上1出现的次数归到三种状态中，分别为模3等于0，模3等于1以及模3等于2。对于每个新来的1，这个状态都会往下一个状态移动。由于这里总共有三种状态，那么我们可以用两个状态once与twice变量来进行表示：

once\=0，twice\=0，表示模3余0。

once\=1，twice\=0，表示模3余1。

once\=0，twice\=1，表示模3余2。

接下来，是需要找到这三个状态的转化过程，设现在新来了一位x，那么：

1、once \= 0，twice \= 0，x \= 1：

此时应该从模3余0转化为模3余1，即

next_once \= 1，next_twice \= 0

2、once \= 0，twice \= 0，x \= 0：

那么无事发生，即

next_once \= 0，next_twice \= 0

3、once \= 1，twice \= 0，x \= 1：

那么应该从模3余1转化到模3余2，即

next_once \= 0，next_twice \= 1

4、once \= 1，twice \= 0，x \= 0：

那么无事发生，即

next_once \= 1，next_twice \= 0

5、once \= 0， twice \= 1，x \= 1：

那么应该从模3余2转化到模3余0，即

next_once \= 0，next_twice \= 0

6、once \= 0， twice \= 1，x \= 0：

那么无事发生，即

next_once \= 0，next_twice \= 1

接下来，将上面这六种情况根据next_once与next_twice的情况分类：

对于next_once，当once \= 0，twice \= 0，x \= 1或者once \= 1，twice \= 0，x \= 0时有next_once \= 1，其他情况中next_once \= 0。可以发现next_once为：

(twice取反) 与 (once异或x)

即next_once \= \~twice & (once ^ x)

对于next_twice，则是once \= 1，twice \= 0，x \= 1或者once \= 0， twice \= 1，x \= 0时有next_twice \= 1，其他情况中next_twice \= 0。可以发现next_twice为：

(once异或twice) 与 (twice异或x)

即next_twice \= (once ^ twice) & (twice ^ x)

于是，我们可以逐个将nums中的数作为x用来更新once与twice，那么最后的答案就是状态1，即once\=1。至此，问题就解决了，同时运用上面的方法，可以解决出现次数更多的情况，只需要设置相应的状态找出转移方法即可。

另外，这一题我也尝试过用zero与once来表示模3的状态，但是这样的话zero的初始值必须是2进制下的[1111...1111]，会存在一些边界问题，于是最后还是采用的once与twice。

最后附上python代码：

```python
class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        once = 0
        twice = 0
        
        for num in nums:
            next_once = ~twice & (once ^ num)
            next_twice = (once ^ twice) & (twice ^ num)
            once = next_once
            twice = next_twice

        return once
```
