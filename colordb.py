from flask import Flask
from flask import request
from rtree import index
from colormath.color_objects import RGBColor
import json


p = index.Property()
p.dimension = 3
p.dat_extension = 'dat'
p.idx_extension = 'idx'
idx = index.Index('colordb', properties=p)


def hex_to_rgb(hex):
    color = RGBColor()
    color.set_from_rgb_hex(hex)
    return color

def insert(color, entry):
    lab = color.convert_to('lab')
    idx.insert(entry, (lab.lab_l, lab.lab_a, lab.lab_b, lab.lab_l, lab.lab_a, lab.lab_b))
    
def nearest(color):
    lab = color.convert_to('lab')
    return idx.nearest((lab.lab_l, lab.lab_a, lab.lab_b, lab.lab_l, lab.lab_a, lab.lab_b), 50)

#test = {111: 'FF9900', 222: '0066FF', 333: '00FF00'}
#for e in test:
#    insert(hex_to_rgb(test[e]), e)


app = Flask(__name__)

@app.route('/<hex_color>', methods=['GET'])
def get_entries(hex_color):
    return json.dumps(list(nearest(hex_to_rgb(hex_color))))

@app.route('/entries', methods=['POST', 'GET'])
def insert_entry():
    entryid = int(request.args.get('entryid'))
    for color in request.args.get('colors','').split(','):
        insert(hex_to_rgb(color), entryid)
        
    return json.dumps('ok')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
