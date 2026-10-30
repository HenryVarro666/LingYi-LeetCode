_P = 'sum(cnt) - (_line == 25) if _line != 27 else None'


def _idx(S):
    if 'cnt' not in S or S.get('_line') == 27:
        return None
    return sum(S['cnt']) - (S.get('_line') == 25)


def _cnt_color(S, i, v):
    ln = S.get('_line')
    if ln == 19 and i == S.get('first'):
        return 'orange'
    if ln == 25 and i == S.get('first'):
        return 'pink'
    if ln in (17, 18, 19) and 'last' in S and i in S['check_digit'].get(S['last'], []):
        return 'green' if v else 'cyan'
    return None


def _txt(S):
    j = _idx(S)
    if j is None or j >= len(S['nums']) or 'last' not in S:
        return '打表 `check_digit[d]`：与个位数 `d` 互质的所有个位数'
    if S.get('_line') in (21, 22, 23):
        return f"求 `{S['nums'][j]}` 的最高位：剩余 `v = {S['v']}`，`first = {S.get('first')}`"
    d = S['last']
    return f"`check_digit[{d}]` = ==" + ','.join(map(str, S['check_digit'][d])) + '=='


CONFIG = dict(
    num=2748, title='美丽下标对的数目', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='互质打表 · 最高位计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1301'],
    code='''
class Solution(object):
    def countBeautifulPairs(self, nums):

        check_digit = {1: [1, 2, 3, 4, 5, 6, 7, 8, 9],
                       2: [1, 3, 5, 7, 9],
                       3: [1, 2, 4, 5, 7, 8],
                       4: [1, 3, 5, 7, 9],
                       5: [1, 2, 3, 4, 6, 7, 8, 9],
                       6: [1, 5, 7],
                       7: [1, 2, 3, 4, 5, 6, 8, 9],
                       8: [1, 3, 5, 7, 9],
                       9: [1, 2, 4, 5, 7, 8]}

        cnt = [0] * 10
        res = 0
        for v in nums:
            last = v % 10
            for first in check_digit[last]:
                res += cnt[first]

            while v:
                first = v % 10
                v //= 10

            cnt[first] += 1

        return res
''',
    call='Solution().countBeautifulPairs([36,52,74,18])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（v = 当前遍历的数）', pointers={_P: 'blue'}, pointer_labels={_P: 'v'}, h=200,
             dim=lambda S, i, v: _idx(S) is not None and i > _idx(S)),
        dict(type='array', var='cnt', label='cnt[d]：已遍历的数中最高位为 d 的个数（绿/青 = 表中，橙 = 正在累加）', h=200, cell=70,
             color=_cnt_color),
        dict(type='text', fn=_txt, h=90, size=30),
    ],
    watch=[('v', 'v', 'blue'), ('last', 'last', 'cyan'), ('first', 'first', 'orange'), ('res', 'res', 'green')],
    skip=['for first in check_digit', 'v //= 10', 5, 6, 7, 8, 9, 10, 11, 12],
    max_steps=70,
    captions={
        'check_digit = {1:': lambda S, B, r: ('打表完成：例如 `check_digit[6] = [1, 5, 7]`' if 'check_digit' in S
                                           else '先把与每个个位数==互质==的个位数打表，后面直接查'),
        'cnt = [0] * 10': '`cnt[d]`：已遍历的数里，最高位为 `d` 的有几个',
        'res = 0': '`res` 统计美丽下标对',
        'for v in nums': lambda S, B, r: (f'遍历到 `v = {S.v}`' if _idx(S) < len(S.nums) else '遍历结束'),
        'last = v % 10': '`v` 的个位数 `last = {last}`，查表 `check_digit[{last}]`',
        'res += cnt[first]': lambda S, B, r: (f'`{S.first}` 与 `{S.last}` 互质：前面最高位为 `{S.first}` 的有 `{S.cnt[S.first]}` 个 → `res = {S.res}`'
                                              if S.cnt[S.first] else f'`{S.first}` 与 `{S.last}` 互质，但前面没有最高位为 `{S.first}` 的数'),
        'while v:': lambda S, B, r: (f'`v = {S.v}` 不为 0，继续取位' if S.v else f'`v` 变成 0：最后取到的 `first = {S.first}` 就是最高位'),
        'first = v % 10': '取当前末位 `first = {first}`，再 `v //= 10`',
        'cnt[first] += 1': '把最高位 `{first}` 的计数加 1 → `cnt[{first}] = {cnt[first]}`',
        'return res': '一共 `{res}` 组美丽下标对',
    },
    cards=dict(
        one_liner='互质关系只在个位数之间：先打表，再按最高位计数',
        complexity='时间 `O(n(9 + log U))`，空间 `O(1)`',
        problem=['`i < j` 且 `nums[i]` 的==第一个数字==与 `nums[j]` 的==最后一个数字==互质',
                 '求这样的美丽下标对数目；示例：`[2,5,1,4]` → `5`',
                 '本视频：`[36,52,74,18]` → `6`'],
        quote='题目考虑的是单个数位上的互质关系，因此可以先将与所有个位数的互质的个位数打表方便使用。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表（这里用数组）记录已遍历数的最高位出现次数',
              '当前数 v：取个位 → 枚举表中与它互质的数 → 累加计数',
              '最后再把 v 的最高位计数加 1'],
        summary=['时间 `O(n(9 + log U))`，空间 `O(1)`',
                 '`while v` 循环最后一次取到的 `v % 10` 就是最高位',
                 '先累加、后计数，保证只数 `i < j`',
                 '原文为 Python 2 写法，`v /= 10` 已改为 `v //= 10`'],
    ),
)
