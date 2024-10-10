class Node:
    def __init__(self,data=None,next=None,prev=None):
        self.data=data
        self.next=next
        self.prev=prev
    
class chain:
    def __init__(self):
        self.head = None
    
    def begin(self,data):
        node=Node(data,next=self.head)
        if self.head:
            self.head.prev=node
        self.head=node
    
    def printb(self):
        if self.head is None:
            return 'error'
        itr=self.head
        while itr.next:
            itr=itr.next
        
        container=''
        while itr:
            container+=str(itr.data)+'<-'
            itr=itr.prev
        print(container)
    
    def printf(self):
        if self.head is None:
            return 'Error'
        itr=self.head
        container=""
        while itr:
            container+=str(itr.data)+'->'
            itr=itr.next
        print(container)

    def remove_value(self,value):
        if self.head is None:
            return 'Empty list'
        if self.head.data==value:
            self.head=self.head.next # Now we get a  new head it means prev is None
        if self.head:
            self.head.prev=None
            return
        
        itr=self.head
        while itr:
            if itr.data==value:
                if itr.next:
                    itr.next.prev=itr.prev
                if itr.prev:
                    itr.prev.next=itr.next
                return
            itr=itr.next
        
    def remove_index(self,index):
            if self.head is None:
                return 'Error'
            if index==0:
                self.head=self.head.next
                if self.head:
                 self.head.prev=None
                return

            itr=self.head
            count=0

            while itr:
                if count==index:
                    if itr.next:
                        itr.next.prev=itr.prev
                    if itr.prev:
                        itr.prev.next=itr.next
                        return
                itr=itr.next
                count+=1
    
    def insert_value(self,data_after,data_insert):
        if self.head is None:
            return 'error'
        itr=self.head
        while itr:
            if itr.data==data_after:
                new_node=Node(data_insert,next=itr.next,prev=itr)

                if itr.next:
                    itr.next.prev=new_node

                itr.next=new_node
                return
            itr=itr.next
            
    def inser_value_by_index(self,index,data_insert):
        if self.head is None:
            return 'Error'
        if index==0:
            self.begin(data_insert)
            return
        
        itr=self.head
        count=0
        while itr:
            if count==index:
                new_node=Node(data_insert,next=itr.next,prev=itr)
                if itr.next:
                    itr.next.prev=new_node
                
                itr.next=new_node
                return
            itr=itr.next
            count+=1
    
    def end_node(self,data):
        itr=self.head
        while itr.next:
            itr=itr.next
        new_node=Node(data,None)
        itr.next=new_node
        new_node.prev=itr
    
    def new_list(self,data):
      self.head = None
      for value in data:
          self.begin(value)






l=chain()
l.begin(1)
l.begin(2)
l.begin(3)
# l.inser_value_by_index(2,'Routex453>6^')
l.end_node('GuestEntred')
l.new_list([2,3,4,5,6,7,8])
l.printf()
l.printb()
