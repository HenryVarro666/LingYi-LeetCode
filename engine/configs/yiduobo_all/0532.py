NUMS, K = [3, 1, 4, 1, 5], 2

CONFIG = dict(
    num=532, title='数组中的 k-diff 数对', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希集合 · 保存较小数去重',
    code='''
class Solution(object):
    def findPairs(self, nums, k):

        res = set()
        num_set = set()

        for num in nums:
            if num - k in num_set:
                res.add(num - k)
            if num + k in num_set:
                res.add(num)
            num_set.add(num)

        return len(res)
''',
    call=f'Solution().findPairs({NUMS}, {K})',
    expect=2,
    views=[
        dict(type='text', size=28, h=80, fn=lambda S: (f"当前数 `num = {S['num']}`，找 `num − k = {S['num'] - S['k']}` 和 `num + k = {S['num'] + S['k']}`" if 'num' in S else '题目要求：数对的差的绝对值 `= k`，且数对要去重')),
        dict(type='array', var='nums', label='nums（k = 2）', cell=100, h=170,
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] else None),
        dict(type='set', var='num_set', label='num_set（之前出现过的数）', font=34, h=170),
        dict(type='set', var='res', label='res（合法数对中较小的那个数，自动去重）', font=34, h=170),
    ],
    watch=[('num', 'num', 'blue'), ('k', 'k'), ('len(res)', 'len(res)', 'green')],
    captions={
        'res = set()': '`res` 存==每个数对里较小的数==：重复数对的较小数必然相同，集合自动去重',
        'num_set = set()': '`num_set` 记录之前出现过的数',
        'for num in nums': '遍历到 `num = {num}`（数组取完则退出循环）',
        'if num - k in num_set': lambda S, B, r: (f'`num − k = {S.num - S.k}` 在 `num_set` 里吗？' + ('在 → `{0}` 和 `{1}` 是一组数对，较小的是 `{0}`'.format(S.num - S.k, S.num) if S.num - S.k in S.num_set else '不在，没有更小的搭档')),
        'res.add(num - k)': '较小的数是 `{num - k}` → 加入 `res`，现在 `res = {sorted(res)}`',
        'if num + k in num_set': lambda S, B, r: (f'`num + k = {S.num + S.k}` 在 `num_set` 里吗？' + ('在 → `{0}` 和 `{1}` 是一组数对，较小的是 当前的 `{0}`'.format(S.num, S.num + S.k) if S.num + S.k in S.num_set else '不在，没有更大的搭档')),
        'res.add(num)': '较小的数是当前的 `{num}` → 加入 `res`，现在 `res = {sorted(res)}`（重复的数对不会让集合变大）',
        'num_set.add(num)': '`{num}` 放进 `num_set`，留给后面的数配对',
        'return len(res)': '`res` 的大小就是不同数对的个数：`{len(res)}`',
    },
    cards=dict(
        one_liner='用集合记住出现过的数，只保存较小数来去重',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['整数数组 `nums` 和整数 `k`，找出==不同==的 k-diff 数对数目',
                 'k-diff 数对 `(a, b)`：`|a − b| = k`，下标不同',
                 '示例：`nums = [3,1,4,1,5]`，`k = 2` → `2`（`(1,3)` 和 `(3,5)`）'],
        quote='对于一个k-diff数对，我们将其中较小的那个数保存在集合res中，那么对于重复的k-diff数对，其较小的那个数也必然相同，此时的res就起到了去重的作用。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历每个数 `now`：前面出现过 `now − k`，说明 `(now−k, now)` 合法',
              '前面出现过 `now + k`，说明 `(now, now+k)` 合法',
              '较小的数放进 `res`，最后 `len(res)` 即答案',
              '本视频第二个 `1` 又配上 `3`，`res` 并没有变大'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`k = 0` 时两个判断都是同一个数：需要它==先前出现过==才算，所以先查再加入',
                 '易错：先判断、后把 `num` 加入集合，否则 `k = 0` 会自己和自己配对',
                 '这是会员/补充题，题面按 LeetCode 原题整理',
                 '原文代码已是 Python 3 写法，未改动'],
    ),
)
