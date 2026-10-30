def _z(x):
    c = 0
    while x:
        c += x // 5
        x //= 5
    return c


CONFIG = dict(
    num=793, title='阶乘函数后K个零', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分 X · 统计因子 5',
    tags=['二分算法', '数学算法'],
    code='''
class Solution(object):
    def preimageSizeFZF(self, K):

        l = 0
        r = K * 5
        while l <= r:
            mid = (l + r) >> 1
            tmp = mid
            cnt = 0
            while tmp:
                cnt += tmp // 5
                tmp //= 5
            if cnt == K:
                return 5
            elif cnt > K:
                r = mid - 1
            else:
                l = mid + 1
        
        return 0
''',
    call='Solution().preimageSizeFZF(2)',
    expect=5,
    views=[
        dict(type='array', var=list(range(11)), label='候选 X（0 ~ 5K）：蓝 = l，粉 = r，黄 = mid', cell=76, h=230,
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'},
             dim=lambda S, i, v: 'l' in S and 'r' in S and not (S['l'] <= i <= S['r']),
             color=lambda S, i, v: 'yellow' if S.get('mid') == i else None),
        dict(type='text', size=28, fn=lambda S: (
            f"`{S['mid']}!` 末尾零的个数 = `{S['mid']}//5 + {S['mid']}//25 + ...` = =={_z(S['mid'])}==" if 'mid' in S else '')),
        dict(type='text', size=28, fn=lambda S: (
            f"累计 `cnt = {S['cnt']}`，当前还要除 5 的数 `tmp = {S['tmp']}`" if 'tmp' in S and S.get('tmp') is not None else '')),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), 'tmp', ('cnt', 'cnt', 'green'), ('K', 'K', 'orange')],
    captions={
        'r = K * 5': '末尾零不少于 K 个，X 不会超过 `5K`：二分区间 `[{l}, {r}]`',
        'mid = (l + r)': '取中点 `mid = ({l} + {r}) >> 1`，得 =={mid}==：算 `{mid}!` 末尾有几个零',
        'tmp = mid': '`tmp = mid`：下面不断除以 5，统计因子 5 的个数',
        'cnt = 0': '`cnt = 0`：累计 `mid!` 里因子 5 的个数',
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp}` 不为 0 → 继续统计' if S.tmp else f'`tmp` 变成 0 → `{S.mid}!` 末尾共 =={S.cnt}== 个零'),
        'cnt += tmp': '`cnt += {B.tmp} // 5`：[1..{mid}] 里每多一层 5 的倍数就多一个因子 5 → `cnt = {cnt}`',
        'tmp //= 5': '`tmp = {tmp}`：继续数 25、125 的倍数多出来的因子',
        'if cnt == K': lambda S, B, r: (f'`cnt = {S.cnt} == K = {S.K}` → ==找到了一个 X==，X 到 X+4 共 5 个都满足' if S.cnt == S.K
                                        else f'`cnt = {S.cnt} != K = {S.K}`，继续判断大小'),
        'elif cnt > K': lambda S, B, r: (f'`cnt = {S.cnt} > K = {S.K}`：零太多，X 太大 → 走 `r = mid - 1`' if S.cnt > S.K
                                         else f'`cnt = {S.cnt} < K = {S.K}`：零不够，X 太小 → 走 else'),
        'r = mid - 1': '零太多，丢掉右半边：`r` → {r}',
        'l = mid + 1': '零不够，丢掉左半边：`l` → {l}',
        'return 5': '存在 X 使得 `X!` 恰有 K 个零 → 答案是 ==5==（X ~ X+4）',
        'return 0': '二分结束都没有命中 K → 没有这样的 X，答案 ==0==',
    },
    skip=['cnt = 0', 'tmp = mid'],
    cards=dict(
        one_liner='X! 末尾零数只在 5 的倍数处增加，二分找有没有恰好 K 个',
        complexity='时间 `O(log^2 K)`，空间 `O(1)`',
        problem=['`f(x)` 是 `x!` 末尾零的个数。给定 `K`，问有多少个非负整数 `x` 满足 `f(x) = K`',
                 '示例：`K = 0` → `5`（0! ~ 4!）；`K = 5` → `0`',
                 '本视频：`K = 2` → `5`（10! ~ 14!）'],
        quote='若X是5的倍数，那么X！末尾零的数量与(X + 1)！、(X + 2)！、(X + 3)！、(X + 4)！末尾零的数量一样多。',
        quote_src='—— yiduobo 题解原文',
        idea=['末尾零个数 = 因子 5 的个数，对 X 不断除以 5 累加',
              '答案只有 0 或 5：存在就是 5（X 到 X+4），不存在就是 0',
              'X 越大零越多，==单调==，直接二分 X；命中 K 就返回 5'],
        summary=['时间 `O(log^2 K)`：二分 `log K` 次，每次数因子 `log X` 步',
                 '上界取 `5K` 就够：`5K!` 的零至少 K 个',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`tmp / 5` → `tmp // 5`，`tmp /= 5` → `tmp //= 5`）',
                 '同类题：172. 阶乘后的零'],
    ),
)
