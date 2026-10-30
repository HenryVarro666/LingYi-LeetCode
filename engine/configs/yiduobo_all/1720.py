def _eq(S):
    if 'num' not in S or 'res' not in S:
        return ''
    r = S['res']
    if S.get('_line', 0) >= 6:
        a, n = r[-2], S['num']
        return f"`{a} ^ {n}` = `{a:03b} ^ {n:03b}` = ==`{a ^ n:03b}`== = =={a ^ n}== → 追加到 res"
    return f"当前 `res[-1] = {r[-1]}`，`encoded` 里的 `num = {S['num']}`"


CONFIG = dict(
    num=1720, title='解码异或后的数组', difficulty='Easy', category='位运算',
    author='yiduobo', technique='异或还原 · 一趟扫描', tags=['灵神题单'],
    code='''
class Solution(object):
    def decode(self, encoded, first):

        res = [first]
        for num in encoded:
            res.append(res[-1] ^ num)

        return res
''',
    call='Solution().decode([1, 2, 3, 4], 3)',
    expect=[3, 2, 0, 3, 7],
    views=[
        dict(type='array', var='encoded', h=170, label='encoded[i] = arr[i] ^ arr[i+1]',
             color=lambda S, i, v: 'yellow' if 'res' in S and i == len(S['res']) - (2 if S.get('_line', 0) >= 6 else 1) else None),
        dict(type='text', size=28, fn=_eq),
        dict(type='array', var='res', h=170, label='res = arr（还原出的数组）',
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('first', 'first', 'blue'), ('num', 'num', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = [first]': '题目给了 `arr[0] = first = {first}`，先放进 `res` 作为起点',
        'for num in encoded': lambda S, B, r: (f'取出 `encoded` 的下一个数 `num = {S.num}`，它等于 `arr[i] ^ arr[i+1]`'
                                               if len(S.res) <= len(S.encoded) else '`encoded` 用完了，数组已还原'),
        'res.append': '两边同时异或 `arr[i]`：`arr[i] ^ arr[i]` = 0，所以 `arr[i+1] = arr[i] ^ encoded[i]` = `{res[-2]} ^ {num}` = =={res[-1]}==',
        'return res': '`encoded` 扫完，返回还原的 `{res}`',
    },
    cards=dict(
        one_liner='两边再异或一次 arr[i]，就能由 arr[i] 推出 arr[i+1]',
        complexity='时间 `O(n)`，空间 `O(1)`（不算结果数组）',
        problem=['有隐藏数组 `arr`，已知 `encoded[i] = arr[i] ^ arr[i+1]` 和 `arr[0] = first`',
                 '还原 `arr`',
                 '示例：`encoded=[1,2,3]`，`first=1` → `[1,0,2,1]`；本视频：`[1,2,3,4]`、`3`'],
        quote='对于encode[i] = arr[i] ^ arr[i + 1]这个式子而言，可以在两侧都异或上arr[i]，那么就有encode[i] ^ arr[i] = arr[i + 1]',
        quote_src='—— yiduobo 题解原文',
        idea=['异或满足交换律，且 `a ^ a = 0`',
              '`encoded[i] ^ arr[i] = (arr[i] ^ arr[i]) ^ arr[i+1] = arr[i+1]`',
              '已知 `arr[0]`，从左到右一趟扫描，每一步用上一个结果 `res[-1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`（不算结果）',
                 '起点是 `first`，所以 `res` 比 `encoded` 长 1',
                 '用的是 `res[-1]`（刚还原的 arr[i]），不是 `encoded` 的前一个数',
                 '相关：2433. 找出前缀异或的原始数组'],
    ),
)
