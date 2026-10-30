---
title: "384. 打乱数组"
aliases: ["yiduobo的每日leetcode 384.打乱数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/166660879"
zhihu_id: "166660879"
zhihu_title: "yiduobo的每日leetcode 384.打乱数组"
question_id: "384"
question: "打乱数组"
problem_url: "https://leetcode.cn/problems/shuffle-an-array/"
created: "2020-08-04T20:31:44+08:00"
updated: "2020-08-04T20:31:44+08:00"
upvotes: 0
comments: 0
---

# 384. 打乱数组

> **[yiduobo的每日leetcode 384.打乱数组](https://zhuanlan.zhihu.com/p/166660879) · 知乎 · 2020-08-04 · 赞同 0**
> 力扣：[384. 打乱数组](https://leetcode.cn/problems/shuffle-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

384.打乱数组<https://leetcode-cn.com/problems/shuffle-an-array/>

昨天刚说到洗牌算法，今天就碰上了。

实现起来很简洁，但是思路十分巧妙。

设数组长度为n，首先第一个位置上要按1/n的概率选则数组中的任意一个数字与第一个数字进行交换，那么每个数字选上的概率为1/n，没被选上的概率就是(n - 1)/n。

接下来对于剩下的n - 1个数，要随机选一个与第二个数进行交换，要求总体的概率也是1/n，于是这一次选择的概率就应该是(1/n) / ((n-1)/n) \= 1/(n-1)，恰好就是从剩下的n - 1个数中随机随机选择一个，那么这n - 1个数选上的概率为1/(n-1)，没被选上的概率则是(n-2)/(n-1)。

接下来，与之前类似，需要对剩下的n - 2个数中随机选一个与第三个数进行交换，要求总体概率也是1/n，于是这一次的概率就应该是(1/n)/ (((n-1)/n) \* ((n-2)/(n-1))) \= 1/(n-2)，恰好就是从剩下的n - 2个数中随机选一个。

更一般的，不妨设现在还剩下n - k个数，那么这n - k个数在前k轮没被选中的概率就应该是

（(n - 1) / n) \* ((n-2) / (n-1)) \* ... \* ((n - k) / (n - k + 1)) \= (n - k) / n

而我们在这一轮的目标则是要求以1/n的总概率来选择剩下n - k个数中的一个，于是这一轮每个位置被选择的概率都应该是

(1/n) / ((n - k) / n) \= 1 / (n - k)

恰好就是从剩下的n - k个数中随机选一个的概率。

到了这里，就得到了一种做法：从左往右一趟扫描，每次随机选择当前位置或当前位置右侧的某一个数与当前位置进行交换即可。

最后附上python代码：

```python
class Solution(object):

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        self.original = nums[:]
        self.now = nums[:]

    def reset(self):
        """
        Resets the array to its original configuration and return it.
        :rtype: List[int]
        """
        self.now = self.original[:]
        return self.now

    def shuffle(self):
        """
        Returns a random shuffling of the array.
        :rtype: List[int]
        """
        for index in range(len(self.now) - 1):
            pos = random.randint(index, len(self.now) - 1)
            self.now[index], self.now[pos] = self.now[pos], self.now[index]

        return self.now

# Your Solution object will be instantiated and called as such:
# obj = Solution(nums)
# param_1 = obj.reset()
# param_2 = obj.shuffle()
```
