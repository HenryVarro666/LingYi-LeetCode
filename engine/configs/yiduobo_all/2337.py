def _info(S):
    if 'p1' not in S:
        return ''
    a, b = S['start'], S['target']
    p1, p2 = S['p1'], S['p2']
    x = a[p1] if p1 < len(a) else '（越界）'
    y = b[p2] if p2 < len(b) else '（越界）'
    return f"start[p1] = `{x}`　　target[p2] = `{y}`"


CONFIG = dict(
    num=2337, title='移动片段得到字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='双指针 · 各自跳过下划线再分类讨论',
    tags=['灵神题单', '难度分 1693'],
    code='''
class Solution(object):
    def canChange(self, start, target):

        p1 = p2 = 0
        while p1 < len(start) or p2 < len(target):
            while p1 < len(start) and start[p1] == '_':
                p1 += 1
            
            while p2 < len(target) and target[p2] == '_':
                p2 += 1

            if p1 < len(start):
                if p2 < len(target):
                    if start[p1] != target[p2]:
                        return False
                    
                    if start[p1] == 'L':
                        if p1 < p2:
                            return False
                    elif p1 > p2:
                        return False
                
                else:
                    return False
            
            elif p2 != len(target):
                return False
        
            p1 += 1
            p2 += 1

        return True
''',
    call='Solution().canChange("_L__R__R_", "L______RR")',
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='string', var='start', pointers={'p1': 'blue'}, label='start', h=150,
             color=lambda S, i, v: ('blue' if 'p1' in S and i == S['p1'] and v != '_' else None)),
        dict(type='string', var='target', pointers={'p2': 'pink'}, label='target', h=150,
             color=lambda S, i, v: ('pink' if 'p2' in S and i == S['p2'] and v != '_' else None)),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink')],
    captions={
        'p1 = p2 = 0': '两个指针 `p1`、`p2` 分别从 start、target 开头往后扫',
        'while p1 < len(start) or': lambda S, B, r: (f"`p1 = {S.p1}`，`p2 = {S.p2}`：还有没扫完的 → 进入一轮" if (S.p1 < len(S.start) or S.p2 < len(S.target)) else "两个字符串都扫完了 → 跳出循环"),
        "start[p1] == '_'": lambda S, B, r: (f"start[{S.p1}] 是 `_` → 下划线不算片段，`p1` 右移" if S.p1 < len(S.start) and S.start[S.p1] == '_' else f"`p1 = {S.p1}`：停在第一个非下划线字符（或已到末尾）"),
        "target[p2] == '_'": lambda S, B, r: (f"target[{S.p2}] 是 `_` → 跳过，`p2` 右移" if S.p2 < len(S.target) and S.target[S.p2] == '_' else f"`p2 = {S.p2}`：停在第一个非下划线字符（或已到末尾）"),
        'p1 += 1': lambda S, B, r: (f"`p1` → {S.p1}" if S.get('_line') == 7 else f"这个片段配对完，`p1` → {S.p1}"),
        'p2 += 1': lambda S, B, r: (f"`p2` → {S.p2}" if S.get('_line') == 10 else f"`p2` → {S.p2}，继续找下一对"),
        'if p1 < len(start)': lambda S, B, r: ("start 还有片段 → 看 target 有没有对应的" if S.p1 < len(S.start) else "start 已经没有片段了 → 看 target 是否也没有"),
        'if p2 < len(target)': lambda S, B, r: ("target 也有片段 → 可以比较这一对" if S.p2 < len(S.target) else "target 没片段了但 start 还有 → 子序列不一致 → ==False=="),
        'if start[p1] != target[p2]': lambda S, B, r: (f"`{S.start[S.p1]}` ≠ `{S.target[S.p2]}`：L、R 不能交换位置 → 子序列不同 → ==False==" if S.start[S.p1] != S.target[S.p2] else f"`{S.start[S.p1]}` = `{S.target[S.p2]}`：字符一致，再比较位置"),
        "if start[p1] == 'L'": lambda S, B, r: ("是 `L`：只能向左走，看 p1 和 p2 的关系" if S.start[S.p1] == 'L' else "是 `R`：只能向右走，看 p1 和 p2 的关系"),
        'if p1 < p2': lambda S, B, r: (f"`p1 = {S.p1} < p2 = {S.p2}`：`L` 想往右走，做不到 → ==False==" if S.p1 < S.p2 else f"`p1 = {S.p1} ≥ p2 = {S.p2}`：`L` 只需向左或不动 → 合法"),
        'elif p1 > p2': lambda S, B, r: (f"`p1 = {S.p1} > p2 = {S.p2}`：`R` 想往左走，做不到 → ==False==" if S.p1 > S.p2 else f"`p1 = {S.p1} ≤ p2 = {S.p2}`：`R` 只需向右或不动 → 合法"),
        'elif p2 != len(target)': 'start 已空，若 target 还有片段 → False；否则一起结束',
        'return True': '全部配对成功，方向都合法 → ==True==',
    },
    skip=['else:'],
    cards=dict(
        one_liner='L、R 不能交换：两个指针各找下一个片段再比位置',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`L` 只能向左挪、`R` 只能向右挪，`_` 是空位',
                 '问 `start` 能否变成 `target`',
                 '示例：`_L__R__R_` → `L______RR` 返回 `true`'],
        quote='L和R是不能相互交换位置的，那么如果抛开start和target中的下划线不看，两个字符串中L和R形成的子序列必须是完全一致的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p1`、`p2` 各自跳过下划线，停在下一个片段上',
              '四种情况：一方没了、字符不同、`L` 要右移、`R` 要左移 → 都是 False',
              '全部扫完都没出问题 → True'],
        summary=['时间 `O(n)`，空间 `O(1)`，不需要 replace 新字符串',
                 '先跳下划线再判断，越界要先判断 `p < len`',
                 '`L` 判 `p1 < p2`，`R` 判 `p1 > p2`，别写反',
                 '对比灵神：灵神先 replace 比较子序列，再只用 i/j 查方向；yiduobo 把子序列检查融进同一个循环'],
    ),
)
