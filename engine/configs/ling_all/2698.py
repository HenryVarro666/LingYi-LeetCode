CONFIG = dict(
    num=2698, title='求一个整数的惩罚数', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='划分型回溯 · 预处理',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1679'],
    code='''
def init():
    global PRE_SUM
    PRE_SUM = [0] * 10
    for i in range(1, 10):
        s = str(i * i)
        n = len(s)
        def dfs(p: int, sum: int) -> bool:
            if p == n:  # 递归终点
                return sum == i  # i 符合要求
            x = 0
            for j in range(p, n):  # 枚举分割出从 s[p] 到 s[j] 的子串
                x = x * 10 + int(s[j])  # 子串对应的整数值
                if dfs(j + 1, sum + x):
                    return True
            return False
        PRE_SUM[i] = PRE_SUM[i - 1] + (i * i if dfs(0, 0) else 0)

class Solution:
    def punishmentNumber(self, n: int) -> int:
        return PRE_SUM[n]
''',
    call='''init()
Solution().punishmentNumber(9)''',
    expect=82,
    views=[
        dict(type='text', fn=lambda S: (f"枚举 `i = {S['i']}`，`i*i = {S['i']*S['i']}`，要把它的数字切成几段，使各段之和 == =={S['i']}==" if 'i' in S and 's' in S else ''), size=26, h=70),
        dict(type='string', var='s', label='s = str(i*i)（蓝 = 当前切出的子串 s[p..j]）', cell=84, h=230,
             pointers={'p': 'pink', 'j': 'blue'},
             color=lambda S, k, v: 'blue' if ('p' in S['_inner'] and 'j' in S['_inner'] and S['_inner']['p'] <= k <= S['_inner']['j']) else None),
        dict(type='calls', h=260),
        dict(type='text', fn=lambda S: '一旦某种切法凑出 `i`，立刻返回 `True`，`i*i` 才会加进 `PRE_SUM`' if 'i' in S else '', size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('p', lambda S: S['_inner'].get('p'), 'pink'), ('sum', lambda S: S['_inner'].get('sum'), 'cyan'),
           ('x', lambda S: S['_inner'].get('x'), 'yellow')],
    skip=['global PRE_SUM', 'n = len(s)', '            x = 0', 'for j in range(p, n)'],
    captions={
        'for i in range(1, 10)': '预处理：逐个判断 `i`，建好前缀和表',
        's = str(i * i)': '`i*i = {i*i}`，转成字符串 `"{s}"`，后面在字符串上切',
        'if p == n': lambda S, B, ret: (f'`p == n = {S.n}`：整串切完了 → ==递归终点==' if S.p == S.n
                                         else f'`p = {S.p} < n = {S.n}`：还有 `{S.s[S.p:]}` 没切，继续'),
        'return sum == i': '各段之和 `{sum}` {"==" if sum == i else "!="} `i = {i}` → ==返回 {ret}==',
                'x = x * 10 + int(s[j])': '枚举子串 `s[{p}..{j}]` = `{s[p:j+1]}`，对应整数 `x = {x}`',
        'if dfs(j + 1, sum + x)': '已切出 `{B.x}`，累计 `sum + x = {B.sum + B.x}`，递归去切 `s[{B.j + 1}:]`',
        'return True': '下面某种切法凑出了 `i` → 一路返回 `True`，不用再试别的切法',
        'return False': '这一层所有切法都试过了，都凑不出 → 返回 `False`（回溯）',
        'PRE_SUM[i] = PRE_SUM[i - 1]': '`dfs(0, 0)`：从头开始切 `i*i`，看能不能凑出 `i`',
        'return PRE_SUM[n]': '查表 `O(1)`：`PRE_SUM[{n}]` = =={ret}==',
    },
    max_steps=66,
    cards=dict(
        one_liner='把 i² 的数字串切成几段，段和等于 i 就算数',
        complexity='预处理 `O(U^1.602)`；每次查询 `O(1)`，空间 `O(U)`',
        problem=['`n` 的惩罚数 = 所有满足条件的 `i`（`1 <= i <= n`）的 `i*i` 之和',
                 '条件：`i*i` 的十进制字符串能切成若干连续子串，整数值之和 `== i`',
                 '示例：`n = 10` → `182`（`1`、`9 = 8+1`、`10 = 10+0`）；本视频演示 `n = 9` → `82`'],
        quote='把 i² 转成字符串 s，然后写一个递归，枚举 s 分割出的第一个子串、第二个子串、……，把每个子串对应的整数值 x 加到 sum 中。递归到终点时，如果 sum = i，则说明 i 符合要求。',
        quote_src='—— 灵茶山艾府题解',
        idea=['划分型回溯：`dfs(p, sum)` 表示 `s[:p]` 已经切好，和为 `sum`',
              '枚举下一段 `s[p..j]`，累加后递归；`p == n` 时看 `sum == i`',
              '`n <= 1000`，一次性预处理出前缀和，查询直接查表'],
        summary=['时间：预处理 `O(U^1.602)`，不计入评测；查询 `O(1)`；空间 `O(U)`',
                 '演示：预处理包进 `init()`，范围缩小为 `[1,9]`（原文是模块级的 `[0]*1001`、`range(1, 1001)`）',
                 '找到一种切法就 `return True`，不用继续枚举',
                 '易错：`PRE_SUM` 累加的是 `i*i`，不是 `i`',
                 '写法二：不转字符串，用 `divmod(val, 10)` 从低位往高位切'],
    ),
)
