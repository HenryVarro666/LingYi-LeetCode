CONFIG = dict(
    num=2928, title='给小朋友们分糖果 I', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='隔板法 + 容斥原理', tags=[],
    code='''
def c2(n: int) -> int:
    return n * (n - 1) // 2 if n > 1 else 0

class Solution:
    def distributeCandies(self, n: int, limit: int) -> int:
        return c2(n + 2) - 3 * c2(n - limit + 1) + 3 * c2(n - 2 * limit) - c2(n - 3 * limit - 1)
''',
    call='Solution().distributeCandies(5, 2)',
    expect=3,
    views=[
        dict(type='text', size=34, h=100, fn=lambda S: '答案 = `C(n+2,2)` − `3·C(n−limit+1,2)` + `3·C(n−2·limit,2)` − `C(n−3·limit−1,2)`'),
        dict(type='text', size=38, h=110, fn=lambda S: '代入 `n=5, limit=2`：`c2(7) − 3·c2(4) + 3·c2(1) − c2(−2)`'),
        dict(type='text', size=44, h=110, fn=lambda S: '`21 − 3×6 + 3×0 − 0` = ==3==' if S.get('_line') == 2 and S.get('n') == -2 else '先逐项算 c2，再合并'),
    ],
    watch=[],
    captions={
        'return n * (n - 1)': lambda S, B, r: {
            7: '所有方案（无限制，隔板法）：`c2(7) = C(7,2) = 21`',
            4: '至少一人超限：先发 `limit+1 = 3` 颗，`c2(4) = 6`，有 3 个人 → `3×6`',
            1: '至少两人超限：`n−2·limit = 1 ≤ 1`，选不出 2 个位置 → `0`',
            -2: '三人都超限：`5−3·2−1 = −2`，糖不够发 → `0`',
        }.get(S.n, f'`c2({S.n}) = {r}`'),
        'return c2(n + 2)': '一行四项：==所有方案 − 至少一个 + 至少两个 − 三个==，依次调用 `c2`',
    },
    cards=dict(
        one_liner='总方案数，减去超限方案；多减的再用容斥加回来',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把 `n` 颗糖分给 3 个小朋友，每人不超过 `limit` 颗，求方案数',
                 '示例：`n=5, limit=2` → `3`',
                 '`(1,2,2)`、`(2,1,2)`、`(2,2,1)`'],
        quote='可以先计算所有方案数（没有 limit 限制），再减去不合法的方案数（至少一个小朋友分到的糖果超过 limit）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['隔板法：`n` 个球 2 个隔板，`C(n+2, 2)` 种',
              '某人超限：先发他 `limit+1` 颗，剩下自由分 → `C(n−limit+1, 2)`',
              '至少一个 − 至少两个 + 三个，就是容斥原理'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`c2(n)` 在 `n ≤ 1` 时返回 0：糖不够先发时，方案数为 0',
                 '易错：发完 `limit+1` 后还可以继续给他发，所以是自由分',
                 '同类：2929、2927 数据更大，同一公式通用'],
    ),
)
