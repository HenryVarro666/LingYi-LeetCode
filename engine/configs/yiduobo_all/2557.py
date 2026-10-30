CONFIG = dict(
    num=2557, title='从一个范围内选择最多整数II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='二分答案 + 被禁数前缀和',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def maxCount(self, banned, n, maxSum):

        banned = sorted(set(banned))
        pre_s = [0]
        for v in banned:
            pre_s.append(pre_s[-1] + v)

        def get_ban(v):
            if v < banned[0]:
                return 0

            left = 0
            right = len(banned) - 1
            while left < right:
                mid = (left + right + 1) // 2
                if v >= banned[mid]:
                    left = mid
                else:
                    right = mid - 1
            
            return left + 1

        left = 0
        right = n
        while left < right:
            mid = (left + right + 1) // 2
            s = (1 + mid) * mid // 2 - pre_s[get_ban(mid)]

            if s <= maxSum:
                left = mid
            else:
                right = mid - 1
        
        return left - get_ban(left)
''',
    call='Solution().maxCount([4,2,4], 5, 6)',
    expect=2,
    views=[
        dict(type='array', var='banned', label='banned（去重排序）', h=150, cell=80),
        dict(type='array', var='pre_s', label='pre_s（被禁数前缀和）', h=150, cell=80),
        dict(type='text', fn=lambda S: (f"二分答案：`left={S['left']}`，`right={S['right']}`" + (f"，试 `mid={S['mid']}`" if 'mid' in S else '')) if 'right' in S else '', size=26),
        dict(type='text', fn=lambda S: (f"选 1..{S['mid']} 中没被禁的数，和 = `{(1+S['mid'])*S['mid']//2}` − 被禁和 = =={S['s']}==" if 's' in S and 'mid' in S and S.get('_inner') is not None and 'n' in S else ''), size=26),
    ],
    max_steps=48,
    watch=['left', 'right', 'mid', ('s', 's', 'green'), 'v'],
    captions={
        'banned = sorted': '被禁数去重后排序：`banned` = {banned}',
        'pre_s.append': '前缀和：`pre_s` = {pre_s}。`pre_s[k]` = 前 k 个被禁数之和',
        'def get_ban': '`get_ban(v)`：数 1..v 里有几个被禁数（二分）',
        'if v < banned[0]': '`v = {v}` {"< 最小被禁数，没有被禁数" if v < banned[0] else "不小于最小被禁数，需要二分查找"}',
        13: '内层二分 `left = 0`',
        24: '外层二分答案：答案在 `[left, right]`，`left = 0`',
        'right = len(banned)': '`right = {right}`：在 `banned` 里找 ≤ v 的最大下标',
        'if v >= banned[mid]': '`v = {v}` {">=" if v >= banned[mid] else "<"} `banned[{mid}] = {banned[mid]}` → {"它不超过 v，向右找" if v >= banned[mid] else "它比 v 大，往左收"}',
        'return left + 1': 'v 以内的被禁数共 `{left} + 1` = =={left + 1}== 个',
        'right = n': '外层二分答案：最多选 `n = {n}` 以内的数，`right = {right}`',
        's = (1 + mid)': '选 1..`{mid}` 里没被禁的数，和 = 求和公式 `{(1+mid)*mid//2}` 减去被禁数之和 → `s` = =={s}==',
        'if s <= maxSum': '`s = {s}` {"<=" if s <= maxSum else ">"} `maxSum = {maxSum}` → {"预算够，答案至少是 mid，左边界右移" if s <= maxSum else "超预算，答案要小于 mid"}',
        'right = mid - 1': '`right` → {right}',
        'return left - get_ban(left)': '二分结束，答案范围 1..`{left}`；再用 `get_ban({left})` 数出其中被禁的个数并减掉',
    },
    cards=dict(
        one_liner='答案越大和越大，二分答案，被禁和用前缀和',
        complexity='时间 `O(log n · log m)`，空间 `O(m)`（m 为 banned 长度）',
        problem=['从 `[1, n]` 选若干整数：不能选 `banned` 里的，每个最多选一次，总和 `<= maxSum`',
                 '求最多能选几个数（2554 的加强版，`n` 达到 1e9）',
                 '示例：`banned=[4,2,4]`，`n=5`，`maxSum=6` → `2`（选 1、3）'],
        quote='由于数据规模的变大了，因此不能再继续使用暴力算法，但是贪心的思路还是一样的，从1开始尽量选择小的且没有被ban的数字。另一方面，如果最终答案越大，其包含的数字和也就越大，因此在这里可以二分答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心：尽量选小的、没被禁的；二分答案 `mid`，表示只用 1..mid 里的数',
              '和 = `(1+mid)*mid/2` 减去 1..mid 中被禁数之和',
              '被禁数去重排序+前缀和，再二分找到 ≤ mid 的个数，就能 O(log m) 得到被禁和'],
        summary=['时间 `O(log n · log m + m log m)`，空间 `O(m)`',
                 '`get_ban` 先判断 `v < banned[0]`，避免没有被禁数时下标错位',
                 '最后答案 = `left` 减去 1..left 里被禁的个数',
                 '原文为 Python 2 写法，`(left + right + 1) / 2` 和求和公式的 `/ 2` 已改为 `//`'],
    ),
)
