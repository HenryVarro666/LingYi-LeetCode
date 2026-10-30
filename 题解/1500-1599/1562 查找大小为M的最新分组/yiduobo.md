---
title: "1562. 查找大小为M的最新分组"
aliases: ["yiduobo的每日leetcode 1562.查找大小为M的最新分组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426984826"
zhihu_id: "426984826"
zhihu_title: "yiduobo的每日leetcode 1562.查找大小为M的最新分组"
question_id: "1562"
question: "查找大小为M的最新分组"
problem_url: "https://leetcode.cn/problems/find-latest-group-of-size-m/"
created: "2021-10-30T22:18:09+08:00"
updated: "2021-10-30T22:18:09+08:00"
upvotes: 0
comments: 0
---

# 1562. 查找大小为M的最新分组

> **[yiduobo的每日leetcode 1562.查找大小为M的最新分组](https://zhuanlan.zhihu.com/p/426984826) · 知乎 · 2021-10-30 · 赞同 0**
> 力扣：[1562. 查找大小为M的最新分组](https://leetcode.cn/problems/find-latest-group-of-size-m/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1562.查找大小为M的最新分组

[力扣](https://leetcode-cn.com/problems/find-latest-group-of-size-m/)

如果将题目中连续的1看做区间的话，那么可能有三种操作：

1、加入一个长度为1的新区间

2、扩展一个当前区间的左边界或者右边界

3、连接两个间隔为1的区间

可以发现，上面三种操作中，操作1不会涉及到任何其他区间，但需要通过已有区间的边界来进行判断；操作2和操作3也只会涉及到已有区间的边界。换言之，在更新区间时，只需要更新区间的边界，也就是说可以在O(1)的时间内完成上述三种操作中的某一种。

使用两个数组left和right，其中left[i]表示当前位置i所在区间的左边界是什么，right[i]则表示当前位置i所在区间的右边界是什么。除此之外，还需要使用一个数组cnt表示，其中cnt[i]表示长度为i的区间数目。

接下来对于arr中的数num：

若num等于1，或者left[num - 1]为空，说明num左侧没有紧紧相邻的区间；否则的话说明num左侧存在一个紧紧相邻的区间，其右边界就是num - 1，而这个区间的左边界可以通过left[num - 1]得到，记为new_left。

若num等于n，或者right[num + 1]为空，说明num右侧没有紧紧相邻的区间；否则的话说明num右侧存在一个紧紧相邻的区间，其左边界就是num + 1，而这个区间的右边界可以通过right[num + 1]得到，记为new_right。

那么此时有四种情况：

1、num左右都没有紧紧相邻的区间。此时num将会形成一个长度为1的新区间，此时应该更新left[num] \= right[num] \= num，同时将cnt[1]加上1

2、num左侧有紧紧相邻的区间，右侧没有。此时应该将num左侧区间的右边界扩展至num，因此应该置right[new_left] \= right[num] \= num，并将left[num]置为new_left。此时一个长度为num - 1 - new_left + 1 \= num - new_left的区间被扩展成了一个长度为num - new_left + 1的区间，因此也需要在cnt中做出相应的更新

3、num右侧有紧紧相邻的区间，左侧没有。此时与情况2对称，置left[new_right] \= left[num] \= num，并将right[num]置为new_right。同样需要更新cnt

4、num两侧都有紧紧相邻的区间。此时num将连接起这两个区间，因此应该更新left[new_right] \= new_left，right[new_left] \= new_left。同样的，两个原始区间被合并成了一个区间，cnt中也要做出对应的更新

更新完成后，若此时的cnt[m]大于零，说明这一步操作之后依然存在一组长度为m的1，因此需要将答案更新为当前的步数

最后附上python代码:

```python
class Solution(object):
    def findLatestStep(self, arr, m):
        """
        :type arr: List[int]
        :type m: int
        :rtype: int
        """

        n = len(arr)
        left = [None] * n
        right = [None] * n
        cnt_list = [0] * (n + 1)
        res = -1
        for step, num in enumerate(arr):
            num -= 1
            if num == 0 or left[num - 1] is None:
                new_left = None
            else:
                new_left = left[num - 1]
            
            if num == n - 1 or right[num + 1] is None:
                new_right = None
            else:
                new_right = right[num + 1]
            
            if new_left is None:
                if new_right is None:
                    left[num] = right[num] = num
                    cnt_list[1] += 1
                else:
                    left[num] = left[new_right] = num
                    right[num] = new_right
                    cnt_list[new_right - num] -= 1
                    cnt_list[new_right - num + 1] += 1
            elif new_right is None:
                right[num] = right[new_left] = num
                left[num] = new_left
                cnt_list[num - new_left] -= 1
                cnt_list[num - new_left + 1] += 1
            else:
                left[new_right] = new_left
                right[new_left] = new_right
                cnt_list[new_right - num] -= 1
                cnt_list[num - new_left] -= 1
                cnt_list[new_right - new_left + 1] += 1

            if cnt_list[m] > 0:
                res = step + 1
        
        return res
```
