CONFIG = dict(
    num=1513, title='仅含 1 的子串数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='记录上个 0 的位置 · 枚举右端点',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1351'],
    code='''
class Solution:
    def numSub(self, s: str) -> int:
        MOD = 1_000_000_007
        ans = 0
        last0 = -1
        for i, ch in enumerate(s):
            if ch == '0':
                last0 = i  # 记录上个 0 的位置
            else:
                ans += i - last0  # 右端点为 i 的全 1 子串个数
        return ans % MOD
''',
    call='Solution().numSub("0110111")',
    expect=9,
    views=[
        dict(type='string', var='s', pointers={'last0': 'pink', 'i': 'blue'}, h=300,
             window=('last0+1', 'i'),
             color=lambda S, i, v: 'pink' if 'last0' in S and i == S['last0'] and v == '0' else None),
        dict(type='text', h=120, fn=lambda S: f"右端点 `i = {S['i']}`：左端点 `{S['last0']+1} … {S['i']}`，共 `{S['i']} − ({S['last0']}) = {S['i']-S['last0']}` 个" if 'i' in S and S['s'][S['i']] == '1' else ''),
    ],
    watch=['i', ('last0', 'last0', 'pink'), ('ans', 'ans', 'green')],
    captions={
        3: '答案取模，但 `ans` 不会超过 64 位整数，最后再取模即可',
        'last0 = -1': '`last0` 记录上一个 0 的位置；一开始没有 0，设为 -1 兼容开头全是 1 的情况',
        "if ch == '0'": lambda S, B, r: (f'`s[{S.i}] = 0` → 包含它的子串都不合法' if S.ch == '0' else f'`s[{S.i}] = 1` → 可以作为全 1 子串的右端点'),
        'last0 = i': '窗口左边界被推到这个 0 的后面：`last0 = {last0}`',
        'ans += i - last0': '右端点为 `{i}` 的全 1 子串，左端点可以是 `{last0 + 1}…{i}`，共 `{i} − {last0}` = =={i - last0}== 个 → `ans = {ans}`',
        'return ans % MOD': '`{ans} % MOD` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举右端点，左端点从上个 0 的后面一路到自己',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，统计所有字符都为 1 的子串个数（对 `1e9+7` 取模）',
                 '示例：`"0110111"` → `9`'],
        quote='如果 s[i]=1，那么对于右端点为 i 的全 1 子串，左端点可以是 last0+1,last0+2,…,i-1,i，一共有 i-last0 个，加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历时记下上个 0 的位置 `last0`',
              '遇到 1：以它为右端点的全 1 子串有 `i - last0` 个',
              '`last0` 初值 -1，公式对开头没有 0 也成立'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '取模放到最后：灵神指出答案不超过 64 位整数',
                 '遇到 0 只更新 `last0`，不加答案',
                 '相似题：2348 全 0 子数组的数目'],
    ),
)
