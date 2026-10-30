TRACK = '''
class KList(list):
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _color(S, i, v):
    k = _k(S)
    if k is None:
        return 'orange' if v == 0 else None
    if i == k and v == 0:
        return 'yellow'
    if i < k:
        return 'blue'
    if v == 0:
        return 'orange'
    return None


def _txt(S):
    if 'now' not in S or _k(S) is None:
        return '左侧元素和 `now`，右侧元素和 = `s − now`'
    now, s = S['now'], S['s']
    return f'left = `now` = =={now}==，right = `s − now` = =={s - now}=='


CONFIG = dict(
    num=3354, title='使数组元素等于零', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='分析走法 · 前缀和对比后缀和',
    tags=['动态规划', '专题：前后缀分解'],
    code='''
class Solution(object):
    def countValidSelections(self, nums):
        
        res = 0
        s = sum(nums)
        now = 0
        for v in nums:
            if v == 0:
                if s - now == now:
                    res += 2
                elif abs(s - now - now) == 1:
                    res += 1
            now += v
        
        return res
''',
    setup=TRACK,
    call='Solution().countValidSelections(TList([1,0,2,0,3]))',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={_k: 'yellow'}, pointer_labels={_k: 'v'}, color=_color, h=300,
             label='nums（橙 = 值为 0 的候选起点，蓝 = 已在 now 里的元素）'),
    ],
    watch=[('s', 's', 'purple'), ('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录有效方案数',
        's = sum': '总和 `s` = =={s}==，后缀和用 `s − now` 得到，不用另开数组',
        'now = 0': '`now` 是当前下标左侧元素之和，从 0 开始',
        'for v in nums': lambda S, B, r: (f'看下标 {_k(S)}：`v = {S.v}`' if _k(S) is not None else '遍历结束'),
        'if v == 0': lambda S, B, r: ('`v = 0`，可以当起点，比较左右两边的和' if S.v == 0
                                      else f'`v = {S.v}` 不是 0，不能当起点，跳过'),
        'if s - now == now': '左侧 `{now}`，右侧 `{s - now}`：{"相等" if s-now==now else "不相等"}',
        'res += 2': '左右和相等：一开始向左或向右走都有效，`res += 2` → =={res}==',
        'elif abs': '左右差 `{abs(s - now - now)}`：{"恰好差 1 → 只有一个方向有效" if abs(s-now-now)==1 else "不是 0 也不是 1 → 无效"}',
        'res += 1': '差 1，必有一个方向是有效方案，`res += 1` → =={res}==',
        'now += v': '`now += {v}` → =={now}=='+'，下标右移后它就是左侧和',
        'return res': '一共 `{res}` 种有效选择',
    },
    cards=dict(
        one_liner='起点左右两边元素和相等或差 1，就是有效方案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选一个值为 0 的下标 `curr` 和方向，遇到正数就减 1 并反向',
                 '走出数组后全为 0 才算有效，问有多少种（下标，方向）',
                 '示例：`[1,0,2,0,3]` → `2`'],
        quote='若nums[0]到nums[curr - 1]之间的元素之和left等于nums[curr + 1]到nums[n - 1]之间的元素之和right，或者left恰好等于right + 1，那么选择在curr处开始向左走就是有效的方案。',
        quote_src='—— yiduobo 题解原文',
        idea=['向左出发，一共往左走 k 次：往右走 k 次或 k−1 次',
              '数左右两边要被减的次数，得到 left 与 right 相等或差 1',
              '向右同理对称；相等加 2，差 1 加 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '后缀和 = 总和 `s` − 前缀 `now`，一趟遍历就够',
                 '`now += v` 放在判断之后：判断时 `now` 不含当前这个 0（本来就是 0，加不加都一样）',
                 '原文本身是 Python 3 可运行的，没有改动'],
    ),
)
