SETUP = '''
class _Str(str):
    k = -1
    def __iter__(self):
        for j, ch in enumerate(str.__iter__(self)):
            self.k = j
            yield ch
        self.k = len(self)
'''
S0 = 'ELEELEELLL'


def _k(S):
    s = S.get('s')
    k = getattr(s, 'k', -1)
    return k if 0 <= k < len(S['s']) else None


def _show(S):
    if 'now' not in S:
        return '要的是“同时在场”的顾客数量'
    return f"当前在场 `now = {S['now']}`，最多出现过 `res = {S['res']}`"


CONFIG = dict(
    num=3168, title='候诊室中的最少椅子数', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 统计同时到达人数',
    tags=[],
    code='''
class Solution(object):
    def minimumChairs(self, s):
        now = 0
        res = 0
        for char in s:
            if char == 'E':
                now += 1
                res = max(res, now)
            else:
                now -= 1

        return res
''',
    setup=SETUP,
    call=f'Solution().minimumChairs(_Str({S0!r}))',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（框 = 当前遍历到的 char）', cell=84, h=210,
             pointers={_k: 'blue'}, pointer_labels={_k: 'char'},
             window=(_k, _k)),
        dict(type='text', fn=_show, size=30, h=100),
    ],
    watch=[('char', 'char', 'blue'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'now = 0': '`now` 统计当前在候诊室的顾客人数，一开始是空的',
        'res = 0': '`res` 记录答案：同时在场的最大人数',
        'for char in s': lambda S, B, ret: (f"遍历到 `s[{_k(S)}] = {S.char}`" if _k(S) is not None else '遍历完成'),
        "if char == 'E'": lambda S, B, ret: (f"`{S.char} == 'E'`：来了一位顾客，占一把椅子" if S.char == 'E'
                                             else f"`{S.char}` 不是 `'E'`：有顾客走了，空出一把椅子"),
        'now += 1': '来了一位，`now` → =={now}==',
        'res = max': '用 `now` 更新答案：`max({B.res}, {now})` = =={res}==',
        'now -= 1': '走了一位，`now` → =={now}==；人变少不会产生更大的值，所以不更新 `res`',
        'return res': '同时在场最多 `{res}` 人 → 需要 =={ret}== 把椅子',
    },
    cards=dict(
        one_liner='椅子数 = 同时在场顾客数的最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s[i]` 为 `E`：来了一位顾客并占用一把椅子；为 `L`：一位顾客离开并空出椅子',
                 '问至少准备多少把椅子，才能让每位顾客都有椅子坐',
                 '示例：`"ELELEEL"` → `2`',
                 '本视频：`"ELEELEELLL"` → `3`'],
        quote='题目实际上要求的是同时到达的顾客数量，于是只需使用一个变量now统计当前的顾客人数，然后一趟遍历……',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `now` 记当前顾客人数，一趟遍历 `s`',
              '遇到 `E`：`now` 加一，并用 `now` 去更新答案 `res`',
              '遇到 `L`：`now` 减一即可'],
        result='同时在场最多 3 人 → 返回 `3` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '只有来人（E）时才可能刷新答案，走人（L）时不用更新',
                 '答案是 `now` 的最大值，不是 E 的总个数',
                 '原文为 Python 2 风格，只删去了 def 后的空行，代码无需其他修改'],
    ),
)
