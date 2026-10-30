N, DELAY, FORGET = 6, 2, 4


def _txt(S):
    if 'index' not in S:
        return '`f[i]` = 到第 `i` 天==知道或曾经知道==秘密的总人数（忘记的人不减）'
    i, d, fo = S['index'], S['delay'], S['forget']
    return f'`f[{i}] = f[{i - 1}] + f[{i - d}] − f[{i - fo}]`' if i >= fo else (
        f'`f[{i}] = f[{i - 1}] + f[{i - d}]`（还没到 `forget` 天，没人可减）' if i >= d else f'`f[{i}] = f[{i - 1}]`（还没到 `delay` 天）')


def _col(S, j, v):
    if 'index' not in S or 'f' not in S:
        return None
    i = S['index']
    if j == i:
        return 'green'
    if S.get('_line') in (9, 10, 11, 12, 13) and j == i - S['delay'] and i >= S['delay']:
        return 'blue'
    if S.get('_line') in (13, 14, 15) and j == i - S['forget'] and i >= S['forget']:
        return 'pink'
    return None


CONFIG = dict(
    num=2327, title='知道秘密的人数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='线性递推 · f 记“曾经知道”的总人数',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def peopleAwareOfSecret(self, n, delay, forget):

        mod = 10 ** 9 + 7
        f = [0, 1]
        for index in range(2, n + 1):
            f.append(f[-1])
            if index >= delay:
                f[index] += f[index - delay]
                if f[index] >= mod:
                    f[index] -= mod
                if index >= forget:
                    f[index] -= f[index - forget]
                    if f[index] < 0:
                        f[index] += mod
                

        res = f[n]
        if n >= forget:
            res -= f[n - forget]
            if res < 0:
                res += mod
        
        return res
''',
    call=f'Solution().peopleAwareOfSecret({N}, {DELAY}, {FORGET})',
    expect=5,
    views=[
        dict(type='text', fn=_txt, size=28, h=80),
        dict(type='array', var='f', label='f[i]（绿 = 正在算的 i，蓝 = f[i−delay]（+），粉 = f[i−forget]（−））', cell=96,
             pointers={'index': 'blue'}, color=_col, h=300),
        dict(type='text', fn=lambda S: '样例：到各天为止曾经知道的人 A、A、AB、ABC、ABCD、ABCDEF → `f` = 1、1、2、3、4、6', size=24, h=70),
    ],
    watch=['index', 'delay', 'forget', ('res', 'res', 'green')],
    skip=['mod =', 'if f[index] >= mod', 'f[index] -= mod', 'if f[index] < 0', 'f[index] += mod', 'if res < 0', 'res += mod'],
    captions={
        'f = [0, 1]': '`f[0] = 0`，`f[1] = 1`：第 1 天只有一个人 A',
        'for index in range': lambda S, B, r: (f'算第 `index = {S.index}` 天' if S.index != B.get('index') else '推到第 `n` 天，循环结束'),
        'f.append(f[-1])': '先继承昨天的人数：`f[{index}] = f[{index - 1}]` = {f[index]}',
        'if index >= delay': lambda S, B, r: (f'`index = {S.index} ≥ delay = {S.delay}`：已经有人到了分享的日子' if S.index >= S.delay
                                              else f'`index = {S.index} < delay = {S.delay}`：还没人能分享，`f` 不变'),
        'f[index] += f[index - delay]': '`f[{index - delay}]` 里的人都满 `delay` 天，今天各分享一个新人：`f[{index}]` += {f[index-delay]} → =={f[index]}==',
        'if index >= forget': lambda S, B, r: (f'`index = {S.index} ≥ forget = {S.forget}`：有人今天忘记了，要修正' if S.index >= S.forget
                                               else f'`index = {S.index} < forget = {S.forget}`：还没人忘记，不用减'),
        'f[index] -= f[index - forget]': '`f[{index - forget}] = {f[index-forget]}` 里的人今天已经忘记，不能分享 → 上一步多算的新人要扣掉：`f[{index}]` −= {f[index-forget]} → =={f[index]}==',
        'res = f[n]': '`f[n] = {f[n]}`：到第 `n` 天知道过秘密的总人数',
        'if n >= forget': lambda S, B, r: (f'`n = {S.n} ≥ forget = {S.forget}`：`f[n−forget] = {S.f[S.n - S.forget]}` 里的人今天都忘记了' if S.n >= S.forget
                                           else '`n < forget`：没人忘记'),
        'res -= f[n - forget]': '减去已经忘记的人：`res = {B.res} − {f[n - forget]}` = =={res}==',
        'return res': '还记得秘密的人数 = =={ret}==',
    },
    cards=dict(
        one_liner='把 f 定义成“曾经知道”的总人数，递推式就不会重复扣人',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['第 1 天一个人发现秘密；发现后 `delay` 天起每天分享给一个新人，`forget` 天后忘记（忘记当天不能分享）',
                 '求第 `n` 天结束时还记得秘密的人数，结果对 `10^9+7` 取余',
                 '示例：`n = 6, delay = 2, forget = 4` → `5`'],
        quote='令 f[i] 表示到时刻 i，知道或曾经知道秘密的总人数。根据这个定义，就可以抛弃掉最后重复计算的这一项 f[i - forget]，得到 f[i] = f[i - 1] + f[i - delay] - f[i - forget]',
        quote_src='—— yiduobo 题解',
        idea=['兔子问题的老套路：`f[i]` 存活数 = 昨天 + 新生 − 死亡',
              '本题直接套会重复扣 `f[i − forget]`：忘记的人已经不在 `f[i−1]` 里了，却又被减一次',
              '换成==“曾经知道”的总数==：已忘记的人不从 `f` 里扣，最后用 `f[n] − f[n−forget]` 得到答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 风格写法，本代码已是 Python 3 可运行，无需改动',
                 '易错：递推式与兔子问题长得一样，但 `f` 的含义变了，最后要再减 `f[n−forget]`',
                 '代码里用加减 `mod` 代替取模，减法后可能为负，要补回 `mod`',
                 '同类：兔子生小兔子（斐波那契变形）'],
    ),
)
