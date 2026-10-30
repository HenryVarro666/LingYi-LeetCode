def _ix(S):
    i = S.get('index')
    return i if isinstance(i, int) and i < len(S['fi']) else None


def _info(S):
    f = S.get('f')
    if f is None:
        return '用 `f[state]` 统计前缀：0 中间 · 1 贴下界 · 2 贴上界 · 3 同时贴两边'
    return ('==f==：' + ' · '.join(f'`f[{k}]={f[k]}`' for k in range(4)) + '\n'
            '0 = 在 start 和 finish 之间，1 = 贴下界，2 = 贴上界，3 = 两边都贴')


CONFIG = dict(
    num=2999, title='统计强大整数的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP · 4 种上下界状态 + 滚动数组',
    tags=['灵神题单', '数位 DP', '难度分 2351'],
    code='''
class Solution(object):
    def numberOfPowerfulInt(self, start, finish, limit, s):

        fi = str(finish)
        n = len(fi)
        st = str(start)
        st = '0' * (n - len(st)) + st

        f = [0, 0, 0, 1]
        for index in range(n - len(s)):
            g = f[:]
            f = [0, 0, 0, 0]

            for v in range(limit + 1):
                if v == int(st[index]):
                    if v == int(fi[index]):
                        f[1] += g[1]
                        f[2] += g[2]
                        f[3] += g[3]
                    else:
                        f[1] += g[1]
                        f[1] += g[3]
                elif v == int(fi[index]):
                    f[2] += g[2]
                    f[2] += g[3]
                
                f[0] += g[0]
                if int(st[index]) < v:
                    f[0] += g[1]
                if v < int(fi[index]):
                    f[0] += g[2]
                if int(st[index]) < v < int(fi[index]):
                    f[0] += g[3]

        l_flag = u_flag = False
        if st[-len(s):] <= s:
            l_flag = True
        if fi[-len(s):] >= s:
            u_flag = True

        res = f[0]
        if l_flag:
            res += f[1]
        if u_flag:
            res += f[2]
        if l_flag and u_flag:
            res += f[3]
        
        return res
''',
    call='Solution().numberOfPowerfulInt(15, 215, 6, "10")',
    expect=2,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='string', var='fi', label='finish = 215（蓝箭头 = 正在填的前缀位 index）', pointers={_ix: 'blue'},
             pointer_labels={_ix: 'index'}, cell=70, h=190),
        dict(type='string', var='st', label='start = 15，补前导 0', pointers={_ix: 'pink'},
             pointer_labels={_ix: 'index'}, cell=70, h=190),
        dict(type='array', var='f', label='f[0..3]（本轮新的状态计数）', cell=90, h=170),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'orange'), ('l_flag', 'l_flag', 'cyan'),
           ('u_flag', 'u_flag', 'pink'), ('res', 'res', 'green')],
    skip=[5, 6, 12],
    max_steps=56,
    captions={
        'fi = str': '`finish` 转成字符串 `fi = {fi!r}`，长度 `n = {len(fi)}`',
        "st = '0'": '`start` 左边补 0 成 `{st!r}`，和 `fi` 对齐',
        'f = [0, 0, 0, 1]': '空前缀：既贴着 `start` 又贴着 `finish` → 只有 `f[3] = 1`',
        'for index in range': '`s` 占后 `{len(s)}` 位，只需构造前 `{n - len(s)}` 位前缀；`index` = {index}',
        'g = f[:]': '`g` 保存上一轮状态；`f` 马上清零，重新算这一位',
        'for v in range': '这一位的数字 `v` 从 0 枚举到 `limit = {limit}`，当前 `v = {v}`',
        'if v == int(st[index])': lambda S, B, r: f'`v = {S.v}` 和下界这一位 `{S.st[S.index]}` {"相等 → 可以继续贴下界" if S.v == int(S.st[S.index]) else "不相等"}',
        'if v == int(fi[index])': lambda S, B, r: f'`v = {S.v}` 和上界这一位 `{S.fi[S.index]}` {"相等" if S.v == int(S.fi[S.index]) else "不相等"}',
        'elif v == int(fi[index])': lambda S, B, r: f'`v = {S.v}` 不是下界位，再看是不是上界位 `{S.fi[S.index]}`：{"是 → 可以继续贴上界" if S.v == int(S.fi[S.index]) else "不是"}',
        'f[1] += g[1]': '继续贴下界：上一轮贴下界，`v` 恰好等于下界这一位 → `f[1] += g[1]`',
        'f[1] += g[3]': '上一轮两边都贴，`v` 等于下界位但小于上界位 → 只剩贴下界 → `f[1] += g[3]`',
        'f[2] += g[2]': '继续贴上界：上一轮贴上界，`v` 恰好等于上界这一位',
        'f[2] += g[3]': '上一轮两边都贴，`v` 等于上界位但大于下界位 → 只剩贴上界 → `f[2] += g[3]`',
        'f[3] += g[3]': '两边这一位相同且 `v` 等于它 → 仍然两边都贴',
        'f[0] += g[0]': '没压线的前缀：`v` 随便填都在范围内 → `f[0] += g[0]`',
        'f[0] += g[1]': '`v` 大于下界位：脱离下界，进入中间状态 → `f[0] += g[1]`',
        'f[0] += g[2]': '`v` 小于上界位：脱离上界，进入中间状态 → `f[0] += g[2]`',
        'f[0] += g[3]': '`v` 严格在两边界位之间：同时脱离 → `f[0] += g[3]`',
        'l_flag = u_flag': '前缀构造完了，接下来看后缀 `s` 能不能贴边',
        'if st[-len(s):] <= s': lambda S, B, r: f'`start` 的后缀 `{S.st[-len(S.s):]}` ≤ `s = {S.s}`？{"是 → 前缀压着下界也没问题" if S.st[-len(S.s):] <= S.s else "否 → 压下界的前缀会让数小于 start"}',
        'if fi[-len(s):] >= s': lambda S, B, r: f'`finish` 的后缀 `{S.fi[-len(S.s):]}` ≥ `s = {S.s}`？{"是 → 前缀压着上界也没问题" if S.fi[-len(S.s):] >= S.s else "否 → 压上界的前缀会让数超过 finish"}',
        'res = f[0]': '没压线的前缀拼上 `s` 一定在范围内 → `res = f[0] = {f[0]}`',
        'res += f[1]': '`l_flag` 成立：压下界的前缀也能用 → `res += f[1]`，得 {res}',
        'res += f[2]': '`u_flag` 成立：压上界的前缀也能用 → `res += f[2]`，得 {res}',
        'res += f[3]': '两个后缀条件同时成立 → `res += f[3]`，得 {res}',
        'return res': '强大整数一共 `{res}` 个',
    },
    cards=dict(
        one_liner='只构造前缀；后缀 s 固定，最后再看 s 能不能贴边',
        complexity='时间 `O(n · limit)`，空间 `O(1)`',
        problem=['正整数 `x` 以字符串 `s` 结尾，且每个数位都 `≤ limit`，称为强大整数',
                 '求 `[start, finish]` 内强大整数的个数',
                 '示例：`start=15, finish=215, limit=6, s="10"` → `2`（110 和 210）'],
        quote='当state为0时，表示当前构造的前index位处于上界和下界前index位之间；当state为1时，表示与下界的前index位相同，但是小于上界的前index位……',
        quote_src='—— yiduobo 题解原文',
        idea=['`s` 固定在末尾，数位 DP 只需要构造前 `n - len(s)` 位前缀',
              '`f[0..3]`：前缀不压线 / 压下界 / 压上界 / 同时压，滚动数组一轮一轮更新',
              '最后看 `s` 与 `start`、`finish` 的后缀关系，决定压线的状态能不能算进答案'],
        summary=['时间 `O(n · limit)`，空间 `O(1)`（滚动数组）',
                 '后缀判断：`st` 后缀 `<= s` 才允许压下界，`fi` 后缀 `>= s` 才允许压上界',
                 '易错点：压线状态 3 要同时满足两个后缀条件才能计入',
                 '对比灵神：灵神用递归记忆化逐位贴边界，yiduobo 把贴边关系压成 4 个状态递推'],
    ),
)
