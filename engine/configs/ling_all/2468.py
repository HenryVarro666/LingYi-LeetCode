def _cap(S):
    if 'i' not in S:
        return ''
    s = f"分 `i = {S['i']}` 段：容量 `cap = {S.get('cap')}`，消息长度 `len(message) = {len(S['message'])}`"
    if S.get('tail_len') is not None and S['_line'] >= 9:
        s += f"，结尾长 `tail_len = {S['tail_len']}`"
    return s


def _ans(S):
    a = S.get('ans')
    if a is None:
        return ''
    return '已切出：' + '  '.join(f'`{x}`' for x in a)


CONFIG = dict(
    num=2468, title='根据限制分割消息', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='枚举分割个数 + 累计容量',
    tags=['贪心算法', '思维题', '难度分 2382'],
    code='''
class Solution:
    def splitMessage(self, message: str, limit: int) -> List[str]:
        i = cap = 0
        while True:
            i += 1
            if i < 10:
                tail_len = 5  # 结尾的长度
            elif i < 100:
                if i == 10: cap -= 9  # 前面的结尾的长度都 +1，那么容量就要减小
                tail_len = 7
            elif i < 1000:
                if i == 100: cap -= 99
                tail_len = 9
            else:
                if i == 1000: cap -= 999
                tail_len = 11
            if tail_len >= limit: return []  # cap 无法增大，寄
            cap += limit - tail_len
            if cap < len(message): continue  # 容量没有达到，继续枚举

            ans, k = [], 0
            for j in range(1, i + 1):
                tail = f"<{j}/{i}>"
                if j == i:
                    ans.append(message[k:] + tail)
                else:
                    m = limit - len(tail)
                    ans.append(message[k: k + m] + tail)
                    k += m
            return ans
''',
    call='Solution().splitMessage("short message", 15)',
    expect=["short mess<1/2>", "age<2/2>"],
    views=[
        dict(type='text', fn=_cap, size=26),
        dict(type='string', var='message', h=230, label='message（绿色 = 已切走，k 指向下一段起点）', cell=60,
             color=lambda S, i, v: 'green' if 'k' in S and i < S['k'] else None,
             pointers={'k': 'blue'}),
        dict(type='text', fn=_ans, size=24),
    ],
    watch=['i', 'cap', 'tail_len', 'k', 'j'],
    captions={
        'i = cap = 0': '`i` 是分割个数，`cap` 是 `i` 段最多能装下的 `message` 字符数；从 `i = 1` 开始枚举',
        'i += 1': '试分成 `i = {i}` 段',
        'tail_len = 5': '`i = {i}` 是一位数：结尾 `<a/b>` 长 ==5==',
        'tail_len = 7': '`i = {i}` 是两位数：结尾长 ==7==',
        'tail_len = 9': '`i = {i}` 是三位数：结尾长 ==9==',
        'tail_len = 11': '`i = {i}` 是四位数：结尾长 ==11==',
        'cap -= 9': '`i` 进位到 10：前面 9 段的结尾都 +1，容量要减 9',
        'cap -= 99': '`i` 进位到 100：前面 99 段的结尾都 +1，容量要减 99',
        'cap -= 999': '`i` 进位到 1000：前面 999 段的结尾都 +1，容量要减 999',
        'if tail_len >= limit': lambda S, B, r: (f"`tail_len = {S.tail_len}` ≥ `limit = {S.limit}`：结尾就占满了，装不下字符，容量无法增大 → ==返回 []==" if S.tail_len >= S.limit else f"`tail_len = {S.tail_len}` < `limit = {S.limit}`：每段还能装 `{S.limit - S.tail_len}` 个字符"),
        'cap += limit - tail_len': '这一段多装 `limit - tail_len = {limit - tail_len}` 个字符：`cap = {B.cap} + {limit - tail_len} = {cap}`',
        'if cap < len(message)': lambda S, B, r: (f"`cap = {S.cap}` {'<' if S.cap < len(S.message) else '≥'} `len(message) = {len(S.message)}`" + (' → 容量不够，继续加一段' if S.cap < len(S.message) else ' → ==装得下了==，`i` 就是最少段数，开始构造')),
        'ans, k = [], 0': '`k` 是 `message` 已经切走的位置',
        'for j in range(1, i + 1)': lambda S, B, r: ('`2` 段都构造好了，退出循环'.replace('2', str(S.i)) if len(S.ans) == S.i else f"构造第 `{S.j}` 段（共 `{S.i}` 段）"),
        'tail = f': '结尾 `tail = {tail}`',
        'if j == i': lambda S, B, r: ('最后一段（`j == i`）：==剩下的全部放进去==，长度可以不足 `limit`' if S.j == S.i else '不是最后一段：必须刚好凑满 `limit`'),
        'ans.append(message[k:]': '最后一段：`{ans[-1]}`',
        'm = limit - len(tail)': '这一段能装 `m = {limit} - {len(tail)} = {m}` 个字符',
        'ans.append(message[k: k + m]': '取 `message[{k}:{k + m}]` 加上结尾 → `{ans[-1]}`',
        'k += m': '`k` 右移 `{m}` → {k}',
        'return ans': '构造完成：{len(ans)} 段，返回 `{ans}`',
    },
    cards=dict(
        one_liner='枚举分割个数，累加每段容量，容量够了就是最少段数',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['把 `message` 切成若干段，每段末尾加 `<a/b>`（编号/总段数）',
                 '除最后一段外，每段长度==恰好==等于 `limit`；段数要最少，不行返回空数组',
                 '示例：`"short message", 15` → `["short mess<1/2>","age<2/2>"]`'],
        quote='枚举分割个数 i，不断增大容量 cap，直到 cap ≥ n 为止，就可以分割了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分 `i` 段，结尾长度只取决于 `i` 的位数：5 / 7 / 9 / 11',
              '每多一段，容量增加 `limit - tail_len`；位数进位时，前面所有结尾变长，要把 `cap` 减掉',
              '第一个满足 `cap ≥ len(message)` 的 `i` 就是答案，再按每段容量切开'],
        summary=['时间 `O(n log n)`（构造答案），空间 `O(1)`',
                 '`tail_len >= limit` 时一段连一个字符都装不下，直接返回 `[]`',
                 '进位时 `cap -= 9 / 99 / 999`：前面各段的结尾都多了一位',
                 '最后一段取剩余全部，不用凑满 `limit`'],
    ),
)
