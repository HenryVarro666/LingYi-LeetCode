def _txt(S):
    if 'num' not in S:
        return '`now` 是当前编号的数位和：先算 `lowLimit`，之后每个数由上一个数推出'
    if 'zero' not in S:
        return f"当前编号 ==`{S['num']}`=="
    if S['zero'] == 0:
        return f"`{S['num']}` 末尾不是 0 → 没有进位，数位和直接 +1"
    return f"`{S['num']}` 末尾有 `{S['zero']}` 个 0 → 上一个数末尾有 `{S['zero']}` 个 9 变成了 0"


CONFIG = dict(
    num=1742, title='盒子中小球的最大数量', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='枚举 + 增量推数位和',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def countBalls(self, lowLimit, highLimit):

        tmp = lowLimit
        now = 0
        while tmp:
            now += tmp % 10
            tmp //= 10
        
        cnt_dict = {now : 1}
        for num in range(lowLimit + 1, highLimit + 1):
            tmp = num
            zero = 0
            while tmp % 10 == 0:
                tmp //= 10
                zero += 1
            
            now = now - zero * 9 + 1
            cnt_dict[now] = cnt_dict.get(now, 0) + 1
        
        return max(cnt_dict.values())
''',
    call='Solution().countBalls(5, 15)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='map', var='cnt_dict', label='cnt_dict：数位和（盒子编号）→ 球数', fmt=lambda k, v: f'盒子 {k}：{v} 个', h=420),
    ],
    watch=[('num', lambda S: S.get('num'), 'blue'), ('zero', lambda S: S.get('zero'), 'orange'),
           ('now', 'now', 'pink')],
    captions={
        'tmp = lowLimit': '先单独算出 `lowLimit = {lowLimit}` 的数位和，作为递推起点',
        'now += tmp % 10': '取个位 `{B.tmp % 10}` 加进数位和：`now = {now}`',
        'tmp //= 10': '去掉个位：`tmp = {tmp}`',
        'cnt_dict = ': '`lowLimit` 自己落进盒子 `{now}`：`cnt_dict = {cnt_dict}`',
        'tmp = num': '处理下一个编号 `num = {num}`',
        'while tmp % 10 == 0': lambda S, B, r: (f'`tmp = {S.tmp}` 末尾是 0 → 统计进位的位数' if S.tmp % 10 == 0 else f'`tmp = {S.tmp}` 个位非 0，不再有进位'),
        'zero += 1': '末尾 0 数量 `zero = {zero}`',
        'now = now': '`x + 1` 的数位和 = 上一个数位和 `+1`，再减去每个 9 变 0 的损失：`now = {B.now} − {zero}×9 + 1` = =={now}==',
        'cnt_dict[now]': '编号 `{num}` 放进盒子 `{now}`，该盒子现有 `{cnt_dict[now]}` 个球',
        'return max': '各盒子球数的最大值 → ==`{ret}`==',
    },
    skip=['zero = 0', 'tmp = num'],
    cards=dict(
        one_liner='从 low 枚举到 high，用上一个数的数位和推下一个',
        complexity='时间 `O(high − low)` 均摊，空间 `O(D·log high)`',
        problem=['编号 `lowLimit` 到 `highLimit` 的球，放进「数位和」对应的盒子',
                 '返回球最多的盒子里的球数',
                 '示例：`5..15` → 盒子 5、6 各 2 个 → `2`'],
        quote='在没有出现进位的情况下，x + 1的数位和显然就等于x的数位和加1，而出现了进位时，则会有若干个9变成1的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x+1` 无进位：数位和 `+1`',
              '有进位：末尾 `zero` 个 9 变 0，每个少 9，再把进位的那位 `+1`',
              '数 `x+1` 末尾 0 的个数，就得到 `zero`，不用逐位重算'],
        summary=['时间约 `O(high − low)`，空间是哈希表大小',
                 '`now = now − zero×9 + 1`：先减进位损失，再加 1',
                 '原文为 Python 2 写法，整数除法 `/=` 已改为 `//=`',
                 '作者说明还有数位 DP（`O(log n)` 级）的做法，这里用朴素做法'],
    ),
)
