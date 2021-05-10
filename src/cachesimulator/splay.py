# coding=utf-8
"""
    Based on mimircache : a slight modification about size calculation
    Author: Yazhuo Zhang <z.yazhuo@gmail.com> 2021/04
"""

import math

class Node:
    def __init__(self, ts, size):
        self.left = None
        self.right = None
        self.size = size # maintained to be the size of nodes rooted here
        self.key = ts
        self.uniqsize = 0
        self.dis = 0

    def __repr__(self):
        return 'TraceNode<%s>: key[%s] size[%i]' %(id(self), self.key, self.size)


def node_size(node):
    if(node == None):
        return 0
    else:
        return node.size

def node_uniq(node):
    if(node == None):
        return 0
    else:
        return node.uniqsize

def node_value(node):
    if(node == None):
        return 0
    else:
        return node.dis


class SplayTree:
    
    def __init__(self):
        self.root = None
        self.header = Node(0, 0)

    
    def insert(self, key, size):

        n = Node(key, size)

        if(self.root == None):
            self.root = n
            return self.root
        
        self.splay(key)
        
        if(key < self.root.key):
            n.left = self.root.left
            n.right = self.root
            self.root.left = None
            #self.root.dis = 1 + node_value(self.root.right)
            self.root.uniqsize = node_size(self.root) + node_uniq(self.root.right)
        #elif(key >= self.root.key):
        else:
            n.right = self.root.right
            n.left = self.root
            self.root.right = None
            #self.root.dis = 1 + node_value(self.root.left)
            self.root.uniqsize = node_size(self.root) + node_uniq(self.root.left)
        #else:
            #return self.root

        n.uniqsize = node_size(n) + node_uniq(n.left) + node_uniq(n.right)
        #n.dis = 1 + node_value(n.left) + node_value(n.right)
        self.root = n

        return self.root

    
    def delete(self, key):

        if(self.root == None):
            return None

        root_value = node_uniq(self.root)
        #root_dis = node_value(self.root)
        self.splay(key)

        if(key == self.root.key):
            if(self.root.left == None):
                self.root = self.root.right
            else:
                x = self.root.right
                self.root = self.root.left
                self.splay(key)
                self.root.right = x

        
            if(self.root != None):
                self.root.uniqsize = root_value - node_uniq(self.root)
                if(math.isnan(self.root.uniqsize)):
                    self.root.uniqsize = float('inf')
                
                #self.root.dis = root_dis - node_value(self.root)
        return self.root

    
    def splay(self, key):
        
        t = self.root
        if(t == None):
            return t

        self.header.left = self.header.right = None
        l = r = self.header
        l_size = r_size = 0

        while True:
            if(key < t.key):
                if(t.left == None):
                    break
                if(key < t.left.key):
                    y = t.left          # rotate right
                    t.left = y.right
                    y.right = t
                    t.uniqsize = node_uniq(t.left) + node_uniq(t.right) + node_size(t)
                    #t.dis = node_value(t.left) + node_value(t.right) + 1
                    t = y
                    if(t.left == None):
                        break
                r.left = t              # link right
                r = t
                t = t.left
                r_size += node_uniq(r.right) + node_size(r)
                #r_size += 1 + node_value(r.right)
            elif(key > t.key):
                if(t.right == None):
                    break
                if(key > t.right.key):
                    y = t.right         # rotate left
                    t.right = y.left
                    y.left = t
                    t.uniqsize = node_uniq(t.left) + node_uniq(t.right) + node_size(t)
                    #t.dis = node_value(t.left) + node_value(t.right) + 1
                    t = y
                    if(t.right == None):
                        break
                l.right = t             # link left
                l = t
                t = t.right
                l_size += node_uniq(l.left) + node_size(l)
                #l_size += 1 + node_value(l.left)
            else:
                break
        
        l_size += node_uniq(t.left)
        r_size += node_uniq(t.right)
        t.uniqsize = l_size + r_size + node_size(t)
        
        '''
        l_size += node_value(t.left)
        r_size += node_value(t.right)
        t.dis = l_size + r_size + 1
        '''

        l.right = r.left = None
        
        
        y = self.header.right
        while(y != None):
            y.uniqsize = l_size
            l_size = l_size - (node_uniq(y.left) + node_size(y))
            if(math.isnan(l_size)):
                l_size = float('inf')
            #y.dis = l_size
            #l_size -= 1 + node_value(y.left)
            y = y.right
        
        y = self.header.left
        while(y != None):
            y.uniqsize = r_size
            r_size = r_size - (node_uniq(y.right) + node_size(y))
            if(math.isnan(r_size)):
                r_size = float('inf')
            #y.dis = r_size
            #r_size -= 1 + node_value(y.right)
            y = y.left

        l.right = t.left
        r.left = t.right
        t.left = self.header.right
        t.right = self.header.left
        
        self.root = t

        return self.root
