def _t(S):
    I = S.get('_inner', {})
    if 'base_k' in I:
        k = S.get('k', '?')
        return f"十进制 `{I.get('num', '…')}`，`{k}` 进制低位在前 `{I['base_k']}`：前后对称就是镜像数字"
    if 'now' in I and 'target_l' in I:
        return f"半边 `now = {I['now']}`，要拼成长度 `{I['target_l']}` 的十进制回文数"
    return '枚举十进制回文数的半边 → 拼成整数 → 转 k 进制检查'


CONFIG = dict(
    num=2081, title='k 镜像数字的和', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='dfs 枚举半边 + 现场检查 k 进制',
    tags=['灵神题单·数学算法', '难度分 2210'],
    code='''
class Solution(object):
    def kMirror(self, k, n):

        def check(now, l, target_l):
            num = 0
            for index in range(target_l):
                if index < l:
                    num = num * 10 + now[index]
                else:
                    num = num * 10 + now[target_l - index - 1]
            
            base_k = []
            tmp = num
            while True:
                base_k.append(tmp % k)
                tmp //= k
                if tmp == 0:
                    break
            
            flag = True
            for index in range(len(base_k) // 2):
                if base_k[index] != base_k[len(base_k) - 1 - index]:
                    flag = False
                    break
            
            if flag:
                return num
            
            return 0

        def dfs(level, now, l, target_l):
            if level == l:
                check_res = check(now, l, target_l)
                if check_res > 0:
                    self.res += check_res
                    self.cnt += 1
                return
            
            for index in range(10):
                if index > 0 or level > 0:
                    now.append(index)
                    dfs(level + 1, now, l, target_l)
                    if self.cnt == n:
                        return
                    now.pop()

        l = 0
        self.cnt = 0
        self.res = 0
        while True:
            l += 1
            dfs(0, [], l, l + l - 1)
            if self.cnt == n:
                break
            dfs(0, [], l, l + l)
            if self.cnt == n:
                break

        return self.res
''',
    call='Solution().kMirror(3, 3)',
    expect=7,
    views=[
        dict(type='text', fn=_t, size=28, h=80),
        dict(type='array', var='now', label='now（十进制回文数的半边）', h=170),
        dict(type='array', var='base_k', label='base_k（k 进制，低位在前）', h=170),
        dict(type='calls', h=150),
    ],
    watch=['l', 'k', 'num', ('res', 'self.res', 'green'), ('cnt', 'self.cnt', 'yellow')],
    skip=['index < l:', 'num = num * 10 + now[index]', 'num = num * 10 + now[target_l - index - 1]', 'tmp //= k', 'if tmp == 0', 'break'],
    max_steps=72,
    captions={
        'dfs(0, [], l, l + l - 1)': '半边长度 `l = {l}`：先拼成==奇数长度== `{l+l-1}` 位的回文数（最后一位不复制）',
        'dfs(0, [], l, l + l)': '再拼成==偶数长度== `{l+l}` 位的回文数（整个半边翻过去）',
        'if level == l': lambda S, B, r: (f"`level = {S.level}` 已填满 `{S.l}` 位 → 拼出完整数字去检查" if S.level == S.l else f"`level = {S.level} < l = {S.l}`：继续选下一位数字"),
        'check_res = check': '半边 `{now}` 翻过去得到十进制回文数，转 k 进制看是否也是回文',
        'for index in range(10)': '枚举这一位填 0~9',
        'if index > 0 or level > 0': '第一位不能是 0（没有前导零）：`index = {index}`，`level = {level}`',
        'now.append(index)': '这一位填 `{index}`：`now = {now}`',
        'now.pop()': '回溯：撤销这一位，试下一个数字',
        'base_k.append(tmp % k)': '`{num}` 的 {k} 进制低位：`{tmp} % {k}` → `base_k = {base_k}`',
        'if base_k[index] != base_k[len': lambda S, B, r: f"对称位置 `base_k[{S.index}] = {S.base_k[S.index]}` vs `base_k[{len(S.base_k)-1-S.index}] = {S.base_k[len(S.base_k)-1-S.index]}`：" + ('不相等 → 不是回文' if S.base_k[S.index] != S.base_k[len(S.base_k)-1-S.index] else '相等，继续'),
        'if flag': '`flag = {flag}`：{"k 进制也是回文 → 返回这个数" if flag else "k 进制不是回文 → 返回 0"}',
        'return num': '`{num}` 是 {k} 镜像数字',
        'return 0': '不是镜像数字，返回 0',
        'self.res += check_res': '累加：`res = {self.res}`',
        'self.cnt += 1': '已找到 `cnt = {self.cnt}` 个',
        'if self.cnt == n': '`cnt = {self.cnt}`，要凑 `n = {n}` 个：{"够了，提前结束" if self.cnt == n else "还不够，继续"}',
        37: '这个半边处理完，回到上一层 dfs',
        44: '凑够 n 个了，层层 return 往上退',
        'return self.res': '最小的 {n} 个 {k} 镜像数字之和 = =={self.res}==',
    },
    cards=dict(
        one_liner='枚举十进制回文数的半边，现场转 k 进制检查',
        complexity='打表思路，数据小，运行时间很短',
        problem=['十进制和 k 进制都是回文的正整数叫 k 镜像数字', '求最小的 n 个 k 镜像数字的和', '本视频：`k = 3, n = 3` → `1 + 2 + 4 = 7`'],
        quote='题目要求十进制数和k进制数都是回文数，那么可以枚举回文数的半边，然后翻转过去得到完整的回文数。',
        quote_src='—— yiduobo 题解原文',
        idea=['按半边长度 `l` 从小到大：数字越短越小，保证是从小到大找', '半边翻过去有两种：长度 `2l-1`（不复制末位）和 `2l`，先奇后偶才有序', 'dfs 填每一位（首位不为 0），拼好后转 k 进制比较头尾，凑够 n 个就停'],
        summary=['原文为 Python 2 写法，`/=`、`len(base_k) / 2` 已改为 `//=`、`//`', '作者提到先直接枚举十进制数会很慢，所以改为枚举半边', '数位检查只比较到一半：`len(base_k) // 2`', '对比灵神：灵神预处理出全部答案再查表；这里每次调用现场 dfs'],
    ),
)
