# -- coding: UTF-8

class String(object):
    def __init__(self):
        super(String, self).__init__()
        
    '''
    类名标准化
    '''
    def class_name_normalize(self, class_name):
        part_list = []
        for item in class_name.split("_"):
            part_list.append("{}{}".format(item[0].upper(), item[1:].lower()))
            
        return "".join(part_list)