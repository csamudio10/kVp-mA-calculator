import streamlit as st
from machine import Machine


st.title('X-ray calibration app')

variable_to_calculate = st.radio('Pick the variable you wish to calculate:', ['kVp','mA'])

st.write('selected varaible is: ',variable_to_calculate)

kVp0 = st.number_input('Enter the initial kVp')
mA0 = st.number_input('Enter the initial mA')

new_kVp = 0
new_mA = 0
if variable_to_calculate == 'kVp':
    new_mA = st.number_input('Enter the modified mA')

if variable_to_calculate == 'mA':
    new_kVp = st.number_input('Enter the modified kVp')

x_ray = Machine(kVp0 = kVp0,
                mA0 = mA0,
                kVp = new_kVp,
                mA = new_mA)

st.write('model created with the following parameters: ')
st.write('kVp0', x_ray.kVp0)
st.write('mA0', x_ray.mA0)
st.write('kVp', x_ray.kVp)
st.write('mA', x_ray.mA)

x_ray.create_model()
x_ray.extract_model_params()
if variable_to_calculate == 'mA':
    st.write('selected varaible is: ',variable_to_calculate)
    st.write('Your new mA is: ',x_ray.calc_new_point('mA',new_kVp))
    
if variable_to_calculate == 'kVp':
    st.write('selected varaible is: ',variable_to_calculate)
    st.write('Your new kVp is: ',x_ray.calc_new_point('kVp',new_mA))
    
    
c= st.checkbox('View Model Statistics')

if c:
   st.write(x_ray.print_model_params().splitlines())
