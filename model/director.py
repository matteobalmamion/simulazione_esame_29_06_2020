from dataclasses import dataclass
@dataclass
class Director:
    id:int
    name:str
    surname:str

    def __hash__(self):
        return hash(self.id)
    def __str__(self):
        return f'{self.id} {self.name} {self.surname}'