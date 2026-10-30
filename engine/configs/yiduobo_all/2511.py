F = [1, 0, 0, -1, 0, 0, 0, 0, 1]

CONFIG = dict(
    num=2511, title='最多可以摧毁的敌人城堡数目', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 · 记录上次出现的 ±1',
    tags=[],
    code='''
class Solution(object):
    def captureForts(self, forts):

        pre_v = 0
        pre_pos = None
        res = 0

        for index, v in enumerate(forts):
            if v == 1 or v == -1:
                if v + pre_v == 0:
                    res = max(res, index - pre_pos - 1)
                pre_v = v
                pre_pos = index

        return res
''',
    call=f'Solution().captureForts({F!r})',
    expect=4,
    views=[
        dict(type='array', var='forts', label='forts', pointers={'pre_pos': 'pink', 'index': 'blue'}, cell=90, h=250,
             color=lambda S, i, v: ('green' if v == 1 else 'orange' if v == -1 else None)),
        dict(type='text', size=30, h=100,
             fn=lambda S: (f"`pre_v = {S['pre_v']}`：上一个 ±1 的值" if 'pre_v' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('pre_v', 'pre_v', 'pink'), ('pre_pos', 'pre_pos', 'pink'), ('res', 'res', 'green')],
    captions={
        'pre_v = 0': '`pre_v`：最后一次出现的是 1 还是 -1，0 表示还没出现',
        'pre_pos = None': '`pre_pos`：它的下标，还没有就是 `None`',
        'res = 0': '`res` 保存最长的一段 0',
        'for index, v': lambda S, B, r: ('全部遍历完，循环结束' if B.get('index') == S.index and B.get('index') is not None else f'看位置 `{S.index}`，值 `{S.v}`'),
        'if v == 1 or v == -1': lambda S, B, r: (f'`v = {S.v}` 是 1 或 -1 → 要检测一下' if S.v else f'`v = 0` 是敌方城堡，什么都不用做'),
        'if v + pre_v == 0': lambda S, B, r: (f'`{S.v} + {S.pre_v} = {S.v + S.pre_v}` → ==为 0==，一正一负，中间这段 0 是可行解' if S.v + S.pre_v == 0 else f'`{S.v} + {S.pre_v} = {S.v + S.pre_v}` ≠ 0，同号或前面没有，无事发生'),
        'res = max': '这段 0 长 `{index} − {pre_pos} − 1 = {index-pre_pos-1}`，`res = max({B.res}, {index-pre_pos-1}) = {res}`',
        'pre_v = v': '无论是否可行，都要用当前的 `{v}` 更新 `pre_v`',
        'pre_pos = index': '`pre_pos` 更新为 `{pre_pos}`',
    },
    cards=dict(
        one_liner='找一段最长的连续 0，两端分别是 1 和 -1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`1` 我方，`-1` 空位，`0` 敌方城堡',
                 '军队只能经过 0，从 1 走到 -1，途经的敌方全被摧毁',
                 '示例：`[1,0,0,-1,0,0,0,0,1]` → `4`'],
        quote='题目要求找出一段最长的连续0，这段0的两侧分别为1和-1。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，用 `pre_v` 和 `pre_pos` 记住最后一次出现的 ±1',
              '遇到新的 ±1，若 `v + pre_v == 0`（相加为 0 即一正一负），这段 0 就是可行解',
              '0 本身不用处理，继续往后走'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：不管是否可行，都要更新 `pre_v` 和 `pre_pos`',
                 '用「相加为 0」判断异号，比较巧妙',
                 '对比灵神：灵神只存下标 `pre`，用 `forts[pre]` 取值；这里把值和下标分开存'],
    ),
)
