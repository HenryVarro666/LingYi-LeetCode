def _cur(S):
    if 'actual' in S and 'minimum' in S and [S['actual'], S['minimum']] in S['tasks']:
        return S['tasks'].index([S['actual'], S['minimum']])
    return None


def _txt(S):
    if 'ans' not in S or 's' not in S:
        return '先按 `minimum − actual` 从大到小排序（交换论证）'
    c = _cur(S)
    if c is None:
        return f'下界取最大值：初始能量 `E0 = {S["ans"]}`'
    return f'已耗 `s = {S["s"]}`，当前任务要求 `E0 ≥ s + minimum = {S["s"]} + {S["minimum"]}` = =={S["s"] + S["minimum"]}=='


CONFIG = dict(
    num=1665, title='完成所有任务的最少初始能量', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='交换论证 · 按 m−a 排序',
    tags=['灵神题单', '难度分 1901'],
    code='''
class Solution:
    def minimumEffort(self, tasks: List[List[int]]) -> int:
        tasks.sort(key=lambda t: t[0] - t[1])  # 按照 minimum - actual 从大到小排序

        ans = 0
        s = 0  # 累计耗费的能量
        for actual, minimum in tasks:
            # 题目要求 E0 - s >= minimum，即 E0 >= s + minimum
            # 由此可以得到 n 个关于 E0 的下界，所有下界的最大值即为答案
            ans = max(ans, s + minimum)
            s += actual
        return ans
''',
    call='Solution().minimumEffort([[1,3],[2,4],[10,11],[10,12],[8,9]])',
    expect=32,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='tasks', cell=150, h=230, label='tasks = [actual, minimum]',
             color=lambda S, i, v: 'yellow' if _cur(S) == i else None,
             dim=lambda S, i, v: _cur(S) is not None and i < _cur(S)),
        dict(type='text', fn=lambda S: ' '.join(f"{t[1]-t[0]}" for t in S['tasks']) and ('各任务 `minimum − actual`：' + '，'.join(str(t[1] - t[0]) for t in S['tasks'])), h=70),
    ],
    watch=[('s', 's', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'tasks.sort': '排序键 `actual − minimum` 从小到大，即 ==`minimum − actual` 从大到小==：前面是「门槛高、花费少」的任务',
        'ans = 0': '`ans` 记录初始能量的下界最大值',
        's = 0': '`s` 累计已经耗费的能量',
        'for actual': '按排序后的顺序依次做任务：`actual = {actual}`，`minimum = {minimum}`',
        'ans = max': '要求 `E0 − s ≥ minimum` → `E0 ≥ {s} + {minimum} = {s + minimum}`；`ans = max({B.ans}, {s + minimum}) = {ans}`',
        's += actual': '做完这个任务，累计耗费 `s` 增加 `{actual}` → {s}',
        'return ans': '所有下界的最大值就是最少初始能量：`{ans}`',
    },
    cards=dict(
        one_liner='按 minimum−actual 从大到小排序，所有下界取最大值',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每个任务 `[actual, minimum]`：开始前能量 ≥ minimum，做完耗掉 actual',
                 '顺序任意，求完成全部任务的最少初始能量',
                 '示例：`[[1,3],[2,4],[10,11],[10,12],[8,9]]` → `32`'],
        quote='设 T 中的一对相邻任务 t1 和 t2 …… 当且仅当 m1−a1 ≥ m2−a2 成立时，先完成 t1 再完成 t2 更优（或者相同）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只看相邻两个任务：先做哪个所需的初始能量更小，推出 ==m−a 大的先做==',
              '类似冒泡排序不断交换相邻逆序对，最终就是按 m−a 从大到小',
              '排好序后，第 i 个任务要求 `E0 ≥ s + m`，所有下界取最大值'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`（不计排序栈）',
                 '易错点：要求是 `E0 − s ≥ minimum`，下界是 `s + minimum`，不是 `s + actual`',
                 '另一种写法：按 m−a 从小到大排序，倒序思考 `e = max(e + actual, minimum)`',
                 '同类交换论证题：2136 全部开花的最早一天'],
    ),
)
