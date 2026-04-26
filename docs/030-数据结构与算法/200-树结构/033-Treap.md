# Treap（树堆）

## 概述

Treap是Tree和Heap的结合体，同时满足二叉搜索树和堆的性质，通过随机优先级保持平衡。

## Treap特点

1. **BST性质**：按键值有序
2. **堆性质**：按优先级有序（小根堆或大根堆）
3. **随机平衡**：优先级随机，期望高度O(log n)
4. **简单实现**：相比AVL、红黑树实现简单

## 数据结构

```c
#include <stdlib.h>
#include <time.h>

typedef struct TreapNode {
    int key;
    int priority;
    struct TreapNode *left;
    struct TreapNode *right;
} TreapNode;

typedef struct {
    TreapNode *root;
} Treap;
```

## 创建节点

```c
TreapNode* createTreapNode(int key) {
    TreapNode *node = (TreapNode*)malloc(sizeof(TreapNode));
    node->key = key;
    node->priority = rand();
    node->left = NULL;
    node->right = NULL;
    return node;
}

Treap* createTreap() {
    Treap *treap = (Treap*)malloc(sizeof(Treap));
    treap->root = NULL;
    srand(time(NULL));
    return treap;
}
```

## 旋转操作

```c
TreapNode* rotateRight(TreapNode *y) {
    TreapNode *x = y->left;
    y->left = x->right;
    x->right = y;
    return x;
}

TreapNode* rotateLeft(TreapNode *x) {
    TreapNode *y = x->right;
    x->right = y->left;
    y->left = x;
    return y;
}
```

## 插入操作

```c
TreapNode* insertTreap(TreapNode *root, int key) {
    if (root == NULL) {
        return createTreapNode(key);
    }
    
    if (key <= root->key) {
        root->left = insertTreap(root->left, key);
        
        if (root->left->priority < root->priority) {
            root = rotateRight(root);
        }
    } else {
        root->right = insertTreap(root->right, key);
        
        if (root->right->priority < root->priority) {
            root = rotateLeft(root);
        }
    }
    
    return root;
}

void insert(Treap *treap, int key) {
    treap->root = insertTreap(treap->root, key);
}
```

## 删除操作

```c
TreapNode* deleteTreap(TreapNode *root, int key) {
    if (root == NULL) return NULL;
    
    if (key < root->key) {
        root->left = deleteTreap(root->left, key);
    } else if (key > root->key) {
        root->right = deleteTreap(root->right, key);
    } else {
        if (root->left == NULL) {
            TreapNode *temp = root->right;
            free(root);
            return temp;
        }
        if (root->right == NULL) {
            TreapNode *temp = root->left;
            free(root);
            return temp;
        }
        
        if (root->left->priority < root->right->priority) {
            root = rotateRight(root);
            root->right = deleteTreap(root->right, key);
        } else {
            root = rotateLeft(root);
            root->left = deleteTreap(root->left, key);
        }
    }
    
    return root;
}

void delete(Treap *treap, int key) {
    treap->root = deleteTreap(treap->root, key);
}
```

## 查找操作

```c
TreapNode* searchTreap(TreapNode *root, int key) {
    if (root == NULL || root->key == key) {
        return root;
    }
    
    if (key < root->key) {
        return searchTreap(root->left, key);
    }
    return searchTreap(root->right, key);
}

TreapNode* search(Treap *treap, int key) {
    return searchTreap(treap->root, key);
}
```

## 分裂操作

```c
void split(TreapNode *root, int key, TreapNode **left, TreapNode **right) {
    if (root == NULL) {
        *left = NULL;
        *right = NULL;
        return;
    }
    
    if (key < root->key) {
        split(root->left, key, left, &root->left);
        *right = root;
    } else {
        split(root->right, key, &root->right, right);
        *left = root;
    }
}
```

## 合并操作

```c
TreapNode* merge(TreapNode *left, TreapNode *right) {
    if (left == NULL) return right;
    if (right == NULL) return left;
    
    if (left->priority < right->priority) {
        left->right = merge(left->right, right);
        return left;
    } else {
        right->left = merge(left, right->left);
        return right;
    }
}
```

## C++ 实现

```cpp
#include <random>
#include <memory>

class Treap {
private:
    struct Node {
        int key;
        int priority;
        std::unique_ptr<Node> left, right;
        
        Node(int k) : key(k), priority(rng()) {}
    };
    
    std::unique_ptr<Node> root;
    static std::mt19937 rng;
    
    std::unique_ptr<Node> rotateRight(std::unique_ptr<Node> y) {
        auto x = std::move(y->left);
        y->left = std::move(x->right);
        x->right = std::move(y);
        return x;
    }
    
    std::unique_ptr<Node> rotateLeft(std::unique_ptr<Node> x) {
        auto y = std::move(x->right);
        x->right = std::move(y->left);
        y->left = std::move(x);
        return y;
    }
    
    std::unique_ptr<Node> insert(std::unique_ptr<Node> root, int key) {
        if (!root) {
            return std::make_unique<Node>(key);
        }
        
        if (key <= root->key) {
            root->left = insert(std::move(root->left), key);
            if (root->left->priority < root->priority) {
                root = rotateRight(std::move(root));
            }
        } else {
            root->right = insert(std::move(root->right), key);
            if (root->right->priority < root->priority) {
                root = rotateLeft(std::move(root));
            }
        }
        
        return root;
    }
    
public:
    void insert(int key) {
        root = insert(std::move(root), key);
    }
    
    bool search(int key) {
        Node* curr = root.get();
        while (curr) {
            if (key == curr->key) return true;
            curr = (key < curr->key) ? curr->left.get() : curr->right.get();
        }
        return false;
    }
};

std::mt19937 Treap::rng(std::random_device{}());
```

## 时间复杂度

| 操作 | 期望 | 最坏 |
|------|------|------|
| 插入 | O(log n) | O(n) |
| 删除 | O(log n) | O(n) |
| 查找 | O(log n) | O(n) |
| 分裂 | O(log n) | O(n) |
| 合并 | O(log n) | O(n) |

## Treap vs 其他平衡树

| 特性 | Treap | AVL | 红黑树 |
|------|-------|-----|--------|
| 实现复杂度 | 简单 | 复杂 | 复杂 |
| 查找效率 | 好 | 最优 | 好 |
| 插入删除 | O(log n)期望 | O(log n) | O(log n) |
| 空间开销 | 存储优先级 | 存储高度 | 存储颜色 |

## 应用场景

1. **动态集合**：支持动态插入删除
2. **区间问题**：分裂合并操作
3. **随机化算法**：简单高效
4. **竞赛编程**：实现简单

## 参考资料

- Seidel, Aragon (1989) Treap论文
- 《数据结构与算法分析》
