def _cand(S):
    return 'candidate' in S and 'x' in S


def _t1(S):
    if 'candidate' not in S:
        return '从 2n 位的 `9999…9` 往下找回文数'
    return f"candidate = `{S['base']}` − `{S['delta_num']}` = =={S['candidate']}=="


def _t2(S):
    if 'candidate' not in S or 'x' not in S or 'flag' not in S:
        return ''
    c, x = S['candidate'], S['x']
    if x * x < c:
        return f"`x×x = {x*x}` < {c}：x 再大也凑不出，这个候选放弃"
    return f"试乘数 `x = {x}`：`{c} % {x} = {c % x}`" + ('  ==整除，找到==' if c % x == 0 else '  不整除')


CONFIG = dict(
    num=479, title='最大回文数乘积', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='枚举回文数 + 试除',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def largestPalindrome(self, n):

        if n == 1:
            return 9

        

        #if n % 2 == 0:
        #    return (10 ** n - 1) * (10 ** n - 10 ** (n/2) + 1) % 1337

        base = 10 ** (n + n) - 1
        max = 10 ** n - 1
        delta = 1
        while True:
            tmp = delta_num = delta
            delta += 1
            l = 0
            while tmp:
                l += 1
                delta_num = delta_num * 10 + tmp % 10
                tmp //= 10
            delta_num *= 10 ** (n - l)
            candidate = base - delta_num

            x = max
            flag = 0
            while x * x >= candidate:
                if candidate % x == 0:
                    return candidate % 1337
                if flag == 0:
                    x -= 2
                    flag = 1
                elif flag == 1:
                    x -= 4
                    flag = 2
                elif flag == 2:
                    x -= 2
                    flag = 3
                else:
                    x -= 2
                    flag = 0
''',
    call='Solution().largestPalindrome(2)',
    expect=987,
    views=[
        dict(type='text', fn=_t1, size=34),
        dict(type='string', var=lambda S: str(S['candidate']) if 'candidate' in S else '', label='候选回文数 candidate', h=170),
        dict(type='text', fn=_t2, size=32),
        dict(type='text', fn=lambda S: (f"下一次 x 减 {[2, 4, 2, 2][S['flag']]}：个位依次 9→7→3→1 轮转" if 'flag' in S else ''), size=26),
    ],
    skip=['delta += 1', 'l = 0', 'flag = 0', 'flag = 1', 'flag = 2', 'flag = 3', 'if flag =='],
    max_steps=44,
    watch=['delta', 'delta_num', 'candidate', 'x', 'flag'],
    captions={
        'if n == 1': 'n = 1 单独处理：`9 × 1` 的最大回文是 ==9==',
        'base = ': '`base` = 2n 位全 9 = `{base}`，乘积最大不超过它',
        'max = ': '`max` = 最大的 n 位数 `{max}`，乘数从它往下试',
        'delta = 1': '`delta` 从 1 起，决定从 base 里减去哪个回文数',
        'tmp = delta_num = delta': '取出 `delta = {delta}`，准备把它镜像成回文',
        'delta += 1': '`delta` 先加一，留给下一轮：{delta}',
        'l = 0': '`l` 记 delta 的位数',
        'while tmp': lambda S, B, r: ('`tmp = ' + str(S.tmp) + '` 非 0：还有位没镜像' if S.tmp else '`tmp = 0`：delta 的每一位都镜像完了'),
        'l += 1': '位数 `l` → {l}',
        'delta_num = delta_num * 10': '把 delta 的末位接到后面：`delta_num` → {delta_num}（做成回文）',
        'tmp //= 10': '去掉末位：`tmp` → {tmp}',
        'delta_num *= 10': '补零对齐：`delta_num` → =={delta_num}==（形如 1100…00 的回文差）',
        'candidate = base': '`candidate = {base} − {delta_num}` = =={candidate}==，它一定是回文',
        'x = max': '`x` 从最大的 n 位数 `{x}` 开始往下找因子；`flag` 控制步长，只试个位为 9/7/3/1 的数',
        'while x * x >= candidate': lambda S, B, r: (f'`x×x = {S.x*S.x} ≥ {S.candidate}`：x 还可能是较大的那个因子，继续试' if S.x * S.x >= S.candidate
                                                      else f'`x×x = {S.x*S.x} < {S.candidate}`：两个因子都 ≤ x，乘积不可能是它 → 换下一个回文'),
        'if candidate % x == 0': lambda S, B, r: (f'`{S.candidate} % {S.x} = 0` → 整除！另一个因子 `{S.candidate // S.x}`' if S.candidate % S.x == 0
                                                   else f'`{S.candidate} % {S.x} = {S.candidate % S.x}` ≠ 0：不是因子'),
        'return candidate % 1337': '`{candidate}` 就是最大回文乘积，题目要 `% 1337` = =={ret}==',
        'x -= 2': '`x -= 2` → {x}（换下一个个位为 9/7/3/1 的数）',
        'x -= 4': '`x -= 4` → {x}（跳过个位为 5 的数）',
    },
    cards=dict(
        one_liner='最大回文一定接近 2n 个 9：从上往下逐个枚举，再试除',
        complexity='时间 约 `O(10^n)`（暴力），空间 `O(1)`',
        problem=['求两个 `n` 位整数乘积中==最大的回文数==，结果对 `1337` 取余',
                 '示例：`n = 2` → 最大是 `9009 = 99 × 91`，`9009 % 1337 = 987`',
                 '本视频：`n = 2`，返回 `987`'],
        quote='首先，两个n位数的乘积最多为2n位，那么最大可能的回文数就是9999...999一共2n个9，此时就是999..998899.999，接下来是999..997799..999。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘积至多 `2n` 位，所以最大回文从 `99…9`（2n 个 9）往下枚举',
              '每次减去的数本身也是回文：`1100…0`、`2200…0`……用 `delta` 镜像构造',
              '对每个候选，用 n 位的 `x`（从大到小，个位只取 9/7/3/1）试除'],
        summary=['原文为 Python 2 写法，`tmp /= 10` 已改为 `tmp //= 10`',
                 '`x * x >= candidate` 是剪枝：x 不能比两个因子里较小的那个还小',
                 'n=1 要单独返回 9；`max` 变量名遮住了内置函数，别模仿',
                 '作者自己也说：没有证明上界，偶数 n 有公式但奇数 n 没找到',
                 '暴力解，n 到 8 才合理；很多人直接打表'],
    ),
)
