def _txt(S):
    if 'num' not in S or 'p' not in S:
        return '把每个数一位一位拆开，给每一位上的 1 计数'
    return f"`num` 还剩 `{S['num']:b}`（拆掉一位清一位），当前看第 =={S['index']}== 位（`p` = {S['p']}）"


CONFIG = dict(
    num=2275, title='按位与结果大于零的最长组合', difficulty='Medium', category='位运算',
    author='yiduobo', technique='拆位 · 逐位统计 1 的数目',
    tags=['灵神题单', '难度分 1642'],
    code='''
class Solution(object):
    def largestCombination(self, candidates):
        
        pow2 = [1]
        for index in range(1, 24):
            pow2.append(pow2[-1] + pow2[-1])

        cnt = [0] * 24
        for num in candidates:
            for index, p in enumerate(pow2):
                if num & p:
                    num ^= p
                    cnt[index] += 1

        return max(cnt)
''',
    call='Solution().largestCombination([5,6,7,4])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='candidates', label='candidates', h=150),
        dict(type='array', var='cnt', label='cnt[index]：第 index 位上是 1 的数的数目', h=200, cell=36,
             pointers={'index': 'pink'},
             color=lambda S, i, v: 'green' if v and v == max(S['cnt']) else None),
    ],
    watch=['num', 'index', 'p', ('max(cnt)', 'max(cnt)', 'green')],
    skip=['pow2.append', 'for index in range(1, 24)', 'for index, p in enumerate(pow2)', 'if num & p'],
    captions={
        'pow2 = [1]': '`pow2` 存 2 的各次幂，用来逐位取出每个二进制位',
        'cnt = [0] * 24': '`cnt[index]`：第 `index` 位等于 1 的数的数目（`10^7 < 2^24`）',
        'for num in candidates': lambda S, B, r: (f'取下一个数 `{S.num}`（二进制 `{S.num:b}`），一位一位拆开' if S.num else '所有数都拆完了，`cnt` 里就是每一位上 1 的数目'),
        'num ^= p': '`num & {p}` 非零：第 {index} 位是 1 → 用异或把它清掉，`num` = {num}',
        'cnt[index] += 1': '给第 {index} 位计数：`cnt[{index}]` = =={cnt[index]}==',
        'return max(cnt)': '要 AND>0 就得有一位全是 1：选这一位是 1 的所有数 → 最大的 `cnt` = =={max(cnt)}==',
    },
    cards=dict(
        one_liner='AND 大于 0，必有一位全是 1：数哪一位的 1 最多',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['从 `candidates` 里选一个组合，要求所有数按位与 `> 0`',
                 '求这样的组合最长是多少',
                 '示例：`[16,17,71,62,12,24,14]` → `4`；本视频用 `[5,6,7,4]` → `4`'],
        quote='那么必须有至少一个二进制位，满足所有参与与运算的数在这一位上都等于1。题目要找的是最长的组合，实际上就是要找出一个二进制位，使得在这一位上等于1的数最多。',
        quote_src='—— yiduobo 题解原文',
        idea=['先造 `pow2`：1, 2, 4, …, 2^23，每个对应一个二进制位',
              '每个数拿 `pow2` 逐位测：`num & p` 非零就计数，并用 `^=` 清掉这一位',
              '各位计数的 ==最大值== 就是答案'],
        summary=['时间 `O(n log U)`，空间 `O(log U)`',
                 '原文是 Python 2 风格，在 Python 3 下可直接运行，未做改动',
                 '视频里为了节奏，省略了「造 `pow2`」和每一位的 `if` 判断步骤，只展示命中 1 的位',
                 '对比灵神：灵神用 `x & 1` 加右移取位，yiduobo 用 2 的幂 + 异或清位'],
    ),
)
