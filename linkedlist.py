#singly linkedlist
# 3. Creating the Chain (Inserting at the Beginning)
# 4. Appending Nodes at the End of the Chain
# 5. Creating a New List
# 6. Displaying the Chain
# 7. Calculating the Length of the Chain
# 8. Removing a Node at a Given Index
# 9. Insert at
# remove by value
# insert by value



class Node:
    def __init__(self,data=None,next=None):
        self.data=data
        self.next=next

class chain:
    def __init__(self):
        self.head=None
    

    def printf(self):
        if self.head is None:
            return ' Not vaild'
        itr=self.head
        count=0
        container=''
        while itr:
            container+=str(itr.data)+ '->'
            itr=itr.next
            count+=1
        print(container[:-2])


    def first_node(self,data):
        node=Node(data,self.head)
        self.head=node
    

    def end_node(self,data):
        itr=self.head
        while itr.next:
            itr=itr.next
            node=Node(data,itr.next)
            itr.next=node
            break
        itr=itr.next

    def get_len(self):
        count=0
        itr=self.head
        while itr:
            count+=1
            itr=itr.next
        return count
    
    def newlist(self,data):
        self.head = None
        for value in data:
            self.first_node(value)

    def remove_at(self,index):
        if index<0 or index>=self.get_len():
            return 'Invaild index'
        if index == 0:
            self.head = self.head.next
            return
        itr=self.head
        count=0
        while itr:
            if count==index-1:
                itr.next=itr.next.next
                break
            itr=itr.next
            count+=1

    def insert_at(self,index,data):
        if index <0 or index>self.get_len():
            return 'Invaild position'
        if index == 0:
            self.first_node(data)
            return
        itr=self.head
        count=0
        while itr:
            if count == index-1:
                itr.next=Node(data,itr.next)
                return
            itr=itr.next
            count+=1
            
    def remove_by_value(self,data):
        if self.head is None:
            return 'Data not found'
        if self.head.data==data:
            self.head=self.head.next
            return
        itr=self.head
        while itr.next:
            if itr.next.data==data:
                itr.next=itr.next.next
                return
            itr=itr.next
    
    def insert_by_value(self,data_after,data_insert):
        if self.head is None:
            return 'Data is not present for operation'
        itr=self.head
        while itr:
            if itr.data==data_after:
                itr.next=Node(data_insert,itr.next)
                return
            itr=itr.next




# python linkedlist.py
start=chain()
start.first_node(3)
start.first_node(4)
start.end_node(23)
start.first_node(56)
start.newlist(['user1','user2','user3','user4'])
print(start.get_len())
start.remove_at(3)
start.insert_at(4,'stored')
start.remove_by_value('user1')
start.insert_by_value('user3','Bill gates')
start.printf()