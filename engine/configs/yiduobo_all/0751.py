def _bits(S):
    if 'now' not in S:
        return ''
    low = S['now'] & 63
    return f"`now` 低 6 位 = `{low:06b}`（十进制 {S['now'] & 255}）；`cnt = {S.get('cnt', 1)}` → 当前块大小 `{1 << (S.get('cnt', 1) - 1)}`"


def _rest(S):
    if 'n' not in S:
        return ''
    return f"还剩 `n = {S['n']}` 个 ip 没有覆盖"


CONFIG = dict(
    num=751, title='IP 到 CIDR', difficulty='Medium', category='位运算',
    author='yiduobo', technique='贪心取最大的 2 的幂块',
    tags=['灵神题单·位运算'],
    code='''
class Solution(object):
    def ipToCIDR(self, ip, n):

        ip = ip.split('.')
        now = (int(ip[0]) << 24) | (int(ip[1]) << 16) | (int(ip[2]) << 8) | int(ip[3])
        cnt = 1
        res = []
        while n > 0:
            while 1 << cnt <= n and (now & (1 << (cnt - 1)) == 0):
                cnt += 1
            
            res.append('%d.%d.%d.%d/%d' % (now >> 24, (now >> 16) & 255, (now >> 8) & 255, now & 255, 32 - cnt + 1))
            now += 1 << (cnt - 1)
            n -= 1 << (cnt - 1)
            cnt = 1
        
        return res
''',
    call="Solution().ipToCIDR('255.0.0.7', 10)",
    expect=['255.0.0.7/32', '255.0.0.8/29', '255.0.0.16/32'],
    views=[
        dict(type='text', fn=_bits, size=26, h=60),
        dict(type='text', fn=_rest, size=26, h=60),
        dict(type='stack', var='res', fmt=lambda x: str(x), label='res：已切出的 CIDR（新加入的为绿色）', h=300),
    ],
    watch=[('now', 'now & 255', 'blue'), ('n', 'n', 'pink'), ('cnt', 'cnt', 'orange'), ('|res|', 'len(res)', 'green')],
    captions={
        'ip = ip.split': 'ip 切成四段：`{ip}`',
        'now = (': '把四段拼成一个 32 位整数 `now`，这样加减、位运算都方便',
        6: '`cnt` 表示块大小为 `2^(cnt-1)`，先从大小 1（`/32`）起步',
        'while n > 0': lambda S, B, r: (f'还剩 `n = {S.n}` 个 ip，继续切' if S.n > 0 else '`n = 0`，全部覆盖 → 结束'),
        'while 1 << cnt': lambda S, B, r: (f'`1<<{S.cnt} = {1 << S.cnt}` 不超过 `n = {S.n}`，且 `now` 的第 {S.cnt - 1} 位是 0 → 块还能再翻倍，`cnt` 增大'
                                          if (1 << S.cnt <= S.n and S.now & (1 << (S.cnt - 1)) == 0) else
                                          ('块再翻倍会超过 `n`，停止扩大' if 1 << S.cnt > S.n else f'`now` 的第 {S.cnt - 1} 位是 1 → 起点不对齐，不能再扩大')),
        'cnt += 1': '块大小翻倍：`cnt = {cnt}`，现在块大小 ==`{1 << (cnt - 1)}`==',
        'res.append': '切出一块：起点 `{res[-1].split("/")[0]}`，前缀长度 `32 - cnt + 1 = {32 - cnt + 1}` → ==`{res[-1]}`==',
        'now += ': '起点后移 `{1 << (cnt - 1)}`，指向下一个未覆盖的 ip',
        'n -= ': '`n` 减去这块的大小，还剩 `{n}`',
        15: '`cnt` 复位为 1，下一块重新从最小开始找',
        'return res': '`n` 用完，得到 `{len(ret)}` 块 CIDR',
    },
    max_steps=80,
    cards=dict(
        one_liner='起点末尾有几个 0，决定了块最大能有多大',
        complexity='时间 `O(log n)` 块数，空间 `O(1)`',
        problem=['给起始 ip 和整数 `n`，要用最少的 CIDR 块恰好覆盖从该 ip 开始的 `n` 个地址',
                 'CIDR 写作 `ip/前缀长度`，块大小是 2 的幂',
                 '示例：`255.0.0.7, n=10` → `["255.0.0.7/32","255.0.0.8/29","255.0.0.16/32"]`'],
        quote='起始ip地址的最后若干位必然为0，而区间中最后一个ip地址的最后若干位必然为1，因此这个区间长度必然是2的幂次。',
        quote_src='—— yiduobo 题解原文',
        idea=['把 ip 当作 32 位整数 `now`：块起点的低位必须全为 0（对齐）',
              '每次找最大的 `2^k`：`2^k <= n`，且 `now` 的低 `k` 位全为 0',
              '切出这一块后，`now` 和 `n` 一起更新，重复到 `n = 0`'],
        summary=['时间 `O(log n)` 块，每块最多检查 32 位，空间 `O(1)`',
                 '块大小 `2^(cnt-1)`，前缀长度是 `32 - cnt + 1`',
                 '扩大条件有两个：不超过 `n`，且 `now` 对应位为 0（对齐）',
                 '原文可直接在 Python 3 运行，无需修改',
                 '例子里 `.7` 是奇数，只能先切一个 `/32`，再用对齐的 `.8` 切 `/29`'],
    ),
)
