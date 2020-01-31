from model import *
from sampler import *

batch_size = 64
num_points = 64
num_labels = 1

pointnet = PointNet(num_points, num_labels)
        
criterion = nn.BCELoss()
optimizer = optim.Adam(pointnet.parameters(), lr=0.001)

loss_list = []
accuracy_list = []

for iteration in range(10000+1):
    
    pointnet.zero_grad()
    
    input_data, labels = data_sampler(batch_size, num_points)
    
    output = pointnet(input_data)
    output = nn.Sigmoid()(output)
    
    error = criterion(output, labels)
    error.backward()
    
    optimizer.step()
    
    with torch.no_grad():
        output[output > 0.5] = 1
        output[output < 0.5] = 0
        accuracy = (output==labels).sum().item()/batch_size
            
    loss_list.append(error.item())
    accuracy_list.append(accuracy)
            
    if iteration % 10 == 0:
        print('Iteration : {}   Loss : {}'.format(iteration, error.item()))
        print('Iteration : {}   Accuracy : {}'.format(iteration, accuracy))
