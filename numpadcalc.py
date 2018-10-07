import tkinter as tk
from tkinter import font
from abc import ABC, abstractmethod
from enum import IntEnum, unique
from builtins import int


class Observer(ABC):
    
    @abstractmethod
    def notify(self):
        pass
    
    
class Observable():
    
    def __init__(self):
        self._observers = set()
    
    def register(self, observer:Observer):
        self._observers.add(observer)
        
    def notify_all(self):
        for observer in self._observers:
            observer.notify()
            
            
@unique
class Operator(IntEnum):
    DIGIT_0 =  0
    DIGIT_1 =  1
    DIGIT_2 =  2
    DIGIT_3 =  3
    DIGIT_4 =  4
    DIGIT_5 =  5
    DIGIT_6 =  6
    DIGIT_7 =  7
    DIGIT_8 =  8
    DIGIT_9 =  9
    PERIOD  = 10
    EQUALS  = 11
    PLUS    = 12
    MINUS   = 13
    MULT    = 14
    DIV     = 15
    CLEAR   = 16
    

class Model(Observable):
    
    def __init__(self):
        Observable.__init__(self);
        self._output = 0
        self._result = 0
        self._error = False
        self._last_operator = None
    
    def operate(self, operator:Operator):
        
        # validate input
        if not isinstance(operator, Operator):
            raise TypeError("operator must be an instance of Operator Enum")
        
        # clear    
        elif operator == Operator.CLEAR:
            self._clear()
            
        # cancel if error
        elif self._error:
            return
        
        # any digit
        elif Operator.DIGIT_0 <= operator <= Operator.DIGIT_9:
            if self._last_operator == Operator.EQUALS:
                self._clear()
            self._output = self._output * 10 + operator
            self.notify_all()
            
        # period
        elif operator == Operator.PERIOD:
            pass # TODO
        
        # equals    
        elif operator == Operator.EQUALS:
            
            # plus
            if self._last_operator == Operator.PLUS:
                self._output += self._result
                self._last_operator = Operator.EQUALS
                
            # minus
            elif self._last_operator == Operator.MINUS:
                self._output = self._result - self._output
                self._last_operator = Operator.EQUALS
                
            # mult
            elif self._last_operator == Operator.MULT:
                self._output *= self._result
                self._last_operator = Operator.EQUALS
                
            # div
            elif self._last_operator == Operator.DIV:
                try:
                    self._output = self._result / self._output
                    self._last_operator = Operator.EQUALS
                except ZeroDivisionError:
                    self._error = True
        
        # plus, minus, mult, div        
        elif Operator.PLUS <= operator <= Operator.DIV:
            self._result = self._output
            self._output = 0
            self._last_operator = operator
        
        # any unhandled operate    
        else:
            raise NotImplementedError("unexpected Enum")
        
        # notify all observers
        self.notify_all()
        
    def _clear(self):
        self._output = 0
        self._result = 0
        self._error = False
        self._last_operator = None
    
    @property    
    def error(self) -> bool:
        return self._error
    
    @property    
    def output(self) -> int:
        return self._output
        
        
class View(tk.Tk, Observer):
    
    CONST_TITLE = "Calculator"
    CONST_GEOMETRY = "300x400"
    CONST_ERROR = "ERROR!1!!!1"
    CONST_MAP_NAMES = {
        Operator.DIGIT_0:"0",
        Operator.DIGIT_1:"1",
        Operator.DIGIT_2:"2",
        Operator.DIGIT_3:"3",
        Operator.DIGIT_4:"4",
        Operator.DIGIT_5:"5",
        Operator.DIGIT_6:"6",
        Operator.DIGIT_7:"7",
        Operator.DIGIT_8:"8",
        Operator.DIGIT_9:"9",
        Operator.PERIOD :".",
        Operator.EQUALS :"=",
        Operator.PLUS   :"+",
        Operator.MINUS  :"-",
        Operator.MULT   :"*",
        Operator.DIV    :"/",
        Operator.CLEAR  :"C"
    }
    CONST_MAP_KEYS = {
        "Key-0"       :Operator.DIGIT_0,
        "Key-1"       :Operator.DIGIT_1,
        "Key-2"       :Operator.DIGIT_2,
        "Key-3"       :Operator.DIGIT_3,
        "Key-4"       :Operator.DIGIT_4,
        "Key-5"       :Operator.DIGIT_5,
        "Key-6"       :Operator.DIGIT_6,
        "Key-7"       :Operator.DIGIT_7,
        "Key-8"       :Operator.DIGIT_8,
        "Key-9"       :Operator.DIGIT_9,
        "Key-period"  :Operator.PERIOD,
        "Key-comma"   :Operator.PERIOD,
        "Return"      :Operator.EQUALS,
        "Key-plus"    :Operator.PLUS,
        "Key-minus"   :Operator.MINUS,
        "Key-asterisk":Operator.MULT,
        "Key-slash"   :Operator.DIV,
        "Key-c"       :Operator.CLEAR,
        "Key-space"   :Operator.CLEAR
    }
    
    def __init__(self, title:str=CONST_TITLE, geometry:str=CONST_GEOMETRY):
        tk.Tk.__init__(self)
        self.title(title)
        self.geometry(geometry)
        self._model = Model()
        self._model.register(self)
        self._frame = tk.Frame(self)
        self._font_display = font.Font(root=self._frame, family="Helvetica", size="19", weight=font.BOLD)
        self._font_buttons = font.Font(root=self._frame, family="Helvetica", size="30", weight=font.BOLD)
        
        # create widgets
        self._display = tk.Label(self._frame, text="INIT", font=self._font_display, justify=tk.RIGHT, anchor=tk.E, bg="white", padx=20, pady=20)
        self._buttons = []
        for operator in Operator:
            self._buttons.append(tk.Button(self._frame, text=View.CONST_MAP_NAMES[operator], font=self._font_buttons, command=lambda operator=operator:self._model.operate(operator)))
        
        # frame layout
        self._frame.pack(fill=tk.BOTH, expand=1)
        for row in range(6):
            self._frame.rowconfigure(row, weight=1)
        for column in range(4):
            self._frame.columnconfigure(column, weight=1)
                
        # widgets layout        
        for button in self._buttons:
            button.grid(sticky="NSWE")
        self._display.grid(row="0", column="0", columnspan="4", sticky="NSWE")
        self._buttons[Operator.DIGIT_0].grid(row="5", column="0", columnspan="2")
        self._buttons[Operator.PERIOD ].grid(row="5", column="2")
        self._buttons[Operator.DIGIT_1].grid(row="4", column="0")
        self._buttons[Operator.DIGIT_2].grid(row="4", column="1")
        self._buttons[Operator.DIGIT_3].grid(row="4", column="2")
        self._buttons[Operator.DIGIT_4].grid(row="3", column="0")
        self._buttons[Operator.DIGIT_5].grid(row="3", column="1")
        self._buttons[Operator.DIGIT_6].grid(row="3", column="2")
        self._buttons[Operator.DIGIT_7].grid(row="2", column="0")
        self._buttons[Operator.DIGIT_8].grid(row="2", column="1")
        self._buttons[Operator.DIGIT_9].grid(row="2", column="2")
        self._buttons[Operator.EQUALS ].grid(row="4", column="3", rowspan="2")
        self._buttons[Operator.PLUS   ].grid(row="2", column="3", rowspan="2")
        self._buttons[Operator.MINUS  ].grid(row="1", column="3")
        self._buttons[Operator.MULT   ].grid(row="1", column="2")
        self._buttons[Operator.DIV    ].grid(row="1", column="1")
        self._buttons[Operator.CLEAR  ].grid(row="1", column="0")
        
        # set key listeners
        for key in self.CONST_MAP_KEYS:
            self._frame.bind("<" + key + ">", lambda event, key=key: self._model.operate(View.CONST_MAP_KEYS[key]))
        self._frame.bind("<Key-Escape>", lambda event: self.quit());
        
        # set focus for key listeners
        self._frame.focus_set()
        
        # refresh GUI
        self.notify()
        
    def notify(self):
        self._display.config(text=View.CONST_ERROR if self._model.error else self._model.output)

     
if __name__ == "__main__":
    View().mainloop()
