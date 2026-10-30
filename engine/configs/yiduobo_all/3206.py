CONFIG = dict(
    num=3206, title='交替组 I', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举中心瓷砖 · 取模处理环', tags=[],
    code='''
class Solution(object):
    def numberOfAlternatingGroups(self, colors):

        res = 0
        n = len(colors)
        for index in range(n):
            pre = (index - 1 + n) % n
            nxt = (index + 1) % n
            if colors[pre] != colors[index] and colors[index] != colors[nxt]:
                res += 1
        
        return res
''',
    call='Solution().numberOfAlternatingGroups([0,1,0,0,1])',
    expect=3,
    views=[
        dict(type='array', var='colors', label='colors（环：末尾与开头相邻）', h=260,
             pointers={'pre': 'pink', 'index': 'blue', 'nxt': 'cyan'},
             color=lambda S, i, v: 'blue' if v == 1 else 'pink'),
        dict(type='text', fn=lambda S: (f"中心 `{S['index']}`：左 `colors[{S['pre']}]={S['colors'][S['pre']]}`，中 `{S['colors'][S['index']]}`，右 `colors[{S['nxt']}]={S['colors'][S['nxt']]}`" if 'nxt' in S else ''), size=28, h=60),
    ],
    watch=['index', 'pre', 'nxt', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计交替组个数',
        'n = len': '`n = {n}`，下标要对 `n` 取模来绕环',
        'for index in range': '把 `{index}` 号瓷砖当作中心',
        'pre = (': '左邻居 `(index - 1 + n) % n` = =={pre}==（`index` 为 0 时绕到末尾，+n 防负数）',
        'nxt = (': '右邻居 `(index + 1) % n` = =={nxt}==（最后一块绕回 0）',
        'if colors[pre]': lambda S, B, r: (f"左 {S.colors[S.pre]}，中 {S.colors[S.index]}，右 {S.colors[S.nxt]}："
                                           + ('左右都和中间不同 → ==是交替组==' if S.colors[S.pre] != S.colors[S.index] and S.colors[S.index] != S.colors[S.nxt] else '有一侧和中间相同 → 不是')),
        'res += 1': '找到一个交替组：`res` → =={res}==',
        'return res': '所有瓷砖都当过中心 → 共 `{res}` 个交替组',
    },
    cards=dict(
        one_liner='3 块交替，就看中间那块和左右是否都不同',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['0/1 数组 `colors` 围成环，连续 3 块颜色交替（中间与左右都不同）算一个交替组',
                 '求交替组个数',
                 '示例：`[0,1,0,0,1]` → `3`'],
        quote='若左侧位置瓷砖的颜色以及右侧位置瓷砖的颜色都不等于当前的颜色，就更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个交替组由唯一的中心瓷砖决定 → 枚举中心，不会重复',
              '环形：左邻居 `(index-1+n)%n`，右邻居 `(index+1)%n`',
              '左右都和中间不同，答案加一'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：左邻居要写成 `(index - 1 + n) % n`，避免下标 -1 的负数取模歧义（Python 里 -1 也能用，但其他语言不行）',
                 '推广：`k` 块交替的环形版本见 3208 交替组 II',
                 '原文本身已是 Python 3 可运行，未做改动'],
    ),
)
