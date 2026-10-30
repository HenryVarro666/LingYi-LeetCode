CONFIG = dict(
    num=3442, title='奇偶频次间的最大差值 I', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='哈希表计数 + 取最大奇数、最小偶数', tags=[],
    code='''
class Solution:
    def maxDifference(self, s: str) -> int:
        cnt = Counter(s)
        max1 = max(c for c in cnt.values() if c % 2 == 1)
        min0 = min(c for c in cnt.values() if c % 2 == 0)
        return max1 - min0
''',
    call='Solution().maxDifference("aaaaabbcc")',
    expect=3,
    views=[
        dict(type='string', var='s', label='s', cell=80, h=150),
        dict(type='map', var='cnt', label='cnt（字母 → 出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', h=90, size=30, fn=lambda S: (
            f"奇数次最大 ==`{S['max1']}`==，偶数次最小 ==`{S['min0']}`==" if 'min0' in S else
            f"奇数次里最大的次数：==`{S['max1']}`==" if 'max1' in S else '')),
    ],
    watch=['max1', 'min0'],
    captions={
        'cnt = Counter': '统计每个字母的出现次数：`cnt = {cnt}`',
        'max1 = max': '要差值最大：被减数取==奇数次里最大==的 → `max1 = {max1}`',
        'min0 = min': '减数取==偶数次里最小==的 → `min0 = {min0}`',
        'return max1 - min0': '答案 = `max1 - min0` = `{max1} - {min0}` = =={ret}==',
    },
    cards=dict(
        one_liner='奇数次要尽量大，偶数次要尽量小，两个值相减',
        complexity='时间 `O(n+|Σ|)`，空间 `O(|Σ|)`',
        problem=['选字母 `a1` 出现奇数次、`a2` 出现偶数次，求 `freq(a1) - freq(a2)` 的最大值',
                 '示例：`"aaaaabbc"` → `5 - 2 = 3`',
                 '本视频：`"aaaaabbcc"`，a 出现 5 次，b、c 各 2 次'],
        quote='要让奇数减偶数尽量大，那么奇数要尽量大，偶数要尽量小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用 `Counter` 数出每个字母的次数',
              '只看次数：奇数里取最大 `max1`，偶数里取最小 `min0`',
              '题目保证两类都存在，所以不用判空'],
        after=[dict(heading='为什么这样取', lines=['差值 = 奇数次的次数 − 偶数次的次数', '被减数越大、减数越小，差越大', '所以各自取极值，互不干扰', '示例里 a 是 5 次，b、c 各 2 次'])],
        summary=['时间 `O(n+|Σ|)`，空间 `O(|Σ|)`，`|Σ|=26`',
                 '偶数要的是==最小的正偶数==：没出现的字母不在 `cnt` 里，不会误取 0',
                 '最大的奇数与最小的偶数互不影响，各扫一遍即可'],
    ),
)
