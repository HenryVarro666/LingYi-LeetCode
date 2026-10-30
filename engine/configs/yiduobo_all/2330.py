CONFIG = dict(
    num=2330, title='有效的回文IV', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='相向双指针 · 数不同的位置对',
    code='''
class Solution(object):
    def makePalindrome(self, s):

        cnt = 0
        left = 0
        right = len(s) - 1
        while left < right:
            if s[left] != s[right]:
                cnt += 1
                if cnt > 2:
                    break
                
            left += 1
            right -= 1
        
        return cnt <= 2
''',
    call='Solution().makePalindrome("aecdbxya")',
    expect=False,
    views=[
        dict(type='text', fn=lambda S: (f"位置对 `({S['left']}, {S['right']})`：`{S['s'][S['left']]}` vs `{S['s'][S['right']]}`，已有 ==差异 {S['cnt']}== 处" if 'right' in S and S['left'] < S['right'] else f"差异共 ==cnt = {S['cnt']}== 处，至多改 2 个字符" if 'cnt' in S else '')),
        dict(type='string', var='s', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), h=300),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('cnt', 'cnt', 'orange')],
    captions={
        'cnt = 0': '`cnt` 记录「首尾对应位置不同」的对数',
        'right = len': '`right = len(s) - 1 = {right}`，左右指针从两端出发',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，还有位置对没比较' if S.left < S.right else f'`left = {S.left} >= right = {S.right}`：所有位置对都比完了'),
        'if s[left] != s[right]': lambda S, B, r: f'比较 `{S.s[S.left]}` 和 `{S.s[S.right]}`：' + ('相同，这一对不用改' if S.s[S.left] == S.s[S.right] else '不同 → 要改一次'),
        'cnt += 1': '这一对不同，改掉其中一个字符就行 → `cnt = {cnt}`',
        'if cnt > 2': lambda S, B, r: (f'`cnt = {S.cnt} > 2`：两次修改不够 → 提前 break' if S.cnt > 2 else f'`cnt = {S.cnt} <= 2`：两次修改还够用，继续'),
        'break': '差异已超过 2 处，不可能修成回文，直接退出循环',
        'left += 1': '这一对处理完，`left` 右移到 {left}',
        'right -= 1': '`right` 左移到 {right}，向中间收拢',
        'return cnt <= 2': '`cnt = {cnt}`，`cnt <= 2` 为 =={ret}==',
    },
    cards=dict(
        one_liner='数一数首尾不同的对数，超过 2 对就不行',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给一个字符串 `s`，做 ==一次或两次==操作：每次把任意位置改成任意字符',
                 '问能否让 `s` 变成回文串',
                 '本视频：`"aecdbxya"` → `False`'],
        quote='从两侧向中间遍历，对于每一组位置对，若二者不同，那么就需要就行一次修改。若s中有两处以上不同的位置，那么答案就是false，否则答案就是true。',
        quote_src='—— yiduobo 题解原文',
        idea=['回文 = 第 `i` 个和倒数第 `i` 个字符相同',
              '每个不同的位置对，改一个字符就能修好，恰好花 1 次操作',
              '不同的对数 ==cnt 不超过 2== 就够用；多出的次数可以随便改（如改成同一字符）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`while left < right`：中间那个字符不用比',
                 '`cnt > 2` 就可以提前 `break`，答案已经是 False',
                 '原文是 Python 2 风格的类定义，在 Python 3 下可直接运行，代码无改动'],
    ),
)
