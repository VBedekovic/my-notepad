class Location:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column
        
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Location): return False
        return self.line == __o.line and self.column == __o.column
    
    def __lt__(self, other):
        if not isinstance(other, Location): raise TypeError
        if self.line < other.line: return True
        elif self.line == other.line:
            return self.column < other.column
        return False
    
    def copy(self):
        return Location(self.line, self.column)

     
class LocationRange:
    def __init__(self, start: Location, end: Location):
        self.start = start
        self.end = end
        self.active = False
        self.activeInput = False

    def valid(self):
        return self.start < self.end
    
    def copy(self):
        return LocationRange(self.start.copy(), self.end.copy())
    