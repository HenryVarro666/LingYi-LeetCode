CONFIG = dict(
    num=1908, title='Nim 游戏 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='SG 函数 · 全部异或',
    tags=['博弈论'],
    code='''
class Solution(object):
    def nimGame(self, piles):

        v = 0
        for p in piles:
            v ^= p
        
        return v > 0
''',
    call='Solution().nimGame([3,4,7])',
    expect=False,
    views=[
        dict(type='array', var='piles', label='piles（每堆石子数）', h=230, cell=110),
        dict(type='text', h=80, size=34,
             fn=lambda S: f"v = =={S['v']}==（二进制 =={bin(S['v'])[2:].zfill(3)}==）" if 'v' in S else ''),
        dict(type='text', h=80, size=30,
             fn=lambda S: f"本次异或：`{S['v'] ^ S['p']}` ^ `{S['p']}` = =={S['v']}==" if 'p' in S and 'v' in S and S.get('_line') == 7 else ''),
    ],
    watch=[('p', 'p', 'yellow'), ('v', 'v', 'green')],
    captions={
        'v = 0': '`v` 保存所有堆的 SG 值异或，初值 0',
        'for p in piles': '逐堆处理：每一堆都是独立子局面，`sg(p) = p`；取完所有堆循环结束',
        'v ^= p': '`v ^= p`：`{B.v}` ^ `{p}` → =={v}==（二进制 {bin(v)[2:]}）',
        'return v > 0': lambda S, B, r: (f'`v = {S.v}`：{"异或和不为 0，先手有必胜策略" if S.v > 0 else "异或和为 0，先手必败"} → ==返回 {r}=='),
    },
    cards=dict(
        one_liner='每一堆的 SG 值就是石子数，整局的 SG 值 = 各堆异或',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`piles[i]` 是第 `i` 堆的石子数，Alice 先手，轮流选一堆取走任意正数个石子',
                 '无法操作的一方输。Alice 能赢返回 `true`',
                 '示例（本视频）：`[3,4,7]` → `false`（3^4^7 = 0）'],
        quote='对于本题，piles中的每一堆石头都可以视为一个平等的子局面，那么对于其中某一堆石头v，都有sg(v) = v。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目就是 Nim 游戏，用 SG 函数：每堆是独立子局面',
              '归纳证明 `sg(v) = v`：`sg(i) = mex(sg(0..i-1)) = mex(0..i-1) = i`',
              '多个子局面的 SG 值异或起来，非 0 先手必胜'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`v > 0` 即先手必胜；`v == 0` 先手必败',
                 '关键结论：`sg(v) = v`，所以不用建 SG 表，直接异或',
                 '原文是 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
