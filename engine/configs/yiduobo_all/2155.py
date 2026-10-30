CONFIG = dict(
    num=2155, title='分组得分最高的所有下标', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 · 一趟遍历',
    code='''
class Solution(object):
    def maxScoreIndices(self, nums):

        all_one = sum(nums)
        max_s = all_one
        res = [0]

        now_one = 0
        for index, num in enumerate(nums):
            now_one += num
            now_s = index + 1 - now_one + all_one - now_one
            if now_s > max_s:
                max_s = now_s
                res = [index + 1]
            elif now_s == max_s:
                res.append(index + 1)
        
        return res
''',
    call='Solution().maxScoreIndices([0,0,1,0,1,0])',
    expect=[2, 4, 6],
    views=[
        dict(type='array', var='nums', h=190, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None),
        dict(type='text', h=90, fn=lambda S: (
            f"下标 `{S['index']+1}`：左 0 的个数 `{S['index']+1} − {S['now_one']}` + 右 1 的个数 `{S['all_one']} − {S['now_one']}` = =={S['now_s']}=="
            if 'now_s' in S and 'index' in S else '')),
        dict(type='array', var='res', label='res（得分最高的下标）', h=150),
    ],
    watch=['all_one', 'now_one', ('now_s', 'now_s', 'yellow'), ('max_s', 'max_s', 'green')],
    captions={
        'all_one = sum': '全体 1 的个数 `all_one = {all_one}`：下标 0 时右半部分就是整个数组',
        'max_s = all_one': '下标 0 的得分 = `{all_one}`，先当作最高分',
        'res = [0]': '答案先放下标 `0`',
        'now_one = 0': '`now_one`：左半部分 1 的个数（前缀和）',
        'now_one += num': '左半部分加入 `{num}`，前缀和 `now_one = {now_one}`',
        'now_s = index': '下标 `{index+1}` 得分：左 0 = `{index+1} − {now_one}`，右 1 = `{all_one} − {now_one}`，合计 =={now_s}==',
        'if now_s > max_s': lambda S, B, r: (f'`{S.now_s} > {S.max_s}`：创新高 → 清空答案' if S.now_s > S.max_s else f'`{S.now_s} > {S.max_s}`：没有更高，看是否打平'),
        'max_s = now_s': '最高分更新为 `{max_s}`',
        'res = [index + 1]': '之前的下标作废，答案重置为 `{res}`',
        'elif now_s == max_s': lambda S, B, r: ('`{} == {}`：打平 → 追加'.format(S.now_s, S.max_s) if S.now_s == S.max_s else f'`{S.now_s} < {S.max_s}`：更低，跳过'),
        'res.append': '同分，下标 `{index+1}` 追加：`{res}`',
        'return res': '最高分 `{max_s}` 的所有下标：`{res}`',
    },
    cards=dict(
        one_liner='左边的 0 = 长度 − 前缀和，右边的 1 = 总和 − 前缀和',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['在下标 `i` 切开：左边 0 的个数 + 右边 1 的个数 = 得分',
                 '返回得分最高的所有下标，顺序任意',
                 '示例：`[0,0,1,0]` → `[2,4]`；本视频用 `[0,0,1,0,1,0]`'],
        quote='左半部分中0的数目，就等于左半部分的长度减去左半部分中1的数目……右半部分中1的数目，就等于全体1的数目减去左半部分中1的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['只需一个前缀和 `now_one`：左半部分 1 的个数',
              '得分 = `(长度 − now_one) + (all_one − now_one)`',
              '边扫边更新：更高就重置答案，打平就追加'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '切分下标有 `n+1` 个：初始 `res=[0]`，循环里记 `index+1`',
                 '==严格大于==才清空答案，相等要追加',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
