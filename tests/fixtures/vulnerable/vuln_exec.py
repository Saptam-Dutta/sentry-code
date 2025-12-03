"""VULNERABLE: Use of eval and exec on user input"""

def calculate_expression(user_input):
    """VULN: PY003 - eval() on untrusted input"""
    result = eval(user_input)
    return result

def execute_code(code_string):
    """VULN: PY003 - exec() on untrusted input"""
    exec(code_string)

def dynamic_import(module_name):
    """VULN: PY003 - eval for imports"""
    mod = eval(f"__import__({module_name})")
    return mod

class Calculator:
    def compute(self, formula):
        # VULN: PY003 - eval in class method
        return eval(formula)
