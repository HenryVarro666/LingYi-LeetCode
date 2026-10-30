SRC, TGT = 'cathe', 'dogwo'


def _fc(S, k, v):
    idx = S.get('index')
    if idx is None or 'f' not in S:
        return None
    if k == idx and S['_line'] in (21, 22, 37):
        return 'yellow'
    if k == idx:
        return 'blue'
    return None


def _sc(S, k, v):
    idx = S.get('index')
    if idx is None or 'f' not in S:
        return None
    return 'blue' if k == idx - 1 else None


def _fx(S):
    idx = S.get('index')
    if idx is None or 'p' not in S:
        return '`f[index]` = `source` 前 `index` 个字母变成 `target` 前 `index` 个字母的最小成本，==-1 表示做不到=='
    return f'正在算 `f[{idx}]`：看第 {idx} 个字母 `source[{idx - 1}] = {SRC[idx - 1]}`，`target[{idx - 1}] = {TGT[idx - 1]}`'


def _same(S, B, ret):
    i = S.index - 1
    if S.source[i] == S.target[i]:
        return f'`source[{i}]` == `target[{i}]`（都是 {S.source[i]}）：不用规则，沿用 `f[{S.index - 1}]`'
    return f'`source[{i}] = {S.source[i]}` ≠ `target[{i}] = {S.target[i]}`：先记 ==-1==，要靠规则才行'


def _skip(S, B, ret):
    p, r = S.p, S.r
    k = S.index - len(p)
    seg = S.target[k:S.index]
    if S.f[k] == -1:
        return f'`f[{k}] = -1`：前面已经做不到，这条规则用不上 → continue'
    if seg != r:
        return f'`target[{k}:{S.index}] = {seg}` ≠ `{r}`：替换结果对不上，规则不能用 → continue'
    return f'`f[{k}] = {S.f[k]}` 可达，且 `target[{k}:{S.index}] = {seg}` 恰好等于 `{r}`：再去看 `source` 能否匹配 `{p}`'


CONFIG = dict(
    num=3995, title='转换字符串的最小成本 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='线性 DP · 枚举规则结尾',
    tags=['其他线性 DP', '难度分 2101'],
    code='''
class Solution(object):
    def minCost(self, source, target, rules, costs):
        
        if len(source) != len(target):
            return -1
        
        f = [0]
        info = sorted(zip(rules, costs), key=lambda d:len(d[0][0]))
        for index in range(1, len(source) + 1):
            if source[index - 1] == target[index - 1]:
                f.append(f[-1])
            else:
                f.append(-1)
            
            for (p, r), c in info:
                if len(p) > index:
                    break
                if f[index - len(p)] == -1 or target[index - len(p): index] != r:
                    continue

                star = 0
                flag = True
                for s_char, p_char in zip(source[index - len(p): index], p):
                    if p_char == '*':
                        star += 1
                        continue
                    if s_char != p_char:
                        flag = False
                        break
                    
                if flag and (f[-1] == -1 or f[-1] > f[index - len(p)] + c + star):
                    f[-1] = f[index - len(p)] + c + star

        return f[-1]
''',
    call=f"Solution().minCost({SRC!r}, {TGT!r}, [['he','wo'],['c*t','dog'],['h*','wx']], [3,2,5])",
    expect=6,
    skip=['for s_char, p_char', "if p_char == '*'", 'star += 1', 'if s_char != p_char', 'flag = False', 'break', 'star = 0', 'flag = True', 'continue'],
    max_steps=80,
    views=[
        dict(type='string', var=lambda S: SRC, label='source', h=130, cell=70, color=_sc),
        dict(type='string', var=lambda S: TGT, label='target', h=130, cell=70, color=_sc),
        dict(type='text', fn=_fx, size=26, h=60),
        dict(type='array', var='f', label='f[index]（蓝 = 正在算的位置；-1 = 做不到）', h=220, cell=76, color=_fc),
    ],
    watch=[('index', 'index', 'blue'), 'p', 'r', ('c', 'c', 'orange'), ('star', 'star', 'pink')],
    captions={
        'if len(source) != len(target)': '先判断长度：题面没写等长，不等就直接 `-1`',
        'f = [0]': '`f[0] = 0`：两个空串天然相同，成本 0',
        'info = sorted': '规则按 `pattern` 长度从短到长排好，后面遇到太长的可以直接 `break`',
        'for index in range': '`index = {index}`：算 `f[{index}]`，即前 {index} 个字母',
        'if source[index - 1]': _same,
        'f.append(f[-1])': '`f[{index}] = f[{index - 1}]` = =={f[-1]}==：这个字母本来就一样',
        'f.append(-1)': '`f[{index}]` 先设 ==-1==：暂时没有办法',
        'for (p, r), c in info': '试规则 `{p} → {r}`，基础成本 `{c}`',
        'if len(p) > index': lambda S, B, r: (f'`len({S.p}) = {len(S.p)}` > `index = {S.index}`：规则放不下，==后面更长的也不行，break==' if len(S.p) > S.index
                                             else f'`len({S.p}) = {len(S.p)}` ≤ `index = {S.index}`：放得下'),
        'if f[index - len(p)] == -1 or': _skip,
        'continue': '这条规则不能用，换下一条',
        'if flag and': lambda S, B, r: (f'`pattern = {S.p}` 与 `source` 的对应段==不匹配==，不能用' if not S.flag
                                        else f'匹配成功，星号 `{S.star}` 个：候选成本 `f[{S.index - len(S.p)}] + {S.c} + {S.star}` = `{S.f[S.index - len(S.p)] + S.c + S.star}`'),
        'f[-1] = f[index - len(p)] + c + star': '更新 `f[{index}]` = =={f[-1]}==',
        'return f[-1]': lambda S, B, ret: f'`f[-1] = {ret}`：整个 `source` 变成 `target` 的最小成本',
    },
    cards=dict(
        one_liner='f[index] 看最后一段：没变就沿用，要变就挑一条结尾刚好的规则',
        complexity='时间 `O(nL)`，空间 `O(n)`',
        problem=['`source` 要变成 `target`，规则 `pattern → replacement` 一次替换一段，`*` 可匹配任意字母',
                 '规则成本 = 基础成本 + `pattern` 里 `*` 的个数；位置不能重复使用',
                 '本视频：`cathe → dogwo`，答案 `6`'],
        quote='可以先检测 target[index - len(pattern): index] 是否恰好等于 replacement，因为这里无需处理 \'*\' 的情况，因此可以直接通过字符串之间的比较进行判断。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index]`：前 `index` 个字符变好的最小成本，`f[0] = 0`，==-1 表示无解==',
              '字母相同可免费沿用 `f[index-1]`；不同先记 -1',
              '再枚举每条规则当作最后一段：先比 `target`，再数星号比 `source`，用 `f[前] + c + star` 取最小'],
        summary=['时间 `O(nL)`，`L` 是规则 `pattern` 长度之和；空间 `O(n)`',
                 '先比 `target` 与 `replacement`（纯字符串比较），不对就不用扫 `pattern`',
                 '`f[...] == -1` 表示前缀做不到，必须跳过，不能当成成本参与比较',
                 '规则按 `pattern` 长度排序，所以太长时可以直接 `break`',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行'],
    ),
)
