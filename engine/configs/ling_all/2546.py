def _has(S, k):
    return '1' in S[k]


CONFIG = dict(
    num=2546, title='执行逐位运算使字符串相等', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='脑筋急转弯 · 有没有 1',
    tags=['灵神题单·位运算', '灵神题单·贪心与思维', '难度分 1605'],
    code='''
class Solution:
    def makeStringsEqual(self, s: str, target: str) -> bool:
        return ('1' in s) == ('1' in target)
''',
    call="Solution().makeStringsEqual('1010', '0110')",
    expect=True,
    views=[
        dict(type='string', var='s', label='s（绿 = 1，灰 = 0）', h=200,
             color=lambda S, i, v: 'green' if v == '1' else None),
        dict(type='string', var='target', label='target（绿 = 1，灰 = 0）', h=200,
             color=lambda S, i, v: 'green' if v == '1' else None),
        dict(type='text', size=34, h=120,
             fn=lambda S: f"s 里有 1：==`{'1' in S['s']}`==　target 里有 1：==`{'1' in S['target']}`==　→ 两边{'一致，可以互相转换' if ('1' in S['s']) == ('1' in S['target']) else '不一致，转不了'}"),
        dict(type='text', size=28, h=150,
             fn=lambda S: '`1` 和 `0` 操作 → `(1,1)`：把 0 变成 1；`1` 和 `1` 操作 → `(1,0)`：把 1 变成 0；`0` 和 `0` → 还是 `(0,0)`'),
    ],
    watch=[('s', 's', 'blue'), ('target', 'target', 'pink')],
    captions={
        'return': '`\'1\' in s` = =={"1" in s}==，`\'1\' in target` = =={"1" in target}==：只看两边是否都有 1（或都没有）→ ==返回 {ret}==',
    },
    cards=dict(
        one_liner='只要有 1，就能随意造 1 和消 1；全 0 则永远是全 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['对二元串 `s` 反复选两个下标 `i, j`：`s[i] = s[i] OR s[j]`，`s[j] = s[i] XOR s[j]`',
                 '问能否把 `s` 变成 `target`',
                 '示例：`s = "1010"`，`target = "0110"` → `true`；`"11"` → `"00"` → `false`'],
        quote='如果字符串中有 1，那么：选 1 和 0 可以把 0 变成 1；选 1 和 1 可以把 1 变成 0。而如果只有 0，是无法得到 1 的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['操作只有三种情形：`(0,0)→(0,0)`，`(0,1)→(1,1)`，`(1,1)→(1,0)`',
              '有 1 时：能造 1，也能消 1，只要至少留一个 1，任何含 1 的串都能到',
              '全 0 的串什么也变不出来，所以只比较「有没有 1」'],
        after=[dict(heading='为什么全 0 变不出 1', lines=[
            '操作后 `s[i] = s[i] OR s[j]`，`s[j] = s[i] XOR s[j]`',
            '两个数都是 0 时，OR 和 XOR 的结果都是 0',
            '所以全 0 的串永远只会是全 0，没法变成含 1 的 target',
            '反过来，含 1 的串总能保留至少一个 1，目标含 1 就能凑出来'])],
        summary=['时间 `O(n)`（`in` 最坏扫整串），空间 `O(1)`',
                 '易错点：不能把最后一个 1 消掉，所以 `"11"` 到 `"00"` 是 false',
                 '本质是脑筋急转弯：把复杂操作化成「是否存在 1」这个不变量',
                 '同类题：找不变量 / 判断可达性的思维题'],
    ),
)
