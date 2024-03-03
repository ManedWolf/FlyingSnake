# IMPORTS

import os       # open close
import json     # load dump
import time     # time
import datetime # datetime.now
import logging  # debug / info / warning / exception/error / critical
import discord
from discord.ext import commands
from discord import app_commands
import re
import random
random.seed()

# COG

class Roll(commands.Cog):

  # INITIALIZATION

  def __init__(self, bot):
    self.bot         = bot
    self.strict_mode = True
    self.re_number   = "([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)"
    self.re_variable = "([a-zA-Z_]+)"
    self.re_operator = "([\+\-\*/]+)"
    self.re_other    = "([\(\)]+)"
    self.re_operand  = f"({self.re_number}|{self.re_variable})"

  @commands.Cog.listener()
  async def on_ready(self):
    logging.info(f'{self.__class__.__name__}: cog loaded')
    #print([c.name for c in self.get_commands()])

  @app_commands.command()
  async def roll(self, interaction, expression:str=""): # Need to figure out how to have multiple optional argument/expression

    """Evaluate arithmetic expressions involving dice."""

    if not expression:
      # call data.py to get variables to roll instead of a formula
      await interaction.response.send_message(f"Roll without expression not yet implemented", ephemeral=True, delete_after=5)

    if not self.strict_mode:
      expression = self.repair_float(expression)
      expression = self.repair_implicit_multiplication(expression) # Not Yet Implemented
      expression = self.repair_invalid_characters(expression) # Not Yet Implemented
      expression = self.repair_empty_parenthesis(expression) # Poor Implementation
      expression = self.repair_imbalance_parenthesis(expression)
      # Will probably never be implemented : Implicit 1D20 die
      # Will probably never be implemented : Add missing leading operand
      # Will probably never be implemented : Allowing * to be represented by a x
      # Will probably never be implemented : Implicit /2 when empty divider
    """
    if self.invalid_tokens(expression): # probably need some refinement
      logging.error("Roll.roll(): malformed expression")
      await interaction.response.send_message("Malformed expression", ephemeral=True, delete_after=5)
    
    if self.invalid_following_operators(expression): # need a rework for literal operators
      logging.error("Roll.roll(): expression with following operators")
      await interaction.response.send_message("Expression with following operators", ephemeral=True, delete_after=5)
    
    if self.invalid_following_operand(expression):
      logging.error("Roll.roll(): expression with following operands")
      await interaction.response.send_message("Expression with following operands", ephemeral=True, delete_after=5)

    if self.invalid_balance(expression):
      logging.error("Roll.roll(): expression with invalid parenthesis balance")
      await interaction.response.send_message("Expression with invalid parenthesis balance", ephemeral=True, delete_after=5)
    
    if self.invalid_expression(expression):  # Not Implemented
      logging.error("Roll.roll(): invalid expression")
      await interaction.response.send_message("Invalid expression", ephemeral=True, delete_after=5)
    """
    logging.info(f"Roll.roll(): Calculating expression: {expression}")
    await interaction.response.send_message(f"{self.old_evaluate(expression)[0]}")

  # REPAIRING MALFORMED EXPRESSION

  def repair_float(self, expression):
    """Replace every ',' with '.'"""
    return expression.replace(",", ".")

  def repair_implicit_multiplication(self, expression):
    """Add implicit '*' outside of parenthesis"""
    """
    def correctMultiplication(formula):
      result = formula[0]
      for i in range(1,len(formula)):
        if formula[i] == '(' and "+-*/(".find(formula[i-1]) == -1:
          result = result + '*' + formula[i]
        elif formula[i-1] == ')' and "+-*/)".find(formula[i]) == -1:
          result = result + '*' + formula[i]
        else:
          result = result + formula[i]
      return result
    """
    return expression

  def repair_invalid_characters(self, expression):
    """Return a string without invalid characters"""
    return expression

  def repair_empty_parenthesis(self, expression):
    """ There's a need to consider empty parenthesis '()' in evaluation
    def correctEmpty(formula):
      result = ''
      for i in range(len(formula)):
        if formula[i] == '(' and formula[i+1] == ')':
          result = result + formula[i] + '0'
        else:
          result = result + formula[i]
      return result
    """
    return expression.replace("()","")

  def repair_imbalance_parenthesis(self, expression):
    """Rebalances parentheses matching of an expression"""
    opening = expression.count('(')
    closing = expression.count(')')
    return '(' * max(0,closing-opening) + expression + max(0,opening-closing) * ')'

  def repair_implicit_die(self, expression): # Not Implemented
    """Add implicit '1' and '20' on dice"""
    """
    def correctDice(formula):
      result = ''
      for i in range(len(formula)):
        if formula[i] == 'D' and (i==0 or "0123456789".find(formula[i-1]) == -1):
          result = result + '1'
        result = result + formula[i]
        if formula[i] == 'D' and (i==len(formula)-1 or "0123456789".find(formula[i+1]) == -1):
          result = result + '20'
      return result
    """
    return expression

  def repair_leading_operand(self, expression):
    """Probably useless now"""
    """
    def correctOperand(formula):
      if formula[0] == '+' or formula[0] == '-':
          formula = '0' + formula
      if formula[0] == '*' or formula[0] == '/':
          formula = '1' + formula
      if formula[-1] == '+' or formula[-1] == '-':
          formula = formula + '0'
      if formula[-1] == '*' or formula[-1] == '/':
          formula = formula + '1'
      return formula
    """
    return expression

  # CHEKING EXPRESSION VALIDITY

  def invalid_tokens(self, expression):
    """Check if the expression only has valid tokens"""
    return not re.fullmatch(f"-*{self.re_operand}({self.re_operator}-*{self.re_operand})*", expression.replace("(","").replace(")",""))

  def invalid_following_operators(self, expression):
    """Checks that operators do not follow each other"""
    return re.fullmatch(f".*{self.re_operators}{self.re_operators}.*", expression.replace("(","").replace(")",""))

  def invalid_following_operands(self, expression):
    """Checks that operand do not follow each other"""
    return re.fullmatch(f".*(([0-9]+\.[0-9]*\.[0-9]+)|({self.re_number}{self.re_variable})|({self.re_variable}{self.re_number})).*", expression.replace("(","").replace(")",""))

  def invalid_balance(self, expression, level=0):
    """Check for parenthesis imbalance"""
    if not expression or level < 0:
        return True
    return invalidBalance(expression[1:], level+int(expression[0]=="(")-int(expression[0]==")"))

  def invalid_expression(self, expression):
    """Check for proper formation of expression, including parenthesis"""
    return False

  # EVUALUATION

  def old_evaluate(self, expression, i=0):
      calc = []
      while i<len(expression) and expression[i] != ')':
          calc.append('')
          if expression[i] == '(':
              (calc[-1],i) = self.old_evaluate(expression,i+1)
          else:
              while i<len(expression) and "0123456789D".find(expression[i]) != -1:
                  calc[-1] += expression[i]
                  i += 1
              calc[-1] = int(self.operand(calc[-1]))
          if i<len(expression) and expression[i] != ')':
              calc.append(expression[i])
              i += 1
      j = 0
      while(j<len(calc)):
          if calc[j] == '*':
              calc[j-1] = str(int(self.operand(calc[j-1]))*int(self.operand(calc[j+1])))
              del calc[j+1]
              del calc[j]
              j -= 1
          elif calc[j] == '/':
              calc[j-1] = str(int(self.operand(calc[j-1]))//int(self.operand(calc[j+1])))
              del calc[j+1]
              del calc[j]
              j -= 1
          j += 1
      j = 0
      while(j<len(calc)):
          if calc[j] == '+':
              calc[j-1] = str(int(self.operand(calc[j-1]))+int(self.operand(calc[j+1])))
              del calc[j+1]
              del calc[j]
              j -= 1
          elif calc[j] == '-':
              calc[j-1] = str(int(self.operand(calc[j-1]))-int(self.operand(calc[j+1])))
              del calc[j+1]
              del calc[j]
              j -= 1
          j += 1
      return (calc[0], i+1)

  def operand(self, text):
      if re.fullmatch("[0-9]+[D][0-9]+", str(text)):
          return sum([random.randint(1,int(text.split("D")[1])) for _ in range(int(text.split("D")[0]))])
      else:
          return text



async def setup(bot):
  await bot.add_cog(Roll(bot))