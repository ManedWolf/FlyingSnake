import os   # path.exists open
import json
import time # time



def load_variable(author, variable):

  if os.path.exists('data/'+str(author)):
    with open("data/"+str(author), 'r') as file:
      loaded = json.load(file)
      return loaded[variable]['history'][loaded[variable]['version']] if variable in loaded else None
  return



def save_variable(author, variable="_", value=""):

  if variable_exists(author, variable):
    with open("./data/"+str(author), 'r+') as file:
      loaded = json.load(file)
      loaded[variable]['history'] = loaded[variable]['history'][:loaded[variable]['version']+1]
      loaded[variable]['history'].append({
        'value': value,
        'date' : int(time.time())
      })
      loaded[variable]['version'] += 1
      file.seek(0)
      file.truncate(0)
      json.dump(loaded, file, indent = 2)

  elif os.path.exists('data/'+str(author)):
    with open("./data/"+str(author), 'r+') as file:
      loaded = json.load(file)
      loaded[variable] = {
          "version": 0,
          "history":
          [
            {
              "value": value,
              "date" : int(time.time())
            }
          ]
        }
      file.seek(0)
      file.truncate(0)
      json.dump(loaded, file, indent = 2)

  else:
    with open("./data/"+str(author), 'w+') as file:
      json.dump(
        {
          variable:
          {
            "version": 0,
            "history":
            [
              {
                "value": value,
                "date" : int(time.time())
              }
            ]
          }
        },
        file,
        indent = 2
      )

  return value



def undo_variable(author, variable="_"):

  if variable_exists(author, variable):
    with open("./data/"+str(author), 'r+') as file:
      loaded = json.load(file)
      loaded[variable]['version'] = max(loaded[variable]['version']-1,0)
      file.seek(0)
      file.truncate(0)
      json.dump(loaded, file, indent = 2)
  return



def redo_variable(author, variable="_"):

  if variable_exists(author, variable):
    with open("./data/"+str(author), 'r+') as file:
      loaded = json.load(file)
      loaded[variable]['version'] = min(loaded[variable]['version']+1,len(loaded[variable]['history'])-1)
      file.seek(0)
      file.truncate(0)
      json.dump(loaded, file, indent = 2)
  return


# aliases

variable_exists = load_variable


# author: discord.Message.author.id
# variable: token
#save or store ?

print(load_variable(213006437750800384,"FOR"))
print(save_variable(213006437750800384,"FOR","A"))
print(save_variable(213006437750800384,"FOR","B"))
print(save_variable(213006437750800384,"FOR","C"))
print(load_variable(213006437750800384,"FOR"))
print(undo_variable(213006437750800384,"FOR"))
print(load_variable(213006437750800384,"FOR"))
print(redo_variable(213006437750800384,"FOR"))
print(redo_variable(213006437750800384,"FOR"))
print(undo_variable(213006437750800384,"FOR"))
print(undo_variable(213006437750800384,"FOR"))
print(undo_variable(213006437750800384,"FOR"))
print(load_variable(213006437750800384,"FOR"))
print(redo_variable(213006437750800384,"FOR"))
print(load_variable(213006437750800384,"FOR"))
print(save_variable(213006437750800384,"FOR","D"))
print(undo_variable(213006437750800384,"FOR"))
print(undo_variable(213006437750800384,"FOR"))
print(undo_variable(213006437750800384,"FOR"))
print(load_variable(213006437750800384,"FOR"))
print(redo_variable(213006437750800384,"FOR"))
print(load_variable(213006437750800384,"FOR"))
print(redo_variable(213006437750800384,"FOR"))
print(load_variable(213006437750800384,"FOR"))
print(redo_variable(213006437750800384,"FOR"))




