from flask import Flask, render_template,send_from_directory,redirect
import os
app = Flask(__name__,static_folder="/static")

@app.route('/')
def index():
  return render_template('/home.html')

@app.route('/attendance/attendance.py')
def my_link():
  from attendance import attendance
  cwd=os.getcwd()
  path=os.path.join(cwd,'attendance','Attendance.txt')
  print(path)
  f=open(path,'r')
  contents=f.read()
  return (contents)


@app.route('/Attentiveness.py')
def my_link3():
  import Attentiveness
  cwd=os.getcwd()
  path=os.path.join('convert.txt')
  f=open(path,'r')
  contents=f.read()
  return (contents)

@app.route('/index.html')
def my_link2():
  return render_template('/index.html')

  
  # cwd=os.getcwd()
  # path=os.path.join(cwd,'attendance','attendance.py')
  # file = open(path, 'r').read()
  # return exec(file)

if __name__ == '__main__':
  app.run(debug=True)