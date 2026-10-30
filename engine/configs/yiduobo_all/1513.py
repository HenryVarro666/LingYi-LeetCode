CONFIG = dict(
    num=1513, title='仅含 1 的子串数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按 0 分段 · 等差数列求和',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1351'],
    code='''
class Solution(object):
    def numSub(self, s):
        
        mod = 10 ** 9 + 7
        res = 0
        l = 0
        for char in s:
            if char == '1':
                l += 1
            else:
                res += l * (l + 1) // 2
                res %= mod
                l = 0
        
        res += l * (l + 1) // 2
        return res % mod
''',
    call='Solution().numSub("0110111")',
    expect=9,
    views=[
        dict(type='string', var='s', h=260,
             label='s（青色 = 1）',
             color=lambda S, i, v: 'cyan' if v == '1' else None),
        dict(type='text', h=140, fn=lambda S: f"当前全 1 段长度 `l = {S['l']}`，能提供 `{S['l']}×{S['l']+1}/2 = {S['l']*(S['l']+1)//2}` 个子串" if 'l' in S else ''),
    ],
    watch=['char', ('l', 'l', 'pink'), ('res', 'res', 'green')],
    captions={
        4: '答案要对 `10^9+7` 取模',
        5: '`res` 累计已结束的各段全 1 串提供的子串数',
        6: '`l` 是最近一段连续 1 的长度',
        7: lambda S, B, r: f'取下一个字符 `{S.char}`' if 'char' in S else '遍历结束',
        "if char == '1'": lambda S, B, r: (f'`{S.char}` 是 1 → 当前全 1 段继续变长' if S.char == '1' else f'`{S.char}` 是 0 → 这一段全 1 串结束，开始结算'),
        'l += 1': '`l = {l}`',
        'res += l * (l + 1) // 2': '长 `{l}` 的全 1 串有 `{l}×({l}+1)/2` = =={l * (l + 1) // 2}== 个合法子串 → `res = {res}`',
        'res %= mod': '取模：`res = {res}`',
        13: '下一段重新计数：`l = 0`',
        'return res % mod': '最后一段 1 没有遇到 0 来结算，所以返回前补加；结果 =={ret}==',
    },
    cards=dict(
        one_liner='按 0 切开，长 k 的全 1 串有 k(k+1)/2 个子串',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，统计所有字符都为 1 的子串个数（对 `1e9+7` 取模）',
                 '示例：`"0110111"` → `9`'],
        quote='可以先按照0来对字符串进行分割，得到若干个全1的字符串。对于某个长度为k的全1字符串而言，……一共有1 + 2 + ... + k = k * (k + 1) / 2个合法的子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['按 0 把字符串切成若干全 1 段',
              '长 `k` 的段：长 1 的 k 个、长 2 的 k-1 个……长 k 的 1 个',
              '每段求和后累加，最后一段要在循环外补算'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：字符串以 1 结尾时，最后一段在循环里没结算，要补一次',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神按右端点累加 `i - last0`，不需要分段公式'],
    ),
)
