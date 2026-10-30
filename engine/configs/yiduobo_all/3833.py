def _txt(S):
    if 'cnt' not in S or 's' not in S or 'v' not in S:
        return ''
    return f"`v × cnt = {S['v']} × {S['cnt']}` = =={S['v'] * S['cnt']}== 　对比 　后缀和 `s` = =={S['s']}=="


def _idx(S):
    if 'cnt' not in S:
        return None
    n = len(S['nums'])
    return n - 1 - S['cnt'] if S['_line'] < 10 else n - S['cnt']


CONFIG = dict(
    num=3833, title='统计主导元素下标数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='倒序遍历 · 后缀和与个数',
    tags=[],
    code='''
class Solution(object):
    def dominantIndices(self, nums):
        
        s = nums[-1]
        cnt = 1
        res = 0
        for v in nums[-2::-1]:
            if v * cnt > s:
                res += 1
            cnt += 1
            s += v
        
        return res
''',
    call='Solution().dominantIndices([5, 4, 3, 8, 1])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（框 = 已经累加进 s 的后缀）', color=lambda S, i, v: 'blue' if _idx(S) == i else None,
             window=(lambda S: len(S['nums']) - S['cnt'] if 'cnt' in S else None, lambda S: len(S['nums']) - 1),
             cell=96, h=230),
        dict(type='text', h=110, size=32, fn=_txt),
    ],
    watch=[('v', 'v', 'blue'), ('cnt', 'cnt', 'orange'), ('s', 's', 'cyan'), ('res', 'res', 'green')],
    captions={
        's = nums[-1]': '`s` 记录后缀之和，先放入最右边元素 `{s}`',
        'cnt = 1': '`cnt` 记录后缀里的元素个数，目前 `1` 个',
        'res = 0': '`res` 统计主导元素',
        'for v in nums': lambda S, B, r: (f'倒数第二个起往前走：`v = {S.v}`，后缀有 `{S.cnt}` 个数、和为 `{S.s}`' if S.cnt < len(S.nums) else '每个元素都处理完，遍历结束'),
        'if v * cnt > s': lambda S, B, r: (
            f'`v` > 平均值 ⇔ `v × cnt > s`：`{S.v} × {S.cnt} = {S.v * S.cnt}` '
            + (f'> `{S.s}` → ==主导元素==' if S.v * S.cnt > S.s else f'≤ `{S.s}` → 不是')),
        'res += 1': '先比较再更新：这个 `v` 是主导元素 → `res = {res}`',
        'cnt += 1': '`v` 并入后缀，个数 → `{cnt}`',
        's += v': '后缀和 `s` 加上 `v` → `{s}`',
        'return res': '共 `{res}` 个主导元素',
    },
    max_steps=60,
    cards=dict(
        one_liner='从倒数第二个往前扫：先比较，再把自己并入后缀',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums[index]` 大于它右侧所有元素的平均值，就称主导元素',
                 '最右侧的元素不算；统计主导元素个数',
                 '本视频：`[5,4,3,8,1]` → `2`'],
        quote='可以从倒数第二个元素开始，往前一趟遍历，使用一个变量s记录当前后缀子数组之和，另外使用一个变量cnt记录后缀子数组中元素的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['需要每个后缀的平均值：和 `s`、个数 `cnt` 一路维护',
              '遍历到 `v` 时，后缀还不含 `v`：先比 `v × cnt > s` 并更新答案',
              '比完再 `cnt += 1`、`s += v`，让 `v` 成为下一个数的后缀'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：先比较、后累加，顺序反了会把自己算进平均值',
                 '`nums[-2::-1]` 从倒数第二个起倒着遍历；`s`、`cnt` 初始值是最右边元素',
                 '用 `v * cnt > s` 代替平均值比较，避免小数',
                 '原文为 Python 2 风格，仅删去了类型说明文档字符串，其余未改'],
    ),
)
