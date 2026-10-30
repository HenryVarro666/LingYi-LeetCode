def _areas(S):
    b = S['beans']
    n = len(b)
    return [(n - i) * v for i, v in enumerate(b)]


def _txt(S):
    if 'n' not in S:
        return ''
    a = _areas(S)
    best = max(a)
    parts = [f"{S['n'] - i}×{v}" + ('' if (S['n'] - i) * v != best else '★') for i, v in enumerate(S['beans'])]
    s = f"保留面积 `(n−i)×v`：" + '，'.join(parts)
    if 'max_save' in S:
        s += f"　→ 最大保留 =={S['max_save']}=="
    return s


CONFIG = dict(
    num=2171, title='拿出最少数目的魔法豆', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 · 枚举保留的矩形',
    tags=['灵神题单', '难度分 1748'],
    code='''
class Solution:
    def minimumRemoval(self, beans: List[int]) -> int:
        beans.sort()
        n = len(beans)
        max_save = max((n - i) * v for i, v in enumerate(beans))
        return sum(beans) - max_save
''',
    call='Solution().minimumRemoval([4,1,6,5,2,9])',
    expect=11,
    views=[
        dict(type='bars', var='beans', h=360, label='beans（排序后）：保留 = 蓝色矩形',
             color=lambda S, i, v: ('green' if 'max_save' in S and (len(S['beans']) - i) * v == S['max_save'] else None)),
        dict(type='text', fn=_txt, h=120),
    ],
    watch=[('n', 'n', 'blue'), ('max_save', 'max_save', 'green')],
    captions={
        'beans.sort()': '先排序：这样「枚举最终每袋剩 `v`」时，大于等于 `v` 的袋子就是后面一段',
        'n = len': '`n = {n}` 个袋子',
        'max_save = max': lambda S, B, r: (f"枚举最终每袋剩 `v = beans[i]`：下标 ≥ i 的 `n−i` 个袋子都留 `v` 颗，面积 `(n−i)·v`；"
                                           f"最大保留 ==max_save = {S.max_save}==（拿出的 = 总数 − 保留）"),
        'return sum': '拿出的最少 = `sum(beans) − max_save` = `{sum(beans)} − {max_save}` = =={sum(beans) - max_save}=='
        ,
    },
    cards=dict(
        before=[dict(heading='先看每个候选的保留面积', lines=[
            '排序后 `[1,2,4,5,6,9]`，`n = 6`',
            '`v = 1` → `6×1 = 6`，`v = 2` → `5×2 = 10`，`v = 4` → `4×4 = 16`',
            '`v = 5` → `3×5 = 15`，`v = 6` → `2×6 = 12`，`v = 9` → `1×9 = 9`',
            '最大是 ==16==；总数 27，所以答案 `27 − 16 = 11`'])],
        one_liner='拿出的最少 = 总数 − 最多能保留的矩形面积',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每个袋子可以拿出若干豆子，使剩下的==非空袋子==豆数都相等，求最少拿出多少',
                 '示例：`[4,1,6,5]` → `4`',
                 '本视频：`[4,1,6,5,2,9]` → `11`'],
        quote='拿出魔法豆 + 剩余魔法豆 = 初始魔法豆之和，我们可以考虑最多能剩下多少个魔法豆，从而计算出最少能拿出多少个魔法豆。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后枚举最终的豆数 `v = beans[i]`：小的清空，大的削到 `v`',
              '保留的豆子正好是底边 `n−i`、高 `v` 的矩形，面积 `(n−i)·v`',
              '总数减去矩形面积的最大值就是答案'],
        summary=['时间 `O(n log n)`（瓶颈是排序），空间 `O(1)`',
                 '要保留的是面积最大值，答案是 `sum − 最大面积`，别写反',
                 '`beans.sort()` 会原地改动输入',
                 '同类：灵神贪心题单 §1.6「先枚举，再贪心」，如 3085 题'],
    ),
)
