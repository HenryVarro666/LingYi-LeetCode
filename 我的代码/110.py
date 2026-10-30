# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def get_height(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            left_h = get_height(node.left)
            right_h = get_height(node.right)
            if left_h == -1 or right_h == -1 or abs(left_h - right_h) > 1:
                return -1
            return max(left_h, right_h) + 1
        return get_height(root) != -1
    

##############################################################

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def get_height(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            left_h = get_height(node.left)
            if left_h == -1:
                return -1  # 提前退出，不再递归
            right_h = get_height(node.right)
            if right_h == -1 or abs(left_h - right_h) > 1:
                return -1
            return max(left_h, right_h) + 1
        return get_height(root) != -1
    



######################################

## 自顶向下的递归
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        def height(root: TreeNode) -> int:
            if not root:
                return 0
            return max(height(root.left), height(root.right)) + 1

        if not root:
            return True
        return abs(height(root.left) - height(root.right)) <= 1 and self.isBalanced(root.left) and self.isBalanced(root.right)


##################################################

## 自底向上的递归

class Solution:
    def isBalanced(self, root: TreeNode) -> bool:
        def height(root: TreeNode) -> int:
            if not root:
                return 0
            leftHeight = height(root.left)
            rightHeight = height(root.right)
            if leftHeight == -1 or rightHeight == -1 or abs(leftHeight - rightHeight) > 1:
                return -1
            else:
                return max(leftHeight, rightHeight) + 1

        return height(root) >= 0
