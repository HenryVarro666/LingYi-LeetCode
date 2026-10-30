CONFIG = dict(
    num=4006, title='统计有效前缀数目', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='0/1 计数差 ≤ 1',
    tags=[],
    code='''
class Solution:
    def countValidPrefixes(self, s: str) -> int:
        # 不用 list 的做法见【Python3 写法二】
        cnt = [0] * 2
        ans = 0
        for ch in s:
            cnt[int(ch)] += 1
            if abs(cnt[0] - cnt[1]) <= 1:
                ans += 1
        return ans
''',
    call='Solution().countValidPrefixes("0010110")',
    expect=5,
    views=[
        dict(type='string', var='s', label='s（绿 = 有效前缀的最后一个字符）', cell=70, h=170,
             pointers={'sum(cnt)-1': 'pink'}, dim=lambda S, i, v: 'cnt' in S and i > sum(S['cnt']) - 1),
        dict(type='array', var='cnt', label='cnt[0]、cnt[1]：已遍历的 0 / 1 个数', cell=100, h=170),
        dict(type='text', size=34, h=120, fn=lambda S: (f"`|{S['cnt'][0]} − {S['cnt'][1]}|` = =={abs(S['cnt'][0]-S['cnt'][1])}==" if 'cnt' in S else '')),
    ],
    watch=['ch', ('cnt', 'cnt', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'cnt = [0] * 2': '`cnt[0]`、`cnt[1]` 分别统计前缀里 0、1 的个数',
        'cnt[int(ch)] += 1': '读到 `{ch}`：`cnt[{ch}]` +1 → `cnt = {cnt}`',
        'if abs': '交替串里 0、1 个数差不超过 1：`|{cnt[0]} − {cnt[1]}| = {abs(cnt[0]-cnt[1])}` ≤ 1 → {"这个前缀有效" if abs(cnt[0]-cnt[1]) <= 1 else "无效，不能重排成交替串"}',
        'ans += 1': '有效前缀 +1 → `ans = {ans}`',
        'return ans': '共 `{ans}` 个有效前缀',
    },
    cards=dict(
        one_liner='重排成交替串，只要 0 和 1 的个数差 ≤ 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，若某个前缀的字符能重排成「相邻字符不相等」的交替串，就是有效前缀',
                 '返回有效前缀的数量',
                 '示例：`"00101"` → `3`（`"0"`、`"001"`、`"00101"`）'],
        quote='所以交替字符串中的 0 和 1 的个数的绝对差 ≤ 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['交替串长度为偶数：0、1 个数相等；为奇数：其中一个多 1',
              '所以前缀有效 ⇔ `|cnt0 − cnt1| ≤ 1`',
              '边遍历边计数，每个前缀 `O(1)` 判断'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '判断的是「能否重排」，不是前缀本身是否交替',
                 '写法二：只记 `cnt1`，`cnt0 = i + 1 - cnt1`，省掉列表'],
    ),
)
