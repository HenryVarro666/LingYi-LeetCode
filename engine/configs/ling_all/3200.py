CONFIG = dict(
    num=3200, title='三角形的最大高度', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='枚举行数 · 两种颜色分配', tags=[],
    code='''
class Solution:
    def maxHeightOfTriangle(self, red: int, blue: int) -> int:
        cnt = [0, 0]
        for i in count(1):
            cnt[i % 2] += i
            if (cnt[0] > red or cnt[1] > blue) and (cnt[0] > blue or cnt[1] > red):
                return i - 1
''',
    setup='from itertools import count',
    call='Solution().maxHeightOfTriangle(2, 4)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: f"red = {S['red']}，blue = {S['blue']}" + (f"　｜　偶数行共 =={S['cnt'][0]}== 个，奇数行共 =={S['cnt'][1]}== 个" if 'cnt' in S else ''), size=30, h=60),
        dict(type='array', var='cnt', label='cnt：[偶数行球数, 奇数行球数]', h=200,
             color=lambda S, i, v: ('blue' if i == 0 else 'pink') if 'i' in S and i == S['i'] % 2 else None),
        dict(type='text', fn=lambda S: (
            f"方案甲：偶数行红、奇数行蓝　{'==够==' if S['cnt'][0] <= S['red'] and S['cnt'][1] <= S['blue'] else '`不够`'}" if 'i' in S else ''), size=28, h=60),
        dict(type='text', fn=lambda S: (
            f"方案乙：偶数行蓝、奇数行红　{'==够==' if S['cnt'][0] <= S['blue'] and S['cnt'][1] <= S['red'] else '`不够`'}" if 'i' in S else ''), size=28, h=60),
    ],
    watch=['red', 'blue', ('i', 'i', 'blue')],
    captions={
        'cnt = [0, 0]': '`cnt[0]` 记偶数行的球数，`cnt[1]` 记奇数行的球数，先都是 0',
        'for i in count': '第 `{i}` 行需要 `{i}` 个同色的球',
        'cnt[i % 2] += i': '第 `{i}` 行是{"奇" if i % 2 else "偶"}数行 → `cnt[{i % 2}]` 增加 {i}，变成 =={cnt[i % 2]}==',
        'if (cnt[0] > red': lambda S, B, r: (
            f"甲方案（偶红奇蓝）{'放不下' if S.cnt[0] > S.red or S.cnt[1] > S.blue else '还放得下'}；"
            f"乙方案（偶蓝奇红）{'放不下' if S.cnt[0] > S.blue or S.cnt[1] > S.red else '还放得下'}"
            + ('，==两种都不行 → 第 %d 行放不满==' % S.i if (S.cnt[0] > S.red or S.cnt[1] > S.blue) and (S.cnt[0] > S.blue or S.cnt[1] > S.red) else '，继续加一行')),
        'return i - 1': '第 `{i}` 行两种分配都放不满 → 最大高度是 `{i} - 1` = =={i - 1}==',
    },
    cards=dict(
        one_liner='奇偶行各放一种颜色，两种分配方式同时放不下就停',
        complexity='时间 `O(√min(red, blue))`，空间 `O(1)`',
        problem=['红球 `red` 个、蓝球 `blue` 个，摆第 `k` 行恰好 `k` 个同色球的三角形',
                 '相邻两行颜色必须不同，求最大高度',
                 '示例：`red = 2, blue = 4` → `3`'],
        quote='用一个长为 2 的 cnt 数组，分别记录偶数行和奇数行分别放了多少个球。从 i=1 开始枚举，如果 i 是奇数则把 cnt[1] 增加 i，如果 i 是偶数则把 cnt[0] 增加 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['颜色只能奇偶行交替：==奇数行一种颜色，偶数行另一种==',
              '只有两种分配：偶红奇蓝，或偶蓝奇红',
              '逐行累加两类行的球数，==两种分配都不够==时，上一行就是答案'],
        summary=['时间 `O(√min(red, blue))`，空间 `O(1)`',
                 '易错：判断条件是两种分配都失败（`and`），一种失败还不能停',
                 '返回 `i - 1`：第 i 行已经放不下',
                 '（setup 里补了 `from itertools import count`，作者代码未改）',
                 '题解方法二：奇数行 k 行需 k^2 球，偶数行需 k^2 + k 球，用 `isqrt` 直接算，O(1)'],
    ),
)
