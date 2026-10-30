---
title: "3605. 数组的最小稳定性因子"
aliases: ["yiduobo的每日leetcode 3605.数组的最小稳定性因子"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/greedy", "leetcode/math", "leetcode/binary-search", "leetcode/sliding-window", "题单/二分算法", "题单/位运算", "题单/二分算法/二-二分答案", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1942077488177057913"
zhihu_id: "1942077488177057913"
zhihu_title: "yiduobo的每日leetcode 3605.数组的最小稳定性因子"
question_id: "3605"
question: "数组的最小稳定性因子"
problem_url: "https://leetcode.cn/problems/minimum-stability-factor-of-array/"
difficulty: "Hard"
rating: 2410
created: "2025-08-22T04:46:31+08:00"
updated: "2025-08-22T04:46:31+08:00"
upvotes: 1
comments: 0
---

# 3605. 数组的最小稳定性因子

> **[yiduobo的每日leetcode 3605.数组的最小稳定性因子](https://zhuanlan.zhihu.com/p/1942077488177057913) · 知乎 · 2025-08-22 · 赞同 1**
> 力扣：[3605. 数组的最小稳定性因子](https://leetcode.cn/problems/minimum-stability-factor-of-array/) · Hard · 灵茶山艾府：[二分答案 + LogTrick / 栈 + 滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3605.数组的最小稳定性因子

[3605. 数组的最小稳定性因子 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-stability-factor-of-array/description/)

题目给出一个整数数组nums以及一个整数maxC。

如果一个子数组的所有元素的最大公约数大于或等于2，那么就称这个子数组是稳定的。

一个数组的稳定性因子定义为其最长稳定子数组的长度。

现在可以将nums中最多maxC个元素修改为任意整数，问最多maxC次修改后，数组的最小可能稳定性因子。若没有稳定的子数组，则返回0。

首先可以明确的是，为了使得子数组不稳定，每次修改都应该将数组中一个大于1的元素修改成1，这样一来包含这个元素的任意子数组的最大公约数都为1，换言之这个1截断了整个数组。

另一方面，对于固定的左边界，右边界越靠后的子数组最大公约数就越小，也就是说本题是符合二分的性质的，可以二分答案，然后将问题转化为判定问题。

对于当前二分到的mid，若经过maxC次修改后数组中所有长度大于等于mid + 1的子数组的最大公约数都为1，那么就说明mid可行，此时应该修改二分上界为mid，否则修改二分下界为mid + 1。

接下来的问题就是如何判断经过maxC次修改后，数组中所以长度大于等于mid + 1的子数组的最大公约数都为1。基于第二点，在这里就只需要判断所有长度刚好为mid + 1的子数组的最大公约数是否为1，而不需要判断更长的子数组，理由是对于某个特定的起点p，若p到p + mid这一段的最大公约数为1，那么以p为左边界的更长的子数组的最大公约数显然也为1，无需再进行额外的判断的。

另一方面，对于某个下标p，若p到p + mid这一段的最大公约数不为1，那么此时就需要修改其中某个元素。如果按照从左到右的顺序遍历这个p的话，在这里就应该修改最后一个元素，也就是p + mid，这样一来就无需再考虑左边界在p到p + mid - 1之间的情况了，因为p + mid的存在，以这些下标为左边界且长度为mid + 1的子数组的最大公约数都为1，也就是说接下来p可以从p + mid + 1开始继续向后考虑。

到了这里，问题就变成了如何计算数组中所有长度为mid + 1的子数组的最大公约数。这个问题乍一看可以用滑动窗口解决，但是实际上处理起来非常困难，因为当左边界向右移动时，最大公约数是有可能变大的，某些出现过但是并非所有元素都具有的质因子，可能因为原来的左边界被移出窗口，变成子数组中所有元素都具有的质因子，从而体现在最大公约数中。例如[2, 3, 6]，2和3的最大公约数为1，但是窗口移动到[3, 6]时，质因子3重新发挥作用，最大公约数就变成3了。

基于上面的结论，就必须另想办法计算最大公约数了。好在最大公约数是满足区间拼接性质的，也就是说从left到right的最大公约数，可以拆分成分别计算left到mid以及mid + 1到right的最大公约数，然后再计算这二者的最大公约数。基于这一点，就可以利用线段树来计算所有子数组的最大公约数。另外由于本题是静态的，使用st算法也是可以的。

到了这里，就得到了一种可行的算法：

首先根据nums建立起线段树，线段树中储存的是节点表示的区间的最大公约数。接下来二分答案mid，二分的上下界分别为n和0。

对于当前二分到的mid，从数组头开始向后遍历，对于当前遍历到的p，通过线段树查找p到p + mid这一段的最大公约数，若为1，那么p向后移动到p + 1，否则对p + mid的元素进行修改，然后将p向后移动到p + mid + 1。重复此过程直到以p为左边界的子数组长度不足mid + 1，或者修改次数不足为止。

若修改次数不足，则调整二分下界为mid + 1，否则调整二分上界为mid。

值得一提的是，对于查询p到p + mid这一段的最大公约数是否为1这一操作，也可以理解成查询以p为左边界，且最大公约数大于1的最大右边界是否小于p + mid。这样一来，就可以先预先进行一趟遍历，计算出以每个下标为左边界时，最靠后且子数组最大公约数大于1的右边界，在这里记为bound_list。那么在接下来的二分步骤时，就可以通过这个bound_list来判断而不用每次都去查询线段树了。需要特别注意的是，计算bound_list时，当右边界移动时可以直接计算gcd，但是左边界移动时必须重新查询线段树。

最后附上python代码：

```python
class Solution(object):
    def minStable(self, nums, maxC):
        """
        :type nums: List[int]
        :type maxC: int
        :rtype: int
        """

        n = len(nums)
        f = [0] * (n * 4)
        
        def gcd(x, y):
            while x % y != 0:
                x, y = y, x % y
            return y

        def build(now, left, right, f):
            if left == right:
                f[now] = nums[left]
            else:
                mid = (left + right) // 2
                build(now + now + 1, left, mid, f)
                build(now + now + 2, mid + 1, right, f)
                f[now] = gcd(f[now + now + 1], f[now + now + 2])
        
        def get(now, left, right, start, end, f):
            if left == start and right == end:
                return f[now]
            
            mid = (left + right) // 2
            if end <= mid:
                return get(now + now + 1, left, mid, start, end, f)
            elif start > mid:
                return get(now + now + 2, mid + 1, right, start, end, f)
            else:
                return gcd(get(now + now + 1, left, mid, start, mid, f), get(now + now + 2, mid + 1, right, mid + 1, end, f))

        build(0, 0, n - 1, f)

        bound_list = []
        p = 0
        for index in range(n):
            if p <= index:
                if nums[index] == 1:
                    bound_list.append(index - 1)
                    continue
                    
                p = index + 1
                g = nums[index]
            else:           
                g = get(0, 0, n - 1, index, p - 1, f)

            while p < n:
                new_g = gcd(g, nums[p])
                if new_g > 1:
                    g = new_g
                    p += 1
                else:
                    break
            
            bound_list.append(p - 1)

        left = 0
        right = n
        while left < right:
            mid = (left + right) // 2
            p = 0
            need = 0
            while p + mid < n:
                while p + mid < n and p + mid > bound_list[p]:
                    p += 1
                if p + mid == n:
                    break
                need += 1
                if need > maxC:
                    break
                p += mid + 1
            
            if need <= maxC:
                right = mid
            else:
                left = mid + 1
        
        return left
```
