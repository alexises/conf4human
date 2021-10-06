from collections import OrderedDict

class FilePosition(object):
    def __init__(self, line: int, column: int, filename: str = None):
        self.line = line
        self.column = column
        self.filename = filename

    def __str__(self):
        if filename is None:
           return '{}:{}'.format(self.line, self.column)
        else:
           return '{}({}:{})'.format(self.filename, self.line, self.column)

class LocalizableObject(object):
    def getStartPosition(self) -> FilePosition:
        raise NotImplemented("This class is an interface")

    def getEndPosition(self) -> FilePosition:
        raise NotImplemented("This class is an interface")

class LocalizableLiteral(LocalizableObject):
    def __init__(self, begin: FilePosition, end: FilePosition, value):
        self.value = value
        self.begin = begin
        self.end = end
   
    def getStartPosition(self) -> FilePosition:
        return self.begin

    def getEndPosition(self) -> FilePosition:
        return self.end

    def getValue(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return not(self == other)

    def serialize(self):
        return self.getValue()

class LocalizableCollection(LocalizableObject):
    def __init__(self, begin: FilePosition):
        self.begin = begin

    def getStartPosition(self) -> FilePosition:
        first = self.getFirst()
        if first is None:
            return self.begin
        else:
            return first.getStartPosition()

    def getEndPosition(self) -> FilePosition:
        end = self.getLast()
        if last is None:
            return first #yep, here we have empty collection, no issue
        else:
            return end.getEndPosition()

    def getFirst(self) -> LocalizableObject:
        raise NotImplemented("This class is abstract")

    def getLast(self) -> LocalizableObject:
        raise NotImplemented("This class is abstract")

    def serialize(self) -> LocalizableObject:
        raise NotImplemented("This class is abstract")

class LocalizableList(LocalizableCollection):
    def __init__(self, begin):
        super().__init__(begin)
        self._list = []

    def getFirst(self) -> LocalizableObject:
        try:
            return self._list[0]
        except IndexError:
            return None

    def getLast() -> LocalizableObject:
        try:
            return self._list[-1]
        except IndexError:
            return None

    def add(self, value: LocalizableLiteral):
        self._list.append(value)

    def __item__(self, idx: int):
        return self._list[idx]

    def serialize(self):
        out = []
        for i in self._list:
            out.append(i.serialize())
        return out

class LocalizableOrderedDict(LocalizableCollection):
    def __init__(self, begin):
        super().__init__(begin)
        self._dict = OrderedDict()

    def getFirst(self) -> LocalizableObject:
        try:
            return next(iter(self._dict.items()))
        except IndexError:
            return None

    def getLast() -> LocalizableObject:
        try:
            return next(reversed(self._list))
        except IndexError:
            return None

    def add(self, key: LocalizableLiteral, value: LocalizableLiteral):
        self._dict[key] = value

    def __item__(self, idx):
        return self._dict[idx]
   
    def serialize(self):
        out = {}
        for key, val in self._dict.items():
            serialized_key = key.serialize()
            serialized_val = val.serialize()
            out[serialized_key] = serialized_val
        return out
