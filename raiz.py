#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from dwave.system import LeapHybridSampler # Este dwave o el de abajo mas avanzado
from dwave.system import DWaveSampler, EmbeddingComposite

from dimod import BinaryQuadraticModel
# Set up scenario
raiz1=4
raiz2=raiz1
numero_op = [0,1,2,3]  #Numero de operaciones diferentes  *,+,- , + que es igual numero de circuitos
version = [0,1]   # Numero de versiones de una operacion  2
Potencia = [[1, 1],
	       [2, 2],
           [4, 4],
           [8, 8]]     #  Potencia micro-W Por operacion y version Filas son operaciones [vesion 0,version1]
Retardo = [[1, 1],
	       [1, 1],
           [1, 1],
           [1, 1]] #  Retardo ns por operacion y version Filas son operaciones [vesion 0,version1]
Potencia_max =290*0.9  #290 = maximo de todos los circuitos

total_Retardo = 0
total_Potencia = 0  

    # Build a variable for each pump
x = [[f'C{p}_Ver1',f'C{p}_Ver2']  for p in numero_op]

    # Initialize BQM
bqm = BinaryQuadraticModel('BINARY')

    # Objective
for p in numero_op:
   for t in version:
        bqm.add_variable(x[p][t],0* Retardo[p][t])


 # Constraint 1: Una raiz
for t in version:
        c2 = [(x[p][t], Potencia[p][t]) for p in numero_op]
        bqm.add_linear_inequality_constraint(c2,
                constant = -raiz1,
                lb=0,
                ub=0,
                lagrange_multiplier = 12,
                label = 'c2_version_'+str(t))


 # Constraint 2: Otra raiz
for t in version:
        c2 = [(x[p][t], Potencia[p][t]) for p in numero_op]
        bqm.add_linear_inequality_constraint(c2,
                constant = -raiz2,
                lb=0,
                ub=0,
                lagrange_multiplier = 12,
                label = 'c2_version_'+str(t))

 

    # Run on hybrid sampler
print("\nRunning hybrid solver...")

#sampler = LeapHybridSampler()
#sampleset = sampler.sample(bqm)
    
sampler = EmbeddingComposite(DWaveSampler())                  # Avanzado
sampleset = sampler.sample(bqm,num_reads=1000,label='Example')

print (sampleset)

sample=sampleset.first.sample   #ordena por energia de menos a mas. La primera es la de menor energia


 # Print out version slots header
print("\n\tCodigo")
 # Generate printout for each pump's usage
for p in numero_op:
    printout = 'C'+str(p)
    for version in range(1):
        printout += "\t" + str(sample[x[p][version]])
        total_Retardo += sample[x[p][version]] * Retardo[p] [version]
        total_Potencia += sample[x[p][version]] * Potencia[p] [version]
    print(printout)

#Print out total Retardo and Potencia information
#print("\nTotal Retardo:\t", total_Retardo)
print("Total Potencia:\t", total_Potencia, "\n")




