def _cand(S):
    if 'max_cnt' not in S or 'res' not in S:
        return ''
    ok = [k for k, v in S['cnt'].items() if v == S['max_cnt']]
    return f'最大出现次数 `max_cnt = {S["max_cnt"]}`，对应的数：{ok}'


CONFIG = dict(
    num=697, title='数组的度', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表记次数与首末位置',
    code='''
class Solution(object):
    def findShortestSubArray(self, nums):

        first = {}
        last = {}
        cnt = {}

        max_cnt = 0

        for index, num in enumerate(nums):
            cnt[num] = cnt.get(num, 0) + 1
            if num not in first:
                first[num] = index
            last[num] = index
            max_cnt = max(max_cnt, cnt[num])

        res = len(nums)
        for num in cnt:
            if cnt[num] == max_cnt:
                res = min(res, last[num] - first[num] + 1)

        return res
''',
    call='Solution().findShortestSubArray([1,2,2,3,1,4,2])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums', cell=80, h=170, pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if S.get('_line', 0) >= 19 and 'num' in S and v == S['num'] else None)),
        dict(type='map', var='cnt', label='cnt（出现次数）', fmt=lambda k, v: f'{k}: {v}', h=110, font=30),
        dict(type='map', var='first', label='first（第一次出现的下标）', fmt=lambda k, v: f'{k}: {v}', h=110, font=30),
        dict(type='map', var='last', label='last（最后一次出现的下标）', fmt=lambda k, v: f'{k}: {v}', h=110, font=30),
        dict(type='text', h=70, size=28, fn=_cand),
    ],
    watch=['index', 'num', ('max_cnt', 'max_cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'first = {}': '`first[x]`：数字 x 第一次出现的下标',
        'last = {}': '`last[x]`：数字 x 最后一次出现的下标',
        'cnt = {}': '`cnt[x]`：数字 x 出现的次数',
        'max_cnt = 0': '`max_cnt` = 数组的度（最大出现次数）',
        'for index, num': lambda S, B, r: ('数组扫描完了，三张表都填好' if B.get('index') == S.index and B.get('num') == S.num
                                          else '扫描第 `{}` 个数 `{}`'.format(S.index, S.num)),
        'cnt[num] = ': '`{num}` 出现次数 +1 → `cnt[{num}] = {cnt[num]}`',
        'if num not in first': lambda S, B, r: ('`{}` 以前没出现过 → 记下首位置'.format(S.num) if S.num not in B['first'] else '`{}` 见过了，首位置不变'.format(S.num)),
        'first[num] = index': '首次出现：`first[{num}] = {index}`',
        'last[num] = index': '每次都更新末位置：`last[{num}] = {index}`',
        'max_cnt = max': '`max_cnt = max({B.max_cnt}, {cnt[num]}) = {max_cnt}`',
        'res = len(nums)': '`res` 先设成整个数组长度 `{res}`（最坏情况）',
        'for num in cnt': lambda S, B, r: ('每个数都看过了' if B.get('num') == S.num
                                          else '枚举每个数 `{}`，看它是不是出现最多的'.format(S.num)),
        'if cnt[num] == max_cnt': lambda S, B, r: ('`cnt[{}] = {}` 等于 `max_cnt`：它是==度的数==，需要算长度'.format(S.num, S.cnt[S.num]) if S.cnt[S.num] == S.max_cnt
                                                  else '`cnt[{}] = {}` < `max_cnt = {}`：不是最多的，跳过'.format(S.num, S.cnt[S.num], S.max_cnt)),
        'res = min(res': '必须包含所有 `{num}`：区间 `[{first[num]}, {last[num]}]`，长度 `{last[num]} − {first[num]} + 1` = {last[num]-first[num]+1}；`res = {res}`',
        'return res': '最短子数组长度 `{res}`',
    },
    cards=dict(
        one_liner='度最大的数 x，最短子数组就是 x 的首到末',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组的度 = 出现次数最多的数的出现次数',
                 '找 `nums` 里度与原数组相同的==最短连续子数组==，返回长度',
                 '示例：`[1,2,2,3,1,4,2]` → `6`（度为 3，数字 2 从下标 1 到 6）'],
        quote='统计完成后，可以得到出现次数最多的数有哪些，依次枚举其中的每一个数x，那么要包含所有的x且最短，那么就需要选择first[x]到last[x]这一段，计算其长度，其中最短的即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['一遍扫描：用 `cnt`、`first`、`last` 三个哈希表分别记次数、首位置、末位置',
              '同时维护最大次数 `max_cnt`',
              '子数组要含 x 的所有出现 → 至少是 `first[x]` 到 `last[x]`',
              '对所有次数 == `max_cnt` 的 x 取最短长度'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '度相同的数可能有多个，要全部枚举取最小',
                 '长度是 `last - first + 1`，别忘了 `+ 1`',
                 '原文为 Python 2 风格，无需任何改动即可在 Python 3 运行'],
    ),
)
