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
    if 'cnt' not in S:
        return '把 E 看成上车，L 看成下车：车上最多多少人？'
    return f"车上现在 `{S['cnt']}` 人，历史最多 `{S['ans']}` 人 = 至少要这么多椅子"


CONFIG = dict(
    num=3168, title='候诊室中的最少椅子数', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='模拟 · 上下车最大人数',
    tags=[],
    code='''
class Solution:
    def minimumChairs(self, s: str) -> int:
        ans = cnt = 0
        for c in s:
            if c == 'E':
                cnt += 1
                ans = max(ans, cnt)
            else:
                cnt -= 1
        return ans
''',
    setup=SETUP,
    call=f'Solution().minimumChairs(_Str({S0!r}))',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（框 = 当前事件）', cell=84, h=210,
             pointers={_k: 'blue'}, pointer_labels={_k: 'c'},
             window=(_k, _k)),
        dict(type='text', fn=_show, size=30, h=100),
    ],
    watch=[('c', 'c', 'blue'), ('cnt', 'cnt', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt = 0': '`cnt` 是候诊室当前人数，`ans` 是出现过的最大人数，开始都是 0',
        'for c in s': lambda S, B, ret: (f"第 `{_k(S)}` 秒：事件 `{S.c}`" if _k(S) is not None else '所有事件处理完毕'),
        "if c == 'E'": lambda S, B, ret: (f"`{S.c} == 'E'` → 有人进来，要占一把椅子" if S.c == 'E'
                                          else f"`{S.c}` 不是 `'E'` → 有人离开，空出一把椅子"),
        'cnt += 1': '进来一位：`cnt` = =={cnt}==',
        'ans = max': '椅子数必须撑得住最拥挤的时刻：`ans = max({B.ans}, {cnt})` = =={ans}==',
        'cnt -= 1': '走了一位：`cnt` = =={cnt}==（人变少，不会产生新的最大值，不用更新 ans）',
        'return ans': '最拥挤时有 `{ans}` 人 → 至少 =={ret}== 把椅子',
    },
    cards=dict(
        one_liner='E 是上车，L 是下车：求车上最多的人数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`E` 表示一位顾客进入候诊室并占一把椅子，`L` 表示一位顾客离开、释放一把椅子',
                 '候诊室一开始是空的，求保证每位顾客都有椅子坐的==最少椅子数==',
                 '示例：`"ELELEEL"` → `2`',
                 '本视频：`"ELEELEELLL"` → `3`'],
        quote='把 E 看成上车，L 看成下车，问：车上最多有多少人？模拟即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cnt` 记录当前人数：E 加一，L 减一',
              '椅子数要满足==任何时刻==都够坐，所以答案是 `cnt` 的历史最大值',
              '只有 `cnt` 变大时才可能刷新答案，所以 `ans = max(...)` 写在 E 的分支里'],
        result='最拥挤时有 3 人 → 返回 `3` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '答案是人数的==最大值==，不是 E 的总数，也不是最终人数',
                 '题目保证进出序列有效，`cnt` 不会变成负数',
                 '本质是前缀和的最大值，同类思路：1646、1893 之类的差分/前缀题'],
    ),
)
