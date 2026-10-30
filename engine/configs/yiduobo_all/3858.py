def _ok(S, i, j, v):
    if 'd' not in S or 'res' not in S:
        return None
    return 'green' if (((v >> S['d']) << S['d']) | S['res']) == S['res'] and (v & (1 << S['d'])) == 0 else 'red'


CONFIG = dict(
    num=3858, title='按位或的最小值', difficulty='Medium', category='位运算',
    author='yiduobo', technique='高位到低位逐位判断',
    tags=['灵神题单·位运算', '难度分 1947'],
    code='''
class Solution(object):
    def minimumOR(self, grid):
        
        res = 0
        for d in range(16, -1, -1):
            flag = True
            for r in grid:
                row_flag = False
                for v in r:
                    if ((v  >> d << d) | res) == res and (v & (1 <<d)) == 0:
                        row_flag = True
                        break
                
                if not row_flag:
                    flag = False
                    break
            
            if not flag:
                res |= (1 << d)
        
        return res
''',
    call='Solution().minimumOR([[3, 5], [6, 4]])',
    expect=5,
    views=[
        dict(type='grid', var='grid', h=240, cell=96, label='grid（绿 = 第 d 位为 0 且高位没有多余的 1，红 = 不可用）', color=_ok),
        dict(type='text', size=34, fn=lambda S: f"`res = {S['res']:05b}`   （第 {S['d']} 位正在判断）" if 'res' in S and 'd' in S else (f"`res = {S['res']:05b}`" if 'res' in S else '')),
        dict(type='text', size=32, fn=lambda S: (f"`v = {S['v']:05b}`  把低 {S['d']} 位清零 = `{(S['v'] >> S['d']) << S['d']:05b}`  `| res = {((S['v'] >> S['d']) << S['d']) | S['res']:05b}`") if 'v' in S and 'd' in S and 'res' in S and S['v'] < 32 else ''),
    ],
    watch=[('d', 'd', 'cyan'), ('flag', 'flag', 'yellow'), ('row_flag', 'row_flag', 'pink'), ('v', 'v', 'blue'), ('res', 'res', 'green')],
    skip=['flag = True', 'flag = False', 'for r in grid', 'for v in r', 'if not row_flag', 'for d in range', 'if not flag', 'break'],
    captions={
        'res = 0': '`res` 是答案，先全填 0（越小越好）',
        'for d in range': lambda S, B, r: (f'从高位往低位判断：第 `{S.d}` 位能不能是 0（`grid` 元素不超过 10^5，答案必小于 2^17）' if not (S.d == 0 and B.d == 0) else '所有位都判断完了'),
        'if ((v': lambda S, B, r: (f'`v = {S.v}`：第 `{S.d}` 位以上没有 `res` 没有的 1，且第 `{S.d}` 位是 0 → ==可用==，这一行满足' if (((S.v >> S.d) << S.d) | S.res) == S.res and (S.v & (1 << S.d)) == 0 else f'`v = {S.v}`：要么高位有 `res` 没有的 1，要么第 `{S.d}` 位是 1 → ==不可用=='),
        'break': '这一行有可用元素，看下一行（若是不可用整行，则这一位判为 1）',
        'res |=': '有一行里找不到可用元素 → 第 `{d}` 位必须是 1：`res = {res:b}`',
        'return': '得到最小按位或 `res = {res}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='按位或要最小，就让高位尽量为 0，一位一位试',
        complexity='时间 `O(mn log U)`，空间 `O(1)`',
        problem=['`grid` 每行恰好选一个整数，求这些整数按位或的最小值，元素不超过 `10^5`',
                 '本视频：`[[3,5],[6,4]]` → `5`'],
        quote='对于当前位d，判断每一行中是否至少存在一个元素，在满足在第d + 1到第15位上不存在当前答案中不具备的1的前提下，在第d位为0。若满足，那么答案的第d位就为0，否则为1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`10^5 < 2^17`，从第 16 位往下判断',
              '`(v >> d << d) | res == res`：v 在第 d 位及以上没有 res 里没有的 1',
              '`v & (1 << d) == 0`：第 d 位自己也要是 0；每行都有这样的 v，才能填 0'],
        summary=['时间 `O(mn log U)`，空间 `O(1)`',
                 '`v >> d << d` 把低于第 d 位清零，低位不影响这一轮判断',
                 '==已经为 1 的高位==：元素这一位是 0 或 1 都行，所以只检查 res 为 0 的位',
                 '原文从 16 位开始，多一位无害；灵神用 `mx.bit_length()` 缩小起点',
                 '和灵神的 `(x | mask) == mask` 是同一个子集判断，写法不同'],
    ),
)
