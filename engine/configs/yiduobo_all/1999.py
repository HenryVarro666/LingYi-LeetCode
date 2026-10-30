def _cand(S):
    c = S.get('candidate')
    if c is None:
        return ''
    tail = '、'.join(str(x) for x in c[-6:])
    return f"已生成 ==%d== 个候选，最近加入：`{tail}`" % len(c) if c else '还没有候选'


def _scan(S):
    if 'v' not in S or S['_line'] < 21:
        return ''
    k = S['k']
    return f"检查 `v = {S['v']}`：`v > {k}` 为 {S['v'] > k}，`v % {k} = {S['v'] % k}`"


CONFIG = dict(
    num=1999, title='最小的仅由两个数组成的倍数', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='dfs 生成全部候选 + 排序检查',
    code='''
class Solution(object):
    def findInteger(self, k, digit1, digit2):

        candidate = []

        def generate(now):
            if now > 2147483647:
                return
            
            candidate.append(now)
            if now > 0:
                generate(now * 10 + digit1)
                generate(now * 10 + digit2)
        

        generate(digit1)
        generate(digit2)

        for v in sorted(candidate):
            if v > k and v % k == 0:
                return v
        
        return -1
''',
    call='Solution().findInteger(3, 1, 2)',
    expect=12,
    views=[
        dict(type='calls', label='generate 调用栈（now = 当前构造出的数）', h=300),
        dict(type='text', fn=_cand, h=70),
        dict(type='text', fn=_scan, h=70),
    ],
    watch=[('k', 'k', 'blue'), ('digit1', 'digit1', 'cyan'), ('digit2', 'digit2', 'pink'), ('now', 'now', 'yellow'), ('v', 'v', 'green')],
    max_steps=46, max_events=40000,
    captions={
        'candidate = []': '`candidate` 收集所有仅由 `digit1`、`digit2` 组成、不超过 2^31-1 的数',
        'if now > 2147483647': '`now = {now}`：{"超过 2^31 - 1，不再往下生成" if now > 2147483647 else "没超过 int 上限，可以收下"}',
        'candidate.append(now)': '把 `{now}` 加入候选，共 `{len(candidate)}` 个',
        'if now > 0': '`now = {now}`：{"大于 0 才继续接下一位；若是 0 再接就会出现多余的前导 0" if now > 0 else "now 是 0，不再扩展，避免生成带前导 0 的数"}',
        'generate(now * 10 + digit1)': '在 `{B.now}` 后面接 `digit1 = {digit1}`，得到 `{B.now * 10 + digit1}`，进入下一层 dfs',
        'generate(now * 10 + digit2)': '在 `{B.now}` 后面接 `digit2 = {digit2}`，得到 `{B.now * 10 + digit2}`，进入下一层 dfs',
        'generate(digit1)': '从 `digit1 = {digit1}` 开始 dfs，一路把能构造的数都收进来',
        'generate(digit2)': '再从 `digit2 = {digit2}` 开始 dfs',
        'for v in sorted(candidate)': '候选从小到大排序，逐个检查：`v = {v}`',
        'if v > k and v % k == 0': '`v = {v}`：`v > {k}` 且 `v % {k} = {v % k}`，{"满足 → 就是最小的倍数" if v > k and v % k == 0 else "不满足，看下一个"}',
        'return v': '最小的合法倍数是 `{v}`',
        'return -1': '所有候选都不满足 → 返回 `-1`',
    },
    cards=dict(
        one_liner='数位只有两种：dfs 把所有候选数全造出来再排序',
        complexity='时间 `O(2^L × L)`（L 约 10 位），空间 `O(2^L)`',
        problem=['给整数 `k`、两个数字 `digit1`、`digit2`，找最小的整数：大于 `k`、是 `k` 的倍数、每一位只能是这两个数字之一',
                 '答案必须在 `[0, 2^31 - 1]` 内，没有就返回 `-1`',
                 '本视频：`k = 3`，`digit1 = 1`，`digit2 = 2` → `12`'],
        quote='完全可以一趟dfs，构造出所有大小在0到2^31 - 1之间且仅由这两个数字构成的数字，然后将这些数排序后逐个检测是否大于k且是k的倍数。',
        quote_src='—— yiduobo 题解原文',
        idea=['数字不超过 2^31，最多 10 位，每位 2 种选择，候选总共只有约两千个',
              'dfs：当前数 `now` 后面接 `digit1` 或 `digit2`，超过上限就返回',
              '注意 `now` 为 0 时不再扩展，避免多余的前导 0'],
        summary=['时间 `O(2^L × L)`，L = 10；空间 `O(2^L)`',
                 '易错点：==digit 可能是 0==，`now > 0` 才继续扩展，否则会无限接 0 或出现前导 0',
                 '上限用 `2147483647`，超过就直接返回',
                 '演示里候选很多，中间的 dfs 步骤被快进，最后排序后第一个满足条件的就是答案',
                 '原文本身可在 Python 3 运行，未做修改'],
    ),
)
