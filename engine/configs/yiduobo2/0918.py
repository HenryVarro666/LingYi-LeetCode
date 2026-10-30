A_IN = [4, -5, 1, 2]


def _P(v):
    return f'({v})' if v < 0 else str(v)


def _idx(S):
    num = S.get('num')
    if num is None or num not in A_IN:
        return None
    k = A_IN.index(num)
    return k - 1 if S.get('_line') in (14, 22) else k


def _seg(S, phase):
    """当前 now 对应的那一段 [start, idx]"""
    ln = S.get('_line') or 0
    if phase == 1 and not (14 <= ln <= 18):
        return None
    if phase == 2 and not (22 <= ln <= 26 or ln == 28):
        return None
    k = len(A_IN) - 1 if ln == 28 else _idx(S)
    if k is None or k < 0:
        return None
    now, start = 0, 0
    after_reset = ln in ((17, 18) if phase == 1 else (25, 26, 28))
    for t in range(k + 1):
        now += A_IN[t]
        if t == k and not after_reset:
            break
        if (phase == 1 and now < 0) or (phase == 2 and now > 0):
            now, start = 0, t + 1
    return (start, k) if start <= k else None


def _w(phase, end):
    def f(S):
        sg = _seg(S, phase)
        return sg[end] if sg else None
    return f


def _kept(S, i, v):
    sg = _seg(S, 2)
    ln = S.get('_line') or 0
    if not (20 <= ln <= 28):
        return None
    if sg and sg[0] <= i <= sg[1]:
        return 'red'
    return 'purple'


def _for(end_msg):
    def f(S, B, ret):
        if S.num == A_IN[-1] and B.get('num') == S.num:
            return end_msg.format(res=S.res)
        return f'加入 `num = {S.num}`'
    return f


def _top(S):
    ln = S.get('_line') or 0
    if ln <= 10:
        return '先扫一遍：是不是==所有数都 ≤ 0==？'
    if ln <= 18:
        return f"第一种：普通的一段　`now = {S.get('now')}`　`res = {S.get('res')}`"
    if 's' in S:
        return f"第二种：首尾两段 = `s − now` = `{S['s']} − {_P(S['now'])}` = =={S['s'] - S['now']}=="
    return '第二种：首尾两段'


CONFIG = dict(
    num=918, title='环形子数组的最大和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='贪心最大子段和 + 总和减最小子段和',
    tags=['面试经典150'],
    code='''
class Solution(object):
    def maxSubarraySumCircular(self, A):
        flag = True
        for num in A:
            if num > 0:
                flag = False
                break

        if flag:
            return max(A)

        res = 0
        now = 0
        for num in A:
            now += num
            if now < 0:
                now = 0
            res = max(res, now)

        now = 0
        s = sum(A)
        for num in A:
            now += num
            if now > 0:
                now = 0
            res = max(res, s - now)

        return res
''',
    call=f'Solution().maxSubarraySumCircular({A_IN})',
    expect=7,
    views=[
        dict(type='text', fn=_top, size=27),
        dict(type='array', var='A', label='第一趟：绿框 = 当前子段（和 < 0 就清零重来）', cell=110, h=215,
             pointers={'A.index(num) if 12 <= _line <= 18 else None': 'blue'},
             pointer_labels={'A.index(num) if 12 <= _line <= 18 else None': 'num'},
             window=(_w(1, 0), _w(1, 1)), window_color='green'),
        dict(type='array', var='A', label='第二趟：红 = 被去掉的中间段（和 > 0 就清零），紫 = 留下的首尾两段', cell=110, h=215,
             pointers={'A.index(num) if _line >= 20 else None': 'blue'},
             pointer_labels={'A.index(num) if _line >= 20 else None': 'num'},
             color=_kept),
    ],
    watch=[('flag', 'flag'), ('now', 'now', 'cyan'), ('s', 's'), ('res', 'res', 'green')],
    captions={
        3: '`flag`：先假设所有数都 ≤ 0',
        4: '检查 `{num}`',
        5: lambda S, B, ret: (f'`{S.num} > 0` → 有正数，不是特殊情况' if S.num > 0 else f'`{S.num} ≤ 0`，继续检查'),
        6: '`flag = False`',
        7: '找到正数就可以停了',
        9: lambda S, B, ret: ('全都 ≤ 0：答案就是数组的最大值' if S.flag else '有正数 → 只有两种可能：==普通的一段==，或==首尾两段=='),
        10: '返回 `max(A) = {ret}`',
        12: '第一种：普通的连续一段，用==贪心==求最大子段和',
        13: '`now`：当前子段和',
        14: _for('第一趟结束：普通的一段最大是 `res = {res}`'),
        15: lambda S, B, ret: f'`now = {B.now} + {_P(S.num)}` = =={S.now}==',
        16: lambda S, B, ret: (f'`now = {S.now} < 0` → 这段只会拖后腿，==从下一个数重新开始==' if S.now < 0
                               else f'`now = {S.now} ≥ 0`，保留这一段'),
        17: '`now = 0`：子段清空',
        18: '`res = max({B.res}, {now})` = =={res}==',
        20: '第二种：首尾两段 = 整个数组==去掉中间和最小的一段==',
        21: '`s = sum(A) = {s}`',
        22: _for('第二趟结束：首尾两段最大也比较完了，`res = {res}`'),
        23: lambda S, B, ret: f'`now = {B.now} + {_P(S.num)}` = =={S.now}==',
        24: lambda S, B, ret: (f'`now = {S.now} > 0` → 去掉它反而让和变小，不能当“最小段”，清零' if S.now > 0
                               else f'`now = {S.now} ≤ 0`，作为被去掉的中间段候选'),
        25: '`now = 0`：中间段清空',
        26: lambda S, B, ret: (f'中间段为空（和 0）：相当于选整个数组 `{S.s}` → `res = {S.res}`' if S.now == 0
                               else f'去掉和为 `{S.now}` 的中间段：`{S.s} − {_P(S.now)}` = `{S.s - S.now}` → `res = {S.res}`'),
        28: '答案 =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='普通一段用贪心；首尾两段 = 总和 − 最小子段和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['==环形==整数数组 `nums`（末尾和开头相连），求非空子数组的最大和',
                 '每个元素最多用一次',
                 '示例：`[5,-3,5]` → `10`；本视频：`[4,-5,1,2]` → `7`（`[1,2,4]` 跨越首尾）'],
        quote='对于后面这种首尾两段的问题，则可以将其看成一个数组，我们需要从中间去除掉一个子段，同时要求这个子段和最小。那么去除掉这个子段之后，剩下的首尾两段之后自然就是最大的。',
        quote_src='—— yiduobo 题解',
        idea=['特殊情况：所有数都 ≤ 0 → 答案就是最大值，先扫一遍判断',
              '普通一段：经典贪心，加入当前数后子段和 < 0 就清零，从下一个数重新开始',
              '首尾两段：同样的贪心求==最小==子段和，答案 = 总和 − 最小子段和'],
        result='普通一段最大 `4`；首尾两段 `2 − (−5) = 7` → 返回 `7` ✓',
        summary=['时间 `O(n)`（扫三趟），空间 `O(1)`',
                 '特判全 ≤ 0：否则第二趟会“去掉整个数组”，得到不合法的空子数组',
                 '第二趟 `now = 0` 时 `s − now = s`：去掉空段 = 选整个数组，合法',
                 '对比灵神：灵神一次遍历同时维护最大、最小，用 `max_s < 0` 特判',
                 '原文为 Python 2 风格，代码未改，仅删去 docstring'],
    ),
)
