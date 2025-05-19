import sys
import types

# Substitui torch.classes por um módulo fictício para evitar introspecção (bug irritante que fica poluindo o log)
sys.modules['torch.classes'] = types.ModuleType('torch.classes')
