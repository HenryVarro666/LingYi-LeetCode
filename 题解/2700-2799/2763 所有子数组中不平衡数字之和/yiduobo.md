---
title: "2763. 所有子数组中不平衡数字之和"
aliases: ["yiduobo的每日leetcode 2763.所有子数组中不平衡数字之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654763091"
zhihu_id: "654763091"
zhihu_title: "yiduobo的每日leetcode 2763.所有子数组中不平衡数字之和"
question_id: "2763"
question: "所有子数组中不平衡数字之和"
problem_url: "https://leetcode.cn/problems/sum-of-imbalance-numbers-of-all-subarrays/"
difficulty: "Hard"
rating: 2700
created: "2023-09-07T05:12:53+08:00"
updated: "2023-09-07T05:12:53+08:00"
upvotes: 0
comments: 0
---

# 2763. 所有子数组中不平衡数字之和

> **[yiduobo的每日leetcode 2763.所有子数组中不平衡数字之和](https://zhuanlan.zhihu.com/p/654763091) · 知乎 · 2023-09-07 · 赞同 0**
> 力扣：[2763. 所有子数组中不平衡数字之和](https://leetcode.cn/problems/sum-of-imbalance-numbers-of-all-subarrays/) · Hard · 灵茶山艾府：[两种方法：枚举/贡献法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2763.所有子数组中不平衡数字之和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/sum-of-imbalance-numbers-of-all-subarrays/description/)

题目的数据规模不大，因此首先想到的就是直接暴力枚举子数组的左边界，然后逐个向右扩展子数组的右边界，通过新加入的数来更新子数组中的不平衡数字。具体来说，不妨设当前遍历到的数为x，那么：

1、子数组中存在x：

这种情况下，新加入另一个x不会对不平衡数字的数目产生任何影响，因此此时无需进行任何操作

2、子数组中不存在x和x + 1，但是存在x - 1：

当x加入子数组后，其将会被排在x - 1的后方。若此时x - 1后方还有其他数，由于前提是不存在x + 1，因此x - 1后方的数必然大于x + 1，这个数将与x形成一组不平衡关系。但是需要注意的是，这个数之前已经与x - 1形成了不平衡关系，此时相当于x - 1被x取代了，因此在这里加入x后也不会对不平衡数字的数目产生影响

3、子数组中不存在x和x - 1，但是存在x + 1：

此时与情况2完全对称，加入x同样不会产生影响

4、子数组中不存在x、x - 1以及x + 1：

若x左右两侧都存在其他数，那么x的加入将会与这两个数分别形成不平衡关系，但是这两个数之前形成的不平衡关系就被x打破了，因此在这种情况下，x的加入将使得不平衡关系加1

若x这有一侧存在其他数，那么x的加入将会与这个数形成不平衡关系，因此这种情况下x的加入同样会使得不平衡关系加1

若x两侧都不存在其他数，说明x是子数组最左侧的数，此时子数组的长度为1，没有讨论的必要，因此在具体计算是可以让子数组右边界从左边界加1的位置开始向后扩展，那么就不可能出现这种情况

综合起来，这种情况下x的加入将会使得不平衡关系的数量加上1

5、子数组中不存在x，但同时存在x - 1以及x + 1：

此时x的加入将会打破x - 1和x + 1的不平衡关系，同时自身也不会产生新的不平衡关系，因此这种情况下x的加入将会使得不平衡关系的数量减去1

根据上面的结论，只需在遍历时，对于当前x利用集合检测x - 1、x、x + 1是否存在，并按对应的情况更新答案就行了。

---

上面做法时间复杂度为O(n^2)，不过受到这里上面这些情况中对于x的加入对答案产生影响的启发，可以想办法计算出数组中每个数在作为不平衡关系中的较小数时对答案产生的贡献，从而在O(n)的时间内得到最终答案。在这里仅计算作为较小数的情况是因为每组不平衡关系中都存在较小数，如果既计算作为较小数时的贡献又计算作为较大数时的贡献，则将会重复计算不平衡关系。

那么对于数组中的某个数nums[index]，设其值为x，此时只需找出在x左侧x或x + 1最后一次出现的位置left，以及x右侧x + 1最后一次出现的位置right，就可以得到所有左边界在left + 1到index之间，右边界在index到right - 1直接的所有子数组中，x要么是其中的最大值，要么存在另一个数大于x，此时这个数将与x形成一组不平衡关系。换言之，在不考虑x作为最大值的情况下，x一共会在(index - left) \* (right - index)个子数组中贡献一组不平衡关系。

这样一来，只需正反两趟遍历，利用哈希表找出每个数对应的left和right的位置，然后再一趟遍历计算答案就行了。需要注意的是，前面给出了不考虑x作为最大值的前提，这也就意味着所有的子数组中，最大值都被当做不平衡关系中的较小值被计算了一次，因此最终答案还需要减去n \* (n + 1) / 2，也就是总的子数组的数目。

另外，上面在处理left时考虑了x和x + 1，但是处理right时只考虑了x + 1，这样做的理由是当子数组中出现相同的x时，只有一个x将会作为较小值产生贡献，因此为了避免重复计算，在这里只让子数组中最左侧的x产生贡献。

最后附上python代码：

```python
class Solution(object):
    def sumImbalanceNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)

        last = {}
        left = []
        for index in range(n):
            v = nums[index]
            left.append(index - max(last.get(v + 1, -1), last.get(v, -1)))
            last[v] = index

        first = {}
        right = []
        for index in range(n - 1, -1, -1):
            v = nums[index]
            right.append(first.get(v + 1, n) - index)
            first[v] = index
        right.reverse()

        res = 0
        for index in range(n):
            res += left[index] * right[index]
        
        return res - n * (n + 1) / 2
```
