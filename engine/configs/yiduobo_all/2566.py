def _txt(S):
    if 'digits' not in S:
        return ''
    ma = S.get('ma'); mi = S.get('mi')
    a = f'最大 `ma` = =={ma}==' if ma is not None else ''
    b = f'最小 `mi` = =={mi}==' if mi is not None else ''
    return '　　'.join(x for x in (a, b) if x) or '两趟扫描：先找最大，再找最小'


CONFIG = dict(
    num=2566, title='替换一个数字后的最大差值', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='贪心 · 两次从高位扫描',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def minMaxDifference(self, num):

        digits = list(str(num))

        p = 0
        while p < len(digits) and digits[p] == '9':
            p += 1
        
        if p < len(digits):
            target = digits[p]       
            ma = int(str(num).replace(target, '9'))
        else:
            ma = num

        p = 0
        while p < len(digits) and digits[p] == '0':
            p += 1
        
        if p < len(digits):
            target = digits[p]
            mi = int(str(num).replace(target, '0'))
        else:
            mi = num
        
        return ma - mi
''',
    call='Solution().minMaxDifference(99517)',
    expect=99917 - 517,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='digits', label='digits（p = 当前扫描位置）', cell=90, h=200,
             pointers={'p': 'pink'},
             color=lambda S, i, v: 'yellow' if 'target' in S and v == S['target'] else None),
    ],
    watch=[('p', 'p', 'pink'), 'target', ('ma', 'ma', 'green'), ('mi', 'mi', 'blue')],
    captions={
        'digits = list': '把 `num` 拆成字符列表 `digits`',
        'p = 0': '从最高位 `p = 0` 开始扫描',
        'while p < len(digits) and digits[p] == \'9\'': lambda S, B, r: (
            f"`digits[{S.p}] = '{S.digits[S.p]}'` 已经是 9，换它没用 → 继续往低位走" if S.p < len(S.digits) and S.digits[S.p] == '9'
            else '碰到非 9（或到头）→ 停下'),
        "while p < len(digits) and digits[p] == '0'": lambda S, B, r: (
            f"`digits[{S.p}] = '0'` 已经是 0，换它没用 → 继续往低位走" if S.p < len(S.digits) and S.digits[S.p] == '0'
            else '碰到非 0（或到头）→ 停下'),
        'p += 1': '`p` → {p}',
        'if p < len': lambda S, B, r: ('找到了可替换的位' if S.p < len(S.digits) else '全是 9（或 0），没有可换的位'),
        'target = digits[p]': '要替换的数字 `target = {target}`',
        "ma = int": '把所有 `{target}` 换成 9 → ==ma = {ma}==，最高的非 9 位变大，收益最大',
        "mi = int": '把所有 `{target}` 换成 0 → ==mi = {mi}==，最高的非 0 位变小，收益最大',
        'ma = num': '全是 9，保持不变',
        'mi = num': '全是 0，保持不变',
        'return': '差值 `{ma} − {mi}` = =={ret}==',
    },
    cards=dict(
        one_liner='最高位的非 9 换成 9，最高位的非 0 换成 0',
        complexity='时间 `O(log num)`，空间 `O(log num)`',
        problem=['把 `num` 里某个数字整体替换成另一个数字（可以不变）',
                 '求替换后最大值与最小值的差',
                 '示例：`11891` → 最大 `99899`，最小 `890`，差 `99009`'],
        quote='为了使得替换后的数字最大，就应该将最高位上的非9的数字替换成9，而为了使得数字最小，则应该将最高位上的非0的数字替换成0。',
        quote_src='—— yiduobo 题解原文',
        idea=['从高位到低位扫两遍：第一遍跳过 9，第二遍跳过 0',
              '停下的那一位就是 `target`，用 `replace` 整体替换',
              '扫到头还没停，说明全是 9（或 0），保持原数'],
        summary=['时间 `O(log num)`，空间 `O(log num)`',
                 '`replace` 会替换所有相同数字，符合题意',
                 '最小值可有前导 0，`int` 会自动去掉',
                 '对比灵神：灵神最小值直接换首位，yiduobo 两趟写得对称'],
    ),
)
