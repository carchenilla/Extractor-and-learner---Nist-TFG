class Vulnerability():
    def __init__(self, name, published, modified, score, vector, description, soft_list):
        self.name = name
        self.published = published
        self.modified = modified
        #self.severity = severity
        self.score = score
        '''self.base_score = base_score
        self.imp_score = imp_score
        self.exp_score = exp_score'''
        self.vector = vector
        self.description = description
        self.soft_list = soft_list

    def to_string(self):
        return "Vulnerability: "+self.name+". Published on "+str(self.published)+". \n"+"Score: "+str(self.score)+". Vector: "\
               +str(self.vector)+"\n"+self.description