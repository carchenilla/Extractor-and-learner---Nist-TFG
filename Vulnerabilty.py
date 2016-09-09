class Vulnerability():
    def __init__(self, name, published, modified, severity, score, base_score, imp_score, exp_score, vector, description):
        self.name = name
        self.published = published
        self.modified = modified
        self.severity = severity
        self.score = score
        self.base_score = base_score
        self.imp_score = imp_score
        self.exp_score = exp_score
        self.vector = vector
        self.description = description

    def to_string(self):
        return "Vulnerability: "+self.name+". Published on "+self.published+". \n"+"Score: "+self.score+". Vector: "\
               +self.vector+"\n"+self.description