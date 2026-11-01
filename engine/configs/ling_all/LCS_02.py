def _counts(S):
    c = S.get('cnt')
    if c is None or 'n' in S:
        return {}
    return {t: v for t, v in enumerate(c) if v}


def _top(S):
    c = S.get('cnt')
    if c is None or 'n' not in S:
        return []
    return list(c[-6:])


CONFIG = dict(
    num='LCS 02', title='完成一半题目', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='按个数从大到小选知识点（Go 原文转写）',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution:
    def halfQuestions(self, a: List[int]) -> int:
        ans = 0
        cnt = [0] * 1001
        for v in a:
            cnt[v] += 1
        cnt.sort()
        i, n = 1000, len(a) // 2
        while n > 0:
            ans += 1
            n -= cnt[i]
            i -= 1
        return ans
''',
    call='Solution().halfQuestions([1,1,2,2,3,3,4,5,6,7])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"还需要选 ==`{S['n']}`== 道题，已选 `{S['ans']}` 种知识点" if 'n' in S
                                        else '先统计每种知识点有几道题')),
        dict(type='array', var='a', label='a（题目的知识点类型）', h=140),
        dict(type='map', var=_counts, label='cnt（知识点 → 题数，只列出非 0 的）', h=180, fmt=lambda k, v: f'{v}'),
        dict(type='array', var=_top, label='cnt 排序后，最大的 6 项（从右往左取）', h=190,
             color=lambda S, k, v: 'green' if 'ans' in S and 'n' in S and k >= 6 - S['ans'] else None),
    ],
    watch=[('ans', 'ans', 'green'), 'i', 'n'],
    captions={
        'cnt = [0]': '知识点类型最大 1000，开一个 `cnt[0..1000]` 计数',
        'for v in a': '看下一道题，知识点类型 `{v}`',
        'cnt[v] += 1': '类型 `{v}` 又出现一次：`cnt[{v}] = {cnt[v]}`',
        'cnt.sort()': '排序：题数最多的排到末尾，从 `cnt[1000]` 往前取就是从大到小',
        'i, n = ': '一共选 `{len(a)} // 2 = {n}` 道题 → 还差 `n = {n}`',
        'while n > 0': '`n = {n}`：' + '{"还没选够，继续选下一种" if n > 0 else "选够了，结束"}',
        'ans += 1': '再选一种知识点：`ans` → =={ans}==',
        'n -= cnt[i]': '这种知识点有 `{cnt[B.i]}` 道题，全选上：还差 `n = {B.n} - {cnt[B.i]} = {n}`',
        'i -= 1': '换下一个更小的计数：`i` → {i}',
        'return ans': '选了 `{ans}` 种知识点就够了',
    },
    cards=dict(
        one_liner='题数最多的知识点先选，选够一半就停',
        complexity='时间 `O(n + U log U)`，U = 1001，空间 `O(U)`',
        problem=['`2N` 道题，每题对应一个知识点类型，`N` 位扣友各选不同的一题',
                 '求被选的 `N` 道题至少涉及几种知识点',
                 '示例：`[1,1,2,2,3,3,4,5,6,7]` → `3`（需选 5 题）'],
        quote='统计每个数的个数，按个数从大到小排序，然后依次选择直到选择个数超过 n/2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每种知识点能「一次带走」它的全部题目',
              '想让种类最少，就先选题数最多的',
              '代码把 `cnt` 升序排序，从 `cnt[1000]` 往回走，`n` 减到不大于 0 为止'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`for i, n := ...; n > 0; i--` 写成 while）',
                 '时间 `O(n + U log U)`，U 为类型上限 1001',
                 '易错点：`cnt` 排序后下标不再是类型，只表示「第几大的计数」',
                 '总题数是偶数，`len(a) // 2` 即 N'],
    ),
)
