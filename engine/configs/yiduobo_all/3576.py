def _top(S):
    if 'target' not in S:
        return ''
    t = S['target']
    s = f'代码里的 `target = {t}`：==两两配对翻掉所有 `{t}`，最终全变 `{-t}`=='
    if 'need' in S:
        s += f"｜已花 `{S['need']}` / `{S['k']}`"
    return s


def _clr(S, i, v):
    if 'p' not in S or 'target' not in S:
        return None
    if i == S['p']:
        return 'blue'
    if i == S.get('q', -9) and S['q'] > S['p']:
        return 'pink'
    return None


CONFIG = dict(
    num=3576, title='数组元素相等转换', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='双指针配对 · 代价 q−p',
    tags=['灵神题单', '贪心与思维', '难度分 1489'],
    code='''
class Solution(object):
    def canMakeEqual(self, nums, k):
        
        def check(target):
            p = 0
            need = 0
            while p < len(nums):
                while p < len(nums) and nums[p] != target:
                    p += 1
                if p == len(nums):
                    return True
                
                q = p + 1
                while q < len(nums) and nums[q] != target:
                    q += 1
                
                if q == len(nums):
                    return False
                
                need += q - p
                if need > k:
                    return False
                p = q + 1

            return True
    
        return check(1) or check(-1)
''',
    call='Solution().canMakeEqual([1,-1,1,-1,1], 3)',
    expect=True,
    views=[
        dict(type='text', fn=_top, h=70, size=26),
        dict(type='array', var='nums', pointers={'p': 'blue', 'q': 'pink'}, h=260, color=_clr),
    ],
    watch=[('target', 'target', 'cyan'), ('p', 'p', 'blue'), ('q', 'q', 'pink'), ('need', 'need', 'orange')],
    captions={
        'p = 0': '`p` 从左往右找“要被翻掉”的数',
        'need = 0': '`need` 累计已用操作次数',
        'while p < len(nums):': '还没扫完，继续找下一对',
        'while p < len(nums) and nums[p] != target': '`p` 向右跳过不是 `target` 的数，停在第一个 `target`：`p = {p}`',
        'if p == len(nums)': lambda S, B, r: ('`p` 走到末尾，没有要处理的数了 → ==可行==' if S.p == len(S.nums) else '`p` 还在数组内，继续配对'),
        'q = p + 1': '从 `p` 右边开始找第二个，`q = {q}`',
        'while q < len(nums) and nums[q] != target': '`q` 向右找下一个 `target`：`q = {q}`',
        'if q == len(nums)': lambda S, B, r: ('只找到 `p` 找不到 `q`，没人能配对 → ==不可行==' if S.q == len(S.nums) else f'找到配对：`p = {S.p}`，`q = {S.q}`'),
        'need += q - p': '用 `q − p = {q - p}` 次操作把 `p` 到 `q` 一路接力翻转：`need = {need}`',
        'if need > k': lambda S, B, r: (f'`need = {S.need} > k = {S.k}`：次数不够 → ==不可行==' if S.need > S.k else f'`need = {S.need} <= k = {S.k}`：次数够用'),
        'p = q + 1': '这一对处理完，`p` 跳到 `q + 1 = {p}`',
        'return False': '这个 `target` 不可行',
        'return True': '==这个 `target` 可行==',
        'return check': '两个方向各检查一次',
    },
    cards=dict(
        one_liner='两个要翻的位置配成一对，代价就是它们的距离',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组只含 `1` 和 `-1`，一次操作把相邻两数同时乘 `-1`',
                 '最多 `k` 次，能否让所有元素相等',
                 '示例：`[1,-1,1,-1,1], k=3` → `true`'],
        quote='使用t次操作修改nums[index]以及nums[index + t]。',
        quote_src='—— yiduobo 题解原文',
        idea=['连续操作 `t` 次，能同时翻转相距 `t` 的两个位置，中间的数翻两次不变',
              '不真改数组：`p` 找第一个要翻的，`q` 找第二个，花 `q − p`',
              '凑不成对、或总花费超过 `k`，就不可行'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '要翻的数必须成对出现，落单就失败',
                 '代码里的 `target` 是“要被翻掉的那种数”，所以 `check(1)` 对应全变 `-1`，两个方向都要试',
                 '对比灵神：灵神逐位贪心加 mul 标记；yiduobo 把操作合并成配对的距离'],
    ),
)
