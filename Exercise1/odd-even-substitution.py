# Read the file and count the number of occurrences of "terrible" 
count = 0
with open("./Exercise1/file_to_read.txt",'r') as file:
    data = file.read()
    count = data.count('terrible')

# Replace the odd and even occurrences of "terrible" 
terrible_list = data.split('terrible')
new_text = ''

# print('len(terrible_list)：',len(terrible_list))
for i in range(len(terrible_list)):
    # print(i)
    if i % 2 == 0:  # Replace the ODD term with "marvellous"
        new_text += terrible_list[i]
        if i < len(terrible_list) - 1:
            new_text += 'marvellous'
    else: # Replace the EVEN term with "pathetic"
        new_text += terrible_list[i]
        if i < len(terrible_list) - 1:
            new_text += 'pathetic'

# Write the updated text to result.txt 
with open('./Exercise1/result.txt', 'w') as file:
    file.write(new_text)

# Show the total number of "terrible" 
print('Total number of occurrences of the word terrible: ', count)
