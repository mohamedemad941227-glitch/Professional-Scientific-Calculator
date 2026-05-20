import re
import math
import tkinter as tk
from tkinter import font as tkfont

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("460x700")
        self.root.resizable(False, False)
        
        # Theme colors
        self.background_color = "#101010"
        self.panel_color = "#171717"
        self.card_color = "#1c1c1c"
        self.accent_color = "#3fe8ff"
        self.text_color = "#f4f7fb"
        self.secondary_text = "#8a97aa"

        self.button_bg = "#232323"
        self.button_fg = "#f4f7fb"
        self.action_bg = "#ff8c42"
        self.action_fg = "#101010"
        self.disabled_bg = "#333333"

        self.root.configure(bg=self.background_color)
        
        # Fonts
        self.title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.display_font = tkfont.Font(family="Consolas", size=34, weight="bold")
        self.button_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.small_font = tkfont.Font(family="Segoe UI", size=10)
        
        # Display variable
        self.display_var = tk.StringVar(value="0")
        self.operation_var = tk.StringVar(value="")
        self.should_reset_display = False
        self.expression_just_evaluated = False
        self.last_result = None
        self.max_expression_length = 140
        
        # Create UI
        self.create_display()
        self.create_buttons()
    
    def create_display(self):
        """Create the display area"""
        title = tk.Label(
            self.root,
            text="Smart Calculator",
            font=self.title_font,
            bg=self.background_color,
            fg=self.accent_color
        )
        title.pack(pady=(18, 2))
        
        subtitle = tk.Label(
            self.root,
            text="Fast. Clean. Elegant.",
            font=self.small_font,
            bg=self.background_color,
            fg=self.secondary_text
        )
        subtitle.pack(pady=(0, 14))

        card_frame = tk.Frame(self.root, bg=self.card_color, bd=0, highlightthickness=0)
        card_frame.pack(padx=18, pady=0, fill=tk.BOTH, expand=True)

        operation_label = tk.Label(
            card_frame,
            textvariable=self.operation_var,
            font=self.small_font,
            bg=self.card_color,
            fg=self.accent_color,
            anchor='e'
        )
        operation_label.pack(fill=tk.X, padx=16, pady=(12, 0))

        display_frame = tk.Frame(card_frame, bg=self.panel_color, bd=0, relief=tk.FLAT)
        display_frame.pack(padx=16, pady=(18, 12), fill=tk.BOTH, expand=False)

        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=self.display_font,
            justify=tk.RIGHT,
            bg=self.panel_color,
            fg=self.text_color,
            bd=0,
            relief=tk.FLAT,
            insertbackground=self.text_color,
            highlightthickness=0
        )
        self.display.pack(fill=tk.BOTH, ipady=26, pady=10, padx=10)

        self.root.bind('<Key>', self.on_key_press)

        instructions = tk.Label(
            card_frame,
            text="Use the calculator buttons on screen. Scientific functions are available.",
            font=self.small_font,
            bg=self.card_color,
            fg=self.secondary_text
        )
        instructions.pack(pady=(0, 10))
        
        self.button_card = tk.Frame(card_frame, bg=self.card_color)
        self.button_card.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
    
    def create_buttons(self):
        """Create calculator buttons"""
        button_frame = self.button_card
        button_frame.configure(bg=self.card_color)

        sci_buttons = [
            ['sin', 'cos', 'tan', 'sqrt'],
            ['ln', 'log', 'exp', 'pi']
        ]

        main_buttons = [
            ['C', '(', ')', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '←']
        ]

        buttons = sci_buttons + main_buttons

        for row_index, row in enumerate(buttons):
            for col_index, btn_text in enumerate(row):
                self.create_button(btn_text, button_frame, row_index, col_index)

        for index in range(4):
            button_frame.columnconfigure(index, weight=1, uniform='button')
        for index in range(len(buttons)):
            button_frame.rowconfigure(index, weight=1)
    
    def create_button(self, text, parent, row, column):
        """Create individual button"""
        if text == '=':
            bg_color = "#3fe8ff"
            fg_color = self.background_color
            active_bg = "#33c7dd"
        elif text == 'C':
            bg_color = "#ff6d8f"
            fg_color = self.background_color
            active_bg = "#e45e7d"
        elif text == '←':
            bg_color = "#ffb86f"
            fg_color = self.background_color
            active_bg = "#e6a560"
        elif text in ['/', '*', '-', '+', '^']:
            bg_color = self.action_bg
            fg_color = self.action_fg
            active_bg = "#d7832f"
        elif text in ['sin', 'cos', 'tan', 'sqrt', 'ln', 'log', 'exp', 'pi', 'e']:
            bg_color = "#5f8cff"
            fg_color = self.background_color
            active_bg = "#4b76d1"
        else:
            bg_color = self.button_bg
            fg_color = self.button_fg
            active_bg = "#2f2f2f"

        button = tk.Button(
            parent,
            text=text,
            font=self.button_font,
            bg=bg_color,
            fg=fg_color,
            bd=0,
            relief=tk.FLAT,
            activebackground=active_bg,
            activeforeground=fg_color,
            command=lambda: self.on_button_click(text)
        )
        button.grid(row=row, column=column, sticky='nsew', padx=5, pady=5)
        button.bind('<Enter>', lambda event, btn=button: self.on_button_hover(btn))
        button.bind('<Leave>', lambda event, btn=button, default=bg_color: self.on_button_leave(btn, default))
        button.configure(cursor='hand2', highlightthickness=0, pady=18)

    def on_button_hover(self, button):
        """Hover effect for buttons"""
        button.configure(bg="#3a3a3a")

    def on_button_leave(self, button, default_color):
        """Reset button color after hover"""
        button.configure(bg=default_color)

    def format_result(self, value):
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return str(value).rstrip('0').rstrip('.')
        return str(value)

    def prepare_expression(self, expression):
        expression = expression.replace(' ', '')
        expression = expression.replace('^', '**')
        replacements = [
            (r'(?<!\.)\bsqrt\(', 'math.sqrt('),
            (r'(?<!\.)\bsin\(', 'math.sin('),
            (r'(?<!\.)\bcos\(', 'math.cos('),
            (r'(?<!\.)\btan\(', 'math.tan('),
            (r'(?<!\.)\bln\(', 'math.log('),
            (r'(?<!\.)\blog\(', 'math.log10('),
            (r'(?<!\.)\bexp\(', 'math.exp('),
            (r'(?<!\.)\bpi\b', 'math.pi'),
            (r'(?<!\.)\be\b', 'math.e')
        ]
        for pattern, replacement in replacements:
            expression = re.sub(pattern, replacement, expression)
        return expression

    def safe_evaluate(self, expression):
        expression = self.prepare_expression(expression)
        if not re.match(r'^[0-9A-Za-z+\-*/()., ]+$', expression):
            raise ValueError("Invalid expression")
        return eval(expression, {"__builtins__": None, 'math': math}, {})

    def update_operation_label(self, expression):
        if len(expression) > self.max_expression_length:
            self.operation_var.set(expression[-self.max_expression_length:])
        else:
            self.operation_var.set(expression)

    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        keysym = event.keysym
        
        ignore_keys = {
            'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R',
            'Caps_Lock', 'Num_Lock', 'Scroll_Lock', 'Super_L', 'Super_R',
            'Menu', 'Pause', 'Print', 'Insert', 'Home', 'End', 'Page_Up', 'Page_Down'
        }
        if keysym in ignore_keys or key == '':
            return

        # Number keys
        if key in '0123456789':
            self.on_button_click(key)
            return

        # Operation keys
        if key in ['+', '-', '*', '/']:
            self.on_button_click(key)
            return

        # Decimal point
        if key == '.':
            self.on_button_click('.')
            return

        # Parentheses
        if key == '(':
            self.on_button_click('(')
            return
        if key == ')':
            self.on_button_click(')')
            return

        # Enter or equals
        if keysym == 'Return':
            self.on_button_click('=')
            return

        # Backspace
        if keysym == 'BackSpace':
            self.on_button_click('←')
            return

        # Escape clears current entry only
        if keysym == 'Escape':
            self.on_button_click('CE')
            return
    
    def on_button_click(self, char):
        """Handle button clicks"""
        current_display = self.display_var.get()

        if current_display.startswith("Error") and char not in ['C', '←']:
            current_display = "0"
            self.display_var.set("0")
            self.should_reset_display = False

        if char not in ['C', '←', '='] and len(current_display) >= self.max_expression_length:
            return

        if char == 'C':
            self.display_var.set("0")
            self.update_operation_label("")
            self.should_reset_display = False
            self.expression_just_evaluated = False
            return

        if char == 'CE':
            if self.should_reset_display or self.expression_just_evaluated:
                self.display_var.set("0")
                self.should_reset_display = False
                self.expression_just_evaluated = False
            elif any(op in current_display for op in ['+', '-', '*', '/']):
                # Remove the last number after the final operator
                last_operator = max(current_display.rfind(op) for op in ['+', '-', '*', '/'])
                if last_operator >= 0:
                    new_value = current_display[:last_operator + 1]
                    self.display_var.set(new_value if new_value != "" else "0")
            else:
                self.display_var.set("0")
            self.update_operation_label(self.display_var.get() if self.display_var.get() != "0" else "")
            return

        if char == '←':
            if self.should_reset_display:
                self.display_var.set("0")
                self.update_operation_label("")
                self.should_reset_display = False
            else:
                if len(current_display) > 1:
                    self.display_var.set(current_display[:-1])
                else:
                    self.display_var.set("0")
            self.update_operation_label(self.display_var.get() if self.display_var.get() != "0" else "")
            return

        if char in ['sin', 'cos', 'tan', 'sqrt', 'ln', 'log', 'exp']:
            if self.should_reset_display or self.expression_just_evaluated or current_display == "0":
                self.display_var.set(f"{char}(")
                self.should_reset_display = False
                self.expression_just_evaluated = False
            else:
                self.display_var.set(current_display + f"{char}(")
            self.update_operation_label(self.display_var.get())
            return

        if char in ['pi', 'e']:
            if self.should_reset_display or self.expression_just_evaluated:
                self.display_var.set(char)
                self.should_reset_display = False
                self.expression_just_evaluated = False
            elif current_display == "0":
                self.display_var.set(char)
            else:
                self.display_var.set(current_display + char)
            self.update_operation_label(self.display_var.get())
            return

        if char == '^':
            if self.should_reset_display:
                self.should_reset_display = False
                self.expression_just_evaluated = False
            if current_display and current_display[-1] not in ['+', '-', '*', '/', '^']:
                self.display_var.set(current_display + '^')
            self.update_operation_label(self.display_var.get())
            return

        if char == '=':
            expression = self.display_var.get()
            if expression and expression[-1] in ['+', '-', '*', '/']:
                expression = expression[:-1]
            try:
                result = self.safe_evaluate(expression)
                formatted = self.format_result(result)
                self.last_result = formatted
                self.operation_var.set(f"{expression} =")
                self.display_var.set(formatted)
                self.should_reset_display = True
                self.expression_just_evaluated = True
            except ZeroDivisionError:
                self.display_var.set("Error: Div by 0")
                self.operation_var.set("")
                self.last_result = None
                self.should_reset_display = True
                self.expression_just_evaluated = False
            except Exception:
                self.display_var.set("Error")
                self.update_operation_label("")
                self.last_result = None
                self.should_reset_display = True
                self.expression_just_evaluated = False
            return

        if char in ['+', '-', '*', '/']:
            if self.should_reset_display or self.expression_just_evaluated:
                self.should_reset_display = False
                self.expression_just_evaluated = False
            if current_display == "0":
                self.display_var.set(f"0{char}")
            elif current_display[-1] in ['+', '-', '*', '/']:
                self.display_var.set(current_display[:-1] + char)
            else:
                self.display_var.set(current_display + char)
            self.update_operation_label(self.display_var.get())
            return

        if char == '(':
            if self.should_reset_display or self.expression_just_evaluated:
                self.display_var.set("(")
                self.should_reset_display = False
                self.expression_just_evaluated = False
            elif current_display == "0":
                self.display_var.set("(")
            else:
                self.display_var.set(current_display + "(")
            self.update_operation_label(self.display_var.get())
            return

        if char == ')':
            if self.should_reset_display:
                self.display_var.set("0")
                self.should_reset_display = False
            else:
                self.display_var.set(current_display + ")")
            self.update_operation_label(self.display_var.get())
            return

        if char == '.':
            if self.should_reset_display or self.expression_just_evaluated:
                self.display_var.set("0.")
                self.should_reset_display = False
                self.expression_just_evaluated = False
                self.update_operation_label(self.display_var.get())
                return
            token = re.split(r'[+\-*/]', current_display)[-1]
            if '.' not in token:
                if current_display == "0" or current_display.endswith(('+', '-', '*', '/')):
                    self.display_var.set(current_display + "0.")
                else:
                    self.display_var.set(current_display + ".")
            self.update_operation_label(self.display_var.get())
            self.should_reset_display = False
            return

        # Number button
        if self.should_reset_display or self.expression_just_evaluated:
            self.display_var.set(char)
            self.should_reset_display = False
            self.expression_just_evaluated = False
        else:
            if current_display == "0":
                self.display_var.set(char)
            else:
                self.display_var.set(current_display + char)
        self.update_operation_label(self.display_var.get())

# Create and run the calculator
if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
